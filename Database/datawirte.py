import mysql.connector


def recordattendance(name, time, date):
    try:
        connection = mysql.connector.connect(
            host="localhost", database="attendance", user="root", password=""
        )

        mySql_Fetch_Table_Query = """INSERT INTO results (Name, Time, Date)
                                VALUES(%s, %s, %s)"""

        val = (name, time, date)

        cursor = connection.cursor()
        result1 = cursor.execute(mySql_Fetch_Table_Query, val)
        connection.commit()
        print(result1)

        print("Table created successfully ")

    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
