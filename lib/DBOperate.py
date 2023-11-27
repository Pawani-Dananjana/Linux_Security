import sqlite3

filedb = {
    'PATH': '',
    'STAT': '',
    'MD5': '',
    'Rule_Type': '',
    'Rule_Check': '',
    'Record': 'o'
}

recordmap = {
    'a': 'ADDED',
    'm': 'MODIFIED',
    'o': 'REMOVED'
}

def SQLcreatetable(c, tablename):
    try:
        c.execute(f"SELECT * FROM {tablename} LIMIT 1;")
        print(f"Table {tablename} already exists.")
        return
    except sqlite3.OperationalError:
        pass

    SQLCreat = f'''CREATE TABLE {tablename}
               (PATH  char(600) PRIMARY KEY  NOT NULL,
               STAT   char NOT NULL,
               MD5        char,
               Rule_Type  char,
               Rule_Check char,
               Record char(1));
                  '''
    c.execute(SQLCreat)
    print('Table created successfully', tablename)

def SQLupdate(tablename, path, data: dict):
    str_ = ''
    SQLUpdate1 = f"UPDATE {tablename} SET "
    SQLUpdate2 = f"WHERE PATH='{path}'"
    for i in data:
        str_ = str_ + f"{i}='{data[i]}',"
    str_ = str_[:-1]
    SQLUpdate = SQLUpdate1 + str_ + SQLUpdate2
    return SQLUpdate

def SQLinsert(tablename, data):
    SQLInsert1 = f"INSERT INTO {tablename} "
    SQLInsert2 = ''
    SQLInsert3 = ''
    for i in data:
        SQLInsert2 = SQLInsert2 + f"{i},"
    SQLInsert2 = SQLInsert2[:-1]
    for i in data:
        SQLInsert3 = SQLInsert3 + f"'{data[i]}'" + ','
    SQLInsert3 = SQLInsert3[:-1]
    SQLInsert = SQLInsert1 + f'({SQLInsert2})VALUES({SQLInsert3});'
    return SQLInsert

def queryFileData(c, tablename, path):
    SQLQuery = f"SELECT * FROM {tablename} WHERE path='{path}'"
    c.execute(SQLQuery)
    values = c.fetchall()
    if values == []:
        return None
    else:
        return values[0]

# Example usage
if __name__ == "__main__":
    # Connect to the database (replace 'your_database.db' with your actual database file)
    conn = sqlite3.connect('Initial.db')
    cursor = conn.cursor()

    # Example: Create a table named 'FILEDB'
    SQLcreatetable(cursor, 'FILEDB')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
