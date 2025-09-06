# CustomSkills in Azure AI Search

## [AML skill in an Azure AI Search enrichment pipeline](https://learn.microsoft.com/en-us/azure/search/cognitive-search-aml-skill)
- Skill inputs
    - Skill inputs are a node of the enriched document created during document cracking. For example, it might be the root document, a normalized image, or the content of a blob. There are no predefined inputs for this skill. For inputs, you should specify one or more nodes that are populated at the time of the AML skill's execution.

- Skill outputs
    - Skill outputs are new nodes of an enriched document created by the skill. There are no predefined outputs for this skill. For outputs, you should provide nodes that can be populated from the JSON response of your AML skill.

- Sample Definition:

```JSON
{
    "@odata.type": "#Microsoft.Skills.Custom.AmlSkill",
    "description": "A custom model that detects the language in a document.",
    "uri": "https://language-model.models.contoso.com/score",
    "context": "/document",
    "inputs": [
      {
        "name": "text",
        "source": "/document/content"
      }
    ],
    "outputs": [
      {
        "name": "detected_language_code"
      }
    ]
}
```


## [GenAI Prompt skill](https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-genai-prompt)

- Sample definition for Text-Only Summarization
```JSON
{
  "@odata.type": "#Microsoft.Skills.Custom.ChatCompletionSkill",
  "name": "Summarizer",
  "description": "Summarizes document content.",
  "context": "/document",
  "timeout": "PT30S",
  "inputs": [
    { "name": "text", "source": "/document/content" },
    { "name": "systemMessage", "source": "='You are a concise AI assistant.'" },
    { "name": "userMessage", "source": "='Summarize the following text:'" }
  ],
  "outputs": [ { "name": "response" } ],
  "uri": "https://demo.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
  "apiKey": "<api-key>",
  "commonModelParameters": { "temperature": 0.3 }
}
```

- Sample definition for Text-Image Description
```JSON
{
  "@odata.type": "#Microsoft.Skills.Custom.ChatCompletionSkill",
  "name": "Image Describer",
  "context": "/document/normalized_images/*",
  "inputs": [
    { "name": "image", "source": "/document/normalized_images/*/data" },
    { "name": "imageDetail", "source": "=high" },
    { "name": "systemMessage", "source": "='You are a useful AI assistant.'" },
    { "name": "userMessage", "source": "='Describe this image:'" }
  ],
  "outputs": [ { "name": "response" } ],
  "uri": "https://demo.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
  "authIdentity": "11111111-2222-3333-4444-555555555555",
  "responseFormat": { "type": "text" }
}
```

- Structured numerical fact-finder
```JSON
{
  "@odata.type": "#Microsoft.Skills.Custom.ChatCompletionSkill",
  "name": "NumericalFactFinder",
  "context": "/document",
  "inputs": [
    { "name": "systemMessage", "source": "='You are an AI assistant that helps people find information.'" },
    { "name": "userMessage", "source": "='Find all the numerical data and put it in the specified fact format.'"}, 
    { "name": "text", "source": "/document/content" }
  ],
  "outputs": [ { "name": "response" } ],
  "uri": "https://demo.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
  "apiKey": "<api-key>",
  "responseFormat": {
    "type": "json_schema",
    "jsonSchemaProperties": {
      "name": "NumericalFactObj",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "facts": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": { "type": "number" },
                "fact": { "type": "string" }
              },
              "required": [ "number", "fact" ]
            }
          }
        },
        "required": [ "facts" ],
        "additionalProperties": false
      }
    }
  }
}
```

## [Custom Entity Lookup: Sample skill definition](https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-custom-entity-lookup)
- A sample skill definition using an inline format is shown below:
```JSON
{
    "@odata.type": "#Microsoft.Skills.Text.CustomEntityLookupSkill",
    "context": "/document",
    "inlineEntitiesDefinition": 
    [
      { 
        "name" : "Bill Gates",
        "description" : "Microsoft founder." ,
        "aliases" : [ 
            { "text" : "William H. Gates", "caseSensitive" : false },
            { "text" : "BillG", "caseSensitive" : true }
        ]
      }, 
      { 
        "name" : "Xbox One", 
        "type": "Hardware",
        "subtype" : "Gaming Device",
        "id" : "4e36bf9d-5550-4396-8647-8e43d7564a76",
        "description" : "The Xbox One product"
      }
    ],    
    "inputs": [
      {
        "name": "text",
        "source": "/document/content"
      }
    ],
    "outputs": [
      {
        "name": "entities",
        "targetName": "matchedEntities"
      }
    ]
  }
```

- Alternatively, you can point to an external entities definition file. A sample skill definition using the entitiesDefinitionUri format is shown below:

```JSON
{
    "@odata.type": "#Microsoft.Skills.Text.CustomEntityLookupSkill",
    "context": "/document",
    "entitiesDefinitionUri": "https://myblobhost.net/keyWordsConfig.csv",    
    "inputs": [
      {
        "name": "text",
        "source": "/document/content"
      }
    ],
    "outputs": [
      {
        "name": "entities",
        "targetName": "matchedEntities"
      }
    ]
  }
```

## [Custom Web API Skill](https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-web-api)

- The Custom Web API skill allows you to extend AI enrichment by calling out to a Web API endpoint providing custom operations.
- Similar to built-in skills, a Custom Web API skill has inputs and outputs. Depending on the inputs, your Web API receives a JSON payload when the indexer runs, and outputs a JSON payload as a response, along with a success status code. 
- The response is expected to have the outputs specified by your custom skill. Any other response is considered an error and no enrichments are performed.



- Sample Definition
```JSON
{
  "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
  "description": "A custom skill that can identify positions of different phrases in the source text",
  "uri": "https://contoso.count-things.com",
  "batchSize": 4,
  "context": "/document",
  "inputs": [
    {
      "name": "text",
      "source": "/document/content"
    },
    {
      "name": "language",
      "source": "/document/languageCode"
    },
    {
      "name": "phraseList",
      "source": "/document/keyphrases"
    }
  ],
  "outputs": [
    {
      "name": "hitPositions"
    }
  ]
}
```
