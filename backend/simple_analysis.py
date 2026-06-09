import requests
import json

API_URL = 'http://127.0.0.1:8000'

print('ChessIQ Batch Analysis\n')
print('Attempting batch analysis...\n')

# Try without auth first (in case endpoint is public)
try:
    response = requests.post(f'{API_URL}/analysis/batch/all-unanalyzed')
    
    if response.status_code == 200:
        print('✅ Analysis Started!')
        data = response.json()
        print(f'   Games analyzed: {data.get("games_analyzed", 0)}')
        print(f'   Moves analyzed: {data.get("moves_analyzed", 0)}')
    elif response.status_code == 401:
        print('❌ Endpoint requires authentication')
        print('   Solution: Check backend auth/login routes')
    else:
        print(f'Status: {response.status_code}')
        print(f'Response: {response.text}')
        
except Exception as e:
    print(f'Error: {e}')