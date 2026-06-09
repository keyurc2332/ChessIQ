# backend/fetch_games.py

import requests
import json

def test_chess_com_api():
    """Test if username works"""
    username = "keyur_2332"
    
    # Test 1: Check if user exists
    user_url = f"https://api.chess.com/pub/player/{username}"
    print(f"Testing: {user_url}")
    
    try:
        response = requests.get(user_url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_chess_com_api()