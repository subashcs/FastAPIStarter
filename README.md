# Fast API Demo
## Getting Started
1. Create a virtual environment named 'env' in the root directory of the project
```
python3 -m venv env

```

2. Activate virtual environment 
```
source env/bin/activate
```

3. Install the required dependencies from requirement.txt file 
```
pip install -r requirement.txt
```

### Running application in development mode
To run the application in development mode use the following command.
```
uvicorn main:app --reload

```
## Database Setup
To setup a postgres database on your device follow [the official guide](https://www.postgresql.org/download/). Once installed follow the following guide.

1. Open postgresql and create a postgres database and an user and grant all privilege in that DB.
2. Customize .env file information
3. Before proceeding further run the migrations using alembic.
   ```
   alembic upgrade head
   ```
## Alembic Guide
1. To see current head location use
   ```
   alembic current
   ```
2. To downgrade a version use:
   ```
   alembic downgrade head
   ```
3. To upgrade a version use
   ```
   alembic upgrade head
   ```
## Running Unit Tests
To test your changes to ensure that they function as intended. Include appropriate tests if applicable. To run unit tests locally:
1. Install additional dependencies for your test environment listed on `test_requirements.txt` file
```
pip install -r test_requirements.txt
```
2. Activate test environment
```
source ./testenv/bin/activate
```
3. To run the test, run
```
python3 -m pytest
```
Or, Using coverage

```
coverage run -m pytest
```
4. Generate coverage report 
```
coverage report -m
```