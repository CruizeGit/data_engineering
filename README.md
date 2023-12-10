# CRUIZE: Your Budgeting Buddy
#### Video Demo:  <https://youtu.be/EXmf9yZ8Wc8>
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

