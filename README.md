# SQL Query Generator with Gemini

This Python application connects to a MySQL database and uses the Gemini Pro model to generate SQL queries based on user prompts.

## Prerequisites

- Python 3.x
- MySQL Server
- Google Gemini API key

## Setup

1. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Create a `.env` file in the same directory as `app.py`.
   - Add your Gemini API key to the `.env` file:
     ```
     GEMINI_API_KEY=YOUR_GEMINI_API_KEY
     ```
     Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key.

3. **Database Setup:**
   - Ensure you have a MySQL database running.
   - The application will prompt you for database connection details (host, user, password, database name) when you run it.

## Running the application

1.  **Start the database (optional)**: If you want to use a local test database, ensure Docker Compose is running:
    ```bash
    docker-compose up -d
    ```
    Then you can connect to the database using the default credentials (host: `localhost`, user: `root`, password: `root`, database: `mydb`).

2. Run the `app.py` script:
   ```bash
   python app.py
   ```

3. **Database Connection:**
   - The application will prompt you to enter MySQL connection details:
     - MySQL Host (default: localhost)
     - MySQL User (default: root)
     - MySQL Password (default: root)
     - MySQL Database Name (default: mydb)
   - You can press Enter to accept the default values if they are applicable to your setup.

4. **Ask questions:**
   - Once connected, you can ask questions about your database in natural language.
   - The application will generate an SQL query based on your question and the database schema.
   - You will be prompted to run the generated query. Press Enter or type `yes` to run the query (yes is the default). Type `no` to skip query execution.
   - The query results will be displayed.
   - Type `exit` to quit the application.

## Example

```
Ask me anything about the database (or type 'exit' to quit): What are the names of all tables?

Generated SQL Query:
-- Show all tables in the database
SHOW TABLES;

Run this query? ([yes]/no): 
Query Results:
['customers', 'employees', 'orders']
('customers',)
('employees',)
('orders',)
Ask me anything about the database (or type 'exit' to quit): exit
Connection closed.

1. Run the `app.py` script:
   ```bash
   python app.py
   ```

2. **Database Connection:**
   - The application will prompt you to enter MySQL connection details:
     - MySQL Host (default: localhost)
     - MySQL User (default: root)
     - MySQL Password (default: root)
     - MySQL Database Name (default: mydb)
   - You can press Enter to accept the default values if they are applicable to your setup.

3. **Ask questions:**
   - Once connected, you can ask questions about your database in natural language.
   - The application will generate an SQL query based on your question and the database schema.
   - You will be prompted to run the generated query. Press Enter or type `yes` to run the query (yes is the default). Type `no` to skip query execution.
   - The query results will be displayed.
   - Type `exit` to quit the application.

## Example

```
Ask me anything about the database (or type 'exit' to quit): What are the names of all tables?

Generated SQL Query:
-- Show all tables in the database
SHOW TABLES;

Run this query? ([yes]/no): 
Query Results:
['customers', 'employees', 'orders']
('customers',)
('employees',)
('orders',)
Ask me anything about the database (or type 'exit' to quit): exit
Connection closed.

For local testing, you can use Docker Compose to create a MySQL database instance. This is helpful if you want to quickly test the application without setting up a MySQL server manually.

1. **Ensure Docker Compose is installed:**
   - Follow the instructions on the [Docker website](https://docs.docker.com/compose/install/) to install Docker Compose if you haven't already.

2. **Start the database:**
   - Docker Compose can be used to easily set up a local MySQL instance for testing purposes.
   - Run the following command in the project directory:
     ```bash
     docker-compose up -d
     ```
   - This command will start a MySQL database instance in the background using the configuration defined in `docker-compose.yml`.
   - Docker must be installed to use docker compose.

3. **Connect to the database:**
   - Once the database is started, you can connect to it using the following default credentials:
     - Host: `localhost`
     - User: `root`
     - Password: `root`
     - Database Name: `mydb`
   - These credentials are pre-configured in both the `.env.example` and `docker-compose.yml` files for ease of use.

4. **Stop the database:**
   - When you are finished testing, you can stop the database by running:
     ```bash
     docker-compose down
     ```

##

For local testing, you can use Docker Compose to create a MySQL database instance.

1. **Ensure Docker Compose is installed:**
   - Follow the instructions on the [Docker website](https://docs.docker.com/compose/install/) to install Docker Compose if you haven't already.

2. **Start the database:**
   - Docker Compose can be used to easily set up a local MySQL instance for testing purposes.
   - Run the following command in the project directory:
     ```bash
     docker-compose up -d
     ```
   - This command will start a MySQL database instance in the background using the configuration defined in `docker-compose.yml`.
   - Docker must be installed to use docker compose.

3. **Connect to the database:**
   - Once the database is started, you can connect to it using the following default credentials:
     - Host: `localhost`
     - User: `root`
     - Password: `root`
     - Database Name: `mydb`
   - These credentials are pre-configured in both the `.env.example` and `docker-compose.yml` files for ease of use.

4. **Stop the database:**
   - When you are finished testing, you can stop the database by running:
     ```bash
     docker-compose down
     ```

## Running the application

1. Run the `app.py` script:
   ```bash
   python app.py
   ```

2. **Database Connection:**
   - The application will prompt you to enter MySQL connection details:
     - MySQL Host (default: localhost)
     - MySQL User (default: root)
     - MySQL Password (default: root)
     - MySQL Database Name (default: mydb)
   - You can press Enter to accept the default values if they are applicable to your setup.

3. **Ask questions:**
   - Once connected, you can ask questions about your database in natural language.
   - The application will generate an SQL query based on your question and the database schema.
   - You will be prompted to run the generated query. Press Enter or type `yes` to run the query (yes is the default). Type `no` to skip query execution.
   - The query results will be displayed.
   - Type `exit` to quit the application.

## Example

```
Ask me anything about the database (or type 'exit' to quit): What are the names of all tables?

Generated SQL Query:
-- Show all tables in the database
SHOW TABLES;

Run this query? ([yes]/no): 
Query Results:
['customers', 'employees', 'orders']
('customers',)
('employees',)
('orders',)
Ask me anything about the database (or type 'exit' to quit): exit
