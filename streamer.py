###Process Tweet stream
import json
import logging
from datetime import datetime
from secrets import (
    API_ACCESS_TOKEN,
    API_ACCESS_TOKEN_SECRET,
    API_CONSUMER_KEY,
    API_CONSUMER_SECRET,
)

import boto3
from tweepy import Stream

from parameters import countries, tags


def upload_s3(json_tuits):
    now = datetime.now()

    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H%M")

    fn = f"{year}/{month}/{day}/{time}.json"

    bucket = "twitter-project-daromi"
    s3_resource = boto3.resource("s3")
    s3_resource.Object(bucket, "data/p.expectativas/streamed/" + fn).put(Body=bytes(json_tuits).decode("utf-8"))
    logger.info(f"Tweets Guardados. Nombre del archivo: {fn}")

class Listener(Stream):
    def on_data(self, data):
        global tuits

        json_map = json.loads(data)

        tuits.append(json_map)

    
        if len(tuits) == 100:
            json_tuits = json.dumps(tuits)
            upload_s3(json_tuits)
            tuits = []

    def on_error(self, status):
        raise Exception(f"Hubo un error en la aplicación {status}")


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="/home/ec2-user/logs/streamer-process.log",
    )
    logger = logging.getLogger("streamer-process.log")

    logger.info(f"Lanzando aplicación streaming. Traking términos: {tags} y países: {countries}")


    tuits = []

    twitter_stream = Listener(
        API_CONSUMER_KEY, API_CONSUMER_SECRET, API_ACCESS_TOKEN, API_ACCESS_TOKEN_SECRET
    )
    twitter_stream.filter(track=tags)
