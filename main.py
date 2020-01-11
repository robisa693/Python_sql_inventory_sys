import sqlite3
import time
from sqlite3 import Error

def sql_connection():
    try:
        connection = sqlite3.connect('mydatabase.db')
        print('Connected to database')
        return connection
    except Error:
        print(Error)

def create_sql_table(con, table):
    sql_cursor = con.cursor()
    sql_cursor.execute(table)
    con.commit

def print_sql_table(con, table_name):
    sql_cursor = con.cursor()
    sqlite_select_query = (f"SELECT * from {table_name}")
    sql_cursor.execute(sqlite_select_query)
    rows = sql_cursor.fetchall()

    print("ID  Count  Last Updated        Name   ")
    for row in rows:
        print(f'{row[0]}  |{row[2]}     |{row[3]}   |{row[1]}')


def add_item_to_inventory_table(con, tablename, date, name):
    if name != "":
        sql_cursor = con.cursor()
        sql = f''' INSERT OR IGNORE INTO {tablename}(name,update_date,count)
                      VALUES('{name.lower()}','{date}', 0) '''
        sql_cursor.execute(sql)
        con.commit()
    else:
        print("Name not specified")

def increment_count_of_item(con, id, table_name, subtract=False):
    sql_cursor = con.cursor()
    new_count = None
    sqlite_select_query = (f"SELECT * from {table_name}")
    sql_cursor.execute(sqlite_select_query)
    rows = sql_cursor.fetchall()
    for row in rows:
       # print(f'{row[0]} and {id}')
        if row[0] == int(id):
        #    print('Found item')
            current_count = row[2]
            name = row[1]
            if current_count == 0 and subtract == True:
                print('Can not subtract from 0, breaking function')
                return
    if id != None:
        if subtract == True and current_count > 0:
            new_count = current_count - 1
        elif subtract == False:
            new_count = current_count + 1
        else:
            print("Could not increment/subtract. Item might already be 0")
        new_date = str(time.strftime("%Y-%m-%d %H:%M"))
        sql_update_query = f"""Update {table_name} set count = {new_count}, update_date = '{new_date}' where id = {id}"""
        print(f'Updating item {name} in table {table_name} with new count of {new_count} and new time of {new_date}')
        sql_cursor.execute(sql_update_query)
    else:
        print("item not found")
    con.commit()

#main
def main():
    date = str(time.strftime("%Y-%m-%d %H:%M"))
    print(date)
    con = sql_connection()
    tablename = 'inventory'
    table = f""" CREATE TABLE IF NOT EXISTS {tablename} (
                id integer PRIMARY KEY,
                name text NOT NULL,
                count integer,
                update_date text,
                UNIQUE(name)
                );"""
    create_sql_table(con, table)
    loop = True
    while loop:

        print("""What would you like to do?
        1.Add new item
        2.Increment item
        3.Decrement item
        4.Print table
        5.Exit
        """)

        inputs = input('answer: ')
        if inputs == "1":
            item_name = input("Name of new item: ")
            add_item_to_inventory_table(con, tablename, date, item_name)
            print_sql_table(con, tablename)

        if inputs == "2":
            item_ID = input("ID of item to increment: ")
            increment_count_of_item(con, item_ID, tablename)
            print_sql_table(con, tablename)

        if inputs == "3":
            item_ID = input("ID of item to decrement: ")
            increment_count_of_item(con, item_ID, tablename, subtract=True)
        if inputs == "4":
            print_sql_table(con, tablename)
        if inputs == "5":
            loop = False

    con.commit()
    print_sql_table(con, tablename)




if __name__ == '__main__':
    main()