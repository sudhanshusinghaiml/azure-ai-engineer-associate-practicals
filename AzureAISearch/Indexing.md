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


### [Create Index Field Definition](https://learn.microsoft.com/en-us/rest/api/searchservice/create-index#-field-definitions-)
- **name**:	Required. Sets the name of the field, which must be unique within the fields collection of the index or parent field.

- **type**:	Required. Sets the data type for the field. Fields can be simple or complex. Simple fields are of primitive types, like Edm.String for text or Edm.Int32 for integers. Complex fields can have sub-fields that are themselves either simple or complex. This allows you to model objects and arrays of objects, which in turn enables you to upload most JSON object structures to your index. See Supported data types (Azure AI Search) for the complete list of supported types.

- **key**:	Required. Set this attribute to true to designate that a field's values uniquely identify documents in the index. The maximum length of values in a key field is 1024 characters. Exactly one top-level field in each index must be chosen as the key field and it must be of type Edm.String. Default is false for simple fields and null for complex fields.
Key fields can be used to look up documents directly and update or delete specific documents. The values of key fields are handled in a case-sensitive manner when looking up or indexing documents. See Lookup Document (Azure AI Search REST API) and Add, Update or Delete Documents (Azure AI Search REST API) for details.

- **retrievable**:	Indicates whether the field can be returned in a search result. Set this attribute to false if you want to use a field (for example, margin) as a filter, sorting, or scoring mechanism but don't want the field to be visible to the end user. This attribute must be true for key fields, and it must be null for complex fields. This attribute can be changed on existing fields. Setting retrievable to true doesn't cause any increase in index storage requirements. Default is true for simple fields and null for complex fields.

- **searchable**: 
    - Indicates whether the field is full-text searchable and can be referenced in search queries. This means it will undergo lexical analysis such as word-breaking during indexing. 
    - If you set a searchable field to a value like "Sunny day", internally it will be normalized and split into the individual tokens "sunny" and "day". 
    - This enables full-text searches for these terms. Fields of type Edm.String or Collection(Edm.String) are searchable by default. This attribute must be false for simple fields of other non-string data types, and it must be null for complex fields.
    - A searchable field consumes extra space in your index since Azure AI Search will process the contents of those fields and organize them in auxiliary data structures for performant searching. If you want to save space in your index and you don't need a field to be included in searches, set searchable to false. See How full-text search works in Azure AI Search for details.

- **filterable**:	
    - Indicates whether to enable the field to be referenced in `$filter` queries. 
    - Filterable differs from searchable in how strings are handled. 
    - Fields of type Edm.String or Collection(Edm.String) that are filterable don't undergo lexical analysis, so comparisons are for exact matches only. For example, if you set such a field f to "Sunny day", `$filter=f` eq 'sunny' will find no matches, but `$filter=f` eq 'Sunny day' will.
    - This attribute must be null for complex fields. Default is true for simple fields and null for complex fields. To reduce index size, set this attribute to false on fields that you won't be filtering on.
- **sortable**:	Indicates whether to enable the field to be referenced in $orderby expressions. By default Azure AI Search sorts results by score, but in many experiences users will want to sort by fields in the documents. A simple field can be sortable only if it's single-valued (it has a single value in the scope of the parent document).
Simple collection fields can't be sortable, since they're multi-valued. Simple sub-fields of complex collections are also multi-valued, and therefore can't be sortable. This is true whether it's an immediate parent field, or an ancestor field, that's the complex collection. Complex fields can't be sortable and the sortable attribute must be null for such fields. The default for sortable is true for single-valued simple fields, false for multi-valued simple fields, and null for complex fields.
- **facetable**:	Indicates whether to enable the field to be referenced in facet queries. Typically used in a presentation of search results that includes hit count by category (for example, search for digital cameras and see hits by brand, by megapixels, by price, and so on). This attribute must be null for complex fields. Fields of type Edm.GeographyPoint or Collection(Edm.GeographyPoint) can't be facetable. Default is true for all other simple fields. To reduce index size, set this attribute to false on fields that you won't be faceting on.
- **analyzer**:	Sets the lexical analyzer for tokenizing strings during indexing and query operations. Valid values for this property include language analyzers, built-in analyzers, and custom analyzers. The default is standard.lucene. This attribute can only be used with searchable string fields, and it can't be set together with either searchAnalyzer or indexAnalyzer. Once the analyzer is chosen and the field is created in the index, it can't be changed for the field. Must be null for complex fields.
- **searchAnalyzer**:	Set this property in conjunction with indexAnalyzer to specify different lexical analyzers for indexing and queries. If you use this property, set analyzer to null and make sure indexAnalyzer is set to an allowed value. Valid values for this property include built-in analyzers and custom analyzers. This attribute can be used only with searchable fields. The search analyzer can be updated on an existing field since it's only used at query-time. Must be null for complex fields.
- **indexAnalyzer**:	Set this property in conjunction with searchAnalyzer to specify different lexical analyzers for indexing and queries. If you use this property, set analyzer to null and make sure searchAnalyzer is set to an allowed value. Valid values for this property include built-in analyzers and custom analyzers. This attribute can be used only with searchable fields. Once the index analyzer is chosen, it can't be changed for the field. Must be null for complex fields.
- **synonymMaps**:	A list of the names of synonym maps to associate with this field. This attribute can be used only with searchable fields. Currently only one synonym map per field is supported. Assigning a synonym map to a field ensures that query terms targeting that field are expanded at query-time using the rules in the synonym map. This attribute can be changed on existing fields. Must be null or an empty collection for complex fields.
- **fields**:	A list of sub-fields if this is a field of type Edm.ComplexType or Collection(Edm.ComplexType). Must be null or empty for simple fields. See How to model complex data types in Azure AI Search for more information on how and when to use sub-fields.
