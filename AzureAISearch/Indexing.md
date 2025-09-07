# Indexing in Azure AI Search

### [Add synonyms in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-synonyms?tabs=python%2Crest-assign)
- On a search service, a synonym map associates equivalent terms, expanding the scope of a query without the user having to actually provide the term. 
- For example, assuming dog, canine, and puppy are mapped synonyms, a query on canine matches on a document containing dog. You might create multiple synonym maps for different languages, such as English and French versions, or lexicons if your content includes technical jargon, slang, or obscure terminology.

- ***Some key points about synonym maps:***
    - A synonym map is a top-level resource that can be created once and used by many indexes.
    - A synonym map applies to string fields.
    - You can create and assign a synonym map at any time with no disruption to indexing or queries.
    - Your service tier sets the limits on how many synonym maps you can create.
    - Your search service can have multiple synonym maps, but within an index, a field definition can only have one synonym map assignment.


### [Configure a suggester for autocomplete and suggestions in a query](https://learn.microsoft.com/en-us/azure/search/index-add-suggesters)
- In Azure AI Search, typeahead or "search-as-you-type" is enabled by using a suggester. 
- A suggester is a configuration in an index that specifies which fields should be used to populate autocomplete and suggested matches. These fields undergo extra tokenization, generating prefix sequences to support matches on partial terms. 
- For example, a suggester that includes a city field with a value for Seattle has prefix combinations of sea, seat, seatt, and seattl to support typeahead.
- Matches on partial terms can be either an autocompleted query or a suggested match. The same suggester supports both experiences.


### You are developing the smart e-commerce project. You need to implement autocompletion as part of the Cognitive Search solution. Which three actions should you perform?
- Official Process of how to create suggester is:
    - Choose the fields
    - Choose the analyzer
    - Use a Suggester

- Answer is:
    - Set the analyzer property for the three product name variants. Because it ensures that the text is processed correctly, considering the specific language or custom processing required. This helps in generating accurate autocomplete suggestions by applying the correct text analysis to the product name fields.
    - Add a suggester that has the three product name fields as source fields. Because a suggester is needed to define the fields from which autocomplete suggestions will be generated. By including all relevant product name fields, the system can provide comprehensive suggestions that account for different ways products might be named or referred to
    - Make API queries to the autocomplete endpoint and include suggesterName in the body. Because it specifies which suggester to use for autocompletion. This is essential for retrieving relevant suggestions based on user input, making the autocomplete functionality effective.


