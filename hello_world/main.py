#Validaciones: Models

# Vimos como combinar dos request bodys en una misma path operation, pero tenemos que saber validar perfectamente los atributos de un request body.
# Esto estará en el nuevo git Branch, “validations_models”, porque vamos a aprender a validar los modelos.
# 1.	Cuando nosotros vamos a validar un request body tenemos que hacerlo directamente en la definición del modelo(clase) que nosotros utilizamos para ese request body. 
# 2.	Vamos a validar todos los atributos que tiene Person. Para ello necesitaremos una nueva clase pydantic, que será Field. Field es exactamente igual a Body, Query y Path pero esta directamente relacionada a los modelos de pydantic.
# 3.	En nuestro Modelo colocaremos al final de todos los atributos un igual seguido del nombre de la clase pydantic, Field
# Por ejemplo:
# first_name: str = Field(…, min_Length=)
# Y el constructor lleva exactamente los mismos atributos de la clase Query y path, es decir que será obligatorio, luego que tendremos un min_length y luego un max_length, la mismas validaciones. Ahora age, tendrá una validación distinta, que serán: obligatorio y que la edad tiene que ser greater than (gt), 0. y menor o igual que 115
# 4.	Para hair color y para is married, sabemos que son opcionales. 
# Para el caso particular de is married utilizaremos la sintaxis de Field, al cual le tendríamos que agregar como parámetro un default=None
# Sin embargo para hair color, sabemos que es un string que debe ser validada, pero hay muchos tipos de hair color, y para ello utilizaremos una nueva clase que viene directamente de Python. Tendremos que llamar el modulo enum para importar la clase Enum
# Enum nos sirve para crear enumeraciones de strings, asi poder definir las validaciones del atributo de hair color.
# Dentro de models vamos a tener que crear una nueva clase llamada HairColor(Enum), que contendrá esas posibles validaciones
# “white” = “white”
# “brown” = “brown”
# Y asi con los demás colores de pelo,
# 5.	Luego en el Model de person, sin bien hair color es Optional, lo cambiaremos por un Field y este Field va tener por default, None. Y el tipo ya no será str sino HairColor, esto nos asegura que esas validaciones sean del tipo que definimos en el Model HairColor

# Si ahora nos vamos a la documentación interactiva. Y si vamos a ver nuestro request body, veremos que swagger automáticamente nos muestra la nueva estructura, si por ejemplo vemos que hair_color por defecto aparece white:


#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr
from pydantic.types import PaymentCardNumber

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path



app = FastAPI()

#Models

class EmailPaypal(EmailStr):
    Paypal = "email"

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

#Location Model
class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

#Person Model
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        Le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    paypal: Optional[EmailPaypal] = Field(default=None)

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
