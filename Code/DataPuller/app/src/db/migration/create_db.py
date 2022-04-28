from os import path
import sqlite3
db_dir = path.realpath(path.join(path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(__file__)))))),'Database'))
db_file=path.join(db_dir,'github.db')
try:
    conn = sqlite3.connect(db_file)
    cur =conn.cursor()
    create_table_query="""
    CREATE TABLE events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repo_id UNSIGNED BIG INT,
        event VARCHAR(50),
        event_time VARCHAR(20),
        created_time VARCHAR(20) 
    );

    CREATE INDEX events_repo_id 
    ON events (repo_id,event);

    CREATE INDEX events_created_time 
    ON events (created_time);


    CREATE TABLE repositories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repo_id UNSIGNED BIG INT,
        repo_url VARCHAR(250),
        created_time VARCHAR(20) 
    );
   
    CREATE UNIQUE INDEX unique_repositories_repo_id 
    ON repositories (repo_id);
    """
    cur.executescript(create_table_query)
    conn.commit()
    conn.close()
except Exception as e:
    print(e)
