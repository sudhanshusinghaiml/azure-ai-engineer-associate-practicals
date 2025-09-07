#!/bin/bash

# ./SampleCodes/entity_linking/script.sh

# LANGUAGE_ENDPOINT = https://mslearn-azureai-foundry.cognitiveservices.azure.com/"
# LANGUAGE_ENDPOINT = https://{resource_name}.cognitiveservices.azure.com/" 

curl -X POST $LANGUAGE_ENDPOINT/language/:analyze-text?api-version=2022-05-01 \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: $LANGUAGE_KEY" \
-d "@./SampleCodes/entity_linking/payload.json" \
-o "./SampleCodes/entity_linking/response.json"
