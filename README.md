# Agriculture Processing Management

Agriculture Processing Management is a Django application designed to manage agricultural activities, schedules, and farmers' equipment.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication (farmers, village admins, system admins)
- Creation and management of crops, equipment, materials, and activity categories
- Generation and update of agricultural activity schedules
- Visualization of planned activities in a Gantt chart
- Option to add optional activities to schedules
- Automatic calculation of estimated harvest dates and quantities

## Prerequisites

- Python 3.x
- Django 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

1. Access the application via a browser at `http://127.0.0.1:8000/`.
2. Log in with your superuser credentials.
3. Use the admin interface to add crops, equipment, materials, and activity categories.
4. Log in as a farmer to create and manage agricultural activity schedules.
5. View planned activities and schedules through the user interface.
