# import requests
# import json

# # Initialize headers as a constant
# HEADERS = {
#     "Authorization": "Bearer secret_vC20y4AQZA3ZUBuGuTRViEMsQZ6zhNcAMu1mmVsHNJY",
#     "Notion-Version": "2022-06-28",
#     "Content-Type": "application/json"
# }


# def fetch_related_item(item_id):
#     fetch_url = f"https://api.notion.com/v1/pages/{item_id}"
#     response = requests.get(fetch_url, headers=HEADERS)
#     return response.json() if response.status_code == 200 else None


# def fetch_db_entries():
#     fetch_url = "https://api.notion.com/v1/databases/b9d81a30289644e3b416b5dfdb1b38d8/query"
#     response = requests.post(fetch_url, headers=HEADERS, json={})
#     return response.json().get("results", []) if response.status_code == 200 else None


# def main():
#     try:
#         results = fetch_db_entries()

#         if results:
#             for entry in results:
#                 process_entry(entry)
#         else:
#             print("Failed to fetch entries.")

#     except requests.RequestException as re:
#         print(f"Request error occurred: {re}")
#     except json.JSONDecodeError as je:
#         print(f"JSON decoding error occurred: {je}")
#     except Exception as e:
#         print(f"An unspecified error occurred: {e}")


# def process_entry(entry):
#     properties = entry.get('properties', {})
#     id_property = properties.get('ID', {}).get('title', [{}])[0].get('plain_text', '')
#     related_items = properties.get('Item', {}).get('relation', [])
#     related_item_ids = [item.get('id') for item in related_items if item.get('id')]
#     quantity_property = properties.get('Quantity', {}).get('number', None)
#     price_data = entry["properties"]["Price"]
#     price_property = price_data.get("rollup", {}).get("number", None)



#     # Fetch details for each related item
#     detailed_related_items = [fetch_related_item(item_id) for item_id in related_item_ids if item_id]

#     for detailed_item in detailed_related_items:
#         if not detailed_item:
#             continue
#         item_properties = detailed_item.get('properties', {})
#         title_list = item_properties.get('Item', {}).get('title', [])
#         for title_entry in title_list:
#             content = title_entry.get('text', {}).get('content', '')
#             if content:
#                 #print(f"ID: {id_property}, Item: {content}")
#                 print(f"ID: {id_property}, Item: {content}, Quantity: {quantity_property}, Price: {price_property}")
#   # Modified line to include Quantity


# if __name__ == "__main__":
#     main()

#####################
import requests
import json

# Constants
HEADERS = {
    "Authorization": "Bearer secret_vC20y4AQZA3ZUBuGuTRViEMsQZ6zhNcAMu1mmVsHNJY",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
DATABASE_URL = "https://api.notion.com/v1/databases/b9d81a30289644e3b416b5dfdb1b38d8/query"

# Helper functions for fetching data
def fetch_data(url, method='post', payload={}):
    response = requests.request(method, url, headers=HEADERS, json=payload)
    return response.json() if response.status_code == 200 else None

def fetch_related_item(item_id):
    return fetch_data(f"https://api.notion.com/v1/pages/{item_id}", method='get')

def fetch_db_entries():
    return fetch_data(DATABASE_URL).get("results", [])

# Helper function for processing entries
def process_entry(entry):
    id_property, related_item_ids, quantity, price, total = extract_properties(entry) 

    detailed_related_items = [fetch_related_item(item_id) for item_id in related_item_ids if item_id]
    for detailed_item in detailed_related_items:
        if detailed_item:
            process_detailed_item(detailed_item, id_property, quantity, price, total)

# Helper function for extracting properties
def extract_properties(entry):
    properties = entry.get('properties', {})
    id_property = properties.get('ID', {}).get('title', [{}])[0].get('plain_text', '')
    related_items = properties.get('Item', {}).get('relation', [])
    related_item_ids = [item.get('id') for item in related_items if item.get('id')]
    quantity_property = properties.get('Quantity', {}).get('number', None)
    price_property = properties.get('Price', {}).get('rollup', {}).get('number', None)
    total_property = properties.get('Total', {}).get('formula', {}).get('number', None) 
    return id_property, related_item_ids, quantity_property, price_property, total_property 

# Helper function for processing detailed items
def process_detailed_item(detailed_item, id_property, quantity, price, total):
    item_properties = detailed_item.get('properties', {})
    title_list = item_properties.get('Item', {}).get('title', [])
    for title_entry in title_list:
        content = title_entry.get('text', {}).get('content', '')
        if content:
            print(f"ID: {id_property}, Item: {content}, Quantity: {quantity}, Price: {price}, Total: {total}")
            entry = {
                "ID": id_property,
                "Item": content,
                "Quantity": quantity,
                "Price": price,
                "Total": total
            }
            create_entry_in_purchase(entry)

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
            # "Date": {"date": {"start": entry["Date"]}}  # Optional, only if you have a Date property
        }
    }

    res = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=transformed_data)
    if res.status_code == 200 or res.status_code == 201:
        print(f'Successfully created entry with ID {entry["ID"]}')
    else:
        print(f'Failed to create entry: {res.json()}')


# Main function
def main():
    try:
        results = fetch_db_entries()
        if results:
            for entry in results:
                process_entry(entry)
        else:
            print("Failed to fetch entries.")

    except requests.RequestException as re:
        print(f"Request error occurred: {re}")
    except json.JSONDecodeError as je:
        print(f"JSON decoding error occurred: {je}")
    except Exception as e:
        print(f"An unspecified error occurred: {e}")

# Entry point
if __name__ == "__main__":
    main()
