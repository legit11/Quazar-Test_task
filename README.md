# User Manager FastAPI

User Manager FastAPI is a straightforward user management API developed using FastAPI. It provides fundamental CRUD (Create, Read, Update, Delete) operations for managing users.


## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing with SwaggerUI](#testing-the-api-with-swagger-ui)
- [Running Tests](#running-tests)
- [Project Author](#project-author)


## Features
- CRUD operations for users (Create, Read, Update, Delete).
- Statistics endpoint.
- Function to count the number of users registered in the last 7 days.
- Function to return the top 5 users with the longest names.
- Function to determine the proportion of users with an email address registered under a specific domain.
- Simple and intuitive project structure.


## Project Structure
The project follows this directory structure:
```text
Quazar-Test_task/
├── alembic/
│   ├── versions/
│   ├── README
│   ├── env.py
│   ├── script.py.mako
├── src/
│   ├── dao/
│   ├── users/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
├── tests/
│   ├── integration_tests/
│   │   ├──test_users.py
│   ├── __init__.py
│   ├── conftest.py
├── .env-docker
├── .env_example
├── .gitignore
├── Dockerfile
├── README.md
├── alembic.ini
├── docker-compose.yaml
├── poetry.lock
├── pyproject.toml
```

- **alembic/**: Contains database migration files.
- **src/**: Holds the main application code.
  - **dao/**: Data Access Objects for database interactions.
  - **users/**: Contains user-related logic and configurations.
    - **config.py**: Configuration settings for the application.
    - **database.py**: Database connection and models.
    - **main.py**: Entry point for the application.
- tests/: Contains test files for the application.
    - **integration_tests**/:
      - **Integration tests for the application**.
- **.env_example**: Example environment variable file.
- **.gitignore**: Specifies files and directories to be ignored by version control.
- **Dockerfile**: Instructions for building the Docker image.
- **README.md**: Documentation for the project.
- **alembic.ini**: Alembic configuration file.
- **docker-compose.yaml**: Configuration for Docker Compose.
- **poetry.lock**: Lock file for project dependencies.
- **pyproject.toml**: Project metadata and dependencies.


## Getting Started
### Prerequisites
Before running the application, ensure you have the following prerequisites installed:

- Python 3.11
- FastAPI
- Asyncpg
- Psycopg
- Alembic
- SQLAlchemy
- Uvicorn
- PostgreSQL

### Installation
To set up the project, follow these steps:

1. Install PostgreSQL (version 15 or higher) from [PostgreSQL's official site](https://www.postgresql.org/).
2. Create a PostgreSQL database.
3. Clone the repository:

   ```bash
   git clone https://github.com/legit11/Quazar-Test_task.git
4. Create a virtual environment (recommended):
   
   ```bash
   python -m venv venv  # Windows
   python3 -m venv venv  # Linux, MacOS
5. Use Poetry to install project dependencies:
   
   ```bash
   poetry lock
   poetry install
6. Copy the .env_example file and rename it to .env. Set the parameter values in the file:
   
   ```
   DB_HOST=<db host>
   DB_PORT=<db port>
   DB_USER=<postgres user>
   DB_PASS=<postgres password>
   DB_NAME=<db name>
   MODE="DEV"/"TEST"
   DB_HOST_TEST=<db host>
   DB_PORT_TEST=<db port>
   POSTGRES_DB_TEST=<db name>
   POSTGRES_USER_TEST=<postgres user>
   POSTGRES_PASSWORD_TEST=<postgres password>
   ```
7. Apply migrations:
   ```bash
   alembic upgrade head

### Running Tests with pytest


Make sure you have pytest installed. If you are using Poetry, you can add it as a development dependency:


1. Set in .env MODE=TEST 
2. ```bash
   poetry run pytest -v
   ```
3. After testing change MODE=DEV

## Usage

### Running the Application

1. To run the FastAPI application locally, use the following command:
  ```bash
  uvicorn src.main:app --reload
  ```
2. To run the FastAPI application with Docker, use the following command:
   ```bash
   docker-compose up -d --build


### API Endpoints

The API exposes the following endpoints:

- `GET /api/users/statistics`: [Features](#features) Info edpoint
- `GET /api/users`: Retrieve a list of users with pagination.
- `POST /api/users`: Create a new user.
- `GET /api/users/{user_id}`: Retrieve a specific user.
- `PUT /api/users/{user_id}`: Update a specific user.
- `DELETE /api/users/{user_id}`: Delete a specific user.


## Testing the API with Swagger UI

Fast API comes with Swagger UI. This tool is automatically generated based on your API's route definitions and Pydantic models.

### Accessing Swagger UI

Once the API is running, Swagger UI can be accessed on the following URL:

```bash
http://localhost:8000/docs
```

You can use swagger UI to:

1. **Browse Endpoints**
2. **Send Requests**
3. **View Responses**
4. **Test Validations**

## To Test with SwaggerUI, you can do the following for each endpoint explained above

1. Open your web browser and navigate to the /docs path as mentioned above.

2. Explore the available endpoints and select the one you want to test.

3. Click on the "Try it out" button to open an interactive form where you can input data.

4. Fill in the required parameters and request body (if applicable) according to the API documentation given above.

5. Click the "Execute" button to send the request to the API.

6. The response will be displayed below, showing the status code and response data.

7. You can also view example request and response payloads, which can be helpful for understanding the expected data format.

## Project author


[Kirill](https://github.com/legit11)




   


   
   
