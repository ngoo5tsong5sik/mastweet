# Mastweet
---
This script syncronizes Mastodon toots to Twitter.
It runs as a cron GitHub Action every 10 min to sync your latest Toot to Twitter. This  was adapted from https://github.com/klausi/mastodon-twitter-sync/

To use it, you need a Twitter Developer account (I am using the Free plan).
1. Create a new Github environment with the name "Cron" at `https://github.com/<USERNAME>/mastweet/settings/environments/new`
2. For access to Mastodon add the `CLIENT_ID`, `CLIENT_SECRET`, `ACCESS_TOKEN` secrets to the Cron environment.
3. For access to Twitter add the `BEARER_TOKEN` secret to the Cron environment.
4. Change the `api_base_url= 'https://mstdn.social'` variable to the URL of your Mastodon instance.

