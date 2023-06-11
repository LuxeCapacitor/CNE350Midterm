#Jarre' Owens
#6/7/23
#CNE350 Midterm Project
#Restful interface that has search and update options for navigating a Zipcode database on Phpmyadmin.

#https://stackoverflow.com/questions/8211128/multiple-distinct-pages-in-one-html-file
#https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
#https://stackoverflow.com/questions/1081750/python-update-multiple-columns-with-python-variables
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#https://github.com/vimalloc/flask-jwt-extended/issues/175

from flask import Flask, render_template, request
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

#Connects to WAMP db and uploads the file 'zip_code_database.csv'
hostname = "127.0.0.1"
uname = "root"
pwd = ""
dbname = "zipcodes"
engine = create_engine(f"mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}")
tables = pd.read_csv(r"C:\Users\owens\OneDrive\Desktop\zip_code_database.csv", dtype={"Population": int})
tables.rename(columns={"zip": "zip_code"}, inplace=True)
tables.rename(columns={"Population": "population"}, inplace=True)
tables.to_sql('zipcodes', con=engine, if_exists='replace', index=False)

#Sets up Flask
app = Flask(__name__)
app.debug = True

#Sets homepage
@app.route('/')
def zipcodes_dash():
    return render_template('login.html')

#Using GET for /search argument
@app.route('/search', methods=['GET'])
def search():
    zip_code = request.args.get('zipCode')

    data = get_zip_results(zip_code)
    population = data.population if data is not None else None

    return render_template('search.html', zipCode=zip_code, population=population)

#Queries the DB using input from zipCode
def get_zip_results(zip_code):
    connection = engine.connect()
    query = text("SELECT * FROM zipcodes WHERE zip_code = :zip_code")
    result = connection.execute(query, {"zip_code": zip_code}).fetchone()
    connection.close()
    return result

#Updates DB if input is valid, otherwise issues a failure message
@app.route('/update', methods=['POST'])
def update():
    zip_code = request.form['zipCode']
    population = request.form['population']

    if zip_code.isdigit() and population.isdigit():
        zip_code = int(zip_code)
        population = int(population)
        if 0 <= zip_code <= 99999 and population >= 0:
            connection = engine.connect()
            query = text("UPDATE zipcodes SET population = :population WHERE zip_code = :zip_code")
            connection.execute(query, {"zip_code": zip_code, "population": population})
            connection.close()
            return render_template('updatesuccess.html')
    return render_template('updatefail.html')

#Runs Flask
if __name__ == '__main__':
    app.run()