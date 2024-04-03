Tekken Combo Creator Web App 

This README file provides instructions on setting up and running your Tekken Django application.

# Prerequisites
  Python 3.x (https://www.python.org/downloads/)
  
  pip (usually comes bundled with Python)
  
# Installation

## Create a virtual environment (recommended):

  A virtual environment helps isolate project dependencies and avoid conflicts with other Python installations on your system. 

## Here's how to create one using venv:

  `python -m venv venv`

## Activate your venv:

  `source venv/bin/activate`  - For Linux/macOS 

  `venv\Scripts\activate.bat` - For Windows


# Install dependencies:

## Activate your virtual environment (if created). Navigate to the root directory of your Tekken Django app and install the required packages listed in requirements.txt:

`pip install -r requirements.txt`

# Navigate to the tekken directory within your project (assuming it's named tekken) and start the Django development server:

`cd tekken`

`python manage.py runserver`

This will typically launch the server at http://127.0.0.1:8000/ in your web browser. You can access your Django app at this URL.

# Usage

  This repo allows users to create a website locally for creating Tekken combo notion images. 

# Contributions

  I welcome contributions to this project!

# License

  This project is licensed under the GNU License

# Acknowledgments

  All image assets are were forked from `LolJohn11`'s github repo: `https://github.com/LolJohn11/NotationImageGenerator/tree/main`
