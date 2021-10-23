# get_database_stock.py
import sqlite3
from contextlib import closing


class GetDatabase:
    def __init__(self, name_of_database):
        """
        :param name_of_database: name of data
        """
        self.name_of_database = name_of_database

    def create_table(self, name_of_table):
        """
        :param name_of_table: name of table query
        """
        with closing(sqlite3.connect(self.name_of_database)) as connection:
            with closing(connection.cursor()) as cursor:
                # SQL piece of code Executed
                try:
                    execute = "DROP TABLE {}".format(name_of_table)
                    cursor.execute(execute)
                except sqlite3.OperationalError:
                    print("Already exists the table")
                    # return

                execute = f"""CREATE TABLE {name_of_table} (Date VARCHAR(255),                                      
                                                            Open FLOAT(2),
                                                            High FLOAT(2),
                                                            Low FLOAT(2),
                                                            Close FLOAT(2),
                                                            Volume INT,
                                                            Currency VARCHAR(5),
                                                            Code VARCHAR(15))"""
                cursor.execute(execute)
                # Changes saved into database
                connection.commit()

    def input_data(self, name_table, list_data, stock_code):
        """
        :param name_table: name of table query
        :param list_data: list have data
        """
        with closing(sqlite3.connect(self.name_of_database)) as connection:
            execute = f"""INSERT INTO {name_table} (Date, Open, High, Low, Close, Volume, Currency, Code)
                        VALUES (?, ?, ?, ?, ?, ?, ?, "{stock_code}")"""
            connection.executemany(execute, list_data)
            # Changes saved into database
            connection.commit()

    def view_data(self, name_of_table):
        """
        :param name_of_table: name of table query
        :return: view data from table
        """
        with closing(sqlite3.connect(self.name_of_database)) as connection:
            with closing(connection.cursor()) as cursor:
                execute = "SELECT * FROM {}".format(name_of_table)
                cursor.execute(execute)
                result = cursor.fetchall()
                for x in result:
                    print(x)


if __name__ == '__main__':
    database = GetDatabase("database.db")
    database.create_table("customers")
    List = [("1/4/2021",	133.52,	133.61,	126.76,	129.41,	143302000, "USD"),
            ("1/5/2021",	128.89,	131.74,	128.43,	131.01,	97665000, "USD"),
            ("1/6/2021",	127.72,	131.05,	126.38,	126.6,	155088000, "USD")]
    database.input_data("customers", List, "AAPI")
    database.view_data("customers")

    print("Finish")
