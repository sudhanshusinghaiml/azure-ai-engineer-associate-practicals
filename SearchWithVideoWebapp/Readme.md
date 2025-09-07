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