from search_with_video import VideoRAGSearch

if __name__ == "__main__":
    rag = VideoRAGSearch()

    video_cu_result = rag.create_analyzer_and_extract_video_content()

    docs = rag.process_cu_scene_description(video_cu_result)
    print("There are " + str(len(docs)) + " documents.")

    # rag.split_documents_into_chunks()

    # embed and index the docs:
    vector_store = rag.embed_and_index_chunks(docs)
    
    # Set your query
    query = "japan"
    
    # Perform a similarity search
    docs = vector_store.similarity_search(
        query=query,
        k=3,
        search_type="similarity",
    )
    for doc in docs:
        print(doc.page_content)

    # Perform a hybrid search using the search_type parameter
    docs = vector_store.hybrid_search(query=query, k=3)
    for doc in docs:
        print(doc.page_content)

    # Setup rag chain
    prompt_str = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {context} 
    Answer:"""

    rag_chain = rag.setup_video_rag_chain(vector_store)
    while True:
        query = input("Enter your query: ")
        if query=="":
            break
        rag.conversational_search(rag_chain, query)