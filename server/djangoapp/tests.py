from django.test import TestCase

import requests

def get_reviews_by_dealer_id(dealer_id, iam_api_key="", couch_url=""):
    url = 'https://us-east.functions.appdomain.cloud/api/v1/web/9103f29e-2898-4270-84f4-08bd82ed47c0/dealership_package/get-review'
    url3="https://us-east.functions.appdomain.cloud/api/v1/web/9103f29e-2898-4270-84f4-08bd82ed47c0/default/testblocking=false&namespace_id=9103f29e-2898-4270-84f4-08bd82ed47c0&usernamespace=9103f29e-2898-4270-84f4-08bd82ed47c0"
    headers2 = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + iam_api_key
    }

    headers = {
        'Content-Type': 'application/json'
    }
    
    params = {
        'dealerId': str(dealer_id)
    }
    
    try:
        response = requests.post(f"{url}.json", params=params,headers=headers)
        print(response.url, response.text)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': response.status_code if 'response' in locals() else 500,
            'message': str(e)
        }

if __name__ == '__main__':
    
    dealer_id = 1
    
    result = get_reviews_by_dealer_id(dealer_id)
    
    print(result)
    print(result.text)
    print(result.reason)

