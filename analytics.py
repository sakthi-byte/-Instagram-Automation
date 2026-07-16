"""
Basic Analytics
Pulls account level and post level insights through the Graph API,
so you can track performance without checking each post manually.
"""

import requests
import os

ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN")
IG_USER_ID = os.environ.get("IG_USER_ID")
GRAPH_API_VERSION = "v19.0"


def get_account_insights(metrics="impressions,reach,profile_views", period="day"):
    """
    Pulls account level insights for the given metrics and period.
    """
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{IG_USER_ID}/insights"
    params = {
        "metric": metrics,
        "period": period,
        "access_token": ACCESS_TOKEN,
    }

    response = requests.get(url, params=params)
    return response.json()


def get_post_insights(media_id, metrics="engagement,impressions,reach,saved"):
    """
    Pulls insights for a specific post, referenced by its media ID.
    """
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{media_id}/insights"
    params = {
        "metric": metrics,
        "access_token": ACCESS_TOKEN,
    }

    response = requests.get(url, params=params)
    return response.json()


if __name__ == "__main__":
    account_data = get_account_insights()
    print("Account insights:")
    print(account_data)

    # Replace with a real media ID from your account to test post level insights
    # post_data = get_post_insights("your_media_id_here")
    # print(post_data)
