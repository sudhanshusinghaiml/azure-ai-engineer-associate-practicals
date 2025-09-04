from search_with_multimodal_rag import MultiModalRAGSearch


if __name__ == "__main__":
    rag = MultiModalRAGSearch()
    all_splits = rag.process_allJSON_content()

    print("There are " + str(len(all_splits)) + " documents.") 
    # Print the content of all doc splits
    for idx, doc in enumerate(all_splits):
        print(f"{idx} split doc content is:", doc.page_content)

    # embed and index the docs:
    vector_store = rag.embed_and_index_chunks(all_splits)

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

    rag_chain = rag.setup_rag_chain(vector_store)
    while True:
        query = input("Enter your query: ")
        if query=="":
            break
        rag.conversational_search(rag_chain, query)