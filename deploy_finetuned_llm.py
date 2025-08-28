""" 
Deploy a fine-tuned model for inferencing
==========================================
    Once your model is fine-tuned, you can deploy the model and can use it in your own application.
    When you deploy the model, you make the model available for inferencing, and that incurs an hourly hosting charge. 
    Fine-tuned models, however, can be stored in Azure AI Foundry at no cost until you're ready to use them.
    Azure OpenAI provides choices of deployment types for fine-tuned models on the hosting structure that fits 
    different business and usage patterns: Standard, Global Standard (preview) and Provisioned Throughput (preview). 
    Learn more about deployment types and concepts of all deployment types:
    https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning-deploy?tabs=python
"""

""" 
    There are multiple types of deployment:
    1. Deploy your fine-tuned model
    2. Cross region deployment
    3. Cross tenant deployment
    4. Use your deployed fine-tuned model
"""

import json
import os
import requests

token = os.getenv("<TOKEN>") 
subscription = "<YOUR_SUBSCRIPTION_ID>"  
resource_group = "<YOUR_RESOURCE_GROUP_NAME>"
resource_name = "<YOUR_AZURE_OPENAI_RESOURCE_NAME>"
model_deployment_name = "gpt-35-turbo-ft" # custom deployment name that you will use to reference the model when making inference calls.

deploy_params = {'api-version': "2024-10-21"} 
deploy_headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}

deploy_data = {
    "sku": {"name": "standard", "capacity": 1}, 
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": "fine_tuned_model", #retrieve this value from the previous call, it will look like gpt-35-turbo-0125.ft-b044a9d3cf9c4228b5d393567f693b83
            "version": "1"
        }
    }
}
deploy_data = json.dumps(deploy_data)

request_url = f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{resource_name}/deployments/{model_deployment_name}'

print('Creating a new deployment...')

r = requests.put(request_url, params=deploy_params, headers=deploy_headers, data=deploy_data)

print(r)
print(r.reason)
print(r.json())