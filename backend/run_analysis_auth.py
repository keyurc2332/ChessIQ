import requests
import json

API_URL = 'http://127.0.0.1:8000'

print('ChessIQ Batch Analysis with Authentication\n')

# Step 1: Signup (or login if already exists)
print('Step 1: Creating/logging in user...')
signup_data = {
    'email': 'test@chessiq.com',
    'password': 'TestPassword123!',
    'chess_com_username': 'keyur_2332',
    'lichess_username': None
}

try:
    response = requests.post(f'{API_URL}/auth/signup', json=signup_data)
    if response.status_code == 200:
        print('✅ User created')
        token_data = response.json()
        token = token_data.get('access_token')
    else:
        print('⚠️ User might already exist, trying login...')
        login_data = {
            'email': signup_data['email'],
            'password': signup_data['password']
        }
        response = requests.post(f'{API_URL}/auth/login', json=login_data)
        if response.status_code == 200:
            print('✅ User logged in')
            token_data = response.json()
            token = token_data.get('access_token')
        else:
            print(f'❌ Auth failed: {response.json()}')
            exit(1)
except Exception as e:
    print(f'❌ Connection error: {e}')
    exit(1)

# Step 2: Run batch analysis with token
print(f'✅ Got token: {token[:20]}...\n')
print('Step 2: Starting batch analysis...')
print('This may take 5-10 minutes...\n')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

try:
    response = requests.post(
        f'{API_URL}/analysis/batch/all-unanalyzed',
        headers=headers
    )
    data = response.json()
    
    if response.status_code == 200:
        print('✅ Analysis Complete!')
        print(f'   Games analyzed: {data.get("games_analyzed", 0)}')
        print(f'   Moves analyzed: {data.get("moves_analyzed", 0)}')
        print(f'   Status: {data.get("status", "unknown")}')
    else:
        print(f'❌ Error: {data}')
        print(f'Status code: {response.status_code}')
except Exception as e:
    print(f'❌ Connection error: {e}')
    print('Make sure backend is running on http://127.0.0.1:8000')

print('\nDone! Check your dashboard at http://localhost:3000')
