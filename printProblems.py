import requests
import json

# Replace with your actual Dynatrace API token and environment ID
DYNATRACE_API_TOKEN = 'token'
DYNATRACE_ENVIRONMENT_ID = 'environment'

# Dynatrace API endpoint for fetching problems
api_url = f'https://{DYNATRACE_ENVIRONMENT_ID}.live.dynatrace.com/api/v2/problems'

#Query parameters for efficient fetching of only open problems
params = {
    'problemSelector': 'status("OPEN")',
    'pageSize': 8
}

# Headers with authorization token
headers = {
    'Authorization': f'Api-Token {DYNATRACE_API_TOKEN}',
    'Content-Type': 'application/json'
}

try:
    # Make GET request to fetch problems
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()  # Raise exception for bad responses

    # Parse JSON response
    problems_data = response.json()

    # Write problems to a file
    with open('dynatrace_problems.json', 'w') as file:
        json.dump(problems_data, file, indent=4)

    print(f"Successfully wrote problems to dynatrace_problems.json")

except requests.exceptions.RequestException as e:
    print(f"Error fetching problems: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
except IOError as e:
    print(f"Error writing to file: {e}")

