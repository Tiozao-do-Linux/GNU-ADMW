# Generate fake entries for Active Directory
# Certify that you have Faker and Unidecode installed before running the script. You can install it using "pip install faker unidecode".
# Author: Jarbas
# Date: 2023-06-26

import sys
import random
from unidecode import unidecode

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
c='BR'
st='MS'
DC='DC=tiozaodolinux,DC=com'
DOMAIN='tiozaodolinux.com'
objectCategory='CN=Person,CN=Schema,CN=Configuration,'+ DC


fake = Faker('pt_BR')
fake.add_provider(person)


existing_logins = set()
def generate_unique_login():
    givenName = fake.first_name()
    sn = fake.last_name()
    first = unidecode(givenName.split(' ')[0].lower())
    len_last=len(sn.split(' '))
    last = unidecode(sn.split(' ')[len_last-1].lower())
    login = f"{first}.{last}"

    while login in existing_logins:
        givenName = fake.first_name()
        sn = fake.last_name()
        first = unidecode(givenName.split(' ')[0].lower())
        len_last=len(sn.split(' '))
        last = unidecode(sn.split(' ')[len_last-1].lower())
        login = f"{first}.{last}"
        
    existing_logins.add(login)
    return [login,givenName,sn]


def main(num_rows):
    for i in range(num_rows):
        login,givenName,sn = generate_unique_login()
        name = f'{givenName} {sn}'
        # employeeNumber = generate_cpf()
        employeeNumber = fake.cpf()
        email = f'{login}@{DOMAIN}'
        department = random.choice(departments)
        company = random.choice(companies)
        employeeType = fake.job()
        title = fake.prefix()
        telephoneNumber = random.choice(telephoneNumbers)
        userAccountControl = random.choice(userAccountControls)
        physicalDeliveryOfficeName = random.choice(physicalDeliveryOfficeNames)
        info = fake.sentence()
        description = fake.job()
        streetAddress = fake.street_address()
        # c = fake.country_code()
        # l = fake.city()
        # st = fake.state()
        l = random.choice(ls)

        print(f'''# Employee #{i+1}
dn: CN={login},CN=Users,{DC}
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
givenName: {givenName}
sn: {sn}
initials: {givenName[0].upper()}.{sn[0].upper()}.
cn: {login}
description: {description}
name: {name}
sAMAccountName: {login}
userPrincipalName: {login}@{DOMAIN}
objectCategory: CN=Person,CN=Schema,CN=Configuration,{DC}
mail: {email}
displayName: {givenName} {sn} - {company}/{st}
employeeNumber: {employeeNumber}
employeeType: {employeeType}
l: {l}
st: {st}
c: {c}
telephoneNumber: {telephoneNumber}
title: {title}
info: {info}
streetAddress: {streetAddress}
company: {company}
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
