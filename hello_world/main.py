# El Request Body. Para entenderlo tenemos que retomar un concepto del curso de intro al Backend. Ya sabemos lo que es un HTTP, que tiene, headers, body, métodos.
# Luego pensemos que tenemos un cliente, que es nuestro pc y tenemos un servidor. Sabemos que esta comunicación se realiza mediante HTTP
 
# Cuando es el cliente que se comunica con el servidor, esta comunicación se denomina Request body, y cuando el servidor toma el request del cliente y responde, tenemos un response body. Ambos body se envían mediante un formato JSON.
# Ahora, para  lo siguiente que haremos es crear otro git Branch, utilizaremos el nombre git checkout -b “request_response_body”.
# Una vez que hacemos este nuevo Branch, empezaremos nuestro proyecto de esta clase:

# #FastAPI
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"Hello": "World"}

#Tenemos importado nuestro FastAPI, además tenemos una variable app que tiene instanciada la clase FastAPI() y, mas abajo, tenemos un path operation, conformado por el path operation decorator, donde estamos utilizando el método http .get, en el endpoint “/”, y para ello utilizaremos una función que retornara un archivo JSON, con la llave hello y el valor world.


#Ahora practicaremos el Request and Response Body
# 1.	Creamos una nueva path operation, en donde tendremos una petición de tipo .post (metodo), porque vamos a enviar datos desde el cliente al servidor y si tuviéramos que recibir desde el servidor hasta el cliente, utilizando el método .get. Y finalmente se nos ocurre que vamos a tener un endpoint llamado /person/new, y si yo accedo a este endpoint, sere capaz de crear una nueva person. Porque pensemos que esta API tendrá la funcionalidad de crear personas nuevas con sus datos.
# Despues definiremos el path operation function, es decir crearemos la función para crear nueva persona.

# @app.post(“/person/new”)
# def create_person():
#          pass

# Y hasta aquí lo dejaremos, porque para aprender request body, tendremos que aprender un concepto mas
#Este concepto es Models
# Para saber que es un Modelo, tenemos que imaginarnos a una entidad. Una entidad puede ser cualquier cosa en el mundo, como una persona, una casa, un animal, etc. Un modelo, no es más que la representación de una entidad en código, al menos de manera descriptiva.
# Como luce un modelo en FastAPI?
# Pensemos que por ejemplo para la API de twitter tenemos un modelo que es el Tweet y el otro modelo que es el User. Es decir un modelo que describa a la entidad Tweet y otro modelo que describa a la entidad User.
# A estos modelos los vamos a crear con una librería llamada Pydantic, de la cual nos traeremos una clase llamada Base Model, que nos va permitir crear los modelos
# En nuestro código
# 1.	Pondremos por encima de FastAPI a Pydantic, porque Pydantic esta en la base o por debajo de FastAPI que funciona sobre Pydantic. Por ello es necesario que vayamos importando con este nivel de abstracción. Y de base de Pydantic podríamos importar incluso librerías nativas de Python, que para este caso necesitaremos de la librería typing, importar un tipo de dato para realizar tipado estatico que será Optional.
# from typing import Optional
# from pydantic import BaseModel
# 2.	Una vez importado BaseModel, crearemos los modelos necesarios para la aplicación. Esto lo haremos por el momento debajo de la definicion de la variable app

# Primero hay que crear una class, luego el nombre del modelo que será Person, tiene que heredar de (BaseModel):
# Debajo empezamos a definir el modelo, colocando los atributos de la entidad.
# Primer atributo sera el first name, que será de tipo str (tipado estatico) y lo mismo con los demas
# first_name: str
# last_name: str
# age: int
# hair_color: str
# is_married: bool
# Pero suponiendo que el hair color  y el is married no es importante, lo dejaremos como opcionales, para eso fue que importamos Optional, de la librería typing.
# Para eso les quitamos el tipo str y bool. Y seguido colocaremos Optional y entre corchetes [ ] vamos a colocar el tipo valor que nosotros esperaríamos, es decir str y bool. 
# Pero además tendremos que tener un valor por defecto por si el usuario no nos introduce los datos que son opcionales. Normalmente, si estamos trabajando en bases de datos, el valor va ser = null. Null en Python esta representado como None, es decir que aquí puede haber algo o no puede haber nada.
# 3.	Ahora iremos al path operation que habíamos creado para persona nueva y en la función podemos retornar directamente person(path) y la cosa va funcionar. Sin embargo necesitamos recibir de la persona el modelo de Person. Como lo recibimos? Con el Request Body, que también es un parámetro que se coloca en la definicion de la función, además tendremos que utilizar tipado estatico, es decir que tendremos a ese person(el path) que será de tipo Person(la clase)
# def créate_person(person: Person):
# 4.	Sin embargo, hay algo mas. De fastapi vamos a importar otra clase llamada Body. Esta clase nos permite decir explícitamente que un parámetro que me esta llegando es de tipo body() y, como parámetro le pasamos el triple punto, este parámetro significa que este Request Body, es obligatorio. Es decir que siempre que encontremos los tres puntos, va significar que un atributo o parámetro es obligatorio.
# def create_person(person: Person = Body(…))
# Ya con esto estamos listos para retornar person



#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

#Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


#Para ver como funciona en la documentacion interactiva, ver las notas