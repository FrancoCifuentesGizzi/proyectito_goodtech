CREAR USUARIO PARA PROGRAMA

CREATE USER 'proyecto'@'localhost' IDENTIFIED BY 'pass123';

grant all privileges on *.* to 'proyecto'@'localhost';

flush privileges;

INICIAR EL PROGRAMA

Python app.py
