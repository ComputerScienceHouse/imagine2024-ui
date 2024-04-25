###############################################################################
#
# File: database.py
#
# Author: Isaac Ingram
#
# Purpose: Provide a connection to the database
#
###############################################################################
import os
import requests

from models import User, Item
from typing import List

API_ENDPOINT = os.getenv("BNB_API_ENDPOINT", '')
AUTHORIZATION_KEY = os.getenv("BNB_AUTHORIZATION_KEY", '')

MOCK_ITEMS = {

    1: Item(1, "Mock Item 1", "123456789012", 9.99, 100, 0.5, 0.1, "images/oof.png", "rectangle"),
    2: Item(2, "Mock Item 2", "234567890123", 19.99, 50, 1.0, 0.2, "images/oof.png", "cylinder"),
    3: Item(3, "Mock Item 3", "345678901234", 29.99, 75, 0.8, 0.15, "images/oof.png", "bottle"),
    4: Item(4, "Mock Item 4", "456789012345", 14.99, 120, 0.6, 0.12, "images/oof.png", "pouch"),
    5: Item(5, "Mock Item 5", "567890123456", 24.99, 90, 1.2, 0.25, "images/oof.png", "cylinder"),
    6: Item(6, "Mock Item 6", "678901234567", 34.99, 60, 0.9, 0.18, "images/oof.png", "rectangle"),
    7: Item(7, "Mock Item 7", "789012345678", 19.99, 100, 0.7, 0.14, "images/oof.png", "pouch"),
    8: Item(8, "Mock Item 8", "890123456789", 39.99, 40, 1.5, 0.3, "images/oof.png", "rectangle"),
    9: Item(9, "Mock Item 9", "901234567890", 49.99, 30, 1.1, 0.22, "images/oof.png", "cylinder"),
    10: Item(10, "Mock Item 10", "012345678901", 29.99, 80, 0.9, 0.18, "images/oof.png", "bottle"),
}

MOCK_USERS = {
    1: User(1, "John Doe", "", 20.00, "credit", "john.doe@example.com", "+1234567890"),
    2: User(2, "Jane Smith", "", 13.75, "dining", "jane.smith@example.com", "+1987654321"),
    3: User(3, "Alice Johnson", "", 18.33, "imagine", "alice.johnson@example.com", "+1122334455"),
    4: User(4, "Michael Brown", "", 12.75, "credit", "michael.brown@example.com", "+1555123456"),
    5: User(5, "Emily Wilson", "", 15.50, "dining", "emily.wilson@example.com", "+16667778888"),
    6: User(6, "David Clark", "", 18.95, "imagine", "david.clark@example.com", "+17778889999"),
    7: User(7, "Sarah Martinez", "", 11.99, "credit", "sarah.martinez@example.com", "+18889990000"),
    8: User(8, "James Taylor", "", 17.25, "dining", "james.taylor@example.com", "+19990001111"),
    9: User(9, "Emma Harris", "", 19.75, "imagine", "emma.harris@example.com", "+12344321543"),
    10: User(10, "Daniel Anderson", "", 14.30, "credit", "daniel.anderson@example.com", "+15551239876"),
}

# Use mock data if USE_MOCK_DATA environment variable is set to 'true'. If it
# isn't set to 'true' (including not being set at all), it this defaults to
# False.
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", 'false').lower() == 'true'

REQUEST_HEADERS = {"Authorization": AUTHORIZATION_KEY}


def is_reachable() -> bool:
    """
    Check if the database is reachable
    :return: True if the database is reachable, False otherwise
    """
    print("Check If Reachable (GET)")
    try:
        requests.get(API_ENDPOINT, headers=REQUEST_HEADERS)
        return True
    except requests.RequestException:
        print(f"\tExperienced Request Exception")
        return False


def get_items() -> List[Item]:
    """
    Get all items
    :return: A List of Item. If there is an error, an empty list is returned
    """
    print("GET /items")
    if USE_MOCK_DATA:
        return list(MOCK_ITEMS.values())
    else:
        url = API_ENDPOINT + "/items"
        # Make request
        response = requests.get(url, headers={"Authorization": AUTHORIZATION_KEY})
        # Check response code
        if response.status_code == 200:
            # Create list of items
            result = list()
            for item_raw in response.json():
                result.append(Item(
                    item_raw['id'],
                    item_raw['name'],
                    item_raw['upc'],
                    item_raw['price'],
                    item_raw['quantity'],
                    item_raw['weight_avg'],
                    item_raw['weight_std'],
                    item_raw['thumb_img'],
                    item_raw['vision_class']
                ))
            return result
        else:
            # Something went wrong so print info and return empty list
            print(f"\tReceived response {response.status_code}:")
            print(f"\t{response.content}")
            return list()


def get_item(item_id: int) -> Item | None:
    """
    Get an item from its ID
    :return: An Item or None if the item does not exist
    """
    print(f"GET /items/{item_id}")
    if USE_MOCK_DATA:
        if item_id in MOCK_ITEMS:
            return MOCK_ITEMS[item_id]
        else:
            return None
    else:
        url = API_ENDPOINT + f"/items/{item_id}"
        # Make request
        response = requests.get(url, headers=REQUEST_HEADERS)
        # Check response code
        if response.status_code == 200:
            item = response.json()
            return Item(
                item['id'],
                item['name'],
                item['upc'],
                item['price'],
                item['units'],
                item['avg_weight'],
                item['std_weight'],
                item['thumbnail'],
                item['vision_class']
            )
        else:
            # Something went wrong so print info and return None
            print(f"\tReceived response {response.status_code}:")
            print(f"\t{response.content}")
            return None


def get_user(user_id=None, user_token=None) -> User | None:
    """
    Get user from either the user id or token
    :param user_id: Optional User ID
    :param user_token: Optional User Token
    :return: A User or None if the User does not exist or no identifier (ID or
    token) was provided
    """
    if USE_MOCK_DATA:
        # Check if user token should be used
        if user_token is not None:
            # Get user from token
            print(f"GET /users/{user_token}")
            for user in MOCK_USERS.values():
                if user.token == user_token:
                    return user
            return None
        # Check if user id should be used
        elif user_id is not None:
            # Get user from ID
            print(f"GET /users/{user_id}")
            if user_id in MOCK_USERS:
                return MOCK_USERS[user_id]
            else:
                return None
        # Can't use token or ID so return None
        else:
            return None
    else:
        # Determine whether URL should query based on token or user ID
        url = ""
        if user_token is not None:
            # Query based on token
            print(f"GET /token/{user_token}")
            url = API_ENDPOINT + f"/token/{user_token}"
        elif user_id is not None:
            # Query based on user id
            print(f"GET /users/{user_id}")
            url = API_ENDPOINT + f"/users/{user_id}"
        else:
            # Neither so return None
            return None

        # Make query determined above
        response = requests.get(url, headers=REQUEST_HEADERS)
        # Check response code
        if response.status_code == 200:
            user = response.json()
            return User(
                user['id'],
                user['name'],
                user['token'],
                user['balance'],
                user['payment_type'],
                user['email'],
                user['phone']
            )
        else:
            # Something went wrong so print info and return None
            print(f"\tReceived response {response.status_code}")
            print(f"\t{response.content}")
            return None


def update_user(user: User) -> User | None:
    """
    Update a User
    :param user: Updated User
    :return: The new User if the update was successful, otherwise None
    """
    print(f"PUT /users/{user.uid}")
    if USE_MOCK_DATA:
        if user.uid in MOCK_USERS:
            MOCK_USERS[user.uid] = user
            return user
        else:
            return None
    else:
        url = API_ENDPOINT + f"/users/{user.uid}"
        params = {
            'id': user.uid,
            'name': user.name,
            'token': user.token,
            'balance': user.balance,
            'payment_type': user.payment_type,
            'email': user.email,
            'phone': user.phone
        }
        response = requests.put(url, params=params, headers=REQUEST_HEADERS)
        if response == 200:
            return user
        else:
            print(f"\tReceived response {response.status_code}")
            print(f"\t{response.content}")
            return None
