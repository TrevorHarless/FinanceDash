from application import app
from flask import flash, redirect, render_template, request, json, Response, session, url_for
from application.forms import LoginForm, RegisterForm
import pymysql
import yfinance as yf


connection = pymysql.Connection(host='localhost', port=3306, database='financeUsers', user='root', password='Soccertrev10.!')

cursor = connection.cursor()

default_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NFLX", "NVDA", "INTC", "AMD"]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        # Insert the user into the database
        cursor.execute(
            'INSERT INTO financeLogin (email, password, first_name, last_name) VALUES (%s, %s, %s, %s)',
            (email, password, first_name, last_name)
        )
        connection.commit()
        
        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for('login'))
    return render_template("register.html", form=form, title="Register", register=True)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        cursor.execute('SELECT * FROM financeLogin WHERE email=%s AND password=%s', (email, password))
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            flash("You are successfully logged in!", "success")
            return redirect(url_for('index'))
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash("You are successfully logged out!", "success")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/budget")
def budget():
    return render_template("budget.html")

@app.route("/stocks", methods=["GET", "POST"])
def stocks():
    if request.method == "POST":
        # Handle search request
        stock_symbol = request.form.get("stock_symbol")
        if stock_symbol:
            # Fetch data for the searched stock
            stock_data = yf.Ticker(stock_symbol)
            if stock_data:
                return render_template("stocks.html", default_stocks=default_stocks, searched_stock=stock_data)
            else:
                # Handle invalid stock symbol
                error_message = "Invalid stock symbol"
                return render_template("stocks.html", default_stocks=default_stocks, error_message=error_message)
    else:
        # Display default list of stocks
        default_stock_data = [yf.Ticker(symbol) for symbol in default_stocks]
        return render_template("stocks.html", default_stocks=default_stock_data)
    
    #return render_template("stocks.html", stock_data=stock_data)


# @app.route("/enrollment", methods=["GET","POST"])
# def enrollment():
#     id = request.form.get('courseID')
#     title = request.form['title']
#     term = request.form.get('term')
#     return render_template("enrollment.html", enrollment=True, data={"id":id,"title":title,"term":term})    

# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     if(idx == None):
#         jdata = courseData
#     else:
#         jdata = courseData[int(idx)]
    
#     return Response(json.dumps(jdata), mimetype="application/json")