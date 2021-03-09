from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import random, requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)



def facts(year):
    """Generate lucky number, get and return facts for number and year"""

    BASE_URL = 'http://numbersapi.com'
    num = random.randint(1, 100)
    num_fact = requests.get(f'{BASE_URL}/{num}/trivia', params={'number': num})
    year = year
    year_fact = requests.get(f'{BASE_URL}/{year}/year', params={'year': year})

    return {
        'num': {'fact': num_fact.text,
                'num': num},
        'year': {'fact': year_fact.text,
                'year': year}
    }

def get_errors(name, email, year, color):
    """Find and return errors"""

    errors = {}
    if name == '':
        errors['name'] = 'This field is required'
    if email == '':
        errors['email'] = 'This field is required'
    if year < 1900:
        errors['year'] = 'Must be between 1900 and 2000'
    if year > 2000:
        errors['year'] = 'Must be between 1900 and 2000'
    if color not in ['red', 'green', 'orange', 'blue']:
        errors['color'] = 'Must be either red, green, orange, or blue'
    return errors


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

@app.route('/api/get-lucky-num', methods=["POST"])
def get_num():
    """Receive data from javascript, check for errors and call appropriate function"""

    year = request.json['year']
    try:
        year = int(year)
    except:
        year = 1
    name = request.json["name"]
    email = request.json["email"]
    color = request.json["color"]
    if name == '' or email == '' or year < 1900 or year > 2000 or color not in ['red', 'green', 'orange', 'blue']:
        return jsonify(get_errors(name, email, year, color))
    else:
        return jsonify(facts(year))





"""My original code is below.  It's basically the same, except I created a User class.
I eventually took it out because I realized it was unnecessary and just added a lot of 
extra code, but I left it here because I wanted to ask if there's any benefit to doing it
that way."""
# class User:

#     def __init__(self, name, email, year, color):
#         self.name = name
#         self.email = email
#         self.year = year
#         self.color = color

#     def facts(self):
#         BASE_URL = 'http://numbersapi.com'
#         num = random.randint(1, 100)
#         num_fact = requests.get(f'{BASE_URL}/{num}/trivia', params={'number': num})
#         year = self.year
#         year_fact = requests.get(f'{BASE_URL}/{year}/year', params={'year': year})

#         return {
#             'num': {'fact': num_fact.text,
#                     'num': num},
#             'year': {'fact': year_fact.text,
#                     'year': year}
#         }

#     def get_errors(self, user):
#         errors = {}
#         if user.name == '':
#             errors['name'] = 'This field is required'
#         if user.email == '':
#             errors['email'] = 'This field is required'
#         if user.year < 1900:
#             errors['year'] = 'Must be between 1900 and 2000'
#         if user.year > 2000:
#             errors['year'] = 'Must be between 1900 and 2000'
#         if user.color not in ['red', 'green', 'orange', 'blue']:
#             errors['color'] = 'Must be either red, green, orange, or blue'
#         return errors


# @app.route("/")
# def homepage():
#     """Show homepage."""

#     return render_template("index.html")

# @app.route('/api/get-lucky-num', methods=["POST"])
# def get_num():
#     year = request.json['year']
#     try:
#         year = int(year)
#     except:
#         year = 1
#     user = User(
#         name=request.json["name"],
#         email=request.json["email"],
#         year=year,
#         color=request.json["color"]
#     )
#     print(user)
#     if user.name == '' or user.email == '' or user.year < 1900 or user.year > 2000 or user.color not in ['red', 'green', 'orange', 'blue']:
#         return jsonify(user.get_errors(user))
#     else:
#         return(jsonify(user.facts()))