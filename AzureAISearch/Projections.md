# [Define projections in a knowledge store](https://learn.microsoft.com/en-us/azure/search/knowledge-store-projections-examples)
- Projections are the component of a knowledge store definition that determines how AI enriched content is stored in Azure Storage. 
- Projections determine the type, quantity, and composition of the data structures containing your content.
- The syntax for each type of projection:
    - Table projections
    - Object projections
    - File projections

Projections are defined under the knowledgeStore property of a skillset:
```JSON
"knowledgeStore" : {
    "storageConnectionString": "DefaultEndpointsProtocol=https;AccountName=<Acct Name>;AccountKey=<Acct Key>;",
    "projections": [
      {
        "tables": [ ],
        "objects": [ ],
        "files": [ ]
      }
    ]
}
```

### Define a table projection
- Table projections are recommended for scenarios that call for data exploration, such as analysis with Power BI or workloads that consume data frames. The tables section of a projections array is a list of tables that you want to project.
- To define a table projection, use the tables array in the projections property. A table projection has three required properties:
    - **tableName**:    Determines the name of a new table created in Azure Table Storage.
    - **generatedKeyName**:	Column name for the key that uniquely identifies each row. The value is system-generated. If you omit this property, a column is created automatically that uses the table name and "key" as the naming convention.
    - **source**:	A path to a node in an enrichment tree. The node should be a reference to a complex shape that determines which columns are created in the table.

- In table projections, **source** is usually the output of a **Shaper skill** that defines the shape of the table. 
- **Tables** have rows and columns, and shaping is the mechanism by which rows and columns are specified. 
- You can use a **Shaper skill** or inline shapes. The Shaper skill produces valid JSON, but the source could be the output from any skill, if valid JSON.

- **Single table example**:
    - The schema of a table is specified partly by the projection (table name and key), and also by the source that provides the shape of table (columns).
    ```JSON
    "projections" : [
        {
            "tables": [
            { "tableName": "Hotels", "generatedKeyName": "HotelId", "source": "/document/tableprojection" }
            ]
        }
    ]
    ```

    - Columns are derived from the "source". The following data shape containing HotelId, HotelName, Category, and Description will result in creation of those columns in the table.
    ```JSON
    {
        "@odata.type": "#Microsoft.Skills.Util.ShaperSkill",
        "name": "#3",
        "description": null,
        "context": "/document",
        "inputs": [
        {
            "name": "HotelId",
            "source": "/document/HotelId"
        },
        {
            "name": "HotelName",
            "source": "/document/HotelName"
        },
        {
            "name": "Category",
            "source": "/document/Category"
        },
        {
            "name": "Description",
            "source": "/document/Description"
        },
        ],
        "outputs": [
        {
            "name": "output",
            "targetName": "tableprojection"
        }
        ]
    }
    ```
- **Multiple table (slicing) example**:
    - For example, assume a Shaper skill outputs an "EnrichedShape" that contains hotel information, plus enriched content like key phrases, locations, and organizations. The main table would include fields that describe the hotel (ID, name, description, address, category). 
    - Key phrases would get the key phrase column. Entities would get the entity columns.
    ```JSON
    "projections" : [
        {
            "tables": [
            { "tableName": "MainTable", "generatedKeyName": "HotelId", "source": "/document/EnrichedShape" },
            { "tableName": "KeyPhrases", "generatedKeyName": "KeyPhraseId", "source": "/document/EnrichedShape/*/KeyPhrases/*" },
            { "tableName": "Entities", "generatedKeyName": "EntityId", "source": "/document/EnrichedShape/*/Entities/*" }
            ]
        }
    ]
    ```

### Define an object projection:
- Object projections are JSON representations of the enrichment tree that can be sourced from any node. 
- In comparison with table projections, object projections are simpler to define and are used when projecting whole documents. Object projections are limited to a single projection in a container and can't be sliced.
- To define an object projection, use the objects array in the projections property. An object projection has three required properties:
    - **storageContainer**:	Determines the name of a new container created in Azure Storage.
    - **generatedKeyName**:	Column name for the key that uniquely identifies each row. The value is system-generated. If you omit this property, a column is created automatically that uses the table name and "key" as the naming convention.
    - **source**:	A path to a node in an enrichment tree that is the root of the projection. The node is usually a reference to a complex data shape that determines blob structure.
    
    - The following example projects individual hotel documents, one hotel document per blob, into a container called hotels.
    ```JSON
    "knowledgeStore": {
        "storageConnectionString": "an Azure storage connection string",
        "projections" : [
            {
            "tables": [ ]
            },
            {
            "objects": [
                {
                "storageContainer": "hotels",
                "source": "/document/objectprojection",
                }
            ]
            },
            {
                "files": [ ]
            }
        ]
    }
    ```

    - The source is the output of a Shaper skill, named "objectprojection". Each blob has a JSON representation of each field input.
    ```JSON
    {
        "@odata.type": "#Microsoft.Skills.Util.ShaperSkill",
        "name": "#3",
        "description": null,
        "context": "/document",
        "inputs": [
            {
                "name": "HotelId",
                "source": "/document/HotelId"
            },
            {
                "name": "HotelName",
                "source": "/document/HotelName"
            },
            {
                "name": "Category",
                "source": "/document/Category"
            },
            {
                "name": "keyPhrases",
                "source": "/document/HotelId/keyphrases/*"
            },
        ],
        "outputs": [
            {
                "name": "output",
                "targetName": "objectprojection"
            }
        ]
    }
    ```


### Define a file projection

- File projections are always binary, normalized images, where normalization refers to potential resizing and rotation for use in skillset execution. 
- File projections, similar to object projections, are created as blobs in Azure Storage, and contain binary data (as opposed to JSON).
- To define a file projection, use the files array in the projections property. A files projection has three required properties:
    - **storageContainer**:	Determines the name of a new container created in Azure Storage.
    - **generatedKeyName**:	Column name for the key that uniquely identifies each row. The value is system-generated. If you omit this property, a column is created automatically that uses the table name and "key" as the naming convention.
    - **source**:	A path to a node in an enrichment tree that is the root of the projection. For images files, the source is always /document/normalized_images/*. File projections only act on the normalized_images collection. Neither indexers nor a skillset will pass through the original non-normalized image.
- The destination is always a blob container, with a folder prefix of the base64 encoded value of the document ID. If there are multiple images, they're placed together in the same folder. 
- File projections can't share the same container as object projections and need to be projected into a different container.
- The following example projects all normalized images extracted from the document node of an enriched document, into a container called myImages.
    ```JSON
    "projections": [
        {
            "tables": [ ],
            "objects": [ ],
            "files": [
                {
                    "storageContainer": "myImages",
                    "source": "/document/normalized_images/*"
                }
            ]
        }
    ]
    ```

### Test projections
- You can process projections by following these steps:
    - Set the knowledge store's storageConnectionString property to a valid V2 general purpose storage account connection string.
    - Update the skillset by issuing a PUT request with your projection definition in the body of the skillset.
    - Run the indexer to put the skillset into execution.
    - Monitor indexer execution to check progress and catch any errors.
    - Use Azure portal to verify object creation in Azure Storage.

If you're projecting tables, import them into Power BI for table manipulation and visualization. In most cases, Power BI autodiscovers the relationships among tables.
