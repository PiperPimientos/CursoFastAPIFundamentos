#Request Body Automaticos

# Recordemos cuando en swagger UI, cada vez que queríamos mandar un Request Body a nuestra API, teníamos que rellenar los datos manualmente. Por ejemplo rellenando los datos de Person, lo teníamos que hacer de manera manual.
# Podemos automatizar este proceso asi:
# 1.	Iremos al modelo que queremos automarizar, que para este caso será Person. Al final crearemos una subclase llamada Config. y esta subclase tendra un atributo llamado schema_extra, que nos sirve para definir esta información por defecto para la documentación.
# Este schema_extra será igual a un JSON. Dentro del JSON definiremos para un tipo en particular de nombre, el test que le queremos hacer, es decir, si contiene ciertos atributos
# Adentro colocaremos esos atributos con su llave y su respectivo valor.
# Hasta el momento, si revisamos en la documentación interactiva, no tendra ningún cambio, esto es porque swagger no cargara los ejemplos si tenemos dos request body en un path operation, pero si por ejemplo comentamos en el path operation todo el request body de location y dejamos solo el path operation de person, si puede funcionar
# Hasta el momento, podemos rellenar de ejemplos a todo el modelo completo que queramos hacer de ejemplo. Pero podemos hacer ejemplos en cada uno de los campos del modelo en particular
# Si agregamos en los parámetros de Field de cada atributo, el parámetro example=”Nombre”, veremos que esto estará funcionando.

# RETO
# Elaborar los ejemplo para el request body del location

# Para los Query y Path parameters, los ejemplos se hacen de la misma forma.
# Veamos por ejemplo las validaciones de Query Parameters
# 1.	Debajo de la descripción del parámetro name, de la path operation function show_person de la path operation de este endpoint /person/detail, agregaremos el example, que será igual a Rocio por ejemplo.


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
