import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost", database="attendance", user="root", password=""
    )

    mySql_Create_Table_Query = """CREATE TABLE users ( 
                             Id int(11) NOT NULL,
                             Name varchar(250) NOT NULL,
                             ImgLink varchar(250) NOT NULL,
                             Roll int(11) NOT NULL,
                             Dept varchar(250) NOT NULL,
                             PRIMARY KEY (Id)) """

    mySql_Fetch_Table_Query = """INSERT INTO users (Id, Name, ImgLink, Roll, Dept)
                            VALUES(%s, %s, %s, %s, %s)"""

    print("Enter ID")
    id = int(input())
    print("Enter Name")
    name = input()
    print("Img Link")
    ImgLink = input()
    print("Roll")
    roll = int(input())
    print("Dept")
    dept = input()
    val = (id, name, ImgLink, roll, dept)

    cursor = connection.cursor()
    # result = cursor.execute(mySql_Create_Table_Query)
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
