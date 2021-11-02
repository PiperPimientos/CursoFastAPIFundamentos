#Validaciones: Path Parameters

# Ahora validaremos el request body.
# 1.	Crearemos la nueva path operation que va utilizar una operation de tipo put, que sirve para actualizar algún contenido en nuestra aplicación.
# 2.	Va tener una path operation que será /person/{person_id}. Es decir que cada vez que se use este path operation se podrá actualizar un contenido, que en este caso será person_id
# 3.	Para que esto funcione, tendremos que hacer un request body. Empezando con la path operation function, que tendrá de nombre update_person(). Dentro de esta tebdrenis obviamente que definir el person id: que será tipo int y que será igual a Path y todos los parámetros que teníamos en person_id.
# 4.	Ahora haremos el request body, a este request body que la persona me envia, yo le tengo que poner un nombre y luego llamar la clase Person que habíamos creado al principio,
# #Models
# class Person(BaseModel):
#     first_name: str
#     last_name: str
#     age: int
#     hair_color: Optional[str] = None
#     is_married: Optional[bool] = None


# Es decir que la persona que nos este enviando el update debería enviarnos un JSON con ese tipo de datos.
# 5.	Ahora finalmente que dicha clase es igual a una clase de fastapi que ya conocemos, = Body(…) que además, sera obligatorio.
# 6.	Ahora, dentro de la funcion, solo nos queda colocar el return, que en este caso será person
# 7.	Si ahora nos vamos a la documentación interactiva, notaremos que tenemos una nueva path operation de método .put, de nombre Update_person, que esta en el path de /person/{person_id}.
# Si lo ejecutamos vemos que nos pedirá el person_id y luego vendrá el request body que viene con un JSON que tendremos que cambiar, porque es además un required.

# Ahora pensemos, que pasa si en este mismo path operation le pedimos al usuario en un request body, el parámetro Location.
# 1.	El request body de nombre Location de tipo Location  será igual a una clase fastapi Body(…) que será obligatorio. Con lo que le estaremos diciendo al usuario en una sola path operation que nos envie no solo 1 sino 2 JSONs, esto se supone que no se puede lograr, pero veremos como lo soluciona FastAPI.
# 2.	Arriba en nuestros Models, crearemos el Modelo Location(class Location), recordando que tendremos que llamar a nuestra clase de pydantic BaseModel, 
# A esa clase le daremos los siguientes atributos:
# a. City: str
# b.	State: str
# c.	Country: str
# 3.	Finalmente volvemos a nuestro request body y la manera en la que podremos retornar esta clase es hacerlo de forma explicita, no podemos dejar a FastAPI que lo haga por si solo. 
# Dentro de la path operation function, tenemos que agregar antes del return, la variable results que tendrá asignado el request body person, convertido a diccionario, ósea con un .dict()
# Ahora, en una nueva línea invocamos la variable results con el método .update(location()) y con el Body location también convertido a diccionario. Lo que estamos haciendo es convertir el diccionario person y el diccionario location
# Y finalmente cambiaremos el return que estaba con person, por results.



#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path


app = FastAPI()

#Models

#Location Model
class Location(BaseModel):
    city: str
    state: str
    country: str

#Person Model
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
    name: Optional[str] = Query(
        None, 
        min_Length=1, 
        max_Length=50,
        title="Person Name",
        description="This is the person name. Its Between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. Its required"
        )
):
    return {name: age}

# Validations: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
            person_id: int = Path(
                ..., 
                gt=0,
                title="Person",
                description="Showing id person"
                ),          
):
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

# Aunque también hay una manera mas resumida de hacerlo, con la unión de diccionarios que recordemos seria con la siguiente sintaxis
# person.dict() & location.dict()
# Sin embargo, FastAPI todavia no soporta esta sintaxis, por lo que toca hacerlo de manera mas clásica. Conviritiendo primero a diccionario el primer parámetro que tenemos y luego con el método .update(location.dict()) de esta variable results, unir como diccionario al segundo parámetro.

# Si hacemos los cambios y luego le damos execute, y al final vamos a ver el Response body, encontraremos un solo formato JSON con todas las respuestas del request body, pero sin diferenciar de los atributos de la clase person y los atributos de la clase location.

