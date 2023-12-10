# dashboard.py
import json
import pandas as pd
import plotly
import plotly.express as px
from cs50 import SQL
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from helpers import login_required
from datetime import datetime, timedelta
import plotly.graph_objs as go
from plotly.subplots import make_subplots


dashboard = Blueprint('dashboard', __name__)

db = SQL("sqlite:///budget.db")

REQUIRED_CATEGORIES = ['rent', 'transportation', 'food' ,'utilities' ,'healthcare' ,'savings' ,'personal spending' ,'recreation and entertainment',
                       'insurance and investing' ,'miscellaneous']

@dashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_data():
    user_id = session["user_id"]
    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        selected_categories = request.form.getlist('categories')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')

        if not selected_categories:
            query = "SELECT category, amount, budget_date FROM budget WHERE (user_id = ?) AND (budget_date BETWEEN ? AND ?)"
            data = db.execute(query, user_id, start_date, end_date)
        else:
            # Create placeholders for selected_categories
            placeholders = ', '.join(['?' for _ in selected_categories])

            # Constructing the query
            query = f"SELECT category, amount, budget_date FROM budget WHERE (user_id = ?) AND (budget_date BETWEEN ? AND ?) AND category IN ({placeholders})"

            # Creating a list of query parameters
            query_params = [session["user_id"], start_date, end_date] + selected_categories

            # Executing the query
            data = db.execute(query, *query_params)


    else: #Get request
        # Get the first day of the current month
        now = datetime.now()
        start_date = datetime(now.year, now.month, 1).strftime('%Y-%m-%d')

        # Get the last day of the current month
        # Since I am having trouble when the month is december, let us make conditions
        if now.month == 12:
            #if the current month is Dec, automatically set next month to January of next year
            last_day = datetime(now.year + 1, 1, 1) - timedelta(days = 1)
        else:
            last_day = datetime(now.year, now.month + 1, 1) - timedelta(days = 1)

        end_date = last_day.strftime('%Y-%m-%d')

        query = "SELECT category, amount, budget_date FROM budget WHERE (user_id = ?) AND (budget_date BETWEEN ? AND ?)"
        data = db.execute(query, user_id, start_date, end_date)


    #Constructing DataFrame
    data_df = pd.DataFrame(data, columns=["category", "amount", "budget_date"])

    #Bar Chart
    fig1 = px.bar(data_df, x="amount", y="category", color="budget_date", title="Category Cost")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    #Pie Chart
    fig2 = px.pie(data_df, values="amount", names="category", title = "Expenses Percentage")
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    #Scatter Chart 1
    fig3 = px.scatter(data_df, x="budget_date", y="amount", color = "category", title = "Expenses Cost vs. Dates")
    fig3.update_traces(marker=dict(size = 16,
                                   line = dict(width = 2, color = 'DarkSlateGray')),
                        selector = dict(mode = 'markers'))
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    #Making Mini Charts - This is Histogram
    # fig4 = px.histogram(data_df, x="budget_date", y="amount", color="category")
    # graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    #Bubble Scatter
    fig5 = px.scatter(data_df, x="amount", y="category", size = "amount", color="amount", log_x = True, size_max = 60, title="Bubble Chart of Category vs. Cost")
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

    #SunBurst Chart
    fig6 = px.sunburst(data_df, path=['category', 'amount'], values='amount',
                  color='budget_date', title="Sunburst in Categories")
    graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

    #We will try to make a histogram out of categories
    categories = [
    ["rent", "transportation"],
    ["food", "utilities"],
    ["healthcare", "savings"],
    ["personal spending", "recreation and Entertainment"],
    ["insurance and investing", "miscellaneous"]
                    ]
    # Create subplots
    fig7 = make_subplots(rows=2, cols=3, subplot_titles=["Rent & Transpo", "Food & Utilities", "Health & Savings", "Personal & Entertainment", "Miscellaneous & Investing"])

    # Loop through categories and add histograms to subplots
    for i, category_pair in enumerate(categories, start=1):
        category_data = data_df[data_df["category"].isin(category_pair)]
        scatter = go.Scatter(x=category_data["amount"], y=category_data["budget_date"],
                        mode='markers', name=f"Category {category_pair}", opacity=0.7)
        print(f"{i}: {category_pair}")
        fig7.add_trace(scatter, row=(i-1)//3 + 1, col=(i-1)%3 + 1)

    # Update layout
    fig7.update_layout(title_text="Scatter Plots On Categories", showlegend=False, yaxis_title="Date")
    graph7JSON = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graph1JSON=graph1JSON, graph2JSON = graph2JSON, graph3JSON = graph3JSON, graph5JSON = graph5JSON,
                           graph6JSON = graph6JSON, graph7JSON = graph7JSON, categories = REQUIRED_CATEGORIES)


#Route for Dashboard of Guest

@dashboard.route('/dashboard_guest', methods=['GET', 'POST'])
def dashboard_guest_func():
    guest_id = session.get('username')
    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        selected_categories = request.form.getlist('categories')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')

        if not selected_categories:
            query = "SELECT category, amount, budget_date FROM budget_guest WHERE (user_id = ?) AND (budget_date BETWEEN ? AND ?)"
            data = db.execute(query, guest_id, start_date, end_date)
        else:
            # Create placeholders for selected_categories
            placeholders = ', '.join(['?' for _ in selected_categories])

            # Constructing the query
            query = f"SELECT category, amount, budget_date FROM budget_guest WHERE (user_id = ?) AND (budget_date BETWEEN ? AND ?) AND category IN ({placeholders})"

            # Creating a list of query parameters
            query_params = [guest_id, start_date, end_date] + selected_categories

            # Executing the query
            data = db.execute(query, *query_params)


    else: #Get request
        # Get the first day of the current month
        now = datetime.now()
        start_date = datetime(now.year, now.month, 1).strftime('%Y-%m-%d')

        # Get the last day of the current month
        # Since I am having trouble when the month is december, let us make conditions
        if now.month == 12:
            #if the current month is Dec, automatically set next month to January of next year
            last_day = datetime(now.year + 1, 1, 1) - timedelta(days = 1)
        else:
            last_day = datetime(now.year, now.month + 1, 1) - timedelta(days = 1)

        end_date = last_day.strftime('%Y-%m-%d')

        query = "SELECT category, amount, budget_date FROM budget_guest WHERE (user_id = ?) AND (budget_date BETWEEN ? AND ?)"
        data = db.execute(query, guest_id, start_date, end_date)

    #Constructing DataFrame

    #Bar Chart
    data_df = pd.DataFrame(data, columns=["category", "amount", "budget_date"])
    fig1 = px.bar(data_df, x="amount", y="category", color="budget_date", title="Categorical Cost")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    #Line Chart
    fig2 = px.pie(data_df, values="amount", names="category", title = "Expenses Percentage")
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)


    #Get all historical data not just filtered ones
    budgets = db.execute(
                "SELECT * FROM budget_guest WHERE user_id = ? ORDER BY budget_date DESC, transaction_date DESC", guest_id)

    return render_template('dashboard_guest.html', graph1JSON=graph1JSON, graph2JSON = graph2JSON, categories = REQUIRED_CATEGORIES, budgets=budgets)
