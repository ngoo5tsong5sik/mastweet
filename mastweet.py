import tweepy
from mastodon import Mastodon
from bs4 import BeautifulSoup
import requests
import pickle
import os

# Mastodon API setup
mastodon = Mastodon(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret = os.environ.get("CLIENT_SECRET"),
    access_token = os.environ.get("ACCESS_TOKEN"),
    api_base_url= 'https://mstdn.social'
)
user = mastodon.account_verify_credentials()
user_id = user['id']

pickle_name = 'synced_toots.pkl'
# synced
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
if latest_toot_id not in synced_toots:
    synced_toots.append(latest_toot_id)
    with open(pickle_name, 'wb') as f:
        pickle.dump(synced_toots, f)

    # Remove HTML tags from toot
    soup = BeautifulSoup(latest_toot_content, 'html.parser')
    latest_toot_text = soup.get_text()

    # Create payload
    payload = {
            "text": latest_toot_text
    }
    # Get new token

    get_token = requests.request(
        "POST",
        "https://api.twitter.com/2/oauth2/token",
        headers={
            'Content-Type':'application/x-www-form-urlencoded'
        },
        data={
            'refresh_token':os.environ.get('TWITTER_REFRESH_TOKEN'),
            'grant_type':'refresh_token',
            'client_id':os.environ.get('TWITTER_CLIENT_ID')
        }
    )

    # Post tweet
    response = requests.request(
        "POST",
        "https://api.twitter.com/2/tweets",
        json=payload,
        headers={
            "Authorization": "Bearer {}".format(get_token),
            "Content-Type": "application/json",
        },
    )

    # Check response
    if response.status_code != 201:
        raise Exception(f"Request returned error: {response.status_code}, {response.text}")
    else:
        print("Successfully tweeted!")
else:
    print('Toot already synced')

