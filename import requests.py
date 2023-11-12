import requests
import datetime
import os

# Initialize tokens and IDs (You could use environment variables here)
# token = "secret_v0PKdcinJODoAJTGQyahVlQvOA6mc2LpKVGoytT2dOj"
# shopping_db_id = "b9d81a30289644e3b416b5dfdb1b38d8"
# purchase_db_id = "0c9df0af85a5469db0ee1cedc49c0330"

# headers = {
#     "Authorization": f"Bearer {token}",
#     "Notion-Version": "2021-05-13",
#     "Content-Type": "application/json",
# }

# # Query Shopping List Database
# def query_database(database_id):
#     query_url = f"https://api.notion.com/v1/databases/{database_id}/query"
#     res = requests.post(query_url, headers=headers)
#     return res.json()

# # Create New Entry in Purchase Records Database
# def create_page(data: dict):
#     create_url = "https://api.notion.com/v1/pages"

#     payload = {"parent": {"database_id": "0c9df0af85a5469db0ee1cedc49c0330"}, "properties": data}

#     res = requests.post(create_url, headers=headers, json=payload)
#     # print(res.status_code)
#     return res


# # # Delete Entry in Shopping List Database (Optional)
# # def delete_entry_in_shopping(entry_id):
# #     delete_url = f"https://api.notion.com/v1/pages/{entry_id}"
# #     res = requests.delete(delete_url, headers=headers)
# #     return res.json()

# # Main Function to Transfer Items
# def transfer_items():
#     # Step 1: Query the Shopping List Database
#     shopping_data = query_database(shopping_db_id)['results']
    
#     # Step 2: Filter Relevant Items (Optional)
#     items_to_transfer = [item for item in shopping_data ]
    
#     # Step 3 & 4: Transform and Insert Data into Purchase Records
#     for item in items_to_transfer:
#         create_page(item)
        
#         # Step 5: Update/Delete from Shopping List (Optional)
#         # Uncomment the line below if you want to delete the transferred entries from the shopping list
#         # delete_entry_in_shopping(item['id'])

# # Execute the Transfer
# transfer_items()

import requests

# Replace YOUR_NOTION_SECRET_API_KEY with the actual key
headers = {
    "Authorization": "Bearer Ysecret_1jOOiqs9PvArcuMa1Brj4P4sLrWoowQ0FYgb4BXbeh7",
    "Notion-Version": "2022-06-28",  # or whichever API version you're using
    "Content-Type": "application/json"
}

# Replace page_id with the ID you're testing
page_id = "5eab92df-39b4-4034-850b-2776a6254aa0"
fetch_url = f"https://api.notion.com/v1/pages/{page_id}"

response = requests.get(fetch_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Received data:", data)
else:
    print(f"Failed to retrieve page with status code: {response.status_code}")
