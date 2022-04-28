from src.classes.Reader import Reader
from src.classes.Writer import Writer
from time import sleep
from os import path

specific_events=['WatchEvent','PullRequestEvent','IssuesEvent']
db_dir = path.realpath(path.join(path.dirname(__file__),path.pardir,path.pardir,'Database'))
db_file=path.join(db_dir,'github.db')
writer=Writer(db_file)

def main():
    reader=Reader(specific_events)
    events=reader.get_new_event()
    if events!=None:
        for row in events:
            writer.create_record(*row)


if __name__ == "__main__":
    while True:
        main()
        sleep(0.7)



