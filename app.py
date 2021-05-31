# Imports for flask and sql
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# Imports for plots
import plotly.express as px
import pandas as pd
import numpy as np
import json
import plotly

# Other imports
from datetime import datetime, date
import re

# Create flask app object and hooking up database
app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

# This class is responsible for a table 'ledger' in database
# In this table are stored information about user operations 
class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    amount = db.Column(db.Float(precision=2))  # The amount of the operation
    date = db.Column(db.Date)  # The date of the operation
    description = db.Column(db.String(200))  # The description of the operation
    category = db.Column(db.String(50))  # The category of the operation - 'Deposit' for each deposit, and custom for others

def get_current_date():
    """
    Function return current date as datetime.
    :return: datetime in format YYYY-MM-DD
    """
    today = date.today()
    today = today.strftime("%Y-%m-%d")
    return today

def get_balance():
    """
    Function return current user balance.
    :return: string looks like float with two decimal places
    """
    if len(Ledger.query.all()) == 0:
        # This part is responsible for return 0 with two decimal places
        return '0.00'
    else:
        # Statement below:
        # - get column amount from ledger
        # - sums this column 
        # - return only number(without parentheses)
        # - return number rounded to two decimal places
        return "{:.2f}".format(db.session.query(func.sum(Ledger.amount)).all()[0][0])


@app.route('/')
def home():
    # Home view displayed when user enter to the website
    db.create_all()  # Create table in database based on Ledger class 
    return render_template('home.html',  # Render 'home.html' template
                            nav_active='home',  # This param is responsible for activation right overlap in menu 
                            balance=get_balance())  # Menu keeps showing users balance


@app.route('/add_deposit', methods=['GET', 'POST'])
def add_deposit():
    # This page allows add deposit to ledger
    # When method is GET, render template with form
    if request.method == 'GET':
        return render_template('add_deposit.html', # Render template 'add_deposit.html'
                                nav_active='add',  # Highlighted tab in menu
                                balance=get_balance(),  # Menu keeps showing users balance
                                today=get_current_date())  # Current date is set in form in input date
    
    # If method is POST, get values from form and save it in table
    else:
        # Default value of dollars - when user doesn't type value 
        dollars = 0 
        # If value is typed in form, get it and save to 'dollars' var
        if 'ad-amount-dollars' in request.form: 
            dollars = request.form['ad-amount-dollars']
        
        # Defaul value of cents - when user doesn't type value 
        cents = 0
        # If value is typed in form, get it and save to 'cents' var
        if 'ad-amount-cents' in request.form:
            cents = request.form['ad-amount-cents']
            # Check if value from form is not empty
            if cents == '':
                # If value is empty, set value = 0
                cents = 0  
            # If value is <10 we have to save eg. 03 insted of 3
            # So we have to save cents to string with 0 before char
            if int(cents) < 10:
                cents = '0' + str(cents)
        
        # Get date from form and save it as datetime to 'date' var
        if 'ad-date' in request.form:
            date = request.form['ad-date']
            date = datetime.strptime(date, '%Y-%m-%d')

        # Default description - get from form and save to 'desc' var
        desc = ''
        if 'ad-description' in request.form:
            desc = request.form['ad-description']

        # Concat dollars and cents into amount 
        # And change amount to float dtype
        amount = str(dollars) + "." + str(cents)
        amount = float(amount)
        
        # Create object Ledger with data from form
        added_row = Ledger(amount=amount, 
                            description=desc,
                            date=date, 
                            category='Deposit') # This category is default for each deposit
        # Add row above to database
        db.session.add(added_row)
        db.session.commit()

        # Display flash about adding a row 
        flash("Row has been added")

        # Redirect to display ledger
        return redirect(url_for('ledger'))


@app.route('/add_withdrawal', methods=['GET', 'POST'])
def add_withdrawal():
    # This page allows to add withdrawal to ledger
    # When method is GET, render template with form
    if request.method == 'GET':
        return render_template('add_withdrawal.html',  # Render template 'add_withdrawal.html'
                                nav_active='add',  # Highlighted tab in menu
                                balance=get_balance(),  # Menu keeps showing users balance
                                today=get_current_date())  # Current date is set in form in input date
    # If method is POST, get values from form and save it in table
    else:
        # Default value of dollars - when user doesn't type value 
        dollars = 0
        # If value is typed in form, get it and save to 'dollars' var
        if 'aw-amount-dollars' in request.form:
            dollars = request.form['aw-amount-dollars']

        # Defaul value of cents - when user doesn't type value 
        cents = 0
        # If value is typed in form, get it and save to 'cents' var
        if 'aw-amount-cents' in request.form:
            cents = request.form['aw-amount-cents']
            # Check if value from form is not empty
            if cents == '':
                # If value is empty, set value = 0
                cents = 0
            # If value is <10 we have to save eg. 03 insted of 3
            # So we have to save cents to string with 0 before char
            if int(cents) < 10:
                cents = '0' + str(cents)
        
        # Get date from form and save it as datetime to 'date' var
        if 'aw-date' in request.form:
            date = request.form['aw-date']
            date = datetime.strptime(date, '%Y-%m-%d')

        # Default description
        desc = ''
        # If description is in form, get from form and save to 'desc' var
        if 'aw-description' in request.form:
            desc = request.form['aw-description']
        
        # Default category 
        category = 'Unsigned'
        # If category is in form, get from form and save to 'category' var
        if 'aw-category' in request.form:
            category = request.form['aw-category']

        # Concat dollars and cents into amount 
        # And change amount to float dtype
        amount = '-' + str(dollars) + "." + str(cents)
        amount = float(amount)

        # Create object Ledger with data from form
        added_row = Ledger(amount=amount, description=desc, date=date, category=category)

        # Add row above to database
        db.session.add(added_row)
        db.session.commit()

        # Display flash about adding a row 
        flash("Row has been added")

        # Redirect to display ledger
        return redirect(url_for('ledger'))


@app.route('/ledger', methods=['GET', 'POST'])
def ledger():
    # When method GET this page display ledger 
    if request.method == 'GET':
        # Get all rows from table ordered by date and save it to 'full_ledger'
        # In 'ledger.html' is counted post-transactional balance after each of operations ordered by date 
        full_ledger = Ledger.query.order_by(Ledger.date).all()
        
        # Get length ledger - if it is empty, in 'ledger.html' an appropriate text will be displayed
        ledger_len = len(full_ledger)
        return render_template('ledger.html',  # Render template 'ledger.html'
                               nav_active='ledger',  # Highlighted tab in menu
                               full_ledger=full_ledger,  # Full ledger to display
                               ledger_len=ledger_len,  # Ledger len to check if ledger not empty
                               balance=get_balance())  # Menu keeps showing users balance
    
    # When ledger is called with method POST, it will deleted row
    else:
        # Button 'delete' in row in ledger call modal
        # Inside modal there is form with id row to delete
        # Get value(id row) from this form
        if 'id_row_to_del' in request.form:
            id_row_to_del = request.form['id_row_to_del']
        
        # Choose row from database, where id == id from form
        row_to_del = Ledger.query.filter(Ledger.id == id_row_to_del).first()

        # Delete row and save changes in database
        db.session.delete(row_to_del)
        db.session.commit()
        
        # Display flash with information about delete row
        flash('Row has been deleted')

        # Redirect to itselft, but with method GET
        return redirect(url_for('ledger'))


@app.route('/edit_row/<int:id_row_to_edit>', methods=['GET', 'POST'])
def edit_row(id_row_to_edit):
    # This page allows to edit deposit and withdrawal
    if request.method == 'GET':
        # With method GET, get row from table in database, where id == id sent in URL
        # Next - load this row into 'row' variable
        # This row will be used to display values from this row in inputs of form in rendered page
        row = Ledger.query.filter(Ledger.id == id_row_to_edit).first()
        # If amount in row is < 0, render edit withdrawal, else - edit deposit
        if row.amount > 0:
            return render_template('edit_deposit_row.html', # Render template 'edit_deposit_row.html'
                                    nav_active='ledger',  # Highlighted tab in menu
                                    row=row,  # Inputs have values from this row
                                    balance=get_balance())  # Menu keeps showing users balance
        else:
            return render_template('edit_withdrawal_row.html', # Render template 'edit_withdrawal_row.html'
                                    nav_active='ledger',  # Highlighted tab in menu
                                    row=row,  # Inputs have values from this row
                                    balance=get_balance())  # Menu keeps showing users balance

    # With method POST, values are getting from form and save in table in database
    else:
        # Default value of dollars - when user delete previous value and send form with empty field
        dollars = 0
        # If value is typed in form, get it and save to 'dollars' var
        if 'edit-dollars' in request.form:
            dollars = request.form['edit-dollars']

        # Default value of cents 
        cents = 0
        # If value is typed in form, get it and save to 'cents' var
        if 'edit-cents' in request.form:
            cents = request.form['edit-cents']
            # Check if value from form is not empty
            if cents == '':
                # If value is empty, set value = 0
                cents = 0
            # If value is <10 we have to save eg. 03 insted of 3
            # So we have to save cents to string with 0 before char
            if int(cents) < 10:
                cents = '0' + str(cents)

        # Get value from date input
        if 'edit-date' in request.form:
            date = request.form['edit-date']
            date = datetime.strptime(date, '%Y-%m-%d')

        # Default description
        desc = ''
        # If description is in form, get from form and save to 'desc' var
        if 'edit-description' in request.form:
            desc = request.form['edit-description']

        # If 'edit-category' is in form, that means the form is for withdrawal
        # Else - form is about deposit
        if 'edit-category' in request.form:
            # If withdrawal - save category and add '-' before value of amount
            category = request.form['edit-category']
            amount = '-' + str(dollars) + "." + str(cents)
        else:
            # If deposit - save 'Deposit' category and amount without '-'
            category = 'Deposit'
            amount = str(dollars) + "." + str(cents)

        # Change amount into float
        amount = float(amount)

        # When we have information from form, we can change them in database
        # Get value from table in database, where id row == id to edit(from URL)
        row = Ledger.query.filter(Ledger.id == id_row_to_edit).first()
        
        # Save information from form into variables from row 
        row.amount = amount
        row.description = desc
        row.date = date
        row.category = category

        # Save changes in database
        db.session.commit()
        
        # Print information about edition
        flash("Row has been edited")

        # Redirect to ledger
        return redirect(url_for('ledger'))


@app.route('/analysis')
def analysis():
    # This page display analysis and visualisations based on rows from ledger
    # Get full ledger ordered by date
    full_ledger = Ledger.query.order_by(Ledger.date).all()

    # Save ledger into dataframe(to analysis)
    ledger_df = pd.DataFrame({
        # Simply values from these rows
        'date': [x.date for x in full_ledger],
        'amount': [x.amount for x in full_ledger],
        'category': [x.category for x in full_ledger]
    })
    # Add new column into data frame about post transaction balance
    # This column will be visualise
    ledger_df['balance'] = np.cumsum(ledger_df['amount'])

    # First, we get number of rows in dataframe
    # If there is not enough rows, plot not display or display ugly
    # So we will display information insted of plot
    len_line = ledger_df.shape[0]

    # Create line plot for balance
    fig_line = px.line(ledger_df, # Data from main ledger dataframe
                        x='date',  # Date as X axis
                        y='balance')  # Balance as Y axis

    # We introduce some cosmetic changes to plot
    fig_line.update_layout(xaxis_title='Date', # X axis title 
                        yaxis_title='Balance',  # Y axis title
                        title='Balance of your ledger') # Plot title

    # We have to encode plot into json to send it to view
    plot_json_line = json.dumps(fig_line, cls=plotly.utils.PlotlyJSONEncoder)

    # To create pie plot of withdrawals by category we have to rebuild dataframe
    # First - get only rows with category other than deposit
    ledger_df_pie = ledger_df[ledger_df['category'] != 'Deposit']
    # Next step is save amount from withdrawal(default negative values) as absolute values
    ledger_df_pie['amount'] = ledger_df_pie['amount'].abs()

    # As with line plot - we need some rows to display plot
    len_pie = ledger_df_pie.shape[0]

    # Now we can create pie plot
    fig_pie = px.pie(ledger_df_pie, values='amount', names='category', title='Expenses by category')
    # Now we can encode this plot into json
    plot_json_pie = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)

    # When we have everything, we can render template
    return render_template(
        'analysis.html', 
        nav_active='analysis',  # Highlighted tab in menu
        balance=get_balance(),  # Menu keeps showing users balance
        len_line=len_line,  # Length of full ledger(to line plot)
        plot_json_line=plot_json_line,  # Line plot
        len_pie=len_pie,  # Length of dataframe with withdrawals
        plot_json_pie=plot_json_pie,  # Pie plot
    )

@app.route('/about')
def about():
    # This page show information about project
    return render_template('about.html', 
        nav_active='about', # Highlighted tab in menu
        balance=get_balance()) # Menu keeps showing users balance

if __name__ == '__main__':
    app.run()
