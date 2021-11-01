#Validaciones: Query Parameterss

# En algunas ocasiones necesitaremos que un query parameter o que un path parameter tenga una forma especifica.
# Por ejemplo tener un query parameter que se refiere al nombre de una persona y este nombre, no debería tener mas de 50 caracteres, de hecho seria muy extraño que exista un nombre de mas de 50 caracteres. Si permitimos que sucedan estas cosas, alguien podría introducir un texto mas grande que la biblia y terminar rompiendo nuestra base de datos.
# Vamos a ver como validar este tipo de parámetros
# Supongamos que tenemos el siguiente path
# http://myapp.com/API/Person/detail

# Y supongamos que este endpoint nos trae el detalle de una persona que se registro en la aplicación. 
# Supongamos que person tiene Name, Age, Hair_color, etc. Y supongamos que la persona necesite información sobre el nombre y la edad. Pues podría hacerlo mediante Query Parameters

# http://myapp.com/API/Person/detail?name=miguel&age=23 

# Ahora, que pasa si por alguna razón, que en el nombre nos pone un texto infinito…
# Vamos a tener que decirle al usuario que ese name no puede ser mayor a 50 caracteres y mayor o igual a 1.
# Vamos a crear un nuevo git Branch para esta clase, llamada validations_query. Esto lo hacemos con git checkout -b “validations_query”
# 1.	Ahora empezaremos con un path decorator que será de método .get que ira dirigido al path /person/detail.
# Despues una path operation function que denominaremos show_person()
# Dentro de los parámetros de la funcion (query parameters), vamos a elaborar los dos, tanto de person, como de age. Pero estos no los tengo que poner en el endpoint del path decorator, los ponemos en los parámetros de la definición de la funcion.
# Diremos que name es un optional porque es un query parameter y recordemos que los query parameters son opcionales. Igual con age. Pero les diremos que es un parámetro de tipo = Query. Para ello tendremos que importar la clase Query de fastapi.
# Con Query tenemos mas o menos los mismos parámetros que en Body, pero tienen algunas diferencias.
# Lo primero que haremos es poner que el default de Query, es None, pero si la persona llega a mandar cierta información, colocamos el min_length=1, es decir que la persona no puede enviar un nombre menor a 1 string y el max_length=50
# Para age, lo mismo, diciendo que es un str y diciendo que es obligatorio, ósea que como  parámetro el Query no recibe None, sino los tres puntos, …, esto no es ideal, pues lo ideal es que un Query siempre sea opcional, pero podría pasar que necesitemos que sea obligatorio. Ahora bien lo que si es buena práctica, es que siempre que un parámetro tenga que ser obligatorio, debería ser un Path Parameter no un Query Parameter

# @app.get(“/person/detail”)
# def show_person(
#                    name: Optional[str] = Query(None, min_Length=1,                      max_Length=50),
#                    age: str = Query(…, 
# ):
# 2.	Ahora cerramos los parametros de la funcion y lo cerraremos con un return del json que tendrá como llave a el str name y un valor que será el age.
# return{name: age}

# Ahora, si vamos a nuestra documentación intereactiva veremos que tendremos otra path operations que será de método .get, que se llama Show Person, y se accede mediante el endpoint /person/detail. 
# Adentro veremos que tenemos un Query Parameter, que tendrá name, con una validación de max length y min length y luego el age que será un required por su obligatoriedad. 


#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query

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

#Request and Response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person( 
    name: Optional[str] = Query(None, min_Length=1, max_Length=50),
    age: str = Query(...)
):

    return {name: age}

