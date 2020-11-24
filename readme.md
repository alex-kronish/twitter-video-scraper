# Twitter Video Scraper

The name says it all. Here's how to use it!

1. Generate your own api keys on dev.twitter.com (you only need read for this program)
2. Plug them into twitter_dist.json and rename the file to twitter.json
3. Plug in a series of video tweets into input.txt, one URL for each line. (input.txt int his repo contains 4 example tweets)
4. Run `python3 main.py` from the command line
5. Now you have a bunch of videos! It's just that easy!

This is based on the 1.1 version of the twitter api. This also presumes that unauthenticated gets on the mp4's is a feature and not a bug.
This may break if 1.1 ever falls out of support and I might not have the free time to update it when that happens.