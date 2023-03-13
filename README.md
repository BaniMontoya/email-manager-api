
# How to use

How to test: 
1.-Clone this repository:  [https://github.com/BaniMontoya/email-manager-api]

2.-Create venv on root of project 
cd email_manager_api
python -m venv venv
 .\venv\Scripts\activate 
 pip install -r requirements.txt

2.-Create database 
cd email_manager_api
python manage.py makemigrations
python manage.py migrate 

3.-Run tests
python .\manage.py test
