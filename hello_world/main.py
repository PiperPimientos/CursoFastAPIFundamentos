#Response Model
# Seguiremos en el mismo repositorio de nuestro antiguo curso de FastAPI fundamentos. Para continuar simplemente haremos una nueva rama de git, que le daremos el nombre de response_model.
# Tenemos un path operation muy importante en nuestra API, que es la que tiene una path operation function de create_person, en /person/new. Esta recibe un request body, que tiene el modelo de Person.
# Esta persona que se va registrar tiene que tener una contraseña. Por lo que deberíamos tener un atributo mas en nuestro modelo de Person, que le llamaremos password.
# Password será obligatorio, será un string y será igual a un Field de nuestro modelo, que va contener como parámetros, obligatorio . . . y un min_Length=8.
# Si ahora nos vamos a nuestra documentación interactiva y revisamos el endpoint. Si intentamos ingresar en nuestro request body nuestra contraseña, estará bien, pero en el response body obtendremos la contraseña tal y como el cliente la envio, y esto es un problema de seguridad.
 
# Hay que tener varias cosas importantes en cuenta a partir de aquí. Primero, jamás se le debe enviar la contraseña a un cliente, es peligroso, porque es un problema de seguridad. Y segundo, jamás se debe almacenar la contraseña que nos da el usuario en texto plano. La contraseña se almacena en un hash.
# Para arreglarlo, podemos hacerlo mediante un response model, que es un atributo de nuestra path operation y se coloca dentro del path operation decorator.
# Despues de nuestra ruta de /person/new”, vamos a agregar response_model= que lleva adentro un modelo de pydantic, va ser un modelo que contenga todos los datos de la persona, pero sin la contraseña, este modelo Pydantic se llamara PersonOut, pero no existe vamos a crearlo.
# Iremos hasta los Models de la API y debajo del modelo Person, crearemos class PersonOut(BaseModel), que hereda de BaseModel:
# Haremos un salto de línea y copiaremos todos los atributos que teníamos en el modelo Person, y lo pegaremos como atributo de PersonOut y, finalmente, le eliminaremos la contraseña porque no tendremos una contraseña como respuesta.
# Y si ahora ejecutamos nuestra path operation e introducimos una contraseña en el request body, veremos que en el response body no tendremos visible la contraseña


#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr

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

#Person Model
class Person(BaseModel):
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

class PersonOut(BaseModel):
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

@app.get("/")
def home():
    return {"Hello": "World"}

#Request and Response body

@app.post("/person/new", response_model=PersonOut)
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
    # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())
    # return results
    return person
