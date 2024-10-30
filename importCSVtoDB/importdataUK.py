import pandas as pd
import sqlite3

# Read CSV file and set column data types
file_path = r'importCSVtoDB\aihitdata-uk-10k.csv'
data2 = pd.read_csv(file_path, dtype={
    'id': str,
    'website': str,
    'url': str,
    'description_shorts': str,
    'people_count': int,
    'senior_people_count': int,
    'emails_count': int,
    'personal_emails_count': int,
    'phones_count': int,
    'addresses_count': int,
    'investors_count': int,
    'clients_count': int,
    'partners_count': int,
    'changes_count': int,
    'people_changes_count': int,
    'contact_changes_count': int
})

# Handle NaN values
data2.fillna('', inplace=True)

# Set up SQLite connection
conn = sqlite3.connect('aihitdata.db')
cursor = conn.cursor()

# Import data into the 'cominfo' table
for _, row in data2.iterrows():
    try:
        cursor.execute('''
            INSERT INTO cominfo (id, name, website, url, description_short, area)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (row['id'], row.get('name', ''), row['website'], row['url'], row.get('description_short', ''), 2))
    except Exception as e:
        print(f"Error inserting row {row['id']} in cominfo: {e}")

# Import data into the 'comlogs' table
for _, row in data2.iterrows():
    try:
        cursor.execute('''
            INSERT INTO comlogs (com_id, people_count, senior_people_count, emails_count, personal_emails_count,
                                 phones_count, addresses_count, investors_count, clients_count, partners_count,
                                 changes_count, people_changes_count, contact_changes_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['id'], row['people_count'], row['senior_people_count'], row['emails_count'],
              row['personal_emails_count'], row['phones_count'], row['addresses_count'], row['investors_count'],
              row['clients_count'], row['partners_count'], row['changes_count'], row['people_changes_count'],
              row['contact_changes_count']))
    except Exception as e:
        print(f"Error inserting row {row['id']} in comlogs: {e}")

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
