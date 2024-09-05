import time
import json
import subprocess
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from datetime import datetime, timedelta

# Initialize Elasticsearch client
es = Elasticsearch(['http://localhost:9200'])

# Load configuration from JSON file
def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Build query for logs
def build_query():
    now = datetime.utcnow()
    five_minutes_ago = now - timedelta(minutes=5)
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    five_minutes_ago_str = five_minutes_ago.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    return {
        "query": {
            "bool": {
                "must": [
                    {"wildcard": {"message": "*error*"}},  # Case-insensitive search using wildcard
                    {
                        "range": {
                            "@timestamp": {
                                "gte": five_minutes_ago_str,  # Start of time range
                                "lte": now_str  # End of time range
                            }
                        }
                    }
                ]
            }
        }
    }

# Function to query Elasticsearch
def get_logs_containing_error(index_pattern, query):
    try:
        response = es.search(index=index_pattern, body=query)
        hits = response['hits']['hits']
        return hits
    except NotFoundError:
        print(f"No indices matching pattern {index_pattern} found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to perform additional searches based on keyword matches
def perform_additional_search(search_pattern):
    additional_query = {
        "query": {
            "match": {
                "message": search_pattern
            }
        }
    }
    response = es.search(index='myindex-*', body=additional_query)
    hits = response['hits']['hits']
    return hits

# Function to run a command and check its output
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Command successful: {command}")
            return result.stdout
        else:
            print(f"Command failed: {command}\nError: {result.stderr}")
            return None
    except Exception as e:
        print(f"An error occurred while running command: {e}")
        return None

# Function to perform actions based on the configuration
def perform_actions(actions):
    for action in actions:
        print(f"Performing action: {action['action']}")
        result = run_command(action['action'])
        if result and action['result'] in result:
            print(f"Action '{action['action']}' completed successfully.")
        else:
            print(f"Action '{action['action']}' did not complete as expected.")

# Main loop to run the query every minute
def main():
    config = load_config('config.json')
    keywords = config.get('keywords', {})

    index_pattern = 'myindex-*'
    
    while True:
        query = build_query()
        logs = get_logs_containing_error(index_pattern, query)
        for log in logs:
            timestamp = log['_source'].get('@timestamp')
            message = log['_source'].get('message')
            file_name = log['_source'].get('log', {}).get('file', {}).get('path', 'unknown')
            print(f"Timestamp: {timestamp}, Message: {message}, Log File: {file_name}")

            # Check for keywords and perform additional search
            for keyword, details in keywords.items():
                if keyword in message:
                    print(f"Keyword '{keyword}' found in log. Performing additional search.")
                    additional_logs = perform_additional_search(details['Success'])
                    if additional_logs:
                        print(f"Additional logs found for keyword '{keyword}'.")
                        # Run health check
                        health_check_output = run_command(details['healthcheck'])
                        if health_check_output:
                            print(f"Health check output: {health_check_output}")

                        # Perform actions
                        if 'Actions' in details:
                            perform_actions(details['Actions'])

                        # Validate recovery (you might want to implement specific validation here)
                        print(f"Validating recovery for keyword '{keyword}'.")
                        # Example: Check if service is healthy
                        validation_output = run_command(details['healthcheck'])
                        if validation_output:
                            print(f"Service is healthy after recovery: {validation_output}")
                        else:
                            print(f"Service is not healthy after recovery.")
        
        # Wait for 1 minute before running the query again
        time.sleep(60)

if __name__ == "__main__":
    main()
