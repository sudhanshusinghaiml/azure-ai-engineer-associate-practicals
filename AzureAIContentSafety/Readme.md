# [AzureAIContentSafety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview)

- Applying basic text moderation with the Content Safety Studio, REST API, or client libraries. The Azure AI Content Safety service provides you with AI algorithms for flagging objectionable content.

### [Analyze text content](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-text?tabs=visual-studio%2Cwindows&pivots=programming-language-rest)
The following section walks through a sample request with cURL. Paste the command below into a text editor, and make the following changes.
    - Replace <endpoint> with the endpoint URL associated with your resource.
    - Replace <your_subscription_key> with one of the keys that come with your resource.
    - Optionally, replace the "text" field in the body with your own text you'd like to analyze
```JSON
curl --location --request POST '<endpoint>/contentsafety/text:analyze?api-version=2024-09-01' \
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "text": "I hate you",
  "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
  "blocklistNames": ["string"],
  "haltOnBlocklistHit": true,
  "outputType": "FourSeverityLevels"
}'
```

### [Create a blocklist](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-blocklist?tabs=visual-studio%2Cwindows&pivots=programming-language-rest)
The following section walks through a sample request with cURL. Paste the command below into a text editor, and make the following changes.
  - Replace <endpoint> with the endpoint URL associated with your resource.
  - Replace <your_subscription_key> with one of the keys that come with your resource.
  - Replace <your_blocklist_name> with a name for your blocklist.
  - Optionally, replace the "description" field in the body with your own description of the list.

```JSON
curl --location --request PATCH '<endpoint>/contentsafety/text/blocklists/<your_blocklist_name>?api-version=2024-09-01' 
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' 
-header 'Content-Type: application/json' 
--data-raw '{"description": "This is a violence list"}'
```

### [Analyze image content](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-image?tabs=visual-studio%2Cwindows&pivots=programming-language-rest)
  - Replace <endpoint> with your resource endpoint URL.
  - Replace <your_subscription_key> with your key.
  - Populate the "image" field in the body with either a "content" field or a "blobUrl" field. For example: {"image": {"content": "<base_64_string>"} or {"image": {"blobUrl": "<your_storage_url>"}.

```JSON
curl --location --request POST '<endpoint>/contentsafety/image:analyze?api-version=2024-09-01' \
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "image": {
    "content": "<base_64_string>"
  },
  "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
  "outputType": "FourSeverityLevels"
}'
```

### [Harm categories in Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/harm-categories?tabs=warning)
- Azure AI Content Safety uses harm categories to flag and rate objectionable content in both text and images. This guide describes all of the harm categories and ratings that Azure AI Content Safety uses. 
- Understanding these categories helps you configure moderation and compliance for your use cases. Both text and image content use the same set of flags.
- Classification can be multi-labeled. For example, when a text sample goes through the text moderation model, it could be classified as both Sexual content and Violence.

#### Severity levels
- Every harm category the service applies also comes with a severity level rating. The severity level is meant to indicate the severity of the consequences of showing the flagged content.

- **Text**: The current version of the text model supports the full 0-7 severity scale. The classifier detects among all severities along this scale. If the user specifies, it can return severities in the trimmed scale of 0, 2, 4, and 6; each two adjacent levels are mapped to a single level.
```Python
[0,1] -> 0
[2,3] -> 2
[4,5] -> 4
[6,7] -> 6
```
- **Image**: The current version of the image model supports the trimmed version of the full 0-7 severity scale. The classifier only returns severities 0, 2, 4, and 6.
```Python
0
2
4
6
```

- **Image with text**: The current version of the multimodal model supports the full 0-7 severity scale. The classifier detects among all severities along this scale. If the user specifies, it can return severities in the trimmed scale of 0, 2, 4, and 6; each two adjacent levels are mapped to a single level.
```Python
[0,1] -> 0
[2,3] -> 2
[4,5] -> 4
[6,7] -> 6
```

### AIContentSafety References:
1. [Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection)
2. [Groundedness detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness)
3. [Protected Material Detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/protected-material?tabs=text)
