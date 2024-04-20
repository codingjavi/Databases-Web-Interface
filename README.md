# Web Interface

Created a web interface for my Database and File Systems class.

## How web interface works
- Used a React front end to display results and ask for user inputs for the queries
- The main front end code is in the App.js file in the source directory
- The index.js renders the App.js component when ran
- Called APIs stored in the Flask server from the front end when user clicks buttons
- The backend Flask server connects to the database using flask_sqlalchemy
- Execute desired queries in Flask APIs 
- Stored models of tables we were going to use 

## Languages Used
- Python
- Javascript
- CSS/HTML

## Running the website
1. Install nessecary packages for Server (Flask, SQLalchemy, flask_sqlalchemy, Python)
2. In the server directory run: python3 server.py
3. Run the mysql database
4. Install nessecary packages for Client directory: npm install
5. Run the front end: npm start

## Features
- Insert a new instructor with attributes in the database.
- Link the new instructor with an existing course and also add the instructor to a student’s committee
- Delete a GRA students who have not passed any milestone yet (to avoid integrity constraint). 

