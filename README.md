# Mastweet
---
This script cross-posts Mastodon toots to Twitter. The code was adapted from https://github.com/twitterdev/FactualCat-Twitter-Bot

It runs as a cron GitHub Action every 10 min to post your latest Toot to Twitter. This action was adapted from https://github.com/klausi/mastodon-twitter-sync/

To use it, you need a Twitter Developer account (I am using the Free plan).
1. Create a new Github environment with the name "Cron" at `https://github.com/<USERNAME>/mastweet/settings/environments/new`
2. For this to work with your accounts, add the corresponding values to the `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`,`TWITTER_ACCESS_TOKEN`,`TWITTER_ACCESS_TOKEN_SECRET`,`MASTODON_CLIENT_ID`, `MASTODON_CLIENT_SECRET`, `MASTODON_ACCESS_TOKEN` and `MASTODON_INSTANCE_URL` (e.g. https://mstdn.social) secrets to the Cron environment.



