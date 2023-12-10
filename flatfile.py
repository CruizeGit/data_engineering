from flask import Blueprint, render_template, request, session, redirect, url_for
from cs50 import SQL
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from helpers import apology, login_required

import csv
import io
import re

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")

flatfile = Blueprint("flatfile", __name__, static_folder="static")

REQUIRED_EXTENSION = {'csv'}
REQUIRED_COLUMNNAMES = {'date', 'name', 'category', 'cost'}
REQUIRED_CATEGORIES = {'rent', 'transportation', 'food' ,'utilities' ,'healthcare' ,'savings' ,'personal spending' ,'recreation and entertainment',
                       'insurance and investing' ,'miscellaneous'}

def required_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in REQUIRED_EXTENSION

def decimal_checker(value):
    pattern = r'^\d+(\.\d+)?$'

    # Use re.match to check if the input matches the pattern
    if re.match(pattern, value):
        return True
    else:
        return False

@flatfile.route("/upload_csv_guest", methods=['GET', 'POST'])
def upload_csv_guest():
    if request.method == 'POST':
        f = request.files['file']

        #Inserting a user into a guest database
        #Will validate first username
        username = request.form.get("username")
        if not username:
            return apology("Must provide Username Info", 400)

        # Checking first if there's an existing username
        duplicate_username = db.execute(
            "SELECT * FROM guest WHERE username = :username",
            username=request.form.get("username"),
        )

        if duplicate_username:  # just means there's already an existing username
            return apology("Username already taken!", 400)

        hashed_password = generate_password_hash(
                "guest", method="pbkdf2:sha256", salt_length=8 )

        #Now inserting records in our database
        db.execute ("INSERT INTO guest (username, hash) VALUES (?,?)", username, hashed_password)

        #I need to remember the user that logged in
        session['username'] = username

        #cChecking if template file is a csv file
        if f and required_extension(f.filename):
            #Read the CSV file
            raw_data = []
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.reader(stream)
            for row in csv_reader:
                raw_data.append(row)

            #We need to countercheck first the columns if it matches with what we needed
            header = raw_data[0]
            header_row = [column.lower() for column in header]
            count = len(header_row)

            if count != 4:
                return "Incorrect Number of Columns"

            #We need to check first if we have the proper columns
            for row in header_row:
                if row not in REQUIRED_COLUMNNAMES:
                    return "Incorrect Column Name"

            #Checking if dates have proper format (mm/dd/yyyy) and converting them into standard formatting
            for row in raw_data[1:]:
                date_value = row[0]
                name = row[1]
                category = row[2].lower()
                amount = row[3]

                try:
                    # using datetime function strptime to parse the value
                    date_str = datetime.strptime(date_value, '%d/%m/%Y')

                    # formatting it into db format 'yyyy-mm-dd' using strftime
                    new_date = date_str.strftime('%Y-%m-%d')

                    row[0] = new_date
                except ValueError:
                    return "Error: Invalid date format. Kindly follow 'dd/mm/yyyy' format"

                if not name:
                    return "Kindly provide the name of your expenses in 'Name' column"
                elif category not in REQUIRED_CATEGORIES:
                    return "Invalid category. Kindly choose from the available category lists"
                elif not decimal_checker(amount) and not amount.isdigit():
                    return "Costs must be numerical or decimal value"
                elif float(amount) == 0:
                    return "Cost must have a value greater than 0"
                elif int(float(amount)) == 0:
                    return "Cost must have a value greater than 0"

                #We will now insert each record in our database
                db.execute("INSERT INTO budget_guest (user_id, name, category, amount, budget_date) VALUES (?, ?, ?, ?, ?)",
								            session['username'], name, category, amount, new_date)

            return redirect(url_for('dashboard.dashboard_guest_func'))

    else:
        return render_template('upload_guest.html')

@flatfile.route("/upload_user", methods=['GET', 'POST'])
@login_required
def upload_user():
    if request.method == 'POST':
        f = request.files['file']

        user_id = session["user_id"]

        #cChecking if template file is a csv file
        if f and required_extension(f.filename):
            #Read the CSV file
            raw_data = []
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.reader(stream)
            for row in csv_reader:
                raw_data.append(row)

            #We need to countercheck first the columns if it matches with what we needed
            header = raw_data[0]
            header_row = [column.lower() for column in header]
            count = len(header_row)

            if count != 4:
                return "Incorrect Number of Columns"

            #We need to check first if we have the proper columns
            for row in header_row:
                if row not in REQUIRED_COLUMNNAMES:
                    return "Incorrect Column Name"

            #Checking if dates have proper format (mm/dd/yyyy) and converting them into standard formatting
            for row in raw_data[1:]:
                date_value = row[0]
                name = row[1]
                category = row[2].lower()
                amount = row[3]

                try:
                    # using datetime function strptime to parse the value
                    date_str = datetime.strptime(date_value, '%d/%m/%Y')

                    # formatting it into db format 'yyyy-mm-dd' using strftime
                    new_date = date_str.strftime('%Y-%m-%d')

                    row[0] = new_date
                except ValueError:
                    return "Error: Invalid date format. Kindly follow 'dd/mm/yyyy' format"

                if not name:
                    return "Kindly provide the name of your expenses in 'Name' column"
                elif category not in REQUIRED_CATEGORIES:
                    return "Invalid category. Kindly choose from the available category lists"
                elif not decimal_checker(amount) and not amount.isdigit():
                    return "Costs must be numerical or decimal value"
                elif float(amount) == 0:
                    return "Cost must have a value greater than 0"
                elif int(float(amount)) == 0:
                    return "Cost must have a value greater than 0"

                #We will now insert each record in our database
                db.execute("INSERT INTO budget (user_id, name, category, amount, budget_date) VALUES (?, ?, ?, ?, ?)",
								            user_id, name, category, amount, new_date)


            #We will redirect user to all expenses to see if his data is being shown
            return redirect('/add')

    else:
        return render_template('upload_user.html')



