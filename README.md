# JTO

JTO is a social network platform for gym goers, where they can update their training progress, upload images and share posts with friends.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

1- Clone the repo.

2- Install PostgresSQL server or if you have a server runining online, then you need the connection URL.

3- If you are using Visual studio code, then better to create a virtual enviroment as below : 
    A- Create new python enviroment : "python -m venv env" ( for python 3 and above, virtualenv will be installed) (http://flask.pocoo.org/docs/1.0/installation/)
    B- Active the enviroment : go to "env/Scripts/" and run "activate.bat" or when start debugging using Visual Studio code.)

### Installing

1- Activate the virtual enviroment. See above 3-A

2- Install requirements

```
pip install -r requirements.txt
```
3- Prepare the database

    A- Create the database manually in PostgresSQL server
    B- Run the following commands, one by one
        - python manage.py db init
        - python manage.py db migrate
        - python manage.py db upgrade
    C- for an online database (AWS for example), the following command will extract the SQL scripts : 
        - python manage.py db upgrade --sql > migration.sql

4- "Flask run" to start the project. 

5- Click on "Create new account" and enjoy!! ^_^

## Running the tests

No tests yet! 

## Deployment

To deploy to AWS : 

1- eb init

2- eb creat [app-name] ( needed for each branch)

3- eb deploy [jtoname] : example eb deploy jto11 ( should be more than 4)

To terminate and delete all created resources : 
- eb terminate

## Built With

* [Semantic UI](https://semantic-ui.com/) 
* [Flask](https://palletsprojects.com/p/flask/)
* [Python](https://www.python.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [PostgreSQL](https://www.postgresql.org/)

## Contributing

---


## Authors

* **Jalal Khalil (jalalk@uab.edu)**
* **Orhun Vural**
* **Temirlan Ismukhanov**


See also the list of [contributors](https://github.com/jalal1/JTO/project/contributors/project/contributors) who participated in this project.

## License

---

