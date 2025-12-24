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

### 4. Install Required Packages
With the virtual environment activated, install all required packages:

pip install django
pip install django-simple-captcha
pip install django-otp
pip install qrcode[pil]
pip install python-decouple
python.exe -m pip install --upgrade pip

You can verify the Django installation:
python -m django --version

Package descriptions:
- django: Main web framework
- django-simple-captcha: CAPTCHA support for forms
- django-otp: Two-factor authentication framework
- qrcode[pil]: QR code generation with image support for 2FA setup
- python-decouple: Environment variable management for secure configuration

(If you have a requirements.txt file, use: pip install -r requirements.txt)

### 5. Configure Environment Variables
Copy the example environment file and configure it:

On Windows:
copy .env.example .env

On macOS/Linux:
cp .env.example .env

Then edit the .env file:
- Generate a new SECRET_KEY (see instructions in .env.example)
- Set DEBUG=True for development, False for production
- Configure ALLOWED_HOSTS (localhost,127.0.0.1 for development)
- Set USE_HTTPS=True when deploying with SSL certificate

### 6. Configure Settings (Optional)
- Open settings.py in the project folder
- Update TIME_ZONE to your timezone (e.g., 'Australia/Sydney')
- For production: Configure database settings in .env (PostgreSQL recommended)

### 7. Run Migrations
python manage.py makemigrations
python manage.py migrate

This creates all necessary database tables including user authentication tables.
