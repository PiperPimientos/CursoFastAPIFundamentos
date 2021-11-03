#Status Code

# El status code es ese pequeño numero de 3 digitos que le indica al cliente que paso con la respuesta de esa petición HTTP.
# Basicamente lo que hace la API es hacer el response que contiene casi siempre un JSON, deberíamos tener distintos status code que nos indiquen como salieron las cosas.
# Dentro de una centena de status code, podemos encontrar otros casos especiales:
# 201: Algo se creo (created), por ejemplo si estamos en una path operation desde el cliente al servidor, que envia una petición de tipo post y en esa petición creamos un usuario y guardamos el usuario en la base de datos, el servidor responde 201.
# 204: No content. Es decir que no hay ninguna respuesta, aunque todo haya salido bien.
# 404: Accedimos a un endpoint que no existe. (No exists)
# 422: Validation error. Es decir que el cliente nos envia un dato que no esta en el formato que esperábamos. Por ejemplo si esperábamos un validation de no mas de 20 caracteres y le llega al server de 21 caracteres.
#  Ahora haremos un git checkout -b para nuestra nueva Branch, que se llamara status_code. 
# Lo que haremos es que cada una de las path operations tenga un status code personalizado. 
# 1.	Importamos el modulo de fastapi, status. Que nos permite acceder a los diferentes status code de http para poder ingresarlos en nuestras path operations.
# 2.	Los status code se colocan en el path operation decorator, justo despues del endpoint
# la sintaxis seria asi: @app.get(“/”, status_code=status.HTTP_200_OK)
# 3.	Para “/” utilizaremos el 200
# Aquí un truco: si al endpoint le agregamos path=, quedara mucho mas ordenado en las líneas de código
# 4.	Para /person/new vamos a ponerle 201 CREATED, porque este endpoint es para crear una persona en nuestra base de datos
# 5.	Para el de  /person/detail vamos a ponerle 200
# 6.	RETO: ponerle el status code al resto de Path operations


#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, status



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
        max_length=50,
        example="Medellin"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Antioquia"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Colombia"
    )

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "city": "Medellin",
    #             "state": "Antioquia",
    #             "country": "Colombia",
    #         }
    #     }

#PersonBase
class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Miguel"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Perez"
    )
    age: int = Field(
        ...,
        gt=0,
        Le=115,
        example=30
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    paypal: Optional[EmailPaypal] = Field(default=None)

#Person Model
class Person(PersonBase):
    password: str = Field(..., min_Length=8)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Felipe",
    #             "last_name": "Restrepo",
    #             "age": 23,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }

class PersonOut(PersonBase):
    pass


#Path Operations

#Home

@app.get(
    #El path= es para que quede mucho mas ordenado
    path="/", 
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "World"}

#Request and Response body

@app.post(
    "/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get(
    "/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person( 
    name: Optional[str] = Query(
        None, 
        min_Length=1, 
        max_Length=50,
        title="Person Name",
        description="This is the person name. Its Between 1 and 50 characters",
        example="Rocio"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. Its required"
        )
):
    return {name: age}

# Validations: Path Parameters

@app.get(
    "/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
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

@app.put(
    "/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())
    # return results
    return person
