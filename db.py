import sqlite3

# ตั้งค่าการเชื่อมต่อกับ SQLite
conn_str = 'aihitdata.db'  # ไฟล์ฐานข้อมูล SQLite

# ฟังก์ชันสำหรับดึงข้อมูลรวมทั้งหมด
def fetch_total_all():
    total_data = []
    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    query = "SELECT SUM(people_count) AS total_emp, SUM(changes_count) AS total_change, COUNT(com_id) AS total_com FROM comlogs;"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        total_data.append({"emp": row[0], "changes": row[1], "com": row[2]})
    conn.close()
    return total_data

# ฟังก์ชันสำหรับดึงข้อมูลของ UK เท่านั้น
def fetch_total_uk():
    total_data = []
    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    query = "SELECT SUM(people_count) AS total_emp, SUM(changes_count) AS total_change, COUNT(com_id) AS total_com FROM comlogs WHERE area = 2;"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        total_data.append({"emp": row[0], "changes": row[1], "com": row[2]})
    conn.close()
    return total_data

# ฟังก์ชันสำหรับดึงข้อมูลทั่วโลก (ยกเว้น UK)
def fetch_total_ww():
    total_data = []
    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    query = "SELECT SUM(people_count) AS total_emp, SUM(changes_count) AS total_change, COUNT(com_id) AS total_com FROM comlogs WHERE area = 1;"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        total_data.append({"emp": row[0], "changes": row[1], "com": row[2]})
    conn.close()
    return total_data

# ฟังก์ชันสำหรับดึงข้อมูลบริษัทตาม com_id ที่ระบุ
def fetch_com(com_id):
    com_data = []  # สร้าง list สำหรับเก็บข้อมูล
    query = ''' 
        SELECT c.name, c.website, c.url, c.description_short, a.type_name,
               l.people_count, l.senior_people_count, l.emails_count, l.personal_emails_count,
               l.phones_count, l.addresses_count, l.investors_count, l.clients_count,
               l.partners_count, l.changes_count, l.people_changes_count, l.contact_changes_count
        FROM cominfo AS c
        JOIN area AS a ON c.area = a.id
        JOIN comlogs AS l ON c.id = l.com_id
        WHERE c.id = ?;
    '''
    
    conn = sqlite3.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, (com_id,))
    rows = cursor.fetchall()
    for row in rows:
        com_data.append({
            "name": row[0], "website": row[1], "url": row[2], "description_short": row[3], "area": row[4],
            "people_count": row[5], "senior_people_count": row[6], "emails_count": row[7], "personal_emails_count": row[8],
            "phones_count": row[9], "addresses_count": row[10], "investors_count": row[11], "clients_count": row[12],
            "partners_count": row[13], "changes_count": row[14], "people_changes_count": row[15], "contact_changes_count": row[16]
        })
    
    conn.close()
    return com_data  # ส่งคืน list ของ dictionary


print(fetch_total_all())
