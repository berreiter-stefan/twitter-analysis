"""
Including utility classes and functions for
encapsulating functionality to make communicating
with the Twitter API easy.
"""
from typing import Dict, List, Any  # for type hinting
import time  # for pausing requests between tweets
import requests  # For sending GET requests from the API
from dotenv import dotenv_values  # to import environment variables
from config import MINISTER_TWITTER_INFO

env_vars = dotenv_values(".env")


class TwitterApiGetter:
    """Providing useful functions to communicate with the GET Api"""

    TWITTER_API_URL = "https://api.twitter.com"
    TWITTER_API_BEARER_TOKEN = env_vars.get("TWITTER_API_BEARER_TOKEN")
    CUSTOM_HEADERS = {"Authorization": f"Bearer {TWITTER_API_BEARER_TOKEN}"}
    MAX_TWEETS_PER_REQUEST = 100
    TIMESTAMP_STR_START_PANDEMIC = "2020-12-30T00:00:00Z"

    def __init__(self):
        pass

    @staticmethod
    def _account_info_params(
        twitter_handle: str, user_fields: List[str]
    ) -> Dict[str, str]:
        """builds together parameters for a GET api call to 'https://api.twitter.com/2/users/by'"""
        return {
            "usernames": f"{twitter_handle.lower()}",
            "user.fields": f"{','.join(user_fields)}",
        }

    def get_all_minister_twitter_bios(
        self,
        custom_user_fields: List[str],
    ) -> List[Dict[str, Any]]:
        """calls a GET api for all ministers in scope and returns a list of dictionaries"""
        user_bio_endpoint = f"{self.TWITTER_API_URL}/2/users/by"
        response_container = []

        for party, minister_handle in MINISTER_TWITTER_INFO.values():
            response = requests.request(
                "GET",
                user_bio_endpoint,
                headers=self.CUSTOM_HEADERS,
                params=self._account_info_params(
                    twitter_handle=minister_handle.lower(),
                    user_fields=custom_user_fields,
                ),
            )
            if response.status_code == 200:
                raw_response_data = response.json()["data"][0]
                public_metrics_data = raw_response_data.pop("public_metrics")
                raw_response_data.update(public_metrics_data)
                raw_response_data["party"] = party
                response_container.append(raw_response_data)
            time.sleep(0.2)
        print(
            f"INFO: {len(response_container)}/{len(MINISTER_TWITTER_INFO)} "
            f"Twitter accounts of ministers with Twitter handles fetched."
        )
        return response_container

    def fetch_user_tweets(
        self,
        user_id: int,
        user_name: str,
    ) -> List[Dict[str, Any]]:
        """
        fetches all possible tweets of a user iteratively and stores tweets in
        a list and returns it in the end.
        """
        params = {
            "start_time": self.TIMESTAMP_STR_START_PANDEMIC,
            "max_results": self.MAX_TWEETS_PER_REQUEST,
            # "exclude": "retweets",
            "expansions": "entities.mentions.username",
            "tweet.fields": "created_at,public_metrics",
        }
        iter_cnt = 0
        all_tweets_of_user: List[Dict[str, Any]] = []

        while True:
            iter_cnt += 1
            response = requests.request(
                "GET",
                f"{self.TWITTER_API_URL}/2/users/{user_id}/tweets",
                headers=self.CUSTOM_HEADERS,
                params=params,
            )
            if response.status_code != 200:
                print(
                    f"INFO [user {user_name} ❌]: Get request failed, not status code 200,"
                    f" but {response.status_code}."
                )
                print(response.json())
                break
            if "data" not in response.json():
                print(f"INFO [user {user_name} ❌]: No data in response.")
                break

            tweets = response.json()["data"]
            # add user_id and author to the information on tweets
            for tweet in tweets:
                tweet.update({"user_id": user_id, "author": user_name})
            # add the tweets to all found tweets from the user
            all_tweets_of_user.extend(tweets)
            print(f"INFO [user {user_name} ✅]: Fetched {len(tweets)} tweets.")

            if "next_token" not in response.json()["meta"]:
                print(
                    f"INFO [user {user_name} ✋]: No next_token in response to further fetch data."
                )
                break

            next_token = response.json()["meta"]["next_token"]
            params["pagination_token"] = next_token
            if iter_cnt > 20:
                print(
                    "INFO ❌❌❌❌: Stopped because of reaching over 20 iterations for one user."
                )
                break
            time.sleep(0.25)
        return all_tweets_of_user
