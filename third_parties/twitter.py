import os
from dotenv import load_dotenv
import tweepy
import requests

load_dotenv()


twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_KEY_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
)


def get_user_details(username, mock: bool = True):
    """
    Fetch user details from Twitter and returns them as dictionary.
    """
    if mock:
        APEKSHA_TWITTER_GIST = "https://gist.githubusercontent.com/apeksha117/f6e1e4c426c63268359808640fad91ee/raw/ac5ec6022d339c6c0938ab3fe987686aac40d0c1/twitter-apeksha-mock-data"
        user_data = requests.get(APEKSHA_TWITTER_GIST, timeout=5).json()

    else:

        user_response = twitter_client.get_user(
            username=username,
            user_fields=[
                "id",
                "name",
                "username",
                "created_at",
                "description",
                "location",
                "profile_image_url",
                "protected",
                "verified",
                "followers_count",
                "following_count",
                "tweet_count",
            ],
        )
        user_data = user_response.data

    user_details = {
        "id": user_data["id"],
        "name": user_data["name"],
        "username": user_data["username"],
        "created_at": user_data["created_at"],
        "description": user_data["description"],
        "location": user_data["location"],
        "profile_image_url": user_data["profile_image_url"],
        "protected": user_data["protected"],
        "verified": user_data["verified"],
        "followers_count": user_data["public_metrics"]["followers_count"],
        "following_count": user_data["public_metrics"]["following_count"],
        "tweet_count": user_data["public_metrics"]["tweet_count"],
    }

    return user_details


if __name__ == "__main__":

    user_details = get_user_details(username="ApekshaAgrawal12")
    print(user_details)
