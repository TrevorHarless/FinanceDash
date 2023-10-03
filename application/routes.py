from application import app, cache
from flask import flash, redirect, render_template, request, json, Response, session, url_for
from application.forms import LoginForm, RegisterForm
import pymysql
import yfinance as yf


connection = pymysql.Connection(host='localhost', port=3306, database='financeUsers', user='root', password='Soccertrev10.!')

cursor = connection.cursor()

default_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NFLX", "NVDA", "INTC", "AMD"]

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
    searched_stock = False
    if request.method == "POST":
        stock_symbol = request.form.get("stock_symbol")
        searched_stock = True
        if stock_symbol:
            # Fetch data for the searched stock symbol
            data = get_stock_data(stock_symbol)
            if data:
                stock_data = [data]
            else:
                flash("Invalid stock symbol", "danger")
                stock_data = []
        else:
            stock_data = get_default_stock_data()
    else:
        # Display default stocks by default
        stock_data = get_default_stock_data()

    return render_template("stocks.html", stock_data=stock_data, searched_stock=searched_stock)

# Helper function to fetch data for default stocks
def get_default_stock_data():
    stock_data = []

    for symbol in default_stocks:
        data = get_stock_data(symbol)
        if data:
            stock_data.append(data)

    return stock_data

# Helper function for fetching stock data by symbol
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    price_data = stock.history(period='1d')

    if not price_data.empty:
        formatted_price = round(price_data.Close[0], 2)
        stock_name = stock.info.get("longName", "")
        return {"symbol": symbol, "name": stock_name, "price": formatted_price}
    else:
        return None



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