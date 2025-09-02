#!/bin/bash

# ./SampleCodes/entity_linking/script.sh

# LANGUAGE_ENDPOINT = https://mslearn-azureai-foundry.cognitiveservices.azure.com/"
# LANGUAGE_ENDPOINT = https://{resource_name}.cognitiveservices.azure.com/"

# Script not working

curl -X POST $LANGUAGE_ENDPOINT/language/:analyze-text?api-version=2023-04-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: $LANGUAGE_KEY" \
-d "@./SampleCodes/sentiment_analysis/payload.json" \
-o "./SampleCodes/sentiment_analysis/response.json"
