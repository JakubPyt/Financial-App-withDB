# Financial-App-withDB
Financial App created with Flask and PostgreSQL.

## App description for normal people
Are you dreaming of a trip around the world? 
Or maybe a rest under a palm tree with a drink in hand? 
Expensive cars, clothes or a new computer? 
You can achieve all of these if you manage your finances well.
Welcome to the financial application! 
Place to manage your finances!

## App description for geeks
There are two versions of this app. Both look identical(almost) and to build both of this apps I used:
 - HTML
 - CSS
 - Bootstrap
 - JavaScript
 - jQuery
 - Flask
 - Python(Pandas, Numpy, Plotly)

<b>The difference between the versions is back-end.</b>

### First version
First version based on pandas DataFrame, and is used for demonstration without the need to install the Python virtual environment by the viewer. 
You find this version and it code at the link:<br>
https://replit.com/@JakubPyt/Financial-App-demo#main.py <br>
You can run this app by green circle in the center of the screen. It takes some time(sometimes even a few minutes) to wake up app.

### Second version
Second version(which you are currently viewing) is based on SQLAlchemy connected to PostgreSQL database.<br>
This version is like ikea furniture - you have to assemble it yourself by steps:
1. (venv) On your machine create python environment e.g. by line:
<pre><code>python -m venv venv</code></pre>
2. (venv) Run this environment.
3. (venv) Install required modules in Python venv:
<pre><code>pip install flask</code></pre>
<pre><code>pip install Flask-SQLAlchemy</code></pre>
<pre><code>pip install psycopg2</code></pre>
<pre><code>pip install pandas</code></pre>
<pre><code>pip install plotly-express</code></pre>
4. (DB) Create empty database with e.g. pgAdmin and Query Tool:
<pre><code>CREATE DATABASE financial_app</code></pre>
5. Download code of this project.
6. Change 'config.cfg' file(information how you should do it is in this file).
7. Run 'app.py' file with venv.
