import requests
import time

# Hard-coded constants 
PROBLEM_FETCH_INTERVAL = 60  # Fetch data every x seconds, default is 60

### LED CONTROLLER API ###
LED_CONTROLLER_API_BASE_URL = 'http://0.0.0.0/api'  # Replace with LED controller API base URL
FAILED_API_FETCH_COLOR = 'FFFFFF'  # White, indicates a fetch error for an environment

### ENVIRONMENT 1 CONSTANTS ### COLOR IS GREEN
ENV1_API_TOKEN = 'placeholder'
ENV1_ID = 'env'  # Replace with Environment ID
ENV1_COLOR_CODE = '00ff00'  # Green
ENV1_YELLOW_THRESHOLD = 10
ENV1_RED_THRESHOLD = 20

### ENVIRONMENT 2 CONSTANTS ### COLOR IS PURPLE
ENV2_API_TOKEN = 'placeholder'
ENV2_ID = 'env'
ENV2_COLOR_CODE = 'c500ff'  # Purple
ENV2_YELLOW_THRESHOLD = 50
ENV2_RED_THRESHOLD = 60

### ENVIRONMENT 3 CONSTANTS ### COLOR IS BLUE
ENV3_API_TOKEN = 'placeholder'
ENV3_ID = 'env'
ENV3_COLOR_CODE = '0000ff'  # Blue
ENV3_YELLOW_THRESHOLD = 50
ENV3_RED_THRESHOLD = 60

### ENVIRONMENT 4 CONSTANTS ### COLOR IS RED
ENV4_API_TOKEN = 'placeholder'
ENV4_ID = 'placeholder'
ENV4_COLOR_CODE = 'ff0000'  # Red
ENV4_YELLOW_THRESHOLD = 50
ENV4_RED_THRESHOLD = 60

### ENVIRONMENT 5 CONSTANTS ### COLOR IS WHITE
ENV5_API_TOKEN = 'placeholder'
ENV5_ID = 'placeholder2'
ENV5_COLOR_CODE = 'FFFFFF'  # White
ENV5_YELLOW_THRESHOLD = 50
ENV5_RED_THRESHOLD = 60

#######################################################################################################################

# Function to fetch all problems from Dynatrace API v2 for each environment
def fetch_all_problems():
    all_problems = {
        ENV1_ID: [],
        ENV2_ID: [],
        ENV3_ID: [],
        ENV4_ID: [],
        ENV5_ID: []
    }

    env_tokens = {
        ENV1_ID: ENV1_API_TOKEN,
        ENV2_ID: ENV2_API_TOKEN,
        ENV3_ID: ENV3_API_TOKEN,
        ENV4_ID: ENV4_API_TOKEN,
        ENV5_ID: ENV5_API_TOKEN
    }

    fetch_status = {
        ENV1_ID: False,
        ENV2_ID: False,
        ENV3_ID: False,
        ENV4_ID: False,
        ENV5_ID: False
    }

    for env_id, api_token in env_tokens.items():
        api_url = f'https://{env_id}.live.dynatrace.com/api/v2/problems'
        params = {
            'problemSelector': 'status("OPEN")',
            # 'pageSize': 300,  # Fetch all problems, adjust as needed
        }
        headers = {
            'Authorization': f'Api-Token {api_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            print(f"Successful GET from {env_id}")
            problems = response.json().get('problems', [])
            all_problems[env_id] = problems  # Store problems in the respective environment's list
            fetch_status[env_id] = True
        except requests.exceptions.RequestException as e:
            print(f"Error fetching problems from {env_id}: {e}")
            fetch_status[env_id] = False

    return all_problems, fetch_status

def get_color_for_problem_count(env_id, count):
    if env_id == ENV1_ID:
        if count < ENV1_YELLOW_THRESHOLD:
            return ''  # Turned off
        elif ENV1_YELLOW_THRESHOLD <= count < ENV1_RED_THRESHOLD:
            return 'ffff00'  # Yellow
        elif count >= ENV1_RED_THRESHOLD:
            return 'ff0000'  # Red
    elif env_id == ENV2_ID:
        if count < ENV2_YELLOW_THRESHOLD:
            return ''  # Turned off
        elif ENV2_YELLOW_THRESHOLD <= count < ENV2_RED_THRESHOLD:
            return 'ffff00'  # Yellow
        elif count >= ENV2_RED_THRESHOLD:
            return 'ff0000'  # Red
    elif env_id == ENV3_ID:
        if count < ENV3_YELLOW_THRESHOLD:
            return ''  # Turned off
        elif ENV3_YELLOW_THRESHOLD <= count < ENV3_RED_THRESHOLD:
            return 'ffff00'  # Yellow
        elif count >= ENV3_RED_THRESHOLD:
            return 'ff0000'  # Red
    elif env_id == ENV4_ID:
        if count < ENV4_YELLOW_THRESHOLD:
            return ''  # Turned off
        elif ENV4_YELLOW_THRESHOLD <= count < ENV4_RED_THRESHOLD:
            return 'ffff00'  # Yellow
        elif count >= ENV4_RED_THRESHOLD:
            return 'ff0000'  # Red
    elif env_id == ENV5_ID:
        if count < ENV5_YELLOW_THRESHOLD:
            return ''  # Turned off
        elif ENV5_YELLOW_THRESHOLD <= count < ENV5_RED_THRESHOLD:
            return 'ffff00'  # Yellow
        elif count >= ENV5_RED_THRESHOLD:
            return 'ff0000'  # Red
    return ''

def update_led_controller(problems, fetch_status):
    env1_problem_color = get_color_for_problem_count(ENV1_ID, len(problems[ENV1_ID])) if fetch_status[ENV1_ID] else FAILED_API_FETCH_COLOR  # White if fetch failed
    env2_problem_color = get_color_for_problem_count(ENV2_ID, len(problems[ENV2_ID])) if fetch_status[ENV2_ID] else FAILED_API_FETCH_COLOR  # White if fetch failed
    env3_problem_color = get_color_for_problem_count(ENV3_ID, len(problems[ENV3_ID])) if fetch_status[ENV3_ID] else FAILED_API_FETCH_COLOR  # White if fetch failed
    env4_problem_color = get_color_for_problem_count(ENV4_ID, len(problems[ENV4_ID])) if fetch_status[ENV4_ID] else FAILED_API_FETCH_COLOR  # White if fetch failed
    env5_problem_color = get_color_for_problem_count(ENV5_ID, len(problems[ENV5_ID])) if fetch_status[ENV5_ID] else FAILED_API_FETCH_COLOR  # White if fetch failed

    url = (
        f'{LED_CONTROLLER_API_BASE_URL}?top_init'
        f'&top=0|3|{ENV1_COLOR_CODE}'
        f'&top=3|3|{ENV2_COLOR_CODE}'
        f'&top=6|3|{ENV3_COLOR_CODE}'
        f'&top=9|3|{ENV4_COLOR_CODE}'
        f'&top=12|3|{ENV5_COLOR_CODE}'
        f'&top_whirl=120|ccw'
        f'&bottom_init'
        f'&bottom=0|3|{env1_problem_color}'
        f'&bottom=3|3|{env2_problem_color}'
        f'&bottom=6|3|{env3_problem_color}'
        f'&bottom=9|3|{env4_problem_color}'
        f'&bottom=12|3|{env5_problem_color}'
        f'&bottom_whirl=120|ccw'
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Updated LED controller")
    except requests.exceptions.RequestException as e:
        print(f"Error updating LED controller: {e}")

def main():
    problems, fetch_status = fetch_all_problems()
    for env_id, problems_list in problems.items():
        print(f"Environment ID: {env_id}, Total Problems: {len(problems_list)}")

    update_led_controller(problems, fetch_status)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(PROBLEM_FETCH_INTERVAL)
