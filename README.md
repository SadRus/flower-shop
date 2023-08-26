![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

# FlowerShop
The website enables the operation of an online flower ordering and delivery store. The software code provides the following functionalities:
- Custom bouquet creation
- Ordering pre-made bouquet from the catalog
- Access to the administrative section (creating additional bouquet ingredients, generating links with the ability to track the number of clicks on them)
- Client's data is stored in the database


## Enviroments

- create the file .env and fill in this data:
    - DEBUG -
      One of the main features of debug mode is the display of detailed error pages. If your app raises an exception when DEBUG is True, Django will display a detailed traceback, including a lot of metadata about your environment, such as all the currently defined Django settings (from settings.py)
    - SECRET_KEY -
      Default: '' (Empty string).
      A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
      django-admin startproject automatically adds a randomly-generated SECRET_KEY to each new project.
    - ALLOWED_HOSTS -
      Default: [] (Empty list).
      A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations.


# For developers
## Installation

To get started go to terminal(mac os) or CMD (Windows)
- create virtualenv, [See example](https://python-scripts.com/virtualenv)

```bash
$python virtualenv venv
```

- clone github repository

```bash
$git clone https://github.com/SadRus/flower-shop.git
```

- install packages

```bash
$pip install -r requirements.txt
```

- run site

```bash
$python manage.py runserver
```

## Working with Database

- run the following commands to migrate models into DB:

```bash
$python manage.py migrate 
```

- for Admin access to database create super user

```bash
$python manage.py createsuperuser"
```

- run the local server and pass to `http://127.0.0.1:8000/admin` to login to admin webpage
```bash
python manage.py runserver
```
## Authors


* **Andrey Alekseev** - [Andrey Alekseev](https://github.com/leksuss)
* **SadRus** - [SadRus](https://github.com/SadRus)
* **Rostislav** - [Rostislav](https://github.com/Rostwik)

# License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


<img src="https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg" alt= “” width="102" height="25">