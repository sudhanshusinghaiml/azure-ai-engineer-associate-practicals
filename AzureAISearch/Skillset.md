# Create a skillset in AzureAI Search
A skillset defines operations that generate textual content and structure from documents that contain images or unstructured text. Examples are optical character recognition (OCR) for images, entity recognition for undifferentiated text, and text translation. A skillset executes after text and images are extracted from an external data source, and after field mappings are processed.

### Rules for skillset definition include:
- Must have a unique name within the skillset collection. A skillset is a top-level resource that can be used by any indexer.
- Must have at least one skill. Three to five skills are typical. The maximum is 30.
- A skillset can repeat skills of the same type. For example, a skillset can have multiple Shaper skills.
- A skillset supports chained operations, looping, and branching.

### Add a skillset definition

```JSON
{
   "name":"skillset-template",
   "description":"A description makes the skillset self-documenting (comments aren't allowed in JSON itself)",
   "skills":[
       
   ],
   "cognitiveServices":{
      "@odata.type":"#Microsoft.Azure.Search.CognitiveServicesByKey",
      "description":"An Azure AI services resource in the same region as Azure AI Search",
      "key":"<Your-Cognitive-Services-Multi-Service-Key>"
   },
   "knowledgeStore":{
      "storageConnectionString":"<Your-Azure-Storage-Connection-String>",
      "projections":[
         {
            "tables":[ ],
            "objects":[ ],
            "files":[ ]
         }
      ]
    },
    "encryptionKey":{ }
}
```

- After the name and description, a skillset has four main properties:

    - **skills** array, an unordered collection of skills. Skills can be utilitarian (like splitting text), transformational (based on AI from Azure AI services), or custom skills that you provide. An example of a skills array is provided in the next section.

    - **cognitiveServices** is used for billable skills that call Azure AI services APIs. Remove this section if you aren't using billable skills or Custom Entity Lookup. If you are, attach an Azure AI services multi-service resource.

    - **knowledgeStore (optional)** specifies an Azure Storage account and settings for projecting skillset output into tables, blobs, and files in Azure Storage. Remove this section if you don't need it, otherwise specify a knowledge store.

    - **encryptionKey (optional)** specifies an Azure Key Vault and customer-managed keys used to encrypt sensitive content (descriptions, connection strings, keys) in a skillset definition. Remove this property if you aren't using customer-managed encryption.


### Add skills
- All skills have a type, context, inputs, and outputs. A skill might optionally have a name and description. The following example shows two unrelated built-in skills so that you can compare the basic structure.

```JSON
"skills": [
    {
        "@odata.type": "#Microsoft.Skills.Text.V3.EntityRecognitionSkill",
        "name": "#1",
        "description": "This skill detects organizations in the source content",
        "context": "/document",
        "categories": [
            "Organization"
        ],
        "inputs": [
            {
                "name": "text",
                "source": "/document/content"
            }
        ],
        "outputs": [
            {
                "name": "organizations",
                "targetName": "orgs"
            }
        ]
    },
    {
        "name": "#2",
        "description": "This skill detects corporate logos in the source files",
        "@odata.type": "#Microsoft.Skills.Vision.ImageAnalysisSkill",
        "context": "/document/normalized_images/*",
        "visualFeatures": [
            "brands"
        ],
        "inputs": [
            {
                "name": "image",
                "source": "/document/normalized_images/*"
            }
        ],
        "outputs": [
            {
                "name": "brands"
            }
        ]
    }
]
```

### Set skill context
- Each skill has a context property that determines the level at which operations take place. If the context property isn't explicitly set, the default is "/document", where the context is the whole document (the skill is called once per document).
- The context property is usually set to one of the following examples:
    - **context: /document**:	(Default) Inputs and outputs are at the document level.
    - **context: /document/pages/**:	Some skills like sentiment analysis perform better over smaller chunks of text. If you're splitting a large content field into pages or sentences, the context should be over each component part.
    - **context: /document/normalized_images/**: For image content, inputs and outputs are one per image in the parent document.

```JSON
"skills":[
  {
    "@odata.type": "#Microsoft.Skills.Text.V3.EntityRecognitionSkill",
    "context": "/document",
    "inputs": [],
    "outputs": []
  },
  {
      "@odata.type": "#Microsoft.Skills.Vision.ImageAnalysisSkill",
      "context": "/document/normalized_images/*",
      "visualFeatures": [],
      "inputs": [],
      "outputs": []
  }
]
```

### Define inputs
- Skills read from and write to an enriched document. Skill inputs specify the origin of the incoming data. It's often the root node of the enriched document. For blobs, a typical skill input is the document's content property.

- Skill reference documentation for each skill describes the inputs it can consume. Each input has a name that identifies a specific input, and a source that specifies the location of the data in the enriched document. The following example is from the Entity Recognition skill:
```JSON
"inputs": [
    {
        "name": "text", 
        "source": "/document/content"
    },
    {
        "name": "languageCode", 
        "source": "/document/language"
    }
]
```

- Skills can have multiple inputs. The name is the specific input. For Entity Recognition, the specific inputs are text and languageCode.

- The source property specifies which field or row provides the content to be processed. For text-based skills, the source is a field in the document or row that provides text. For image-based skills, the node providing the input is normalized images.

    - **source:/document**:	For a tabular data set, a document corresponds to a row.
    - **source:/document/content**:	For blobs, the source is usually the blob's content property.
    - **source:/document/some-named-field**: For text-based skills, such as entity recognition or key phrase extraction, the origin should be a field that contains sufficient text to be analyzed, such as a description or summary.
    - **source:/document/normalized_images/**: For image content, the source is image that's been normalized during document cracking.


### Define outputs
- Each skill is designed to emit specific kinds of output, which are referenced by name in the skillset. A skill output has a name and an optional targetName.

- Skill reference documentation for each skill describes the outputs it can produce. The following example is from the Entity Recognition skill:

```JSON
"outputs": [
    {
        "name": "persons", 
        "targetName": "people"
    },
    {
        "name": "organizations", 
        "targetName": "orgs"
    },
    {
        "name": "locations", 
        "targetName": "places"
    }
]
```

- Skills can have multiple outputs. The name property identifies a specific output. For example, for Entity Recognition, output can be persons, locations, organizations, among others.

- The targetName property specifies the name you would like this node to have in the enriched document. This is useful if skill outputs have the same name. If you have multiple skills that return the same output, use targetName for name disambiguation in enrichment node paths. If the target name is unspecified, the name property is used for both.