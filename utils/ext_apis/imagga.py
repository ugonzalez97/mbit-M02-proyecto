import requests
from .. import credentials

def get_image_tags(image_url, min_confidence):
    credential = credentials.get_credentials('imagga')
    auth = (credential['key'], credential['secret'])
    url = f"https://api.imagga.com/v2/tags?image_url={image_url}"
    response = requests.get(url, auth=auth)

    return [
        {
            "tag": t["tag"]["en"],
            "confidence": t["confidence"]
        }
        for t in response.json()["result"]["tags"]
        if t["confidence"] > min_confidence
    ]
