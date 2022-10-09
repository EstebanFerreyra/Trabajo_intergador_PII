import sqlite3

class ProgramaPrincipal:

    def menu(self):
        opcion: int = 99
        while opcion != 0:
            print("MENU DE OPCIONES")
            print("1 - Cargar monopatienes")
            print("2 - Modificar datos de un monopatin")
            print("3 - Borrar un monopatin")
            print("4 - Cargar disponibilidad")
            print("5 - Listado de productos")
            print("6 - Tabla")
            print("7 - Tabla de historico/precios")
            print("8 - Registros anteriores a una fecha en específico de la tabla monopatin")
            print("9 - PRIMERA Y UNICA VEZ")
            print("0 - Salir")
            opcion = int(input("Ingrese el numero correspondiente a la seccion: "))
            if opcion >=0 and opcion <= 9:
                if opcion == 0:
                    break
                elif opcion == 1:
                    print("CARGA DE MONOPATINES")
                    marca = str(input("Ingrese la marca del monopatin: "))
                    precio = float(input("Ingrese el precio del monopatin: "))
                    stock = int(input("Ingrese la cantidad disponible: "))
                    nuevo_monopatin = Monopatin(marca, precio, stock)
                    nuevo_monopatin.cargar_monopatin()
                elif opcion == 2:
                    print("MODIFCAR EL PRECIO DE UN MONOPATIN")
                    nuevo_id = int(input("Ingrese ID del monopatin que desea modificar: "))
                    nuevo_precio = float(input("Ingrese el nuevo precio del monopatin: "))
                    Monopatin.modificar_precio(self, nuevo_id, nuevo_precio)
                elif opcion == 3:
                    print("ELIMINAR MONOPATIN")
                    borrar_id = int(input("Ingrese ID del monopatin que desea eliminar: "))
                    Monopatin.eliminar_monopatin(self, borrar_id) 
                elif opcion == 4:
                    print("MODIFICAR DISPONIBILIDAD")
                    nuevo_id = int(input("Ingrese ID del monopatin que desea modificar la disponibilidad: "))
                    nuevo_stock = int(input("Ingrese la cantidad que desee agregar al stock: ")) 
                    Monopatin.cargar_disponibilidad(self, nuevo_id, nuevo_stock)
                elif opcion == 5:
                    print("LISTADO DE MONOPATINES")
                    Monopatin.obtener_monopatines(self, "SELECT * FROM BdMonopatines")
                elif opcion == 6:
                    tabla()
                elif opcion == 7:
                    tabla_historico_precios()
                elif opcion == 8:
                    registros_anteriores()
                elif opcion == 9:
                    self.crearTablas()
                else:
                    print("Opcion invalida - Reingresar")
            else:
                print("Opcion incorrecta - Reingresar")

    def crearTablas(self):
        conexion = Conexiones() #Esto
        conexion.abrirConexion() #ESTO
        conexion.miCursor.execute("DROP TABLE IF EXISTS BdMonopatines")
        conexion.miCursor.execute("CREATE TABLE BdMonopatines (_id INTEGER PRIMARY KEY , marca  VARCHAR(30), precio FLOAT NOT NULL, stock INTEGER NOT NULL,UNIQUE(marca))")    
        conexion.miConexion.commit()  #ESTO     
        conexion.cerrarConexion() # ESTO SIEMPRE LO MISMO


class Conexiones:

    def abrirConexion(self):
        self.miConexion = sqlite3.connect("BdMonopatines")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close() 


class Monopatin():

    _id: int = 0

    def __init__(self, marca: str, precio: float, stock: int) -> None:
        self.marca = marca
        self.precio = precio
        self.stock = stock
        self._id = self._get_next_id()

    @classmethod
    def _get_next_id(cls) -> int:
        cls._id += 1
        return cls._id

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

    def cargar_disponibilidad(self, nuevo_id, nuevo_stock) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("UPDATE BdMonopatines SET stock='{}' where _id='{}' ".format(nuevo_stock, nuevo_id))
            conexion.miConexion.commit()
            print("Monopatin modificado correctamente")
        except:
            print('Error al actualizar un Monopatin')
        finally:
            conexion.cerrarConexion()

    def obtener_monopatines(self, sql) -> None:
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(sql)
            monopatines = conexion.miCursor.fetchall()
            print("Correcta visualizacion de lista")
        except:
            print("Error al mostrar la lista de monopatines")
        finally:
            conexion.cerrarConexion()

        for m in monopatines:
            print(m)


def tabla():
    print("opcio 6")

def tabla_historico_precios():
    print("opcion 7")

def registros_anteriores():
    print("opcion 8")


# CREACION DEL OBJETO PROGRAMA
programa = ProgramaPrincipal()
programa.menu()
