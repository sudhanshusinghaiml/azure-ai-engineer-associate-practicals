#!/bin/bash

# ./SampleCodes/key_phrase_extraction/script.sh

# LANGUAGE_ENDPOINT = https://mslearn-azureai-foundry.cognitiveservices.azure.com/"
# LANGUAGE_ENDPOINT = https://{resource_name}.cognitiveservices.azure.com/" 

curl -X POST $LANGUAGE_ENDPOINT/language/:analyze-text?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: $LANGUAGE_KEY" \
-d "@./SampleCodes/language_detection/payload.json" \
-o "./SampleCodes/language_detection/response.json"


