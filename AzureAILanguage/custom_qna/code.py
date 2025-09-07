from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering import models as qna
import os
from dotenv import load_dotenv
load_dotenv()


endpoint = os.environ["LANGUAGE_ENDPOINT"]
credential = AzureKeyCredential("" + os.environ["LANGUAGE_KEY"])


def main():
    client = QuestionAnsweringClient(endpoint, credential)
    with client:
        question="How long does it takes to charge a surface?"
        input = qna.AnswersFromTextOptions(
            question=question,
            text_documents=[
                "Power and charging. It takes two to four hours to charge the Surface Pro 4 battery fully from an empty state. " +
                "It can take longer if you're using your Surface for power-intensive activities like gaming or video streaming while you're charging it.",
                "You can use the USB port on your Surface Pro 4 power supply to charge other devices, like a phone, while your Surface charges. " +
                "The USB port on the power supply is only for charging, not for data transfer. If you want to use a USB device, plug it into the USB port on your Surface.",
            ]
        )


        output = client.get_answers_from_text(input)

    best_answer = [a for a in output.answers if a.confidence > 0.9][0]
    print(u"Q: {}".format(input.question))
    print(u"A: {}".format(best_answer.answer))
    print("Confidence Score: {}".format(output.answers[0].confidence))

# def main():
#     client = QuestionAnsweringClient(endpoint, credential)
#     with client:
#         question="How much battery life do I have left?"
#         output = client.get_answers(
#             question = question,
#             project_name=knowledge_base_project,
#             deployment_name=deployment
#         )
#     print("Q: {}".format(question))
#     print("A: {}".format(output.answers[0].answer))

if __name__ == '__main__':
    main()