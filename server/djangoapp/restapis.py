import requests
import json
from requests.auth import HTTPBasicAuth

from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        if "apikey" in kwargs:
            response = requests.get(url, headers={
                                    'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(
                url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    print(response.reason, response.text)
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload):
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                    json=json_payload)
    except Exception as e:
        # If any error occurs
        print(f"Network exception occurred: {e}")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    print(response.text)
    return status_code

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url=url,dealerId=dealerId)
    #print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["docs"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a CarDealer object with values in `doc` object
            dealer_obj = DealerReview(dealership=review_doc.get("dealership"), 
                                      name=review_doc.get("name"), purchase=review_doc.get("purchase"),
                                   review=review_doc.get("review"), purchase_date=review_doc.get("purchase_date"), 
                                   car_make=review_doc.get("car_make"),
                                   car_model=review_doc.get("car_model"),
                                   car_year=review_doc.get("car_year"), 
                                   sentiment=analyze_review_sentiments(review["review"]), 
                                   id=review_doc["_id"])
            results.append(dealer_obj)
    return results


def get_dealer_from_cf_by_id(url, dealer_id):
    json_result = get_request(url, id=dealer_id)
    if json_result:
        dealer = json_result["rows"][0]
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], zip=dealer["zip"])
    return dealer_obj

def analyze_review_sentiments(dealer_review):
    API_KEY = "zqiu0jFN7DBObry0txR0CSVfK3o1phqYKXpnmDg9Ur5p"
    NLU_URL = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/50320dab-e7f8-4eb4-9171-694a68986ca5'
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)
    try:
        response = natural_language_understanding.analyze(text=dealer_review, features=Features(
            sentiment=SentimentOptions(targets=[dealer_review]))).get_result()
        print(response)

        label = json.dumps(response, indent=2)
        label = response['sentiment']['document']['label']
        return(label)
    except Exception as e:
        print(e)
        return "undertermined"
