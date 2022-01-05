"""
Including utility classes and functions for
encapsulating functionality to make communicating
with the Twitter API easy.
"""
from typing import Dict, Tuple, List, Any  # for type hinting
import time  # for pausing requests between tweets
import requests  # For sending GET requests from the API
from dotenv import dotenv_values  # to import environment variables

# Import env variables into static vars
env_vars = dotenv_values(".env")
TWITTER_API_BEARER_TOKEN = env_vars.get("TWITTER_API_BEARER_TOKEN")


def account_info_params(twitter_handle: str, user_fields: List[str]) -> Dict[str, str]:
    """builds together parameters for a GET api call to 'https://api.twitter.com/2/users/by'"""
    return {
        "usernames": f"{twitter_handle.lower()}",
        "user.fields": f"{','.join(user_fields)}",
    }


def get_all_minister_twitter_bios(
    minister_twitter_info: Dict[str, Tuple[str, str]], custom_user_fields: List[str]
) -> List[Dict[str, Any]]:
    """calls a GET api for all ministers in scope and returns a list of dictionaries"""
    custom_headers = {"Authorization": f"Bearer {TWITTER_API_BEARER_TOKEN}"}
    user_bio_url = "https://api.twitter.com/2/users/by"
    response_container = []
    for party, minister_handle in minister_twitter_info.values():
        response = requests.request(
            "GET",
            user_bio_url,
            headers=custom_headers,
            params=account_info_params(
                twitter_handle=minister_handle.lower(), user_fields=custom_user_fields
            ),
        )
        if response.status_code == 200:
            raw_response_data = response.json()["data"][0]
            public_metrics_data = raw_response_data.pop("public_metrics")
            raw_response_data.update(public_metrics_data)
            raw_response_data["party"] = party
            response_container.append(raw_response_data)
        time.sleep(0.2)
    return response_container
