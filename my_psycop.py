import psycopg2

def connect_and_make_cursor(host, dbname, user, password):
    """host = IP of host service
    dbname = database which to connect to
    user = username
    password = password associated with username"""
    
    try:
        conn = psycopg2.connect(f"host = {host}, dbname = {dbname} user = {user} password = {password}")
        conn.set_session(autocommit = True)
        cur = conn.cursor()
    except psycopg2.Error as e:
        print(e)
    return conn, cur

def close_connection():
    """closes both cursor and connection in that order"""
    
    cur.close()
    conn.close()

def insert_columns(table_name, col_type_dict):
    """ table_name = Name of Table to insert columns
        col_type_dict = Dictionary containing key value pairs of column name : column type"""
    try:
        for col_name, type_ in col_type_dict.items():
            cur.execute(f"ALTER TABLE {table_name} \
                        ADD COLUMN IF NOT EXISTS {col_name} {type_};")
    except psycopg2.Error as e:
        print(e)

def insert_rows(table_name, cols, data):
    """table_name = table which to insert rows into
    cols = list of columns which will recieve the data. Expects string in format "(col1, col2, col3, coln)"
    data = the actual data which you will like to insert into each row contained in tuple"""
    
    count = len(data)
    query = f"INSERT INTO {table_name} {cols} \
                    VALUES (" + "%s,"*count  + ")"
    query = query[::-1].replace(',', '', 1)
    query = query[::-1]
    try:
        cur.execute(query, data)
    except psycopg2.Error as e:
        print(e)

def update_row(table_name, col_name, data, condition = None):
    """table_name = table which to update
    col_name = column in which to update the value
    data = data which you would like to change the field to
    condition = Optional. Conditional requirement with which to query using WHERE clause"""
    
    if condition != None:
        try:
            cur.execute(f"UPDATE {table_name}\
            SET {col_name} = {data} \
            WHERE {condition};")
        except psycopg2.Error as e:
            print(e)
            
    else:
        try:
            cur.execute(f"UPDATE {table_name}\
            SET {col_name} = {data};")
        except psycopg2.Error as e:
            print(e)