import requests

API_URL = 'http://127.0.0.1:8000'

print('=== ChessIQ Auth Debug ===\n')

# Test 1: Health check
print('Test 1: Health Check')
try:
    response = requests.get(f'{API_URL}/health')
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}\n')
except Exception as e:
    print(f'Error: {e}\n')

# Test 2: Signup
print('Test 2: Signup')
signup_data = {
    'email': 'test@chessiq.com',
    'password': 'TestPassword123!',
    'chess_com_username': 'keyur_2332',
    'lichess_username': None
}
try:
    response = requests.post(f'{API_URL}/auth/signup', json=signup_data)
    print(f'Status: {response.status_code}')
    print(f'Headers: {dict(response.headers)}')
    print(f'Response Text: {response.text}')
    try:
        print(f'Response JSON: {response.json()}')
    except:
        print('(Not JSON)\n')
except Exception as e:
    print(f'Error: {e}\n')

# Test 3: Login
print('Test 3: Login')
login_data = {
    'email': 'test@chessiq.com',
    'password': 'TestPassword123!'
}
try:
    response = requests.post(f'{API_URL}/auth/login', json=login_data)
    print(f'Status: {response.status_code}')
    print(f'Response Text: {response.text}')
    try:
        print(f'Response JSON: {response.json()}')
    except:
        print('(Not JSON)\n')
except Exception as e:
    print(f'Error: {e}\n')

print('=== Debug Complete ===')
