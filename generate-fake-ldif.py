# Generate fake entries for Active Directory
# Certify that you have Faker installed before running the script. You can install it using pip install faker.
# Author: Jarbas
# Date: 2023-06-26

import sys
import random

from faker import Faker
from faker.providers import person

# Random
companies = ["Matriz", "Filial 01", "Filial 02" ]
departments = ["NOC", "RH", "TI", "Financeiro", "Marketing"]
employeeTypes = ['Analista','Desenvolvedor','Gestor','Administrador']
titles = ['Sr','Sra']
telephoneNumbers = ['+556711112222','+556733334444','+556755556666']
userAccountControls = ['512','514']
ls = ['Campo Grande','Rio Verde do Mato Grosso','Brasilândia','Corumbá','Ivinhema']
physicalDeliveryOfficeNames = ['Escritório 1', 'Escritório 2', 'Escritório 3', 'Escritório 4']
infos = ['Informação #1', 'Informação #2', 'Informação #3']
descriptions = ['Descrição #1', 'Descrição #2', 'Descrição #3']
companys = ['Company #1', 'Company #2', 'Company #3']

# Some variables
cn=givenName=sn=company=department=description=displayName=sAMAccountName=''
userPrincipalName=mail=employeeNumber=employeeType=info=initials=title=''
telephoneNumber=physicalDeliveryOfficeName=c=l=st=streetAddress=''
userAccountControl=objectCategory=''

# Fixed
objectCategory='CN=Person,CN=Schema,CN=Configuration,DC=seudominio,DC=com,DC=br'
c='BR'
st='MS'
DC='DC=seudominio,DC=com,DC=br'
DOMAIN='seudominio.com.br'

existing_logins = set()

fake = Faker()
fake.add_provider(person)

def generate_cpf():
    def calculate_digit(cpf):
        total = 0
        for i, digit in enumerate(cpf):
            total += int(digit) * (10 - i)
        remainder = total % 11
        return str(11 - remainder) if remainder > 1 else '0'

    cpf = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        cpf.append(calculate_digit(cpf))
    return ''.join(map(str, cpf))


def generate_unique_login(existing_logins):
    givenName = fake.first_name().lower()
    sn = fake.last_name().lower()
    login = f"{givenName}.{sn}"
    while login in existing_logins:
        givenName = fake.first_name().lower()
        sn = fake.last_name().lower()
        login = f"{givenName}.{sn}"
    existing_logins.add(login)
    return [login,givenName,sn]


def generate_name_from_login(login):
    parts = login.split('.')
    capitalized_parts = [part.capitalize() for part in parts]
    return ' '.join(capitalized_parts)

def main(num_rows):
    for i in range(num_rows):
        login,givenName,sn = generate_unique_login(existing_logins)
        name = generate_name_from_login(login)
        employeeNumber = generate_cpf()
        email = f'{login}@{DOMAIN}'
        department = random.choice(departments)
        company = random.choice(companys)
        employeeType = random.choice(employeeTypes)
        title = random.choice(titles)
        telephoneNumber = random.choice(telephoneNumbers)
        userAccountControl = random.choice(userAccountControls)
        physicalDeliveryOfficeName = random.choice(physicalDeliveryOfficeNames)
        info = random.choice(infos)
        description = random.choice(descriptions)
        streetAddress = f"Rua {random.randint(1, 100)}, {random.randint(1, 100)}"
        l = random.choice(ls)

        print(f'''# Employee #{i+1}
dn: CN={login},CN=Users,{DC}
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: {login}
sn: {sn.capitalize()}
initials: {givenName[0].upper()}.{sn[0].upper()}.
description: {description}
givenName: {givenName.capitalize()}
name: {name}
sAMAccountName: {login}
userPrincipalName: {login}@{DOMAIN}
objectCategory: CN=Person,CN=Schema,CN=Configuration,{DC}
mail: {email}
displayName: {givenName.capitalize()} {sn.capitalize()} - {company}/{st}
employeeNumber: {employeeNumber}
employeeType: {employeeType}
l: {l}
st: {st}
c: {c}
telephoneNumber: {telephoneNumber}
title: {title}
info: {info}
streetAddress: {streetAddress}
o: {company}
department: {department}
physicalDeliveryOfficeName: {physicalDeliveryOfficeName}
userAccountControl: {userAccountControl}
accountExpires: 0
''')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <num_rows>")
        sys.exit(1)
    num_rows = int(sys.argv[1])
    main(num_rows)
