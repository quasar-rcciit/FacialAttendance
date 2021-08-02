import mysql.connector
import json


def fetch_json():
    try:
        connection = mysql.connector.connect(
            host="localhost", database="attendance", user="root", password=""
        )

        mySql_Fetch_Table_Query = """SELECT * FROM users"""

        cursor = connection.cursor()
        result1 = cursor.execute(mySql_Fetch_Table_Query)
        items = []

        result = cursor.fetchall()
        for row in result:
            items.append(
                {
                    "id": row[0],
                    "imagename": row[1],
                    "imagepath": row[2],
                    "roll": row[3],
                    "dept": row[4],
                }
            )

        connection.commit()
        # result1=str(result1)
        out_file = open("myfile.json", "w")

        json.dump(items, out_file, indent=6)

        # print(items)

        print("Table fetched successfully ")

    except mysql.connector.Error as error:
        print("Failed to fetch in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return items


print(fetch_json())
