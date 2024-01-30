# Fetch Receipt Processor Challenge

# About the project

This is a take home challenge for Fetch where the requirement is to build a webservice containing two API endpoints, POST and GET. 
The POST request accepts a receipt in its payload containing information on the retailer, purchase date, purchase time, items purchased and the total price. Based on the information contained in the receipt data, points are calculated based on a set of defined rules. The receipt ID along with the points allocated to the receipt is stored in memory as there is no requirement for the data to persist when the application stops. The generated receipt ID is sent in response to the POST request. 
The GET request contains the receipt ID as a variable in its URL and it returns the points allocated for that receipt in its response. 

I have used Python and Flask to build the webserver. For ease of running the application, I have used Docker. Also, I have used two Python packages, UUID and flask_expects_json. The need for these has been explained in the comments in main.py. My thought process and any other assumptions made while creating the application have also been mentioned in the comments. 

# Getting Started

## Prerequisites

You need to have Docker installed in your system to run this project. 

## Build

1. Clone the repo.
    `git clone https://github.com/shalini-agarwal/fetch-take-home-assessment.git`
2. Navigate to the folder in your terminal.
    `cd fetch-take-home-assessment`
3. Make sure you have Docker running in your local system.
4. Build the docker container after navigating to the folder.
    `docker compose up --build`
5. You can test the functioning of the APIs by navigating to `localhost:5001\<api-endpoint>` in your system.

# Usage

Once you have started the docker container, you may use Postman to hit the GET and POST endpoints for testing the results. I have included two screenshots from my Postman environment, once each for the POST and GET requests below. 

- POST request
![Screenshot for the POST request with receipt data as payload and generated receipt ID as response](/example-results/POST-request.png)


- GET request
![Screenshot for the GET request with calculated points against the given receipt ID as response](/example-results/GET-request.png)

