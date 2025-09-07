import os

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv

load_dotenv()

# set `<your-key>`, `<your-endpoint>`, and  `<region>` variables with the values from the Azure portal
key = os.getenv("AITRANSALTOR_API_KEY")
endpoint = os.getenv("AITRANSALTOR_ENDPOINT")
region = os.getenv("AITRANSLATOR_REGION")

# print(f"key: {key}")
# print(f"endpoint: {endpoint}")
# print(f"region: {region}")

credential = TranslatorCredential(key, region)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

try:
    source_language = "en"
    target_languages = ["hi"]
    input_text_elements = [ InputTextItem(text = "How are you") ]

    response = text_translator.translate(content = input_text_elements, to = target_languages, from_parameter = source_language)
    translation = response[0] if response else None

    if translation:
        for translated_text in translation.translations:
            print(f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")

except HttpResponseError as exception:
    print(f"Error Code: {exception.error.code}")
    print(f"Message: {exception.error.message}")