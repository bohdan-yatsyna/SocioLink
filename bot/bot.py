import json
import os
import random
import requests
import logging

from faker import Faker
from typing import Dict, Any


BOT_DIRECTORY = "bot"
CONFIG_PATH = os.path.join(BOT_DIRECTORY, "config.json")


def load_configurations(path: str) -> Dict[str, Any]:
    with open(path, "r") as file:
        return json.load(file)


CONFIGURATIONS = load_configurations(CONFIG_PATH)
BASE_URL = CONFIGURATIONS.get("base_url", "http://app:8000/api")

fake = Faker()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: bot_message '%(message)s'"
)
logger = logging.getLogger("BotLogger")


def get_headers(token: str = None) -> Dict[str, str]:
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def handle_request(response: requests.Response) -> Dict[str, Any]:
    """Raise HTTPError in case of 4xx and 5xx responses"""

    response.raise_for_status()
    return response.json()


def get_url(endpoint: str, additional_id: int = None) -> str:
    url = f"{BASE_URL}/{endpoint}/"

    if additional_id:
        url += f"{additional_id}/"

    return url


def signup_user() -> Dict[str, str]:
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "pseudonym": fake.user_name(),
    }

    logger.info(f"Signing up user: {user_data['email']}")
    response = requests.post(get_url("users/signup"), data=user_data)
    handle_request(response)
    logger.info(f"User signed up successfully: {user_data['email']}")

    return user_data


def login_user(email: str, password: str) -> str:
    login_data = {
        "email": email,
        "password": password
    }

    logger.info(f"Logging in user: {email}")
    response = requests.post(get_url("users/login"), data=login_data)
    login_response = handle_request(response)
    logger.info(f"User logged in successfully: {email}")

    return login_response["access"]


def create_post(token: str) -> Dict[str, Any]:
    headers = get_headers(token)
    post_data = {
        "title": fake.sentence(),
        "text": fake.text()
    }

    logger.info(f"Creating post: {post_data['title']}")
    response = requests.post(get_url("posts"), data=post_data, headers=headers)
    post_response = handle_request(response)
    logger.info(f"Post created successfully: {post_data['title']}")

    return post_response


def like_post(token: str, post_id: int) -> None:
    headers = get_headers(token)

    logger.info(f"Liking post ID: {post_id}")
    response = requests.post(
        get_url("posts", post_id) + "like/",
        headers=headers,
    )
    handle_request(response)
    logger.info(f"Post ID {post_id} liked successfully")


def simulate_user_activity() -> None:
    users_counter = 0

    for _ in range(CONFIGURATIONS["number_of_users"]):
        logger.info("Starting process for a new user")
        user_data = signup_user()
        access_token = login_user(user_data["email"], user_data["password"])

        for _ in range(
                random.randint(1, CONFIGURATIONS["max_posts_per_user"])
        ):
            create_post(access_token)

        logger.info("Fetching all post IDs for like...")
        response = requests.get(get_url("posts"))
        post_response = handle_request(response)
        post_ids = [post["id"] for post in post_response["results"]]

        for _ in range(
                random.randint(1, CONFIGURATIONS["max_likes_per_user"])
        ):
            post_id = random.choice(post_ids)
            like_post(access_token, post_id)
            post_ids.remove(post_id)

        users_counter += 1
        logger.info(f"___Process completed for user №:{users_counter} ___\n")

    logger.info("___Process is finished successfully___")


if __name__ == "__main__":
    simulate_user_activity()
