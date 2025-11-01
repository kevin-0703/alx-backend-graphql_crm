from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    # Step 1: Prepare timestamp
    current_time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Step 2: Initialize GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,  # disable SSL verification for localhost
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Step 3: Define simple GraphQL query
    query = gql("""
        query {
            hello
        }
    """)

    # Step 4: Execute query safely
    try:
        response = client.execute(query)
        message = f"{current_time} CRM is alive - GraphQL hello: {response.get('hello', 'No response')}"
    except Exception as e:
        message = f"{current_time} CRM heartbeat failed - {str(e)}"

    # Step 5: Append log message to file
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(message + "\n")

    print(message)
