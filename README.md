# Backend Focused

Backend application in Python 3, Flask as web framework, PeeWee as ORM, PostgreSQL as a database containing REST APIs to create, list, read, update, delete data model objects


# Problem Statement

Create a menu planning service which allows to manage weekly menu and associated recipies.

## Context
1. A weekly menu contains a set of recipies. Each week different set of recipies are selected. See example menu for this week.
2. A recipe contains ingredients, step-by-step instructions, nutirtional information, classification, and other metadata. See examples recipes here 1, 2, 3.
3. A customer can review weekly menu as well as recipe by assigning ratings and/or adding comments.


## Run

Activate the virtual environment

```bash
cd venv
#activate the virtual env
./Scripts/activate
```

Install required libraries

```bash
pip install -r requirements.txt
```

To Create DB

```bash
cd model
py create_db
```

Run the application

```bash
flask run
```