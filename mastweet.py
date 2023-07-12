from mastodon import Mastodon
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1
import requests
import pickle
import os

# Mastodon API setup
mastodon = Mastodon(
    client_id=os.environ.get("MASTODON_CLIENT_ID"),
    client_secret = os.environ.get("MASTODON_CLIENT_SECRET"),
    access_token = os.environ.get("MASTODON_ACCESS_TOKEN"),
    api_base_url= os.environ.get("MASTODON_INSTANCE_URL"),
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

    # Twitter API setup
    consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    def connect_to_oauth(consumer_key, consumer_secret, acccess_token, access_token_secret):
        url = "https://api.twitter.com/2/tweets"
        auth = OAuth1(consumer_key, consumer_secret, acccess_token, access_token_secret)
        return url, auth


    def main():
        payload = { "text": latest_toot_text }

        url, auth = connect_to_oauth(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        print(url, auth)
        request = requests.post(
            auth=auth, url=url, json=payload, headers={"Content-Type": "application/json"}
        )

        # Check response
        if request.status_code != 201:
            raise Exception(f"Request returned error: {request.status_code}, {request.text}")
        else:
            print("Successfully tweeted!")

    main()


else:
    print('Toot already synced')

