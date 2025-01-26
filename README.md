# What is GNU-ADMW

GNU-ADMW is an Active Directory Management Web in a GNU GENERAL PUBLIC LICENSE

# Introduction

This project is a Web Interface for Active Directory made using **Django** (https://www.djangoproject.com/) and **ms_active_directory** (https://ms-active-directory.readthedocs.io/) focusing on ease of use and simplicity provide by **Bootstrap** (https://getbootstrap.com/)

It's using the connecting user's credentials to connect to the directory and allow a variety of operations.

The goal is to be able to do most common directory operations directly through this web interface rather than have to rely on command tools or Windows interfaces.

It's compatible with both **Windows Active Directory** and **Samba4** domain controllers.

If you don't know how to install samba4 see https://wiki.tiozaodolinux.com/Guide-for-Linux/Active-Directory-With-Samba-4

# History

This project started in december 2024 with objetive of simplify the management of Users, Groups, Lists, Organizatinal Units

In my job we have the RH area with demands to NOC area create new Users, reset password Users, etc

The main objetive is RH area make yours needs without NOC area dependencies

# Install and run

```sh
# Download clone project
git clone https://github.com/jarbelix/GNU-ADMW.git
cd GNU-ADMW

# Create virtualenvironment
python -m venv .venv
. .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Setup Environment

Copy the env.example file to .env and udpate the settings to match your environment.

```sh
cp env.example .env
```

## Initial testing

### Config .env

```sh
python test-config-env.py
```

### Connection to Active Directory

```sh
python test-active-directory.py
```

#### Output example
```
# Retrieve the configuration parameters:
	AD_DOMAIN=tiozaodolinux.com
	AD_SERVER=ldaps://dc01.tiozaodolinux.com
	AD_ADMIN_USER=Administrator@tiozaodolinux.com
	AD_ADMIN_PASSWORD=XXXXXXXXXXXXXXXXXXXXXXXXXXX
	AD_USER_ATTRS=['cn', 'sn', 'title', 'description', 'physicalDeliveryOfficeName', 'telephoneNumber', 'givenName', 'displayName', 'department', 'company', 'name', 'sAMAccountName', 'userPrincipalName', 'mail', 'loginShell', 'objectGUID', 'objectSid']
	AD_GROUP_ATTRS=['cn', 'sn', 'description', 'name', 'sAMAccountName', 'member', 'objectGUID', 'objectSid']
# Connect with AD_SERVER - ldaps://dc01.tiozaodolinux.com with Administrator@tiozaodolinux.com / XXXXXXXXXXXXXXXXXXXXXXXXX
# Find user by name="tiozao
# Display user info

======================================================================
USER:..... CN=tiozao,CN=Users,DC=tiozaodolinux,DC=com
======================================================================
cn----------------------------  :  tiozao
sn----------------------------  :  do Linux
title-------------------------  :  Título do Cargo
description-------------------  :  ['Descrição Opcional']
physicalDeliveryOfficeName----  :  Endereço Completo
telephoneNumber---------------  :  +55 67 9 81183482
givenName---------------------  :  Tiozão
displayName-------------------  :  Tiozão do Linux
department--------------------  :  Nome do Departamento
company-----------------------  :  Nome da Empresa
name--------------------------  :  tiozao
sAMAccountName----------------  :  tiozao
userPrincipalName-------------  :  tiozao@tiozaodolinux.com
mail--------------------------  :  jarbelix@gmail.com
loginShell--------------------  :  /bin/bash
objectGUID--------------------  :  {ec206896-e6e2-4edc-a4b0-6accc8e3e981}
objectSid---------------------  :  S-1-5-21-253206946-2420641807-3433596073-1124

```

### Start application
```sh

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

```