# I have used python and flask to create the web-server for this task.
from flask import Flask, request, jsonify
'''
Used flask-expects-json package for validating the POST endpoint request data. It checks whether the request has all the necessary fields along with their data types.
This package didn't have enough documentation to specify the validation process for an array with a nested object i.e. for items key. Hence, tested the format for items separately.
There could be additional validations, for example, pattern matching for purchase date and time. But, given the scope and requirements of the challenge and in the interest of time, I have not implemented those currently.
'''
from flask_expects_json import expects_json
import math
# Used Python package uuid to generate unique IDs.
import uuid

app = Flask(__name__)

# Defined the expected schema for validation
process_schema = {
    'type': 'object',
    'properties': {
        'retailer': {'type': 'string'},
        'purchaseDate': {'type': 'string'},
        'purchaseTime': {'type': 'string'},
        'total': {'type': 'string'},
        'items': {'type': 'array'}
    },
    'required': ['retailer', 'purchaseDate', 'purchaseTime', 'total', 'items']
}

# For the in-memory database, used dictionary data structure to store the receipt ID and their points in a key-value format respectively.
receipts = {}

@app.route("/receipts/process", methods=["POST"])
@expects_json(process_schema) # Decorator for flask-expects-json
def process_receipt():
    # Extracted request body and stored it in varible data
    data = request.json
    items = data['items']

    # Custom schema validation - Checked whether the items array has atleast one item and if both the fields - "short description" and "price" - are present.
    if len(items) == 0:
        return 'items is required', 400
    for item in items:
        if not 'shortDescription' in item or not 'price' in item:
            return 'item is incorrect', 400

    # Used the uuid4() function from Python's UUID module to generate random ID. This would be used as receipt ID and would be sent as a response to the request.
    receipt_id = str(uuid.uuid4())
    # Calculated the points againts the receipt provided in calculate_points() function and stored the calculated points against the generated UUID. 
    receipts[receipt_id] = calculate_points(data)

    return receipt_id, 200

@app.route("/receipts/<id>/points", methods=["GET"])
def get_points(id):
    # If requested ID is not present in the database, send a 404 status code
    if not id in receipts:
        return 'No receipt found for that id', 404
    return jsonify({"points": receipts[id]}), 200

def retailer_name_points(retailer):
    points = 0
    # Checking if each of the characters in the retailer name is an alphanumeric character.
    for c in retailer:
        if c.isalnum():
            points += 1

    return points

def value_points(total):
    points = 0
    # Extracting the last two digits from the total value and checking if the number of cents is 0.
    cents = total[-2:]
    if cents == '00':
        points += 50

    # Checking if the total is a multiple of 0.25 is the same as checking if the cents are a multiple of 25.
    if int(cents) % 25 == 0:
        points += 25

    return points

def items_points(items):
    points = 0
    number_of_items = len(items)
    # Checking how many pairs of items we have.
    points += (number_of_items // 2) * 5

    for item in items:
        short_desc, price = item['shortDescription'], float(item['price'])
        # Checking if item description length is a multiple of 3.
        if len(short_desc.strip()) % 3 == 0:
            points += math.ceil(price * 0.2)

    return points

def purchase_date_points(purchase_date):
    points = 0
    # Extracting the one's digit from the date value to check whether the date is an odd or even number.
    date_ones_digit = purchase_date[-1]
    if (int(date_ones_digit) % 2 == 1):
        points += 6

    return points

def purchase_time_points(purchase_time):
    points = 0
    purchase_hour, purchase_minute = purchase_time[0:2], purchase_time[3:5]
    # Checking if the purchase hour falls between 2 pm (14:00) and 4 pm (16:00)(not including these two times).
    # For this, we need to check for two things - purchase time is >= 2:01PM and purchase time is <= 3:59PM.
    if (purchase_hour == '14' and purchase_minute != '00') or purchase_hour == '15':
        points += 10

    return points

# Calls specific function to calculate the points against each of the rules defined based on the keys in the JSON receipt data
def calculate_points(data):
    points = 0

    # Extracting the information for each of the different keys from the data dictionary.
    retailer = data['retailer']
    purchase_date = data['purchaseDate']
    purchase_time = data['purchaseTime']
    total = data['total']
    items = data['items']

    # Calculating the points for each of the different rules using separate functions.
    points += retailer_name_points(retailer)
    points += value_points(total)
    points += items_points(items)
    points += purchase_date_points(purchase_date)
    points += purchase_time_points(purchase_time)

    return points

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5001)