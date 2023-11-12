# Import the required libraries
import requests
import datetime
import json 

# Initialize the headers for the API request
headers = {
    "Authorization": f"Bearer secret_vC20y4AQZA3ZUBuGuTRViEMsQZ6zhNcAMu1mmVsHNJY",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28", # updated
}
# Function to handle the rollup type for the 'Price' field
def get_rollup_price(price_data):
    return price_data.get("rollup", {}).get("number", None)
# Function to handle the formula type for the 'Total' field
def get_formula_total(total_data):
    return total_data.get("formula", {}).get("number", None)


def fetch_entries_from_shopping_list():
    fetch_url = "https://api.notion.com/v1/databases/b9d81a30289644e3b416b5dfdb1b38d8/query"
    res = requests.get(fetch_url, headers=headers)
    if res.status_code == 200: # Simplified
        return res.json()['results']
    else:
        print(f"Failed to fetch entries with status {res.status_code}: {res.json()}")
        return []

# Function to fetch an entry by its ID
def fetch_entry_by_id(entry_id):
    fetch_url = f"https://api.notion.com/v1/pages/{entry_id}"
    res = requests.get(fetch_url, headers=headers) # Changed to GET
    if res.status_code == 200: # Simplified
        return res.json()
    else:
        print(f"Failed to fetch entry by ID {entry_id} with status {res.status_code}: {res.json()}")
        return None

# Function to fetch related items based on their IDs
def fetch_related_items(relation_ids):
    related_items = []
    for relation in relation_ids:
        item_id = relation.get("id")
        if item_id:
            item_data = fetch_entry_by_id(item_id)
            if item_data:
                item_name = item_data["properties"]["Name"]["title"][0]["text"]["content"]
                related_items.append(item_name)
    if len(related_items) == 1:
        return related_items[0]
    else:
        return related_items
    return related_items

# Function to create a new entry in the "Purchase Records" database
def create_entry_in_purchase(entry):
    print("Entry:", entry)
    
    if "Total" not in entry:
        entry["Total"] = entry["Quantity"] * entry["Price"]
        
    transformed_data = {
        "parent": {"type": "database_id", "database_id": "0c9df0af85a5469db0ee1cedc49c0330"},
        "properties": {
            "ID": {"title": [{"type": "text", "text": {"content": str(entry["ID"])} }]},
            "Item": {"rich_text": [{"type": "text", "text": {"content": entry["Item"]}}]},
            "Quantity": {"number": entry["Quantity"]},
            "Price": {"number": entry["Price"]},
            "Total": {"number": entry["Total"]},
            "Date": {"date": {"start": entry["Date"]}}
        }
    }
    
    res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=transformed_data)
    if res.status_code == 200 or res.status_code == 201:
        print(f'Successfully created entry with ID {entry["ID"]}')
    else:
        print(f'Failed to create entry: {res.json()}')

# Main function
if __name__ == '__main__':
    shopping_entries = fetch_entries_from_shopping_list()

    for entry in shopping_entries:
        id_value = entry["properties"]["ID"].get("number", None)
        
        item_relation_ids = entry["properties"]["Item"].get("relation", [])
        item_value = None
        if item_relation_ids:
            item_value = fetch_related_items(item_relation_ids)
        
        quantity_value = entry["properties"]["Quantity"].get("number", None)
        # Handle rollup type for the 'Price' field
        price_data = entry["properties"]["Price"]
        price_value = get_rollup_price(price_data)
        date_value = entry["properties"]["Date"]["date"].get("start", None)
        # Handle formula type for the 'Total' field
        total_data = entry["properties"]["Total"]
        total_value = get_formula_total(total_data)

        if all([id_value, item_value, quantity_value, price_value, date_value]):
            total_value = quantity_value * price_value
            new_entry = {
                "ID": id_value,
                "Item": item_value,
                "Quantity": quantity_value,
                "Price": price_value,
                "Total": total_value,
                "Date": date_value
            }
            create_entry_in_purchase(new_entry)
        else:
            print(f"Skipping entry due to missing values: {entry}")



