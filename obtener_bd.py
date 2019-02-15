from pymongo import MongoClient
from producto import Producto
from bson.objectid import ObjectId

def obtener_bd():
	host = "localhost"
	puerto = "27017"
	usuario = "daniel"
	palabra_secreta = "babuino"
	base_de_datos = "tienda"
	cliente = MongoClient("mongodb://{}:{}@{}:{}".format(usuario, palabra_secreta, host, puerto))
	return cliente[base_de_datos]

def insertar(producto):
	base_de_datos = obtener_bd()
	productos = base_de_datos.productos
	return productos.insert_one({
		"nombre": producto.nombre,
		"precio": producto.precio,
		"cantidad": producto.cantidad,
		}).inserted_id

def obtener():
	base_de_datos = obtener_bd()
	return base_de_datos.productos.find()

def actualizar(id, producto):
	base_de_datos = obtener_bd()
	resultado = base_de_datos.productos.update_one(
		{
		'_id': ObjectId(id)
		}, 
		{
			'$set': {
				"nombre": producto.nombre,
				"precio": producto.precio,
				"cantidad": producto.cantidad,
			}
		})
	return resultado.modified_count

def eliminar(id):
	base_de_datos = obtener_bd()
	resultado = base_de_datos.productos.delete_one(
		{
		'_id': ObjectId(id)
		})
	return resultado.deleted_count

menu = """Bienvenido, que desea hacer?.
1 - Insertar producto
2 - Ver todos
3 - Actualizar
4 - Eliminar
5 - Salir
"""
eleccion = None
while eleccion is not 5:
	print(menu)
	eleccion = int(input("Elige: "))
	if eleccion is 1:
		print("Insertar")
		nombre = input("Nombre del producto: ")
		precio = float(input("Precio del producto: "))
		cantidad = float(input("Cantidad del producto: "))
		producto = Producto(nombre, precio, cantidad)
		id = insertar(producto)
		print("El id del producto insertado es: ", id)
	elif eleccion is 2:
		print("Obteniendo productos...")
		for producto in obtener():
			print("=================")
			print("Id: ", producto["_id"])
			print("Nombre: ", producto["nombre"])
			print("Precio: ", producto["precio"])
			print("Cantidad: ", producto["cantidad"])
	elif eleccion is 3:
		print("Actualizar")
		id = input("Cual es el id: ")
		nombre = input("Nuevo nombre: ")
		precio = float(input("Nuevo precio: "))
		cantidad = float(input("Nueva cantidad: "))
		producto = Producto(nombre, precio, cantidad)
		productos_actualizados = actualizar(id, producto)
		print("Cantidad de productos actualizados: ", productos_actualizados)

	elif eleccion is 4:
		print("Eliminar")
		id = input("id: ")
		productos_eliminados = eliminar(id)
		print("Cantidad de productos eliminados: ", productos_eliminados)