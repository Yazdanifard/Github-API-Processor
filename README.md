# GitHub API Proccessor
This processor includes three major components:
   - A database which is a simple sqlite database since the project is just a POC!
   - A Python app that reads https://api.github.com/events and stores data in the database
   - A Flask app that provides REST API for end-users

Based on the [C4 model](https://c4model.com/) (level 1), you can see the relationships between these components:

![C4 Model - Level 1](https://raw.githubusercontent.com/Yazdanifard/Github-API-Processor/ce2be7023b6bb08fb25dd52379b6a68dbcc72040/Docs/Diagram.drawio.png)


# ✨ How to use it
- Get the code and go to the code folder
-  Virtualenv modules installation (Unix based systems)
   - python -m venv virtualenv
   - source virtualenv/bin/activate
-  Virtualenv modules installation (Windows based systems)
   - python -m venv virtualenv
   - .\virtualenv\Scripts\activate
-  Install requirements
   -  pip3 install -r requirements.txt
- Set the .env varibale: [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
  - With GitHub PAT you can send 5000 requests/hour. The program sends a request in each 0.7 second (0.7*5000=3500 seconds ~ 1 hour)
- Run DataPuller/app/app.py
- Run REST_API/app/app.py

### Access the dashboard in browser: http://127.0.0.1:5000/

## ✨ Code structure

```
< PROJECT ROOT >
   |
   |-- Database/
   |     |-- github.db                                   # A created db for testing purposes
   |     |                          
   |-- DataPuller/
   |     |-- app/                   
   |     |     |-- src/               
   |     |     |     |--classes/                  
   |     |     |     |     |-- Reader.py                 # Reads the API and processes the required data
   |     |     |     |     |-- Writer.py                 # Writes data into sqlite db
   |     |     |     |--db/                    
   |     |     |     |     |-- migration/              
   |     |     |     |           |-- create_db.py        # creates a sqlite db if it does not exit
   |     |     |-- app.py              
   |     |-- .env                                        # Set the Github Personal Token by the user 
   |     |                       
   |-- REST_API/
   |     |
   |     |-- app/                   
   |     |     |-- src/               
   |     |     |     |--classes/                  
   |     |     |     |     |-- DBReader.py               # The class for reading data from db
   |     |     |     |     
   |     |     |     |--templates/  
   |     |     |     |     |-- 404.html                  # 404 html page
   |     |     |     |     |-- base.html                 # Base template 
   |     |     |     |     |-- doughnut_chart.html       # The html chart for showing the top Watched Repositories
   |     |     |     |     |-- index.html                # The html home page
   |     |     |     |     |-- line_chart.html           # The html chart as an extra section
   |     |     |-- app.py
   |     |     
   |-- requirements.txt                                  # Python Requirments for running the project
   |
   ************************************************************************
```

# ✨ DEMO

![Demo by Mostafa Yazdanifard](https://github.com/Yazdanifard/Github-API-Processor/blob/0f1f7b5f36479215628fbb23b8302fc7ad1a7303/Docs/Github-API-Processor.gif)