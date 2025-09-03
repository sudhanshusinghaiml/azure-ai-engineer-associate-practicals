"""
language_support: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt
"""

import os
import azure.cognitiveservices.speech as speechsdk

from dotenv import load_dotenv

load_dotenv()

def recognize_from_microphone():
     # This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
     # Replace with your own subscription key and endpoint, 
     # the endpoint is like : "https://YourServiceRegion.api.cognitive.microsoft.com"

    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get('SPEECH_KEY'), 
        endpoint=os.environ.get('SPEECH_ENDPOINT'),
        region = "eastus2")
    
    speech_config.speech_recognition_language="en-US"

    # Audio Files downloaded from: https://www.kaggle.com/datasets/pavanelisetty/sample-audio-files-for-speech-recognition?resource=download
    audio_config = speechsdk.audio.AudioConfig(filename="SampleCodes/speech/audio.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and endpoint values?")


def recognize_from_mic():
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get('SPEECH_KEY'), 
        endpoint=os.environ.get('STT_SPEECH_ENDPOINT')
        # region = "eastus2"
    )
    
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    return speech_recognition_result


def recognize_from_file():
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get('SPEECH_KEY'), 
        endpoint=os.environ.get('SPEECH_ENDPOINT')
        # region = "eastus2"
    ) 
    audio_config = speechsdk.AudioConfig(filename= "SampleCodes/speech/audio.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    return speech_recognition_result


if __name__ == "__main__":
    speech_recognition_result = recognize_from_mic()
    # speech_recognition_result = recognize_from_file()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


