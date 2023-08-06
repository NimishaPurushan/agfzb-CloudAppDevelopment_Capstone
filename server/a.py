import json
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def analyze_review_sentiments(dealer_review):
    API_KEY = "zqiu0jFN7DBObry0txR0CSVfK3o1phqYKXpnmDg9Ur5p"
    NLU_URL = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/50320dab-e7f8-4eb4-9171-694a68986ca5'
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)

    # Split the dealer_review into sentences using a library like NLTK or SpaCy
    # For example, using NLTK:

    sentences = sent_tokenize(dealer_review)

    sentiments = []
    for sentence in sentences:
        try:
            response = natural_language_understanding.analyze(
                text=sentence,
                features=Features(sentiment=SentimentOptions(targets=[sentence]))
            ).get_result()
            label = response['sentiment']['document']['label']
            sentiments.append(label)
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            sentiments.append("undetermined")

    return sentiments

# Example usage:
dealer_review = "Very bad."
sentiments = analyze_review_sentiments(dealer_review)
print(sentiments)
