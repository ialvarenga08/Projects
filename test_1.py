

import requests
import datetime

today = datetime.datetime.now()

Data_Base_ID = "0c9df0af85a5469db0ee1cedc49c0330"
token = "secret_v0PKdcinJODoAJTGQyahVlQvOA6mc2LpKVGoytT2dOj"


db_headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2021-05-13",
}

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13",
}
def post(title: str) -> None:
    """
    Creates a new page in a Notion database with the specified title and other properties.
    
    Parameters:
    title (str): The title of the new page.
    
    Returns:
    None
    """
    print('Creating page now, please wait...')
    
    # Set up the properties for the new page
    page_properties = {
        "title": {
            "title": [{
                "type": "text",
                "text": {
                    "content": title}}]
        },
        "Date": {
            "date": {
                "start": f"{today}"
            },
        },
        "WkStartTime": {
                "number": wkstart
        },
        "WkEndTime": {
            "number": wkend_time
        },
    }
    
    # Send the POST request to create the new page in the database
    response = requests.request(
        "POST",
        "https://api.notion.com/v1/pages",
        json={
            "parent": {"type": "database_id", "database_id": databaseID},
            "properties": page_properties
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2021-05-13",
        },
    )
    
    print(f'New Page in Notion created and named: {title}')
def queryDatabase(databaseID: str) -> None:
    """
    Queries a Notion database and checks if there is already a daily tracking entry for today.
    
    Parameters:
    databaseID (str): The ID of the Notion database to query.
    
    Returns:
    None
    """
    
    db_readurl = f'https://api.notion.com/v1/databases/{databaseID}/query'
    res = requests.request("POST", db_readurl, headers=db_headers)
    data = res.json()
    
    today = datetime.now().strftime('%B-%d')
    last_entry = data['results'][0]['properties']['Open']['title'][0]['plain_text']
    
    if today == last_entry:
        print('There is already a Daily Tracking Entry')
    else:
        print(f'Today is: {today} whereas Last_Entry is: {last_entry}')
        post(today)


# queryDatabase(databaseID)