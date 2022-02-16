# School Management System

### A Django + Next.js powered School Managament Web Application System equipped with various features!

<br>

> Status: **Paused Development**

> The site isn't 100% ready to be used practically (neither it is recommended to do so) but still works just fine. It is an educational project and is not meant to be used in production (unless you know what you're doing). I have to pause (or maybe stop?) it's development due to examinations, and since it was an assignment, I'll have to submit it now anyways. There are some known (minor) bugs to be fixed later but most of the site is still operable.

<br>
<hr>


## Table of Contents

- [Features](#features)
- [Preview](#preview)
- [Requirements](#requirements)
- [Setup Guide](#setup-guide)
- [How to Setup Credentials](#how-to-setup-credentials)
- [Using pip as the package manager](#using-pip-as-the-package-manager)

<br>
<hr>

## Features

- Secure
- REST API based
- Optimized for performance
- JWT Authentication System with Refresh Tokens
- Light + Dark Mode
- Student, Teacher, Management and Admin Dashboard
- Create Users, Classes, Subjects, Assignments
- Uses (mostly) Material UI
- ... and a lot more!

<br>
<hr>

## Preview

<details>
  <summary>Click to expand</summary>
  <br>

  > There are more images than the ones mentioned here, and even more features than images! These are some of the preview images of how the site looks. Check out more in the [images directory](./images) of the project.

  <br>

  ## Home Page
  <img alt="Home Page (Dark)" src="./images/home-dark.png" />

  <br>

  ## Contact Us
  <img alt="Contact Us (Dark)" src="./images/contact-us-dark.png" />

  <img alt="Contact Us (Light)" src="./images/contact-us-light.png" />

  <br>

  ## Admin Dashboard - Create User
  <img alt="Admin Dashboard - Create User (Dark)" src="./images/admin-create-user-dark.png" />

  <img alt="Admin Dashboard - Create User (Light)" src="./images/admin-create-user-light.png" />

  <br>

  ## Admin Dashboard - Search User
  <img alt="Admin Dashboard - Search User (Dark)" src="./images/admin-search-user-dark.png" />

  <img alt="Admin Dashboard - Search User (Light)" src="./images/admin-search-user-light.png" />

  <br>

  ## Profile Page
  <img alt="Profile Page (Dark)" src="./images/profile-parent-user-dark.png" />

</details>

<br>
<hr>

## Requirements

- Python 3.9 or above
- Node.js 16 or above
- PostgreSQL 13 or above
- Redis 3.0 or above

> The project is originally created on software versions listed above and is not tested on other versions. So there might be chances that the project also works fine with different versions.

<br>
<hr>

## Setup Guide

- Install and setup [Redis](https://redis.io/) and [PostgreSQL](https://www.postgresql.org/).

- The project uses [Poetry](https://python-poetry.org/) as the default package manager, so it is recommended to have poetry installed in your system. In case you prefer to use [Pip](https://pypi.org/project/pip/) instead of poetry, refer to [Using pip as the package manager](#using-pip-as-the-package-manager).

- Git clone the repository and switch the current directory to the project directory
    ```bat
    git clone https://github.com/AkshuAgarwal/SchoolManagementSystem
    cd SchoolManagementSystem
    ```

- Install the required Packages:
    - Python:
        ```bat
        poetry install
        ```

        > **[Windows]**: In case the ValueError occurs while installing the packages, you can try deleting the `AppData\Local\pypoetry\Cache\artifacts` directory and retry installation. More Info <sup>[Github Issue](https://github.com/python-poetry/poetry/issues/4479) / [StackOverflow Answer](https://stackoverflow.com/a/69425375)</sup>

        > Refer to [Using pip as the package manager](#using-pip-as-the-package-manager) to setup using pip instead.

    - Node.js:
        ```bat
        npm install
        ```

- Setup Credentials and Variables:
    - Rename [`.env.example`](./.env.example) to `.env`.

    - Rename [`constants.json.example`](./constants.json.example) to `constants.json`.

    - Fill all the credentials and values accordingly. (Refer to [How to setup Credentials](#how-to-setup-credentials) for detailed guide).

- Setup Database
    - Run the given command to migrate the database to create required tables:
        ```bat
        poetry run python manage.py migrate
        ```

- Create Super User:
    - To use the system, you must create a superuser account using which you can access the site and admin panel.

    - To create one, run:
        ```bat
        poetry run python manage.py createsuperuser
        ```
        or (if using pip):
        ```bat
        # Unix/macOS
        python manage.py createsuperuser

        # Windows
        py manage.py createsuperuser
        ```
        and fill the fields accordingly.

- Start the project:
    - Start Redis Server on the given url listed in `.env`.

    - Make sure the PostgreSQL server is running on the same credentials mentioned in `.env`.

    - Open a terminal and start the Django server:
        ```bat
        poetry run python manage.py runserver
        ```
        or (if using pip):
        ```bat
        # Unix/macOS
        python manage.py runserver

        # Windows
        py manage.py runserver
        ```

    - Open another terminal and start Next App:
        ```bat
        npm run dev
        ```

        To run the server on custom port, add the port number with argument `-p`, like:
        ```bat
        npm run dev -p 8080
        ```

        The default port is `3000`.

    - And your site is ready to go 🚀

> You don't need to take care of creating .venv yourself! Poetry automatically creates a venv in your project directory. If you're using pip instead of poetry, you may need to refer to [Using pip as the package manager](#using-pip-as-the-package-manager) for handling `.venv` creation and usage.

> You don't need to take care of creating any required directories by yourself. Django automatically checks for the required directories and creates them (if missing).

<br>
<hr>

## How to Setup Credentials

- ### .env
    - **PRODUCTION** - Whether to run the server in Production (`true`) or in Development (`false`)

    - **DJANGO_SECRET_KEY** - A Secret key used by Django.

        To generate one, run:
        ```bat
        poetry run python manage.py generatesecretkey
        ```
        or (if using pip):
        ```bat
        # Unix/macOS
        python manage.py generatesecretkey

        # Windows
        py manage.py generatesecretkey
        ```
        and copy-paste the key. You can also create a strong secret key yourself!

        > Note that this key is generated by Django automatically. For production, you should create your own secret key instead of using this command.

    - **DJANGO_PROTOCOL** - Protocol to run the Django Server on (`http`/`https`)

    - **DJANGO_HOSTNAME** - Host Name to run the Django Server on

    - **DJANGO_PORT** - Port to run the Django Server on

    - **[ALLOWED_HOSTS](https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts)** - Django's ALLOWED_HOSTS Setting. For setting multiple values, separate every item by a comma. Example: `".localhost,127.0.0.1,[::1]"`

    - **[CORS_ALLOWED_ORIGINS](https://github.com/adamchainz/django-cors-headers#cors_allowed_origins-sequencestr)** - Django Cors Headers CORS_ALLOWED_ORIGINS setting. For setting multiple values, separate every item by a comma. Example: `"http://127.0.0.1:3000,http://localhost:3000"`

    - **[CSRF_TRUSTED_ORIGINS](https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins)** - Django's CSRF_TRUSTED_ORIGINS setting. For setting multiple values, separate every item by a comma. Example: `"http://127.0.0.1:3000,http://localhost:3000"`

    - **ANALYZE** - **[Development Only]** Enables the `@next/bundle-analyzer` to analyze bundle size. (`true`/`false`)

    - **SITE_URL** - URL of the frontend site

    - **DB_HOST** - Database Host Name

    - **DB_PORT** - Database Port

    - **DB_USER** - Database User

    - **DB_PASS** - Database Password

    - **DB_NAME** - Database Name

    - **REDIS_URL** - URL on which the redis server is running

    - **EMAIL_CONNECTION** - Connection to use when talking to SMTP server. (`tls`/`ssl`). More Info <sup>[tls](https://docs.djangoproject.com/en/4.0/ref/settings/#email-use-tls) / [ssl](https://docs.djangoproject.com/en/4.0/ref/settings/#email-use-ssl)</sup>

    - **[FROM_EMAIL](https://docs.djangoproject.com/en/4.0/ref/settings/#default-from-email)** - Default email address to use for various automated correspondence from the site manager(s).

    - **[EMAIL_HOST](https://docs.djangoproject.com/en/4.0/ref/settings/#email-host)** - Host to use for sending the email

    - **[EMAIL_PORT](https://docs.djangoproject.com/en/4.0/ref/settings/#email-port)** - Port the use for the SMTP server

    - **[EMAIL_HOST_USER](https://docs.djangoproject.com/en/4.0/ref/settings/#email-host-user)** - Username to use for the SMTP server

    - **[EMAIL_HOST_PASSWORD](https://docs.djangoproject.com/en/4.0/ref/settings/#email-host-password)** - Password to use for the SMTP server

    - **[EMAIL_SUBJECT_PREFIX](https://docs.djangoproject.com/en/4.0/ref/settings/#email-subject-prefix)** - Subject-line prefix for email messages sent with `django.core.mail.mail_admins` or `django.core.mail.mail_managers`. You’ll probably want to include the trailing space

- ### constants.json
    - **SCHOOL_NAME** - Name of the School (will be displayed in Frontend)

    - **[TIME_ZONE](https://docs.djangoproject.com/en/4.0/ref/settings/#time-zone)** - Time Zone for Django

    - **[PASSWORD_RESET_TIMEOUT](https://docs.djangoproject.com/en/4.0/ref/settings/#password-reset-timeout)** - No. of seconds the Password Reset Link will be valid for

    - **FOOTER_TEXT** - Text to be displayed in Footer (in frontend)

<br>
<hr>

## Using pip as the package manager

- Pip by default does not create a virtual environment. If you're planning to use pip, you'll have to create it by yourself.

- To create one, run the following command:
    ```bat
    # Unix/macOS
    python -m venv .venv

    # Windoes
    py -m venv .venv
    ```
    This will create a folder named `.venv` in your project root directory.

- Activate the virtual environment using:
    ```bat
    # Unix/macOS
    source ./.venv/bin/activate
    
    # Windows
    .venv\Scripts\activate
    ```
    > To exit the environment, just type `deactivate`.
    
    After successfully installing and activating venv, you can now install the packages.

- The project also comes with `requirements.txt` (and `requirements.dev.txt` for dev dependencies) by which you can install the packages. To install, just run:
    ```bat
    pip install -r requirements.txt
    ```

- You have successfully installed packages using pip.

> Note that to run any command mentioned above with poetry, you must activate the venv first and then directly use `python` or `py` to run scripts.
