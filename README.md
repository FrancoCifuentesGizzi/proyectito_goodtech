**************

CREAR USUARIO PARA PROGRAMA

CREATE USER 'proyecto'@'localhost' IDENTIFIED BY 'pass123';

grant all privileges on goodtech.* to 'proyecto'@'localhost';

flush privileges;

**************

FUNCTIONS para el programa antes de iniciar

CREATE PROCEDURE ProductoIn(cantidad INT, precio INT, current INT) 

BEGIN

update venta set total = total + (cantidad*precio) where ( id_venta = current );

END;

=======================================================================

CREATE PROCEDURE ProductoOut(cantidad INT, precio INT, current INT)

BEGIN

update venta set total = total - (cantidad*precio) where ( id_venta = current );

END;

**************

INICIAR EL PROGRAMA

  Python app.py

**************
