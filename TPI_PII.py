from datetime import date, datetime
import sqlite3

#¡ATENCION! - En caso de ser el primer uso del programa de debe ingresar al apartado crear una tabla

# Creamos la clase ProgramaPrincipal para crear un objeto programa y comenzar la ejecucion de la aplicacion 
class ProgramaPrincipal:

    # Creacion del manu principal
    def menu(self) -> None:
        opcion: int = 99
        while opcion != 0:
            print("\n--------------------------------------------------------------------------")
            print("\tMENU DE OPCIONES")
            print("¡ATENCION! - En caso de ser el primer uso del programa de debe ingresar al apartado crear una tabla")
            print("8 - Crear tabla principal")
            print("9 - Borrar tablas")
            print("1 - Cargar datos")
            print("2 - Modificar precio de una unidad")
            print("3 - Borrar una unidad")
            print("4 - Aumentar disponibilidad (+1)")
            print("5 - Mostrar listado de productos actuales")
            print("6 - Actualizar a precio dolar - Mostrar registros historicos")
            print("7 - Mostrar registros anteriores a una fecha en específico")
            print("0 - Salir")
            opcion = int(input("Ingrese el numero correspondiente a la opcion: "))
            print("--------------------------------------------------------------------------")
            if opcion >=0 and opcion <= 9:
                if opcion == 0:
                    break

                elif opcion == 1:
                    print("\n\tCARGA DE MONOPATINES")
                    modelo = str(input("Ingrese el modelo del monopatin: "))
                    marca = str(input("Ingrese la marca del monopatin: "))
                    potencia = str(input("Ingrese la potencia del monopatin: "))
                    precio = float(input("Ingrese el precio del monopatin: "))
                    color = str(input("Ingrese el color del monopatin: "))
                    stock = int(input("Ingrese la cantidad disponible: "))
                    fechaUltimoPrecio = date.today()
                    nuevo_monopatin = Monopatin(modelo, marca, potencia, precio, color, stock, fechaUltimoPrecio)
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
                    print("\n\tMODIFICAR DISPONIBILIDAD")
                    nuevo_marca = str(input("Ingrese la marca del monopatin que desea modificar la disponibilidad: "))
                    Monopatin.cargar_disponibilidad(self, nuevo_marca)

                elif opcion == 5:
                    print("\n\tLISTADO DE MONOPATINES")
                    print("ID | MODELO | MARCA | POTENCIA | PRECIO | COLOR | STOCK | FECHA ")
                    sql = "SELECT * FROM Monopatin"
                    Monopatin.obtener_monopatines(self, sql)

                elif opcion == 6:
                    # Variable aumento_dolar para indicar porcentaje de aumento de acuerdo al dolar
                    aumento_dolar: float = 0.23
                    sql = "UPDATE Monopatin SET precio=precio+(precio*'{}') ".format(aumento_dolar)
                    sql2 = "UPDATE Monopatin SET fechaUltimoPrecio='{}' ".format(date.today())
                    Monopatin.actualizar_a_dolar(self, sql, sql2)
                    sql3 = "SELECT * FROM HistoricoMono"
                    print("\n\tTABLA REGISTROS HISTORICOS")
                    print("ID | MODELO | MARCA | POTENCIA | PRECIO | COLOR | STOCK | FECHA ")
                    Monopatin.actualizar_historica(self)
                    Monopatin.obtener_monopatines(self, sql3)

                elif opcion == 7:
                    print("\n\tREGISTROS ANTERIORES")
                    anio = str(input("Ingrese el año: "))
                    mes = str(input("Ingrese el mes: "))
                    dia = str(input("Ingrese el dia: "))
                    fecha_ingresada = date(int(anio), int(mes), int(dia))
                    fecha_cero = date(1000,1,1)
                    print("ID | MODELO | MARCA | POTENCIA | PRECIO | COLOR | STOCK | FECHA ")
                    Monopatin.obtener_monopatines(self, "SELECT * FROM Monopatin where fechaUltimoPrecio BETWEEN '{}' AND '{}' ".format(fecha_cero, fecha_ingresada))
                
                elif opcion == 8:
                    # Apartado para crear la tabla donde vamos a guardar los datos de los monopatines creados
                    borrar_sql = "DROP TABLE IF EXISTS Monopatin"
                    sql = "CREATE TABLE Monopatin (_id INTEGER PRIMARY KEY , modelo VARCHAR(30), marca  VARCHAR(30), potencia VARCHAR(30), precio REAL, color VARCHAR(30), stock INTEGER, fechaUltimoPrecio DATETIME)"
                    borrar_sql2 = "DROP TABLE IF EXISTS HistoricoMono"
                    sql2 = "CREATE TABLE HistoricoMono (_id INTEGER PRIMARY KEY , modelo VARCHAR(30), marca  VARCHAR(30), potencia VARCHAR(30), precio REAL, color VARCHAR(30), stock INTEGER, fechaUltimoPrecio DATETIME)"
                    self.crearTablas(borrar_sql, sql)
                    self.crearTablas(borrar_sql2, sql2)

                elif opcion == 9:
                    # Apartado para borrar las tablas de nuestra base de datos
                    sql = "DROP TABLE IF EXISTS Monopatin"
                    sql2 = "DROP TABLE IF EXISTS HistoricoMono"
                    self.borrar_tablas(sql)
                    self.borrar_tablas(sql2)
            else:
                print("Opcion incorrecta - Reingresar")

    # Funcion para crear tablas en nuestra base de datos SQLite
    # Definimos que la funcion reciba dos parametros (comandos SQL) para poder reutilizar
    def crearTablas(self, borrar_sql, sql) -> None:
        conexion = Conexiones() 
        conexion.abrirConexion() 
        try:
            conexion.miCursor.execute(borrar_sql)
            conexion.miCursor.execute(sql)    
            conexion.miConexion.commit()
            print("Tabla creada correctamente")
        except:
            print("Error al crear tabla")
        finally:             
            conexion.cerrarConexion() 

    # Funcion para borrar tablas en nuestra base de datos SQLite
    def borrar_tablas(self, sql) -> None:
        conexion = Conexiones() 
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(sql)
            conexion.miConexion.commit()   
            print("Tabla monopatines eliminada correctamente")
        except:
            print("Error al eliminar tabla monopatines") 
        finally: 
            conexion.cerrarConexion() 


# Creamos esta clase para crear un objeto que nos permita interactuar con la base de datos
class Conexiones:

    # Metodo para abrir la conexion con nuestra base de datos
    def abrirConexion(self) -> None:
        self.miConexion = sqlite3.connect("BdMonopatines")
        self.miCursor = self.miConexion.cursor()
        
    # Metodo para cerrar la conexion con nuestra base de datos
    def cerrarConexion(self) -> None:
        self.miConexion.close() 


# Creamos esta clase para crear monopatines
class Monopatin():

    # Variable de clase para llevar un ID de cada monopatin creado
    _id: int = 0

    # Metodo constructor que inicializa las propiedades del monopatin
    def __init__(self, modelo: str, marca: str, potencia: str, precio: float, color: str, stock: int, fechaUltimoPrecio: datetime) -> None:
        self.modelo = modelo
        self.marca = marca
        self.potencia = potencia
        self.precio = precio
        self.color = color
        self.stock = stock
        self.fechaUltimoPrecio = fechaUltimoPrecio
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
            conexion.miCursor.execute("INSERT INTO Monopatin(modelo,marca,potencia,precio,color,stock,fechaUltimoPrecio) VALUES('{}', '{}','{}','{}','{}','{}','{}')".format(self.modelo, self.marca, self.potencia, self.precio, self.color, self.stock, self.fechaUltimoPrecio))
            conexion.miCursor.execute("INSERT INTO HistoricoMono(modelo,marca,potencia,precio,color,stock,fechaUltimoPrecio) VALUES('{}', '{}','{}','{}','{}','{}','{}')".format(self.modelo, self.marca, self.potencia, self.precio, self.color, self.stock, self.fechaUltimoPrecio))
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
            conexion.miCursor.execute("UPDATE Monopatin SET precio='{}' where _id='{}' ".format(nuevo_precio, nuevo_id))
            conexion.miConexion.commit()
            print("Precio modificado correctamente")
        except:
            print('Error al actualizar el precio')
        finally:
            conexion.cerrarConexion()

    # Metodo para eliminar monopatines en la tabla de nuestra base de datos
    def eliminar_monopatin(self, borrar_id) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("DELETE FROM Monopatin where _id='{}' ".format(borrar_id))
            conexion.miConexion.commit()
            print("Monopatin eliminado correctamente")
        except:
            print("Error al eliminar monopatin")
        finally:
            conexion.cerrarConexion()

    # Metodo para aumentar la disponibilidad de un monopatin dado la marca
    def cargar_disponibilidad(self, nuevo_marca) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("UPDATE Monopatin SET stock=stock+1 where marca='{}'".format(nuevo_marca))
            conexion.miConexion.commit()
            print("Stock modificado correctamente")
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

    # Metodo para actualizar el precio en la tabla Monopatin
    def actualizar_a_dolar(self, sql, sql2) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(sql)
            conexion.miCursor.execute(sql2)
            conexion.miConexion.commit()
        except:
            print("Error al actualizar los precios y las fechas")
        finally:
            conexion.cerrarConexion()

    # Metodo para actualizar la tabla historica
    def actualizar_historica(self) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("UPDATE HistoricoMono * SELECT * FROM Monopatin")  
            conexion.miConexion.commit()
        except:
            print("Error al actualizar la tabla historica")
        finally:
            conexion.cerrarConexion()

# Creacion del objeto programa
# Comienzo de la ejecucion de nuestra aplicacion
try:
    programa = ProgramaPrincipal()
    programa.menu()
except:
    print("\n\tERROR DE PROGRAMA")
    print("ATENCION")
    print(" - Controlar que la tabla monopatines se encuentre correctamente creada")
    print(" - Controlar que los tipos de datos ingresados sean los correspondientes")
finally:
    print("Fin del programa")


# Las lineas 279 y 280 nos permiten hacer la misma ejecucion del programa pero, en caso de error
# nos mostraran los errores detalladamente
"""programa = ProgramaPrincipal()
programa.menu()"""
