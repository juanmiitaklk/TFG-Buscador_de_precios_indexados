@echo off
cd backend
call venv\Scripts\activate
cd ..
set FLASK_APP=backend.app:create_app
set FLASK_ENV=development
flask run
