import os

from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import SingleDocumentTranslationClient
# from azure.ai.translation.document.aio import DocumentTranslateContent

from dotenv import load_dotenv


load_dotenv()

key = os.getenv("AITRANSALTOR_API_KEY")
endpoint = os.getenv("AITRANSALTOR_ENDPOINT")
region = os.getenv("AITRANSLATOR_REGION")


"""
FILE: synchronous_document_translation.py

DESCRIPTION:
    This sample demonstrates how to invoke synchronous document translation operations.

USAGE:
    python synchronous_document_translation.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_DOCUMENT_TRANSLATION_ENDPOINT - the endpoint to your Document Translation resource.
    2) AZURE_DOCUMENT_TRANSLATION_KEY - your Document Translation API key.
"""

TEST_INPUT_FILE_NAME = os.path.abspath(
    os.path.join(os.path.abspath(__file__), "..", "input.txt")
)

print(f"TEST_INPUT_FILE_NAME: {TEST_INPUT_FILE_NAME}")

def single_document_translation():
    # [START synchronous_document_translation]

    client = SingleDocumentTranslationClient(endpoint, AzureKeyCredential(key))
    target_languages = "hi"
    file_name = os.path.basename(TEST_INPUT_FILE_NAME)
    print(f"File for translation: {file_name}")
    file_type = "text/html"
    with open(TEST_INPUT_FILE_NAME, "r") as file:
        file_contents = file.read()

    document_content = (file_name, file_contents, file_type)
    document_translate_content = DocumentTranslateContent(document=document_content)

    response_stream = client.translate(body=document_translate_content, target_language=target_languages)
    translated_response = response_stream.decode("utf-8-sig")  # type: ignore[attr-defined]
    print(f"Translated response: {translated_response}")

    # [END synchronous_document_translation]


def multiple_document_translation():

    client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))

    sourceUrl = "<your-source container-url>"
    targetUrl = "<your-target-container-url>"
    targetLanguage = "<target-language-code>"

    poller = client.begin_translation(sourceUrl, targetUrl, targetLanguage)
    result = poller.result()

    print(result)

if __name__ == "__main__":
    multiple_document_translation()