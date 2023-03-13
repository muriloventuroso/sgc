# SGC - Sistema de Gerenciamento Congregacional

O SGC é um sistema desenvolvido para ajudar em processos mecânicos das congregações de Testemunhas de Jeová.

Este projeto é um desenvolvimento pessoal e não tem relação com as entidades jurídicas das Testemunhas de Jeová.

# Requerimentos

- Python 3.8 ou superior
- MongoDB 5 ou superior
- Memcached

# Instalação

- Crie um ambiente virtual utilizando o `virtualenv`
- Instale as bibliotecas do projeto (`pip install -r requirements.txt`)
- Crie as migrações (`python manage.py makemigrations`)
- Rode as migrações (`python manage.py migrate`)
- Crie um superusuário (`python manage.py createsuperuser`)
- Execute a aplicação (`python manage.py runserver`)
