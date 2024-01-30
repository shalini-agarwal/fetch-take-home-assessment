from flask import Flask, request, jsonify
from flask_expects_json import expects_json
import math
import uuid

app = Flask(__name__)

# Used flask-expects-json decorator for validating the POST endpoint request data. It checks whether the request has all the necessary fields along with the data types.
# This decorator didn't have enough documentation to specify the validation process for nested schema format i.e. for items key. Hence, tested the format for items separately.
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

# Used dictionary data structure to store the receipt ID and their points in a key-value format respectively.
receipts = {}

@app.route("/receipts/process", methods=["POST"])
@expects_json(process_schema)
def process_receipt():
    # The variable data contains the receipt information in a dictionary data type.
    data = request.json
    items = data['items']

    # Checked whether the items array has atleast one item and if both the fields "short description" and "price" is present.
    if len(items) == 0:
        return 'items is required', 400
    for item in items:
        if not 'shortDescription' in item or not 'price' in item:
            return 'item is incorrect', 400

    # Used the uuid4() function to generate random UUID using UUID module from Python as receipt ID.
    receipt_id = str(uuid.uuid4())
    # Calculated the points againts the receipt provided in calculate_points() function and stored the calculated points against the generated UUID. 
    receipts[receipt_id] = calculate_points(data)

    return receipt_id, 200

@app.route("/receipts/<id>/points", methods=["GET"])
def get_points(id):
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
    # Extracting the last two digits from the total value and checking if the value doesn't contain any cents.
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
    points += (number_of_items // 2) * 5

    for item in items:
        short_desc, price = item['shortDescription'], float(item['price'])
        if len(short_desc.strip()) % 3 == 0:
            points += math.ceil(price * 0.2)

    return points

def purchase_date_points(purchase_date):
    points = 0
    # Extracting the one's digit from the date value to check whether the date is an odd or even number
    date_ones_digit = purchase_date[-1]
    if (int(date_ones_digit) % 2 == 1):
        points += 6

    return points

def purchase_time_points(purchase_time):
    points = 0
    purchase_hour, purchase_minute = purchase_time[0:2], purchase_time[3:5]
    # Checking if the purchase hour falls between 14:00+ and 16:00- i.e. any time between this period will have 14:00+ hour and 15 hour. 16:00 time will be 4 pm which is invalid. 
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

    # Calculating the points for each of the different rules using separate functions
    points += retailer_name_points(retailer)
    points += value_points(total)
    points += items_points(items)
    points += purchase_date_points(purchase_date)
    points += purchase_time_points(purchase_time)

    return points

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5001)