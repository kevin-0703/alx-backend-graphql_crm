#!usr/bin/env python3
import datetime
from gql import Client,gql
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql/"
LOG_FILE = "/tmp/order_reminders_log.txt"

transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT, verify=False)
client = Client(transport=transport, fetch_schema_from_transport=False)

query = gql("""
{
            allOrders {
                edges {
                    node {
                        id
                        totalAmount 
                        orderDate 
                        customer {
                            email
                        }
                        }
                    }
                }
            }""")

one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

try:
    result = client.execute(query)
    orders = result.get("allOrders", {}).get("edges", [])
    reminder_count = 0

    with open(LOG_FILE, "a") as log:
        for order in orders:
            node = order.get("node", {})
            order_date = datetime.datetime.fromisoformat(node.get("orderDate").replace("Z", "+00:00"))
            if order_date >= one_week_ago:
                email = node.get("customer", {}).get("email", "unknown")
                log.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - Reminder sent for Order ID {node.get('id')} to {email}\n")
                reminder_count += 1

    print(f"Order reminders processed! ({reminder_count} reminders logged)")

except Exception as e:
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - Error: {(e)}\n")
        print(f"Error occurred while processing reminders.")