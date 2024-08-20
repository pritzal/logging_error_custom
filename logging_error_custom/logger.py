from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from logging_error_custom import ExceptionLogger  # Import from your package
import mysql.connector
import os
from typing import List, Optional

app = FastAPI()

# Define the Pydantic model for incoming log data
class ApplicationException(BaseModel):
    application_name: str
    application_type: str
    category: str
    message: str
    stack_trace: str
    exception_details: str = None
    exp_object: str = None
    exp_process: str = None
    inner_exception: str = None

class ApplicationDetails(BaseModel):
    application_name: str
    application_type: str
    created_date: str
    updated_date: str
    user_id: Optional[int] = None

@app.post("/save-application-exception/")
async def save_application_exception(app_expt: ApplicationException):
    try:
        logger = ExceptionLogger()  # Use the class from your package
        logger.log_exception(
            application_name=app_expt.application_name,
            application_type=app_expt.application_type,
            category=app_expt.category,
            message=app_expt.message,
            stack_trace=app_expt.stack_trace,
            exception_details=app_expt.exception_details,
            exp_object=app_expt.exp_object,
            exp_process=app_expt.exp_process,
            inner_exception=app_expt.inner_exception
        )
        return {"status": "success", "message": "Exception logged successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-application-exceptions/")
async def get_application_exceptions(
    type: str,
    application_id: int
):
    try:
        # Initialize the ExceptionLogger
        logger = ExceptionLogger()

        # Create a database connection
        conn = mysql.connector.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()

        # Fetch exceptions by type and application ID
        query = """
        SELECT * FROM ApplicationException
        WHERE category_id = (
            SELECT id FROM ExceptionCategory WHERE category = %s
        ) AND application_id = %s
        """
        cursor.execute(query, (type, application_id))
        exceptions = cursor.fetchall()

        # Format the results
        result = []
        for exc in exceptions:
            result.append({
                "id": exc[0],
                "exception_details": exc[1],
                "message": exc[2],
                "exp_object": exc[3],
                "exp_process": exc[4],
                "application_id": exc[5],
                "category_id": exc[6],
                "created_datetime": exc[7],
                "inner_exception": exc[8],
                "stack_trace": exc[9]
            })

        # Close the database connection
        cursor.close()
        conn.close()

        return {"status": "success", "data": result}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-application-details/")
async def get_application_details(app_id: int):
    try:
        # Create a database connection
        conn = mysql.connector.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()

        # Fetch application details by ID
        query = """
        SELECT app_name, app_type_id, created_date, updated_date, user_id
        FROM ApplicationMaster
        WHERE id = %s
        """
        cursor.execute(query, (app_id,))
        app_details = cursor.fetchone()

        if app_details is None:
            raise HTTPException(status_code=404, detail="Application not found")

        # Fetch application type description
        cursor.execute("SELECT app_type FROM ApplicationTypeMaster WHERE id = %s", (app_details[1],))
        app_type = cursor.fetchone()
        app_type_description = app_type[0] if app_type else "Unknown"

        # Format the results
        result = {
            "application_name": app_details[0],
            "application_type": app_type_description,
            "created_date": app_details[2],
            "updated_date": app_details[3],
            "user_id": app_details[4]
        }

        # Close the database connection
        cursor.close()
        conn.close()

        return {"status": "success", "data": result}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
