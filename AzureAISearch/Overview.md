# Basic: AI Enrichment Workflow

- An enrichment pipeline consists of indexers that have skillsets. Post-indexing, you can query an index to validate your results.

- Start with a subset of data in a supported data source. Indexer and skillset design is an iterative process. The work goes faster with a small representative data set.

    - Create a data source that specifies a connection to your data.

    - Create a skillset. Unless your project is small, you should attach an Azure AI services multi-service resource. If you're creating a knowledge store, define it within the skillset.

    - Create an index schema that defines a search index.

    - Create and run the indexer to bring all of the above components together. This step retrieves the data, runs the skillset, and loads the index. An indexer is also where you specify field mappings and output field mappings that set up the data path to a search index.

    - Optionally, enable enrichment caching in the indexer configuration. This step allows you to reuse existing enrichments later on.

    - Run queries to evaluate results or start a debug session to work through any skillset issues.

- To repeat any of the above steps, reset the indexer before you run it. Or, delete and recreate the objects on each run (recommended if you’re using the free tier). If you enabled caching the indexer pulls from the cache if data is unchanged at the source, and if your edits to the pipeline don't invalidate the cache.


## Resources for Reference:

1. [Python samples for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/samples-python)

2. [AI enrichment in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/cognitive-search-concept-intro)

3. [Knowledge store in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/knowledge-store-concept-intro?tabs=portal)

4. [Skillset concepts in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/cognitive-search-working-with-skillsets)

5. [Indexers in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-indexer-overview)

5. [Create a skillset in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/cognitive-search-defining-skillset)

6. [Create a knowledge store using REST](https://learn.microsoft.com/en-us/azure/search/knowledge-store-create-rest)

7. [Knowledge Store Projections](https://learn.microsoft.com/en-us/azure/search/knowledge-store-projection-overview)