# event_parser
Simple prototype event app to listen events from the external parties (via Webhook) and persists them in the DB. 
Also, it allows querying event per `customer_id`. 

It is a FastAPI and uses local filesystem as the database solution given the 2h time constraint of the solution.

# How to run locally
First create a local environment and then start the app

## Create environment

Change directory to your local repository
```shell script
cd <path-to-your-local-repository>
```

Create conda environment
```shell script
conda create --name event_parser_39 python=3.9
```

Activate environment
```shell script
conda activate event_parser_39
```

Install requirements
```shell script
pip install -r requirements.txt
```

Add repository path to PYTHONPATH 
```shell script
export PYTHONPATH=<path-to-your-repo-root>
```

Run unit tests
```shell script
py.test tests
```
## Start the app

```shell script
uvicorn app.main:app
```

# Further Improvement Areas for a productionready solution
- Use proper DB solution like mongoDB, mySQL or any other DB solution depending on the requirements
- Enable authentication for the app
- Decouple event parsing and even loading logic from the app.main.py and move to code to dedicated Python modules
- Containerize the app with Docker so that it is runnable in any environment