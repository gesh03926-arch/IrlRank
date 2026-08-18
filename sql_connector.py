import mysql.connector

class SQL_Connector:

    def __init__(self, host:str, user:str, password:str, database:str):
        self.mydb = mysql.connector.connect(
            host=host,
            user = user, password=password,
            database=database)
        self.mycursor = self.mydb.cursor()

    def get_users_data(self):

        sql = "SELECT * FROM users"
        self.mycursor.execute(sql)

        table_content = self.mycursor.fetchall()
        for row in table_content:
            print(row)
        self.mydb.commit()

    def insert_values(self, name:str, rank:str):
        sql_query = "INSERT INTO users(username, irl_rank) VALUES (%s, %s)"
        sql_values = [name, rank]
        self.mycursor.execute(sql_query, sql_values)
        self.mydb.commit()