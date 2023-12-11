# CRUIZE: Your Budgeting Buddy
<img src="/static/Original.png" width="1000" height="450">

![Static Badge](https://img.shields.io/badge/python-test?style=for-the-badge&logo=python&labelColor=black&color=%23ffd343) ![Static Badge](https://img.shields.io/badge/html-test?style=for-the-badge&logo=HTML5&labelColor=black&color=%23E34F26) ![Static Badge](https://img.shields.io/badge/css-test?style=for-the-badge&logo=CSS3&labelColor=black&color=%231572B6) ![Static Badge](https://img.shields.io/badge/css-test?style=for-the-badge&logo=JavaScript&labelColor=black&color=%23F7DF1E) ![Static Badge](https://img.shields.io/badge/pandas-test?style=for-the-badge&logo=pandas&labelColor=black&color=%23150458) ![Static Badge](https://img.shields.io/badge/plotly-test?style=for-the-badge&logo=Plotly&labelColor=black&color=%233F4F75)

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries such as flask, pandas, plotly and cs50 sqlite

```bash
pip install cs50 flask pandas plot plotly-express
```
## Overview
Cruize: Your Budgeting Buddy is a web application designed to assist users in tracking their financial expenses through engaging visualizations such as charts and dashboards. The application caters to both guest and member users, each offering unique levels of functionality.

### Guest Access
Guests are granted limited access to the platform. Upon selecting 'Continue as a Guest' on the login page, they are directed to a page where they can upload their expense data. This involves providing a username and selecting a CSV file that adheres to predefined columns - date, name, category, and cost. A sample CSV file is available for download through a provided Google Drive link.

https://drive.google.com/file/d/18kanlS7lVHZ6_YIl8j0VaHuoxuw5vJOx/view

Expense categories include rent, transportation, food, utilities, healthcare, savings, personal spending, recreation and entertainment, insurance and investing, and miscellaneous. It is crucial for guests to choose from these categories to ensure a smooth upload process. Following a successful upload, a dashboard is generated, presenting the user's expenses in a tabular format. Exiting the guest page results in the deletion of all guest data, including any generated dashboards.

| Login | Adopt |
| :---: | :---: |
| <img src="Screenshots/img1.png" width="400">  | <img src="Screenshots/img3adopt.png" width="400">|

#### Description:
Background:
Cruize: Your Budgeting Buddy is a website that allows users to track their financial expenses through colorful visualizations such as charts and dashboards. Like in some modern website, a user has a choice to be a member(paid susbscription) or be a guest(trial subscription).

Being a guest has limited access to the website. Upon clicking the 'Continue as a Guest' in login page, he will be redirected to a site that lets him upload his data via entering a username(just any name you would like, e.g. user2561) and a textbox that browse through his desktop that searches for a csv file. Note that this csv file is pre-defined and downloadale via a google drive link.

In order to process, here are the columns included - date (follows format of dd/mm/yyyy), name (basically just a label for your expenses), category(rent, transportation, food, utilities, healthcare, savings, personal spending, recreation and entertainment, insurance and investing, miscellaneous), and cost (numerical/decimal value of your expense). Note that the choices for categories (as well as the additonal rules) must be followed to avoid errors. For categories, guests just need to make a decision to which category they seem their expenses to fit in.

After uploading successfully, guest will be presented with a dashboard that shows his/her expenses and a table. Upon exiting the guest page, all of the guest's data will be deleted, including the dashboards generated.

For the member, it has two ways of uploading the data, it can be either done manually (one expense at a time), or through the same template that the guest followed. Given that member follows the rule mentioned above, but his/her  will always be saved unless the member has an option to choose to delete certain record(s). The member's table of expenses can also be sorted via a column. A member also has a separate page just for all the dashboards and charts.

Dashboard Filters - both guest and member have a filter on date range(start date and end date) as well as the categories. By not choosing any categories will set to default(that's right, all categories) or if by preference you can just choose categories that you want to focus on(personal spending and savings, etc.).

Logo is a paid design from WiX Logo

Source Files:
app.py >> contains all routes such as login, password reset, logout, registration, dashboard, guest_exit
dashboard.py >> contains all the logic for dashboard implementation
flatfile.py >> contans all the logic for processing of the template file(csv file)
helpers.py >> derived from CS50 week 9, used the functions for login_required and apology
budget.db >> database for the impelementation of Cruize (includes all data for guest and members)
template folder >> location of all the layout file and html files
static folder >> contains all the css, images, and js files used

Technology Stack:
Frontend- JavaScript, HTML, CSS, Bootstrap
Backend - Flask
Libraries - Python's Pandas, Plotly Express
Database - CS50's sqlite DB

