This Flask API is designed to handle articles, providing endpoints for various operations related to article, user and admin management.

## Prerequisites:

1. Install [Python](https://www.python.org/downloads/) (Python version 3.7.1 or higher)

## Setup

1. Clone this repository by running the following command

   ```bash.
   git clone https://github.com/vedhagirisrinivasan/embeddings.git
   ```

2. Install and configure `virtualenv` by running the following command:

   ```bash
   pip install virtualenv
   ```

   - For Linux/Mac:
  
     a) Create a virtual environment:

        ```bash
        python3 -m venv venv
        ```

     b) Activate the environment:

        ```bash
        source venv/bin/activate
        ```

   - For Windows:
  
     a) Create a virtual environment:

        ```bash
        py -m venv venv
        ```

     b) Activate the environment:

        ```bash
        .\env\Scripts\activate
        ```

3. Install the required packages by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file by verifying the .env.example file variables

5. Obtain the openapi key and add it in .env along with db credentials


6. Create a database and install the uuid extension to create unique id's:

   - On Linux/Ubuntu:

     ```bash
     - sudo -u postgres psql -c "CREATE DATABASE <database_name>"
     - CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  --> Extension to install uuid (Do it in Pgadmin4)
     - CREATE EXTENSION vector; --> vector extension
     ```

5.  To run flask application:
    ```bash
        flask run
    ```

The ` directory contains the following folders:

- `auth`: Contains the logic for authenticate the user (ie:login, signup )
- `embed`: It contains logic for embedding and retrieving embeds
- `models`: Contains database schemas (models).

- Finally all the aboue folders have routes and controller files,
    `routes` - It have end points for the api's
    `controller` - It have the logics for the specific api's

## Commands

1. Migrations (To run below commands you need to be in atri-publications-back-end folder):

   - If the migrations folder does not exist in the project, initialize it with the following command:

     ```bash
     flask db init
     ```

   - To create migrations, run the following commands:

     ```bash
     flask db migrate -m "Initial migration."
     ```

   - To apply migrations, run the following command:

     ```bash
     flask db upgrade
     ```

2. To run the server (To run below commands you need to be in atri-publications-back-end folder):

   ```bash
   flask run
   ```

   The Flask server runs on the default port 5000. Access it at [http://127.0.0.1:5000/].

3. To kill port 5000, use the following command:

   ```bash
   sudo fuser -k 5000/tcp
   ```
