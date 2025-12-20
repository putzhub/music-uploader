import requests


#Can READ from API, but not write. just make it easy to copy & paste info
# Set your API key and user ID
API_KEY = ''
#SER_ID = ''
with open('itch_key') as f:
    API_KEY = f.readline()

# Make the request to create the project
response = requests.get(
    f'https://itch.io/api/1/{API_KEY}/my-games',
    headers={
        'Authorization': f'Bearer {API_KEY}'
    }
)

# Check the response
if response.status_code == 200:
    print('Project created successfully!')
    print('Response:', response.json())
else:
    print('Failed to create project.')
    print('Response:', response.json())