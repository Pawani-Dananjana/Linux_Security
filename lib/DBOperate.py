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
        c.execute('''DROP TABLE %s;''' % tablename)
    except:
        pass
    SQLCreat = '''CREATE TABLE %s
               (PATH  char(600) PRIMARY KEY  NOT NULL,
               STAT   char NOT NULL,
               MD5        char,
               Rule_Type  char,
               Rule_Check char,
               Record char(1));
                  ''' % tablename
    c.execute(SQLCreat)
    print('Table created successfully', tablename)

def SQLupdate(tablename, path, data: dict):
    str_ = ''
    SQLUpdate1 = "UPDATE %s SET " % tablename
    SQLUpdate2 = "WHERE PATH='%s'" % path
    for i in data:
        str_ = str_ + i + "='" + data[i] + "',"
    str_ = str_[:-1]
    SQLUpdate = SQLUpdate1 + str_ + SQLUpdate2
    return SQLUpdate

def SQLinsert(tablename, data):
    SQLInsert1 = "INSERT INTO %s " % tablename
    SQLInsert2 = ''
    SQLInsert3 = ''
    for i in data:
        SQLInsert2 = SQLInsert2 + i + ','
    SQLInsert2 = SQLInsert2[:-1]
    for i in data:
        SQLInsert3 = SQLInsert3 + "'" + data[i] + "'" + ','
    SQLInsert3 = SQLInsert3[:-1]
    SQLInsert = SQLInsert1 + '(' + SQLInsert2 + ')VALUES(' + SQLInsert3 + ');'
    return SQLInsert

def queryFileData(c, tablename, path):
    SQLQuery = "SELECT * FROM %s WHERE path=\'%s\'" % (tablename, path)
    c.execute(SQLQuery)
    values = c.fetchall()
    if values == []:
        return None
    else:
        return values[0]
