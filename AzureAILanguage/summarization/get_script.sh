curl -X GET $LANGUAGE_ENDPOINT/language/analyze-text/jobs/203c3b88-8186-4315-8232-218379903046?api-version=2023-04-01 \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: $LANGUAGE_KEY" \
-o "./SampleCodes/summarization/response2.json"