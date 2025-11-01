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


def update_low_stock():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                message
                updatedProducts {
                    id
                    name
                    stock
                }
            }
        }
    """)

    try:
        result = client.execute(mutation)
        updated_products = result.get("updateLowStockProducts", {}).get("updatedProducts", [])
        message = result.get("updateLowStockProducts", {}).get("message", "No message returned.")

        log_lines = [f"{current_time} - {message}"]
        for product in updated_products:
            log_lines.append(f"    {product['name']}: new stock = {product['stock']}")

    except Exception as e:
        log_lines = [f"{current_time} - Stock update failed: {str(e)}"]

    # Write to log file
    with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
        for line in log_lines:
            log_file.write(line + "\n")

    print("\n".join(log_lines))
