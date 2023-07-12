import tweepy
from mastodon import Mastodon
from bs4 import BeautifulSoup
import requests
import pickle
import os
from requests_oauthlib import OAuth1Session
import json


# Mastodon API setup
mastodon = Mastodon(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret = os.environ.get("CLIENT_SECRET"),
    access_token = os.environ.get("ACCESS_TOKEN"),
    api_base_url= 'https://mstdn.social'
)
user = mastodon.account_verify_credentials()
user_id = user['id']

# Search for already synced Toots
pickle_name = 'synced_toots.pkl'
try:
    with open(pickle_name, 'rb') as f:
        synced_toots = pickle.load(f)
    print(synced_toots)
except:
    synced_toots = []

# Get latest Toots
toots = mastodon.account_statuses(user_id, limit=1)
latest_toot_content = toots[0]['content']
latest_toot_id = toots[0]['id']

# Only continye if latest Toot has not been previously synced
if latest_toot_id not in synced_toots:
    synced_toots.append(latest_toot_id)
    with open(pickle_name, 'wb') as f:
        pickle.dump(synced_toots, f)

    # Remove HTML tags from toot
    soup = BeautifulSoup(latest_toot_content, 'html.parser')
    latest_toot_text = soup.get_text()


    # Twitter API setup
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")


    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print("There may have been an issue with the consumer_key you entered")

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)

    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Create payload
    payload = {
            "text": latest_toot_text
    }
    
    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

else:
    print('Toot already synced')

