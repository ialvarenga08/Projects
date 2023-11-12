from notion.client import NotionClient
import requests

# Initialize Notion client
# client = NotionClient(token_v2="secret_v0PKdcinJODoAJTGQyahVlQvOA6mc2LpKVGoytT2dOj")
# # Data_Base_ID = "0c9df0af85a5469db0ee1cedc49c0330"
# # token = "secret_yqckRKjbmGke8vtTET5OxZlhWrBSRjAUQ4Z0BD03lWY"
import os
token_v2 = os.environ.get("secret_v0PKdcinJODoAJTGQyahVlQvOA6mc2LpKVGoytT2dOj")
client = NotionClient(token_v2=token_v2)
db_headers = {
    "Authorization": f"Bearer {token_v2}",
    "Notion-Version": "2021-05-13",
}

headers = {
    "Authorization": f"Bearer {token_v2}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

# Get the collections for Shopping List and Purchase Records
shopping_list = client.get_collection_view("b9d81a30289644e3b416b5dfdb1b38d8")
purchase_records = client.get_collection_view("0c9df0af85a5469db0ee1cedc49c0330")

# Loop through the rows in Shopping List to transfer them to Purchase Records
# for row in shopping_list.collection.get_rows():
#     print(f"Fetching record: {row.name}")  # This line will print the name of each item
#     new_row = purchase_records.collection.add_row()
#     new_row.name = row.name
#     new_row.Quantity = row.Quantity
#     new_row.Price = row.Product_Name.Price
#     row.remove()  # Remove the row from Shopping List

# Loop through the rows in Shopping List to transfer them to Purchase Records
# for row in shopping_list.collection.get_rows():
#     new_row = purchase_records.collection.add_row()
#     new_row.name = row.name
#     new_row.Quantity = row.Quantity
#     new_row.Price = row.Product_Name.Price  # Assuming the 'Product_Name' field in Shopping List links to the 'Product Prices' database
#     row.remove()  # Remove the row from Shopping List

# Note: This is a basic example and does not include error handling or edge cases.
