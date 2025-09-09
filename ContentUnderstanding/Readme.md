# [Multimodal Retrieval Augmented Generation with Content Understanding](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/tree/main/notebooks)

### Overview
- Azure AI Content Understanding provides a powerful solution for extracting data from diverse content types, while preserving semantic integrity and contextual relationships ensuring optimal performance in Retrieval Augmented Generation (RAG) applications.

- This sample demonstrates how to leverage Azure AI's Content Understanding capabilities to extract:
    - OCR and layout information from documents
    - Image description, summarization and classification
    - Audio transcription with speaker diarization from audio files
    - Shot detection, keyframe extraction, and audio transcription from videos

This module illustrates how to extract content from unstructured multimodal data and apply it to Retrieval Augmented Generation (RAG). The resulting output can be converted to vector embeddings and indexed in Azure AI Search. When a user submits a query, Azure AI Search retrieves relevant chunks to generate a context-aware response.

### Steps for building Multimodal RAG with Search
- Create analyzers with pre-defined schemas.
    - Feel free to start with the provided sample data as a reference and experiment with your own data to explore its capabilities.

- Use created analyzers to extract multimodal content

- Organize multimodal data:
    - Preprocess JSON output data
    - Split document markdown into semantic chunks

- Embed and Index Chunks into AzureSearch

- Retrieve relevant chunks based on a question
    - Execute a pure vector similarity search
    - Execute hybrid search. Vector and nonvector text fields are queried in parallel, results are merged, and top matches of the unified result set are returned.
    - Choose the best strategy for chunking

- Question & Answers Chatbot:
    - We can utilize OpenAI GPT completion models + Azure Search to conversationally search for and chat about the results. (If you are using GitHub Codespaces, there will be an input prompt near the top of the screen)


# [Video Search with Azure Content Understanding](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_video.ipynb)

### Objective
- This document is meant to present a guideline on how to leverage the Azure Video Content Understanding API for AI Search. The sample will demonstrate the following steps:
    - Process a video file from Azure Blob storage with the Azure Video Content Understanding service to generate a video description grounding document.
    - Process the video description grounding document with Azure Search client to generate an Azure Search index.
    - Utilize OpenAI completion and embedding models to search through content in the video search index.


# [Visual Document Search with Azure Content Understanding](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_visual_document.ipynb)

- This document illustrates an example workflow for how to leverage the Azure AI Content Understanding API to enhance the quality of document search.

- The sample will demonstrate the following steps:

    - Extract the layout and content of a document using Azure AI Document Intelligence.
    - For each figure in the document, extract its content with a custom analyzer using Azure AI Content Understanding, and insert it into the corresponding location in the document content.
    - Chunk and embed the document content with LangChain and Azure OpenAI, and index them with Azure Search to generate an Azure Search index.
    - Utilize an OpenAI chat model to search through content in the document with a natural language query.


# [Video Search Webapp with Azure Content Understanding](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_video_webapp.ipynb)
- This document will guide you through how to run and use the Video Search Webapp sample as well as providing the backend server.
    - Set up Azure resources and acquire the necessary endpoints, API keys, API versions, and deployment names.
    - Build and run node.js server that serves the frontend webapp.
    - Launch and port forward the backend server through this Python Notebook.


# Reference:
- [Azure AI Content Understanding service quotas and limits](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/service-limits)