import datetime
import requests

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm CRM system health.
    Optionally checks the GraphQL endpoint's responsiveness.
    """
    log_path = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Default message
    message = f"{timestamp} CRM is alive"

    # Optional: Verify GraphQL hello field
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200 and "Hello, GraphQL!" in response.text:
            message += "  GraphQL endpoint OK"
        else:
            message += f" ⚠️ GraphQL endpoint returned status {response.status_code}"
    except Exception as e:
        message += f" GraphQL check failed: {e}"

    # Append log message
    with open(log_path, "a") as log:
        log.write(message + "\n")
