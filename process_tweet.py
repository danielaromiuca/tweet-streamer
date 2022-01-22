"Streams Tweets"
import json
import re

import emoji

stop = list()
f = open("/home/ec2-user/tweet-streamer/stopwords-es.txt", encoding="utf8")
for x in f:
    a = (
        x.replace("\n", "")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )
    stop.append(a)


def procesa_tuit(text):
    text = [x.lower() for x in text.split(" ") if "@" not in x]
    text = [x for x in text if x not in stop]
    text = [x for x in text if "http" not in x]
    text = [x for x in text if "rt" not in x]
    text = " ".join(text)
    text = re.sub(r"[^\w\s]", " ", text).lower()
    text = re.sub("[0-9]", " ", text)
    text = text.replace("á", "a")
    text = text.replace("é", "e")
    text = text.replace("í", "i")
    text = text.replace("ó", "o")
    text = text.replace("ú", "u")
    text = text.replace("'", "")
    text = text.replace("\n", " ")
    text = "".join([x for x in text if x not in emoji.UNICODE_EMOJI])
    return text


def procesa_texto(text):

    text = [x.lower() for x in text.split(" ") if "@" not in x]
    text = [x for x in text if "http" not in x]
    text = [x for x in text if "rt" not in x]
    text = " ".join(text)
    ###text=re.sub(r'[^\w\s]','',text).lower()
    text = text.replace("á", "a")
    text = text.replace("é", "e")
    text = text.replace("í", "i")
    text = text.replace("ó", "o")
    text = text.replace("ú", "u")
    text = text.replace("'", "")
    text = text.replace("\n", " ")
    text = "".join([x for x in text if x not in emoji.UNICODE_EMOJI])
    return text


def user_men(tuit):
    remove = [",", ";", ".", ":"]
    users = "".join([x for x in tuit if x not in remove])
    users = " ".join([x for x in users.split(" ") if "@" in x])
    return users


def web_men(tuit):
    webs = " ".join([x for x in tuit.split(" ") if "http" in x])
    return webs


def hash(x):
    hash = " "
    cont = 0
    for i in x:
        if cont == 0:
            hash = i["text"]
        else:
            hash = hash + ";" + i["text"]
        cont += 1
    return hash
