"""
    Source: Promptflow to manage conversations: https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/03-Use-prompt-flow-chat.html
    A prompt flow provides a way to orchestrate prompts and other activities to define an interaction with a 
    generative AI model. In this exercise, you’ll use a template to create a basic chat flow for an AI assistant 
    in a travel agency.
"""

"""
    Using the instructions, create a chatflow and test it. Then deploy the changes into server.
    Once the endpoint is deployed, we can test it using the below sample code.
"""


import urllib.request
import json
import os
from dotenv import load_dotenv

_ = load_dotenv()

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
def main():
        
    data = {}

    body = str.encode(json.dumps(data))

    url = os.getenv("PROMPTFLOW_CHAT_APP_ENDPOINT")
    # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
    api_key = os.getenv("CHAT_APP_ENDPOINT_API_KEY")
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")


    headers = {'Content-Type':'application/json', 'Accept': 'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))


if __name__ == '__main__':
    main()