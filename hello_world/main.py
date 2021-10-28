# 1.	Para importar FastAPI, from fastapi import FastAPI. Si colocamos el cursor encima de FastAPI, nos daremos cuenta que esta es una class.
# 2.	Definiremos una variable llamada app, que va contener a TODA nuestra aplicación y para poder inicializarla bien, tenemos que hacer una instancia de la clase FastAPI(), sabemos que es una instancia de FastAPI, porque colocamos los paréntesis. Esto quiere decir que la clase FastAPI se va ejecutar y con el constructor se va crear un objeto tipo FastAPI() y se va guardar dentro de app.]
# app = FastAPI()
# Una vez nosotros tenemos una variable con FastAPI() instanciado, es esta misma variable la que nos va permitir correr un proyecto.
# 3.	Ahora utilizaremos un path operation con el signo @.
# Un Path Operation se construye asi.
# @app.get(“/ ”) #Esto es un Path Operation Decorator y lo veremos mas adelante.
# Basicamente, como es un decorador, significa que vamos a decorar una funcion que crearemos posteriormente.
# Este decorador esta utilizando el método get, que viene del objeto app, que a su vez es una instancia de FastAPI. El método get es esa funcion que va decorar la funcion que vamos a crear abajo que va controlar esta primera Path Operation que estamos creando
# 4.	Dentro del decorador Path Operator tenedremos que hacer nuestra funcion, home(), el primer lugar en que un usuario de nuestro API va aparecer cuando entre a la misma. Y que va retornar un JSON, esto es porque una API transmite información entre diferentes partes del software con el formato interlenguaje JSON y recordemos que esto en Python es un diccionario.
# def home():
#             return {“Hello“: “World”}
# Esto ya hace que nuestra aplicación funcione


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "World"}

# 5.	Ahora vamos a la terminal y vamos a ejecutar nuestra API con unicorn, despues main, que es donde tenemos el código, dos puntos, y luego la variable que contiene el objeto que contiene nuestra aplicación que es app y luego un modificador que es –reload, esto es para lograr un efecto llamado en programación hot reloading, que significa que cada vez que hagamos un cambio en el código, solo será abrir el navegador y veremos el cambio uvicorn main:app –reload
# Ejecutamos el comando, uvicorn va empezar a cargar nos va dar los siguientes mensajes
# Will watch… directories: que nos dice donde veremos guardados los cambios
# Uvicorn running on: nos dice que en que IP PORT va estar unicorn
# Starter reloader: que nos muestra que se inicio ese hot reloader
# Started server: recordemos que uvicorn es un servidor y su proceso será el numero que nos de
# App… startup complete: la app se inicio correctamente
# Ahora le damos ctrl + click al ip port que nos apareció y de ahí podremos ir a la pestana del navegador a ver.
#Esto con lo que nos responde el navegador en el IP port, es un archivo JSON que tiene una llave Hello y un valor World
