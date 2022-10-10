from datetime import date, datetime
import sqlite3

class ProgramaPrincipal:

    # Creacion del manu principal
    def menu(self) -> None:
        opcion: int = 99
        while opcion != 0:
            print("\n--------------------------------------------------------------------------")
            print("\tMENU DE OPCIONES")
            print("1 - Cargar monopatienes")
            print("2 - Modificar datos de un monopatin")
            print("3 - Borrar un monopatin")
            print("4 - Cargar disponibilidad")
            print("5 - Listado de productos")
            print("6 - Tabla")
            print("7 - Tabla de historico/precios")
            print("8 - Registros anteriores a una fecha en específico de la tabla monopatin")
            print("9 - CREAR TABLA MONOPATINES")
            print("10 - BORRAR TABLA MONOPATINES")
            print("0 - Salir")
            opcion = int(input("Ingrese el numero correspondiente a la seccion: "))
            print("--------------------------------------------------------------------------")
            if opcion >=0 and opcion <= 10:
                if opcion == 0:
                    break
                elif opcion == 1:
                    print("\n\tCARGA DE MONOPATINES")
                    marca = str(input("Ingrese la marca del monopatin: "))
                    precio = float(input("Ingrese el precio del monopatin: "))
                    stock = int(input("Ingrese la cantidad disponible: "))
                    nuevo_monopatin = Monopatin(marca, precio, stock)
                    nuevo_monopatin.cargar_monopatin()
                elif opcion == 2:
                    print("\n\tMODIFCAR EL PRECIO DE UN MONOPATIN")
                    nuevo_id = int(input("Ingrese ID del monopatin que desea modificar: "))
                    nuevo_precio = float(input("Ingrese el nuevo precio del monopatin: "))
                    Monopatin.modificar_precio(self, nuevo_id, nuevo_precio)
                elif opcion == 3:
                    print("\n\tELIMINAR MONOPATIN")
                    borrar_id = int(input("Ingrese ID del monopatin que desea eliminar: "))
                    Monopatin.eliminar_monopatin(self, borrar_id) 
                elif opcion == 4:
                    # ! REVISAR ENUNCIADO, PIDE QUE AUMENTE DE A UNO ME PARECE 
                    print("\n\tMODIFICAR DISPONIBILIDAD")
                    nuevo_id = int(input("Ingrese ID del monopatin que desea modificar la disponibilidad: "))
                    Monopatin.cargar_disponibilidad(self, nuevo_id)
                elif opcion == 5:
                    print("\n\tLISTADO DE MONOPATINES")
                    Monopatin.obtener_monopatines(self, "SELECT * FROM BdMonopatines")
                elif opcion == 6:
                    # ? PREGUNTAR Y REVISAR
                    borrar_sql = "DROP TABLE IF EXISTS Monopatin"
                    sql = "CREATE TABLE Monopatin (id_mono INTEGER PRIMARY KEY , modelo VARCHAR(30), marca  VARCHAR(30), potencia VARCHAR(30), precio INTEGER, color VARCHAR(30), fechaUltimoPrecio DATATIME)"
                    self.crearTablas(borrar_sql, sql)
                elif opcion == 7:
                    aumento: float = 0.23
                    # llamar a crear tabla y crear la nueva
                    """Por el aumento del dólar se decidió actualizar los precios de todos los monopatines en un 23%. 
                    Se desea mantener el historial de registros de precios actuales. 
                    Insertar los registros viejos en una tabla llamada “historicoprecios” y 
                    actualizar el precio y fecha en la tabla monopatin. 
                    Para este punto se debe de crear la tabla historico_mono que tendrá exactamente las mismas 
                    características que la tabla monopatin. Previo a actualizar los precios en la tabla monopatin, 
                    se deberá de insertar los datos actuales en la tabla historico_mono"""
                    # ! HACER
                    tabla_historico_precios()
                elif opcion == 8:
                    # ! CAMBIAR EL SELEC POR EL QUE FILTRA POR FECHA
                    # ? VER COMO HACER PARA QUE MUSTRE HASTA TAL FECHA
                    print("\n\tREGISTROS ANTERIORES")
                    fecha_ingresada = str(input("Ingrese la fecha hasta donde desee ver los registros: "))
                    Monopatin.obtener_monopatines(self, "SELECT * FROM Monopatin where fechaUltimoPrecio BETWEEN '0000-00-00' AND {} ".format(fecha_ingresada))
                elif opcion == 9:
                    # Apartado para crear la tabla donde vamos a guardar los datos de los monopatines creados
                    borrar_sql = "DROP TABLE IF EXISTS BdMonopatines"
                    sql = "CREATE TABLE BdMonopatines (_id INTEGER PRIMARY KEY , marca  VARCHAR(30), precio FLOAT NOT NULL, stock INTEGER NOT NULL,UNIQUE(marca))"
                    self.crearTablas(borrar_sql, sql)
                elif opcion == 10:
                    # Apartado para borrar las tablas de nuestra base de datos
                    self.borrar_tablas()
            else:
                print("Opcion incorrecta - Reingresar")

    # Funcion para crear tablas en nuestra base de datos SQLite
    def crearTablas(self, borrar_sql, sql) -> None:
        conexion = Conexiones() 
        conexion.abrirConexion() 
        try:
            conexion.miCursor.execute(borrar_sql)
            conexion.miCursor.execute(sql)    
            # para probar si la tabla Monopatin se estaba cargando
            #conexion.miCursor.execute("INSERT INTO Monopatin(id_mono,modelo,marca,potencia,precio,color,fechaUltimoPrecio) VALUES(1,'modelo','marca','fuerte',100,'rojo','2019-10-10')")
            conexion.miConexion.commit()
            print("Tabla creada correctamente")
        except:
            print("Error al crear tabla")
        finally:             
            conexion.cerrarConexion() 

    # Funcion para borrar tablas en nuestra base de datos SQLite
    def borrar_tablas(self) -> None:
        conexion = Conexiones() 
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("DROP TABLE IF EXISTS BdMonopatines")
            conexion.miCursor.execute("DROP TABLE IF EXISTS Monopatin")
            conexion.miConexion.commit()   
            print("Tabla monopatines eliminada correctamente")
        except:
            print("Error al eliminar tabla monopatines") 
        finally: 
            conexion.cerrarConexion() 


class Conexiones:

    # Metodo para abrir la conexion con nuestra base de datos
    def abrirConexion(self) -> None:
        self.miConexion = sqlite3.connect("BdMonopatines")
        self.miCursor = self.miConexion.cursor()
        
    # Metodo para cerrar la conexion con nuestra base de datos
    def cerrarConexion(self) -> None:
        self.miConexion.close() 


class Monopatin():

    # Variable de clase para llevar un ID de cada monopatin creado
    _id: int = 0

    # Metodo constructor que inicializa las propiedades del monopatin
    def __init__(self, marca: str, precio: float, stock: int) -> None:
        self.marca = marca
        self.precio = precio
        self.stock = stock
        self._id = self._get_next_id()

    # Metodo de clase creado para llevar un ID incremental para cada monopatin creado
    @classmethod
    def _get_next_id(cls) -> int:
        cls._id += 1
        return cls._id

    # Metodo para cargar monopatines en la tabla de la base de datos
    def cargar_monopatin(self) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("INSERT INTO BdMonopatines(marca,precio,stock) VALUES('{}', '{}','{}')".format(self.marca, self.precio, self.stock))
            conexion.miConexion.commit()
            print("Monopatin cargado exitosamente")
        except:
            print("Error al agregar un monopatin")
        finally:
            conexion.cerrarConexion()

    # Metodo para modificar el precio de un monopatin dado su ID
    def modificar_precio(self, nuevo_id, nuevo_precio) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("UPDATE BdMonopatines SET precio='{}' where _id='{}' ".format(nuevo_precio, nuevo_id))
            conexion.miConexion.commit()
            print("Monopatin modificado correctamente")
        except:
            print('Error al actualizar un Monopatin')
        finally:
            conexion.cerrarConexion()

    # Metodo para eliminar monopatines en la tabla de nuestra base de datos
    def eliminar_monopatin(self, borrar_id) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("DELETE FROM BdMonopatines where _id='{}' ".format(borrar_id))
            conexion.miConexion.commit()
            print("Monopatin eliminado correctamente")
        except:
            print("Error al eliminar monopatin")
        finally:
            conexion.cerrarConexion()

    # Metodo para aumentar la disponibilidad de un monopatin dado su ID
    def cargar_disponibilidad(self, nuevo_id) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        nuevo_stock = self.stock + 1
        try:
            conexion.miCursor.execute("UPDATE BdMonopatines SET stock='{}' where _id='{}' ".format(nuevo_stock, nuevo_id))
            conexion.miConexion.commit()
            print("Monopatin modificado correctamente")
        except:
            print('Error al actualizar un Monopatin')
        finally:
            conexion.cerrarConexion()

    # Metodo para obtener y mostrar los datos de la tabla de nuestra base de datos
    def obtener_monopatines(self, sql) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(sql)
            monopatines = conexion.miCursor.fetchall()
            for m in monopatines:
                print(m)
        except:
            print("Error al mostrar la lista de monopatines")
        finally:
            conexion.cerrarConexion()


def tabla_historico_precios():
    print("opcion 7")

def registros_anteriores():
    print("opcion 8")


# Creacion del objeto programa principal
try:
    programa = ProgramaPrincipal()
    programa.menu()
except:
    print("\n\tERROR DE PROGRAMA")
    print("ATENCION")
    print(" - Controlar que la tabla monopatines se encuentre correctamente creada")
finally:
    print("Fin del programa")

"""programa = ProgramaPrincipal()
programa.menu()"""