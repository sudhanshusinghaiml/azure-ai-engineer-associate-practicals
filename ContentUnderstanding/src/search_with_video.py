from langchain import hub
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.vectorstores.azuresearch import AzureSearch
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import Document
import requests
import json
import sys
import uuid
import os
from dotenv import load_dotenv
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from python.content_understanding_client import AzureContentUnderstandingClient

load_dotenv()

# Load and validate Azure AI Services configs
AZURE_AI_SERVICE_ENDPOINT = os.getenv("AZURE_AI_SERVICE_ENDPOINT")
AZURE_AI_SERVICE_API_VERSION = os.getenv("AZURE_AI_SERVICE_API_VERSION") or "2024-12-01-preview"
AZURE_DOCUMENT_INTELLIGENCE_API_VERSION = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION") or "2024-11-30"

# Load and validate Azure OpenAI configs
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
AZURE_OPENAI_CHAT_API_VERSION = os.getenv("AZURE_OPENAI_CHAT_API_VERSION") or "2024-08-01-preview"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
AZURE_OPENAI_EMBEDDING_API_VERSION = os.getenv("AZURE_OPENAI_EMBEDDING_API_VERSION") or "2023-05-15"

# Load and validate Azure Search Services configs
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

# Add the parent directory to the path to use shared modules
parent_dir = Path(Path.cwd()).parent
sys.path.append(str(parent_dir))

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
ANALYZER_TEMPLATE_PATH = "../analyzer_templates/video_content_understanding.json"
ANALYZER_ID = "video_analyzer" + "_" + str(uuid.uuid4())
VIDEO_LOCATION = Path("../data/FlightSimulator.mp4")

class VideoRAGSearch:
    def __init__(self):
        # self.analyzer_configs = self.set_analyzer_configs()
        self.client = self.get_content_understanding_client()

    def get_content_understanding_client(self):
        # Create Content Understanding client
        return AzureContentUnderstandingClient(
            endpoint=AZURE_AI_SERVICE_ENDPOINT,
            api_version=AZURE_AI_SERVICE_API_VERSION,
            token_provider=token_provider,
            # x_ms_useragent="azure-ai-content-understanding-python/content_extraction", # This header is used for sample usage telemetry, please comment out this line if you want to opt out.
        )

    def create_analyzer_and_extract_video_content(self):
        # Iterate through each config and create an analyzer
        try:
            # Create the analyzer using the content understanding client
            # Create analyzer
            response = self.client.begin_create_analyzer(ANALYZER_ID, analyzer_template_path=ANALYZER_TEMPLATE_PATH)
            result = self.client.poll_result(response)
            
            # Submit the video for content analysis
            response = self.client.begin_analyze(ANALYZER_ID, file_location=VIDEO_LOCATION)

            # Wait for the analysis to complete and get the content analysis result
            video_cu_result = self.client.poll_result(response, timeout_seconds=3600)  # 1 hour timeout

            # Print the content analysis result
            print(f"Video Content Understanding result: ", video_cu_result)
            
        except Exception as e:
            print(f"Failed to create analyzer")
            print(f"Error: {e}")
        return result
    
    def convert_values_to_strings(self,json_obj):
        return [str(value) for value in json_obj]


    def remove_markdown(self,json_obj):
        for segment in json_obj:
            if 'markdown' in segment:
                del segment['markdown']
        return json_obj


    def process_cu_scene_description(self, scene_description):
        audio_visual_segments = scene_description["result"]["contents"]
        filtered_audio_visual_segments = self.remove_markdown(audio_visual_segments)
        audio_visual_splits = [
            "The following is a json string representing a video segment with scene description and transcript ```"
            + v
            + "```"
            for v in self.convert_values_to_strings(filtered_audio_visual_segments)
        ]
        docs = [Document(page_content=v) for v in audio_visual_splits]
        return docs
    

    # Embed the splitted documents and insert into Azure Search vector store
    def embed_and_index_chunks(self, docs):
        aoai_embeddings = AzureOpenAIEmbeddings(
            azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
            openai_api_version=AZURE_OPENAI_EMBEDDING_API_VERSION,  # e.g., "2023-12-01-preview"
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider=token_provider
        )

        vector_store: AzureSearch = AzureSearch(
            azure_search_endpoint=AZURE_SEARCH_ENDPOINT,
            azure_search_key=None,
            index_name=AZURE_SEARCH_INDEX_NAME,
            embedding_function=aoai_embeddings.embed_query
        )
        vector_store.add_documents(documents=docs)
        return vector_store
    

    # Setup rag chain
    def setup_video_rag_chain(self, vector_store, prompt_str):
        retriever = vector_store.as_retriever(search_type="similarity", k=3)

        prompt = ChatPromptTemplate.from_template(prompt_str)
        llm = AzureChatOpenAI(
            openai_api_version=AZURE_OPENAI_CHAT_API_VERSION,
            azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
            azure_ad_token_provider=token_provider,
            temperature=0.7,
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return rag_chain
    
    # Setup conversational search
    def conversational_search(self, rag_chain, query):
        print(rag_chain.invoke(query))