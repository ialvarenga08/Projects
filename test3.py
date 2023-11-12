# Import the required libraries
import requests
import datetime

# Initialize the headers for the API request
headers = {
        "Authorization": "Bearer secret_vC20y4AQZA3ZUBuGuTRViEMsQZ6zhNcAMu1mmVsHNJY",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }


def fetch_entries_from_shopping_list():
    fetch_url = f"https://api.notion.com/v1/databases/{'b9d81a30289644e3b416b5dfdb1b38d8'}/query"
    res = requests.post(fetch_url, headers=headers)
    if res.status_code != 200:
        print(f"Failed to fetch entries: {res.json()}")
        return []
    return res.json()['results']
# Function to handle the rollup type for the 'Price' field
def get_rollup_price(price_data):
    return price_data.get("rollup", {}).get("number", None)
# Function to handle the formula type for the 'Total' field
def get_formula_total(total_data):
    return total_data.get("formula", {}).get("number", None)

# Function to create a new entry in the "Purchase Records" database
def create_entry_in_purchase(entry):
    print("Entry:", entry)
    
    if "Total" not in entry:
        entry["Total"] = entry["Quantity"] * entry["Price"]
        
    transformed_data = {
        "parent": {"type": "database_id", "database_id": "0c9df0af85a5469db0ee1cedc49c0330"},  # replace with your actual database ID
        "properties": {
            "ID": {
                "title": [{
                    "type": "text",
                    "text": {"content": str(entry["ID"])}
                }]
            },
            "Item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": entry["Item"]}
                }]
            },
            "Quantity": {
                "number": entry["Quantity"]
            },
            "Price": {
                "number": entry["Price"]
            },
            "Total": {
                "number": entry["Total"]
            },
            "Date": {
                "date": {"start": entry["Date"]}
            }
        }
    }
    res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=transformed_data)
    if res.status_code == 200 or res.status_code == 201:
        print(f'Successfully created entry with ID {entry["ID"]}')
    else:
        print(f'Failed to create entry: {res.json()}')


# Example usage
# new_entry = {
#     'ID': 1,
#     'Item': 'Apple',
#     'Quantity': 2,
#     'Price': 1.5,
#     'Total': 2 * 1.5,  # Quantity multiplied by Price
#     'Date': '2023-09-10T01:33:14.234441'
# }

if __name__ == '__main__':
    shopping_entries = fetch_entries_from_shopping_list()

    for entry in shopping_entries:
        # Assume that you can map the entry from Shopping List DB to Purchase Records DB easily
        # If not, you need to write transformation logic here
        quantity = entry["properties"]["Quantity"]["number"]
        price = entry["properties"]["Price"]["number"]
        total = quantity * price

        new_entry = {
            "ID": entry["properties"]["ID"]["number"],
            "Item": entry["properties"]["Item"]["title"][0]["text"]["content"],
            "Quantity": quantity,
            "Price": price,
            "Total": total,
            "Date": entry["properties"]["Date"]["date"]["start"]
        }
        create_entry_in_purchase(new_entry)
