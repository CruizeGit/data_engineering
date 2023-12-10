import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from flatfile import flatfile
from helpers import apology, login_required
from dashboard import dashboard

# Configure application
app = Flask(__name__)

#Register blueprints
app.register_blueprint(flatfile, url_prefix="")
app.register_blueprint(dashboard)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")

REQUIRED_CATEGORIES = {'rent', 'transportation', 'food' ,'utilities' ,'healthcare' ,'savings' ,'personal spending' ,'recreation and entertainment',
                       'insurance and investing' ,'miscellaneous'}

def decimal_checker(value):
    pattern = r'^\d+(\.\d+)?$'

    # Use re.match to check if the input matches the pattern
    if re.match(pattern, value):
        return True
    else:
        return False

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return redirect("/dashboard")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        date = request.form.get("date")
        name = request.form.get("name")
        category = request.form.get("category")
        amount = request.form.get("amount")

        #We will first make checks before inserting these values in our tables

        #Just checking first the date
        try:
            #since we all know that html will process date as yyyy-mm-dd but as a string, we will still parse it
            date_str = datetime.strptime(date, '%Y-%m-%d')

            # formatting it into db format 'yyyy-mm-dd' using strftime
            new_date = date_str.strftime('%Y-%m-%d')

            date = new_date
        except ValueError:
            return "Error processing date format. Kindly follow 'dd/mm/yyyy' format"

        if not name:
            return "Kindly provide the name of your expenses in 'My Expense' column"
        elif category not in REQUIRED_CATEGORIES:
            return "Invalid category. Kindly choose from the available category lists"
        elif not decimal_checker(amount) and not amount.isdigit():
            return "Costs must be numerical or decimal value"
        elif float(amount) <= 0:
            return "Cost must have a value greater than 0"
        elif int(float(amount)) <= 0:
            return "Cost must have a value greater than 0"

        #Inserting data into our database
        user_id = session["user_id"]
        db.execute("INSERT INTO budget (user_id, name, category, amount, budget_date) VALUES (?, ?, ?, ?, ?)",
                   user_id, name, category, amount, date)

        return redirect("/add")

    else:
        #I need the current data of users
        budgets = db.execute(
                "SELECT * FROM budget WHERE user_id = ? ORDER BY budget_date DESC, transaction_date DESC", session["user_id"])

        #Just presenting it as a table
        return render_template("manual.html", categories = REQUIRED_CATEGORIES, budgets = budgets)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username, password and confirmation is not blank was submitted
        if (
            not request.form.get("username")
            or not request.form.get("password")
            or not request.form.get("confirmation")
        ):
            return apology("Username/Password/Confirmation MUST NOT BE blank!", 400)

        # Checking if password and confirmation match:
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and Confirmation must MATCH!", 400)

        # Checking first if there's an existing username
        duplicate_username = db.execute(
            "SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"),
        )
        if duplicate_username:  # just means there's already an existing username
            return apology("Username already taken!", 400)

        # If all conditions have been met, let's first hash the password
        hashed_password = generate_password_hash(
            request.form.get("password"), method="pbkdf2:sha256", salt_length=8
        )

        # Adding data into database
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            hashed_password,
        )

        # Remember which user has logged in
        row = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = row[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """Changes the password of user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        password_checker = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists and password is existing
        if len(password_checker) != 1 or not check_password_hash(
            password_checker[0]["hash"], old_password
        ):
            return apology("Invalid username and/or Existing Password", 403)

        # Checking if password matches confirmation and new pasword
        if new_password != confirmation:
            return apology("New Password and Confirmation MUST BE THE SAME", 403)

        # Updates the database with new password
        # If all conditions have been met, let's first hash the password
        hashed_password = generate_password_hash(
            request.form.get("new_password"), method="pbkdf2:sha256", salt_length=8
        )

        # Adding data into database
        db.execute(
            "UPDATE users SET hash = ? WHERE username = ?", hashed_password, username
        )

        # Remember which user has logged in
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = row[0]["id"]

        # Redirect user to home page
        flash("Password has been changed! Redirecting to your portfolio", "info")
        return redirect("/")

    # User reached route via GET (as by clicking href link)
    else:
        return render_template("password.html")


@app.route("/exit_guest")
def guest_exit():
    guest_id = session['username']
    username = session['username']

    #Delete All Records of Guest from the Budget table
    db.execute("DELETE FROM budget_guest WHERE user_id = ? ", guest_id)

    #Delete the Guest from the Guest database
    db.execute("DELETE FROM guest WHERE username = ? ", username)

    #Delete session data - session['username']
    session.clear()

    return redirect("/login")

#Route for deletion of a record of user
@app.route('/delete_budgets', methods=['POST'])
@login_required
def delete_budgets():
    try:
        selected_ids = request.json['selected_ids']

        # Delete selected records from the 'budget' table
        for budget_id in selected_ids:
            db.execute("DELETE FROM budget WHERE id = (?) AND user_id = (?)", budget_id, session["user_id"])

        #Return response 'success' given that it deletes a record
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)



