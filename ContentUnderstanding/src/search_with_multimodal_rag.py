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

class MultiModalRAGSearch:
    def __init__(self):
        self.analyzer_configs = self.set_analyzer_configs()
        self.content_understanding_client = self.get_content_understanding_client()
        self.analyzer_content = self.extract_multimodal_content()

    def set_analyzer_configs(self):
        #set analyzer configs
        analyzer_configs = [
            {
                "id": "doc-analyzer" + str(uuid.uuid4()),
                "template_path": "../analyzer_templates/content_document.json",
                "location": Path("../data/sample_layout.pdf"),
            },
            {
                "id": "image-analyzer" + str(uuid.uuid4()),
                "template_path": "../analyzer_templates/image_chart_diagram_understanding.json",
                "location": Path("../data/sample_report.pdf"),
            },
            {
                "id": "audio-analyzer" + str(uuid.uuid4()),
                "template_path": "../analyzer_templates/call_recording_analytics.json",
                "location": Path("../data/callCenterRecording.mp3"),
            },
            {
                "id": "video-analyzer" + str(uuid.uuid4()),
                "template_path": "../analyzer_templates/video_content_understanding.json",
                "location": Path("../data/FlightSimulator.mp4"),
            },
        ]
        return analyzer_configs

    def get_content_understanding_client(self):
        # Create Content Understanding client
        return AzureContentUnderstandingClient(
            endpoint=AZURE_AI_SERVICE_ENDPOINT,
            api_version=AZURE_AI_SERVICE_API_VERSION,
            token_provider=token_provider,
            # x_ms_useragent="azure-ai-content-understanding-python/content_extraction", # This header is used for sample usage telemetry, please comment out this line if you want to opt out.
        )

    def create_custom_analyzer(self):
        # Iterate through each config and create an analyzer
        for analyzer in self.analyzer_configs:
            analyzer_id = analyzer["id"]
            template_path = analyzer["template_path"]
            try:
                # Create the analyzer using the content understanding client
                response = self.content_understanding_client.begin_create_analyzer(
                    analyzer_id=analyzer_id,
                    analyzer_template_path=template_path
                )
                result = self.content_understanding_client.poll_result(response)
                print(f"Successfully created analyzer: {analyzer_id}")
                
            except Exception as e:
                print(f"Failed to create analyzer: {analyzer_id}")
                print(f"Error: {e}")

        return result
    
    def extract_multimodal_content(self):
        # Iterate through each analyzer created and analyze content for each modality
        analyzer_results =[]
        extracted_markdown = []
        analyzer_content = []
        for analyzer in self.analyzer_configs:
            analyzer_id = analyzer["id"]
            template_path = analyzer["template_path"]
            file_location = analyzer["location"]
            try:
                # Analyze content
                    response = self.content_understanding_client.begin_analyze(analyzer_id, file_location)
                    result = self.content_understanding_client.poll_result(response)
                    analyzer_results.append({"id":analyzer_id, "result": result["result"]})
                    analyzer_content.append({"id": analyzer_id, "content": result["result"]["contents"]})
                            
            except Exception as e:
                    print(e)
                    print("Error in creating analyzer. Please double-check your analysis settings.\nIf there is a conflict, you can delete the analyzer and then recreate it, or move to the next cell and use the existing analyzer.")

        print("Analyzer Results:")
        for analyzer_result in analyzer_results:
            print(f"Analyzer ID: {analyzer_result['id']}")
            print(json.dumps(analyzer_result["result"], indent=2))

        return analyzer_content
    
    def convert_values_to_strings(self, json_obj):
        return [str(value) for value in json_obj]

    # process all content and convert to string      
    def process_allJSON_content(self, all_content):

        # Initialize empty list to store string of all content
        output = []

        document_splits = [
            "This is a json string representing a document with text and metadata for the file located in "
            +str(self.analyzer_configs[0]["location"])+" "
            + v 
            + "```"
            for v in self.convert_values_to_strings(all_content[0]["content"])
        ]
        docs = [Document(page_content=v) for v in document_splits]
        output += docs

        #convert image json object to string and append file metadata to the string
        image_splits = [
        "This is a json string representing an image verbalization and OCR extraction for the file located in "
        +str(self.analyzer_configs[1]["location"])+" "
        + v
        + "```"
        for v in self.convert_values_to_strings(all_content[1]["content"])
        ]
        image = [Document(page_content=v) for v in image_splits]
        output+=image

        #convert audio json object to string and append file metadata to the string
        audio_splits = [
            "This is a json string representing an audio segment with transcription for the file located in "
            +str(self.analyzer_configs[2]["location"])+" " 
        + v
        + "```"
        for v in self.convert_values_to_strings(all_content[2]["content"])
        ]
        audio = [Document(page_content=v) for v in audio_splits]
        output += audio

        #convert video json object to string and append file metadata to the string
        video_splits = [
            "The following is a json string representing a video segment with scene description and transcript for the file located in "
            +str(self.analyzer_configs[3]["location"])+" "
            + v
            + "```"
            for v in self.convert_values_to_strings(all_content[3]["content"])
        ]
        video = [Document(page_content=v) for v in video_splits]
        output+=video    
        
        return output
    
    # This is unused method
    # Optional - Split document markdown into semantic chunks
    def split_into_semantic_chunks(self):
    # Configure langchain text splitting settings
        EMBEDDING_CHUNK_SIZE = 512
        EMBEDDING_CHUNK_OVERLAP = 20

        # Split the document into chunks base on markdown headers.
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]

        text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

        docs_string = self.analyzer_content[0]['content'][0]['markdown'] #extract document analyzer markdown (first item in the list) is the document analyzer markdown output
        docs_splits = text_splitter.split_text(docs_string)

        print("Length of splits: " + str(len(docs_splits)))

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
    def setup_rag_chain(self, vector_store, prompt_str):
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


    