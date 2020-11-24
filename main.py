import json
import requests
import operator
from requests_oauthlib import OAuth1
import re


# to use: put a bunch of twitter URL's that have videos in "input.txt"
# replace twitter_dist.json with your personal api keys and then rename to twitter.json
# run command python3 main.py from the bash terminal (or windows cmd if you're a monster)

def generateToken():
    credfile = open("config/twitter.json", "rt+")
    creds = json.load(credfile)
    credfile.close()
    oauth = OAuth1(
        creds["twitter"]["api_key"],
        client_secret=creds["twitter"]["api_secret"],
        resource_owner_key=creds["twitter"]["access_token"],
        resource_owner_secret=creds["twitter"]["access_secret"]
    )
    return oauth


def getTweetIds(urlarray):
    remove_pattern = r"https:\/\/twitter\.com\/.+\/status\/"
    ids = []
    for i in urlarray:
        a = re.sub(remove_pattern, '', i).strip("\n")
        ids.append(a)
    ids_str = ",".join(ids)
    print(ids_str)
    # the twitter bulk api uses a parameter that wants basically a csv of tweet id's so let's format it that way
    return ids_str


def getTweetURLs(filename):
    f = open(filename, "rt+")
    tweetlist = []
    for i in f:
        tweetlist.append(i.strip("\n"))
    f.close()
    # print(tweetlist)
    return tweetlist


def getTweetData(ids_str, oauth):
    # twitter has a batch endpoint for getting data from multiple tweets in one go, so let's use that.
    geturl = "https://api.twitter.com/1.1/statuses/lookup.json?include_entities=true&tweet_mode=extended&id=" + ids_str
    req = requests.get(url=geturl, auth=oauth)
    if req.status_code != 200:
        print("Something has gone wrong getting the tweets. Dumping the output to the console.")
        print(" ")
        print(str(req.status_code))
        print(req.text)
    d = req.json()
    return d


def main(debugflag):
    oauth = generateToken()
    turls = getTweetURLs("input.txt")
    ids = getTweetIds(turls)
    datajson = getTweetData(ids, oauth)
    video_urls = []
    for o in datajson:
        v = o["extended_entities"]["media"][0]["video_info"]["variants"]
        vid_filename = o["id_str"]
        v2 = []
        for i in v:  # sometimes twitter throws m3u8's in there which we do not want.
            if "bitrate" in i:  # aforementioned m3u8 entries won't have a bitrate field.
                v2.append(i)
            else:
                pass
        v3 = sorted(v2, key=operator.itemgetter("bitrate"), reverse=True)
        # sorted by bitrate descending, the highest bitrate is presumably what we want to grab (i dont know why you
        # would want to grab the worst bitrate version but you can do reverse=false if you want to do that)
        url = v3[0]["url"]
        video_urls.append({"url": url, "filename": vid_filename + ".mp4"})
        # now that we have the tweet video url and the tweet id let's append them as a single object so
        # that we can do a bunch of gets & write them out as binary files
    for v4 in video_urls:
        r = requests.get(v4["url"])
        if not debugflag:
            f = open(v4["filename"], "wb+")
            f.write(r.content)
            f.close()
        print("wrote file " + v4["filename"])


if __name__ == "__main__":
    main(debugflag=False)  # set to True if you dont want to download any files
