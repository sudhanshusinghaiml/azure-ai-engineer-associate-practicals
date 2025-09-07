"""
    Source: https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/01-Explore-ai-studio.html
    Prepare for an AI development project
"""

import os
from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv

_ = load_dotenv()


llm = AzureChatOpenAI(
    api_version= os.getenv("OPENAI_API_VERSION"),
    azure_endpoint= os.getenv("AZURE_ENDPOINT"),
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    max_tokens = 15000,
    temperature = 1.0,
    azure_deployment = os.getenv("MODEL_NAME")
)

print(f"Client for AzureOpenAI Created....")

messages = [
    (
        "system",
        "You are a helpful Tax Assistant",
    ),
    (
        "user",
        "I want to understand the latest changes in the Indian Tax systems",
    ),
]

response = llm.invoke(messages)

print(response.content)