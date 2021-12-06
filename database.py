import mysql.connector
class Database:
    def __init__(self):
        self.db = None
        self.cursor = None
        try:  # Intenta conectarse a la base de datos
            self.db = mysql.connector.connect ( host="localhost",
                                                user="proyecto", passwd="pass123", database="goodtech" )
            self.cursor = self.db.cursor ()
            print("Conectado exitosamente")
            print ( "GOOD - TECH" )
        except mysql.connector.Error as err:  # Si no puede, avisa
            print("No conectó a la base de datos")
            print(err)
            exit ()  # Termina la aplicación

    def run_select(self, sql):  # Función que corre un select
        # sql se un string con un select en lenguaje sql
        try:
            self.cursor.execute ( sql )  # ejecuta
            result = self.cursor.fetchall ()  # Guarda el resultado en result
        except mysql.connector.Error as err:  # Si no resulta, avisa
            print("No se pueden obtener los datos")
            print(err)
        return result  # Retorna result

    def run_select_filter(self, sql, params):
        try:
            self.cursor.execute ( sql, params )
            result = self.cursor.fetchall ()
        except mysql.connector.Error as err:
            print("No se pueden obtener los datos")
            print(err)
        return result

    def run_sql(self, sql, params):
        try:
            self.cursor.execute ( sql, params )
            self.db.commit ()
        except mysql.connector.Error as err:
            print("No se puede realizar la sql")
            print(err)
