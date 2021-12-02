# Airflow

Use in building pipeline

### Setup

```
pip install -r requirements.txt
```

### Redis Installation

Use this link to install redis [install redis]

### Configuration

1. Open **airflow.cfg** file and change the following
2. `broker_url = redis://localhost:6379/0`
3. `sql_alchemy_conn = put your db url here`
4. `executor = CeleryExecutor`

- Change these path to point to yours
- `plugins_folder`
- `base_log_folder`
- `dags_folder`

### Database Migration

1. Copy all details from **"alembic.example.ini"** to a new file called **"alembic.ini"**
   ```
   cp -b alembic.example.ini alembic.ini
   ```
2. Edit **"line 43"** from **"alembic.ini"** file with _key=sqlalchemy.url_ with your sqlalchemy database url details
   for the project.

- Create a revision file

> The command below creates a migration file with an empty message.

```
$ alembic revision --autogenerate
```

- Write changes to database

> Here we are going to perform the updates in our database.

```
$ alembic upgrade head
```

### Start Server

1. Export **AIRFLOW_HOME** to point to your root dir of source code
2. Init airflow configuration in db

   ```
   airflow db init
   ```

3. Create a new airflow user

   ```
   airflow users create \
       --username admin \
       --firstname Fedjio \
       --lastname Raymond \
       --role Admin \
       --email fedjioraymond@gmail.com
   ```

   Start webserver on port 8080

   ```
   airflow webserver --port 8080
   ```

4. Start scheduler

   ```
   airflow scheduler
   ```

5. Start Worker

   ```
   airflow celery worker
   ```
