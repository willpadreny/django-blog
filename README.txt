# Django Blog Project

A simple blog application built with Django featuring user authentication and blog post management.

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

## Setup Instructions

### 1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

### 2. Create Virtual Environment in VSCODE
Open the project folder in VS Code:
code .

Create a virtual environment using one of these methods:

Method 1 - Using Command Palette:
1. Open the Command Palette (Ctrl+Shift+P on Windows/Linux, Cmd+Shift+P on macOS)
2. Type "Python: Create Environment"
3. Select "Venv"
4. Select your Python interpreter (Python 3.8 or higher)
5. VS Code will create the virtual environment and activate it

Method 2 - Using Terminal:
Open a terminal in VS Code (Ctrl+` or Terminal > New Terminal) and run:

On Windows:
py -3 -m venv .venv

On macOS/Linux:
python3 -m venv .venv

### 3. Activate Virtual Environment

VS Code should automatically activate the virtual environment when you open a new terminal.

If not activated automatically:

On Windows:
.venv\Scripts\activate

On macOS/Linux:
source .venv/bin/activate

You'll know it's activated when you see (.venv) at the beginning of your terminal prompt.

### 4. Install Django
With the virtual environment activated, install Django:

pip install django

You can verify the installation:
python -m django --version

(If you have a requirements.txt file, use: pip install -r requirements.txt)

### 5. Configure Settings
- Open settings.py in the project folder
- Update TIME_ZONE to your timezone (e.g., 'Australia/Sydney')
- Update SECRET_KEY if deploying to production
- Configure database settings if not using SQLite

### 6. Run Migrations
python manage.py makemigrations
python manage.py migrate

This creates all necessary database tables including user authentication tables.