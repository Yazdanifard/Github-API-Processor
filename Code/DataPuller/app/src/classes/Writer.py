import sqlite3
from datetime import datetime
from sqlite3 import Error

class Writer:
    
    def __init__(self,db_file) -> None:
        self.conn=None
        self.__create_connection(db_file)

    def __del__(self):
        self.conn.close()

    def __create_connection(self,db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return self.conn

    def create_record(self,repo_id:int,event_name:str,event_time:str,repo_name:str):
        """
        Create a new project into the events table
        :param conn:
        :param project:
        :return: row id
        """
        cur = self.conn.cursor()
        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        repo_url='https://github.com/'+repo_name
        list_queries = [
            ["INSERT INTO events(repo_id,event,event_time,created_time) VALUES (?,?,?,?)",[repo_id,event_name,event_time,create_time]],
            ["INSERT OR IGNORE INTO repositories(repo_id,repo_url,created_time) VALUES (?, ?, ?); ",[repo_id,repo_url,create_time]]
            ]
        for query in list_queries:
            cur.execute(query[0], query[1])
            self.conn.commit()
        return cur.lastrowid