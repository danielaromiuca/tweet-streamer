###Process Tweet stream
import json
import logging
import time
from secrets import (
    API_ACCESS_TOKEN,
    API_ACCESS_TOKEN_SECRET,
    API_CONSUMER_KEY,
    API_CONSUMER_SECRET,
)

import pandas as pd
from tweepy import Stream

from parameters import countries, tags


def upload_s3(df, fn):

    bucket = "twitter-project-daromi"
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource("s3")
    s3_resource.Object(bucket, "data/streamed/" + fn).put(Body=csv_buffer.getvalue())


class Listener(Stream):
    def on_data(self, data):

        fields = [""] * 16

        json_map = json.loads(data)

        try:
            fields[0] = str(json_map["created_at"])
        except:
            pass
        try:
            fields[1] = str(json_map["in_reply_to_status_id"])
        except:
            pass
        try:
            fields[2] = str(json_map["id_str"])
        except:
            pass
        try:
            fields[3] = str(hash(json_map["entities"]["hashtags"]))
        except:
            pass
        try:
            fields[4] = str(
                procesa_texto(json_map["entities"]["user_mentions"][0]["name"])
            )
        except:
            pass
        try:
            fields[5] = str(json_map["entities"]["user_mentions"][0]["id"])
        except:
            pass
        try:
            fields[6] = str(json_map["retweet_count"])
        except:
            pass
        try:
            fields[7] = str(json_map["user"]["followers_count"])
        except:
            pass
        try:
            fields[8] = str(json_map["user"]["friends_count"])
        except:
            pass
        try:
            fields[9] = str(json_map["user"]["id"])
        except:
            pass
        try:
            fields[10] = procesa_texto(json_map["user"]["location"])
        except:
            pass
        try:
            fields[11] = procesa_tuit(json_map["extended_tweet"]["full_text"])
            fields[12] = user_men(json_map["extended_tweet"]["full_text"])
            if "rt" in json_map["extended_tweet"]["full_text"].lower():
                fields[15] = "RT"
            fields[13] = web_men(json_map["extended_tweet"]["full_text"])
            fields[14] = None
        except:
            fields[11] = procesa_tuit(json_map["text"])
            fields[12] = user_men(json_map["text"])
            if "rt" in json_map["text"].lower():
                fields[15] = "RT"
            fields[13] = web_men(json_map["text"])
            fields[14] = None

        tuits.append(fields)
        if len(tuits) == 1000:
            tuits = pd.DataFrame(tuits)
            fn = "/home/ec2-user/tweet-streamer/tweets" + str(time.time()) + ".csv"
            upload_s3(tuits, fn)
            logger.info(f"Tweets Guardados. Nombre del archivo: {fn}")
            tuits = []

    def on_error(self, status):
        logger.error(f"Error en la aplicación: {status}")


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="/home/ec2-user/logs/streamer-process.log",
    )
    logger = logging.getLogger("streamer-process.log")

    logger.info(f"Lanzando aplicación streaming")

    tuits = []

    twitter_stream = Listener(
        API_CONSUMER_KEY, API_CONSUMER_SECRET, API_ACCESS_TOKEN, API_ACCESS_TOKEN_SECRET
    )
    twitter_stream.filter(track=tags)
