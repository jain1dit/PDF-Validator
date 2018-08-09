import cx_Oracle


# library helper methon
def db_connect(json_string):
    '''
    input:
        json string containing at least:
            {
            "connection": {
              "host": "", "ip": "", "port": "",
              "sid": "", "user": "", "password": ""
             }
            }
    output: cursor object connected to database according to input details
    '''
    connection_dict = json_string['connection']  # contains a dictionary
    db_ip = connection_dict['ip']
    db_port = connection_dict['port']
    db_sid = connection_dict['sid']
    db_user = connection_dict['user']
    db_password = connection_dict['password']

    # Return a string suitable for use as the dsn parameter for connect().
    # This string is identical to the strings in the tnsnames.ora file.
    db_ora_dsn = cx_Oracle.makedsn(db_ip, db_port, db_sid)
    db_connection = cx_Oracle.connect(db_user, db_password, db_ora_dsn)
    return db_connection


# library helper methon
def result_to_json(database_cursor):
    '''
    input: open cursor after query execution
    output:
        a tuple of 2 objects:
            1. rows count (integer)
            2. list of dictionaries containign column-row pairs
    '''
    # cursor.description is a tuple containing:
    # (name, type, display_size, internal_size, precision, scale, null_ok)
    col_list = list(x[0] for x in database_cursor.description)

    # fetchall() returns a list of tuples each tuple containing oen row data
    # expected a single row
    rows_list = database_cursor.fetchall()
    data_result = []

    if len(rows_list) > 0:
        for row in rows_list:
            # create a dictionary containing column-name:column-value
            row_as_dict = {col: str(val) for col, val in zip(col_list, row)}
            data_result.append(row_as_dict)

    return len(rows_list), data_result


# library helper methon
def run_alter_query(db_connection, alter_query):
    '''
    input:
        db_connection: established connection
        alter_query: query string to be executed
    output:
        successful: the dictionary {"Status": "Success"}
        failure: the dictionary {"Status": "Success", "Error": error-details}}
    Note:
        db_connection will not be closed by this function
    '''
    error = None
    db_cursor = db_connection.cursor()

    try:
        db_cursor.execute(alter_query)
    except cx_Oracle.DatabaseError as ex:
        # error of type cx_Oracle._Error, available read-only attributes:
        # code, offset, message, context, isrecoverable
        error = ex.args[0]

    # create dictionaly to be converted to JSON response
    if error is None:
        response = {"Status": "Success"}
    else:
        response = {"Status": "Failure", "Error": error.message}

    return response
