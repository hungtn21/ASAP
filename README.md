# Techbridge

**Visit our website here:** techbridgeofasap.pythonanywhere.com

Our project helps address communication issues in online interactions between members from different countries within IT projects. By applying AI, the project solves three main problems:

**1. Language Barriers:** Typically, when members with different languages communicate, they need to use a third-party platform for translation. This process is time-consuming as it requires switching back and forth between the chat platform and the translation tool. We have implemented AI to directly translate members' messages, then display them in the language that the user selected when registering their account.

**2. IT Knowledge Disparity:** In a group, especially among students, there is often a disparity in IT skills. Our system automatically detects and explains IT terms that might be difficult. Users can understand the basic meaning of these terms just by hovering over the message.

**3. Lengthy Conversations:** When a conversation becomes long, it takes a lot of time for new members to read everything and grasp the main points of the discussion. We have utilized AI to implement a 'Summary' feature that helps users quickly capture the key points of the conversation."

**Instruction**

Make sure that the Python version you are using is the latest version.

Please install the following frameworks and packages before you test the program:

```
    pip install Django

    pip install PyMySQL

    pip install Jinja2

    pip install google-generativeai
```

We're using MySQL for this web app, you can download this at:

```
    https://dev.mysql.com/downloads/
```

After installing MySQL, please create a database and name it.

Edit the settings.py file to configure your database connection. Replace the DATABASES setting with your MySQL credentials:
```
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
    }
```

Create your 'local_settings.py' in the same folder as 'aifunction.py' and add your API key in it. We are using API of Gemini, you can get a free API key on Gemini website.

After that, apply migrations:
```
python manage.py migrate
```
Run the server:
```
python manage.py runserver
```
Open your browser and go to http://127.0.0.1:8000/ to access the application.

Many thanks to: **Sun Asterisk**, **Hanoi University of Science and Technology (HUST)**, **Shibaura Institute of Technology (SIT)** on supporting us on this project.
