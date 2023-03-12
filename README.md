
# How to use


How to test: 
1.-clone this repository:  [https://github.com/BaniMontoya/email-manager-api]

2.-create venv on root of project 
python -m venv venv
 .\venv\Scripts\activate 
 pip install -r requirements.txt

2.-create database 
python manage.py makemigrations
 python manage.py migrate 

3.-tests
python .\manage.py test
