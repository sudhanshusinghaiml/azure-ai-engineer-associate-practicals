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

ANALYZER_TEMPLATE_PATH = "../analyzer_templates/content_document.json"
ANALYZER_ID = "layout-sample-" + str(uuid.uuid4())
DOC_LOCATION = Path("../data/sample_layout.pdf")

class DocumentRAGSearch:
    def __init__(self):
        self.client = self.get_content_understanding_client()
        self.splits = self.create_custom_analyzer()
        self.splits = None

    # Create Content Understanding client
    def get_content_understanding_client(self):
        return AzureContentUnderstandingClient(
            endpoint=AZURE_AI_SERVICE_ENDPOINT,
            api_version=AZURE_AI_SERVICE_API_VERSION,
            token_provider=token_provider,
            # x_ms_useragent="azure-ai-content-understanding-python/content_extraction", # This header is used for sample usage telemetry, please comment out this line if you want to opt out.
        )


    # Create analyzer and use analyzer to extract document content with layout analysis
    def create_custom_analyzer(self):
        try:
            # Create analyzer
            response = self.client.begin_create_analyzer(ANALYZER_ID, analyzer_template_path=ANALYZER_TEMPLATE_PATH)
            result = self.client.poll_result(response)
            
            # Analyze document
            response = self.client.begin_analyze(ANALYZER_ID, file_location=DOC_LOCATION)
            result = self.client.poll_result(response)
            result_data = result.get("result", {})
            contents = result_data.get("contents", [])

            #extract markdown content
            for content in contents:
                markdown_content = content.get("markdown", "")
                print(f"Markdown", markdown_content)
            print(json.dumps(result, indent=2))
            return markdown_content
        except Exception as e:
            print(e)
            print("Error in creating analyzer. Please double-check your analysis settings.\nIf there is a conflict, you can delete the analyzer and then recreate it, or move to the next cell and use the existing analyzer.")


    def split_documents_into_chunks(self):
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
        self.splits = text_splitter.split_text(self.markdown_content)
        print("Length of splits: " + str(len(self.splits)))

        return


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
    
    # Retrieve relevant chunks based on the question
    def setup_document_rag_chain(self, vector_store, query):
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

        retrieved_docs = retriever.get_relevant_documents(query)

        print(retrieved_docs[0].page_content)

        # Use a prompt for RAG that is checked into the LangChain prompt hub (https://smith.langchain.com/hub/rlm/rag-prompt?organizationId=989ad331-949f-4bac-9694-660074a208a7)
        prompt = hub.pull("rlm/rag-prompt")
        llm = AzureChatOpenAI(
            openai_api_version=AZURE_OPENAI_CHAT_API_VERSION,  # e.g., "2023-12-01-preview"
            azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
            temperature=0,
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
    
    # Setup document search
    def document_search(self, rag_chain, query):
        print(rag_chain.invoke(query))
