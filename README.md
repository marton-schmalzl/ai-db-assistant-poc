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

## Local Test Database with Docker Compose

For local testing, you can use Docker Compose to create a MySQL database instance.

1. **Ensure Docker Compose is installed:**
   - Follow the instructions on the [Docker website](https://docs.docker.com/compose/install/) to install Docker Compose if you haven't already.

2. **Start the database:**
   - Run the following command in the project directory:
     ```bash
     docker-compose up -d
     ```
   - This command will start a MySQL database instance in the background using the configuration defined in `docker-compose.yml`.

3. **Connect to the database:**
   - You can now connect to the database using the following credentials:
     - Host: `localhost`
     - User: `root`
     - Password: `root`
     - Database Name: `mydb`
   - These are the default values used in the `.env.example` file and the `docker-compose.yml` file.

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
Connection closed.
