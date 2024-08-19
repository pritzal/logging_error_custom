# logging_error_custom
# Exception Logger

`ExceptionLogger` is a Python library created by Aayush Chaudhary, designed to log exceptions into a MySQL database. It provides a robust way to track errors, categorize them, and store them for future analysis. This library ensures that the required tables are automatically created and allows for easy integration with various applications.

## Features

- **Automatic Database Connection:** Connects to a MySQL database using credentials provided via environment variables or passed directly to the `ExceptionLogger` class.
- **Dynamic Table Creation:** Ensures that necessary tables (`ExceptionCategory`, `ApplicationTypeMaster`, `ApplicationMaster`, `ApplicationException`) are created if they don't already exist.
- **Application and Exception Logging:** Logs exceptions, including application details, categories, error messages, and stack traces.
- **Environment Variables:** Supports loading of database credentials from `.env` files using `dotenv`.

## Installation

```bash
pip install mysql-connector-python
pip install python-dotenv

# Usage
1. Setting Up Environment Variables
Create a .env file in your project root with the following content:

dotenv

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_NAME=ApplicationPerfDB

2. Using the ExceptionLogger

from logger import ExceptionLogger

# Initialize the logger
logger = ExceptionLogger()

# Log an exception
logger.log_exception(
    application_name="MyApp",
    application_type="backend",
    category="Runtime Error",
    message="An unexpected error occurred.",
    stack_trace="Traceback (most recent call last): ..."
)

# Always close the logger when done
logger.close()

3. Using ExceptionLogger in a with Context
You can also use the logger in a with context to ensure it closes properly:


from logger import ExceptionLogger

with ExceptionLogger() as logger:
    logger.log_exception(
        application_name="MyApp",
        application_type="backend",
        category="Runtime Error",
        message="An unexpected error occurred.",
        stack_trace="Traceback (most recent call last): ..."
    )

Tables Created by the Library
ExceptionCategory: Stores categories of exceptions.
ApplicationTypeMaster: Stores types of applications (e.g., backend, frontend).
ApplicationMaster: Stores applications with their names, types, and timestamps.
ApplicationException: Stores logged exceptions, linking them to specific applications and categories.

# Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# License

This project is licensed under the MIT License.

### **Notes:**
- Update any placeholders (like `your_db_user`) in the environment variables section with actual values.
- Adjust the text as needed to match the specific features and functionalities of your `ExceptionLogger` library
