"""
Scheduled Posting
A minimal example showing how to publish a post to Instagram through
the official Graph API, using a media container and a publish step.
"""

import requests
import os
import time

ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN")
IG_USER_ID = os.environ.get("IG_USER_ID")
GRAPH_API_VERSION = "v19.0"


def create_media_container(image_url, caption):
    """
    Step one, upload the media and caption as a container.
    Instagram needs a publicly accessible image URL here, not a local file.
    """
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{IG_USER_ID}/media"
    params = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN,
    }

    response = requests.post(url, params=params)
    data = response.json()

    if "id" not in data:
        raise Exception(f"Failed to create media container: {data}")

    return data["id"]


def publish_container(container_id):
    """
    Step two, publish the container that was just created.
    """
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{IG_USER_ID}/media_publish"
    params = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN,
    }

    response = requests.post(url, params=params)
    return response.json()


def post_now(image_url, caption):
    """
    Runs both steps together. For genuine scheduling, wrap this in your
    own cron job or task scheduler and call it at the time you want the
    post to go live.
    """
    container_id = create_media_container(image_url, caption)

    # A short pause helps avoid publishing before the container finishes processing
    time.sleep(5)

    result = publish_container(container_id)
    print(f"Publish result: {result}")


if __name__ == "__main__":
    post_now(
        image_url="https://example.com/your-image.jpg",
        caption="Posted automatically through the Graph API.",
    )
