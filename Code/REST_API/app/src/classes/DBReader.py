import json
import sqlite3
from datetime import datetime
from sqlite3 import Error,Connection
from time import sleep
import json
class DBReader:
    
    def __init__(self,db_file) -> None:
        """ initial class
        :param db_file: database file
        :return: None
        """
        self.conn=None
        self.__create_connection(db_file)

    def __del__(self):
        self.conn.close()

    def __create_connection(self,db_file:str)->Connection:
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

    def __get_record_by_repo_id(self,repo_id:int)->list[tuple]:
        """ create a database connection to the SQLite database
            specified by db_file
        :param repo_id: Repository ID
        :return: list of records in tuple or None
        """
        sql = ''' SELECT * from events WHERE repo_id== ? '''
        cur = self.conn.cursor()
        cur.execute(sql, [repo_id])
        self.conn.commit()
        results=cur.fetchall()
        if results==[]:
            return 'There is no record with this Repository ID'
        else:
            return results

    def get_average_time(self,repo_id:int)->float:
        """
        calculate the average time between events
        :param repo_id: Repository ID
        :return: float in string format
        """
        times_list=[datetime.strptime(x[3], '%Y-%m-%d %H:%M:%S') for x in self.__get_record_by_repo_id(repo_id)]
        return sum([(j-i).total_seconds() for i, j in zip(times_list[:-1], times_list[1:])])/(len(times_list)-1)

        
    def get_events_grouped_by_event_type(self,time_offset:int,time_scale:str='minutes')->dict:
        """ create a database connection to the SQLite database
            specified by db_file
        :param time_offset: time offset from now like 10 which is 10 minutes ago
        :param time_scale: it can be 'seconds' , 'minutes', 'hours','days'
        :return: Connection object or None
        """
        sql=f'''
            SELECT event,count(*) "count" FROM events
            where created_time>= DATETIME('now','localtime','-{time_offset} {time_scale}')
            group by event
            
        '''
        cur = self.conn.cursor()
        # print(sql)
        cur.execute(sql)
        self.conn.commit()
        results=cur.fetchall()
        return dict(results)
    
    def get_chart_data(self,event_type='PullRequestEvent')->str:
        
        while True:
            last_row=self.get_events_grouped_by_event_type(1,'seconds')
            if 'PullRequestEvent' in last_row:
                value=last_row[event_type]
            else:
                value=0
            
            json_data = json.dumps(
                    {
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "value": int(value)
                    }
                )
            
            yield f"data:{json_data}\n\n"
            sleep(1)
        # sleep(10)

    def get_top_watchevent_repos(self,limit=5)->list[tuple]:
        """ create a database connection to the SQLite database
            specified by db_file
        :param limit: the number of top results 
        :return: list of records of database
        """
        sql = f''' 
                with cte as (
                SELECT repo_id,count(*) as count FROM events 
                where event='WatchEvent' 
                group by repo_id,event
                order by count(*) desc
                LIMIT {limit})
                select repositories.repo_url,cte.count from repositories join cte on cte.repo_id=repositories.repo_id
                order by cte.count desc
                '''
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        results=cur.fetchall()
        return results