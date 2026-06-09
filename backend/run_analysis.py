import requests
import json

API_URL = 'http://127.0.0.1:8000'

print('Starting batch analysis of all games...')
print('This may take 5-10 minutes...\n')

try:
    response = requests.post(f'{API_URL}/analysis/batch/all-unanalyzed')
    data = response.json()
    
    if response.status_code == 200:
        print('✅ Analysis Complete!')
        print(f'   Games analyzed: {data.get("games_analyzed", 0)}')
        print(f'   Moves analyzed: {data.get("moves_analyzed", 0)}')
    else:
        print(f'❌ Error: {data}')
        print(f'Status code: {response.status_code}')
except Exception as e:
    print(f'❌ Connection error: {e}')
    print('Make sure backend is running on http://127.0.0.1:8000')
