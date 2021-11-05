#HTTPException

# Que pasa si un usuario de nuestra aplicación intenta acceder a un dato que no existe o un dato que no tiene permiso. Para esto FastAPI nos da una clase muy útil que es HTTPException. Esta clase nos ayuda a controlar el funcionamiento de los errores dentro de FastAPI.
# Lo primero es importar la clase HTTPException de fastapi.
# Hay errores que tienen un status code del orden de 400, ahí es donde utilizaremos HTTPException para que nuestras path operation queden mas completas.
# Vamonos por ejemplo a las validaciones de Path parameters que esta en el path /person/detail/{person_id}. Aquí no hay ninguna lógica, simplemente decimos que tiene que ser mayor a 0 ese person id, y que un ejemplo podría ser 123.
# Pero además, podríamos validar que no existe ningún person_id y que aparezca por ejemplo un 404. Para eso vamos a crear una lista en esa misma validación que diga por ejemplo las personas que si se han registrado, es decir los person_id que si existen. Ejemplo: persons = [1, 2, 3, 4, 5]
# Por lo tanto, vamos a cambiar un poco la lógica de nuestro path operation.
# Antes del return vamos a poner una condicional, diciendo:
# if person_id not in persons:
#                 raise HTTPException() 
# Recordemos que cuando trabajamos con excepciones, no hacemos un return sino que hacemos un raise.
# Ese HTTPException va tener los parámetros de status_code en 404. Luego un detail que va contener “This person doesnt exist”
# Ya con esto nos podemos ir a la documentación interactiva y veremos en nuestro /person/detail/{person_id} que si ingresamos un person_id que no esta dentro de la lista persons, nos saldrá como response un 404.

#Con esta clase fastapi HTTPException es suficiente para manejar cualquier error que tenga el cliente

#Python
from typing import Optional
from enum import Enum
from fastapi.datastructures import Default

#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, status, Form, Header, Cookie, File, UploadFile, HTTPException



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

#LoginOut Model
class LoginOut(BaseModel):
    username: str = Field(
        ..., 
        max_length=20, 
        example="Miguel2021"
        )
    message: str = Field(default="Login Succesfully!")

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
persons = [1, 2, 3, 4, 5]
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
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesnt exist"
        )
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

#Form de login

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

#Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
)
def contact(
    first_name: str = Form(
        ...,
        max_Length=20,
        min_Length=1
    ),
    last_name: str = Form(
        ...,
        max_Length=20,
        min_Length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_Length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent


#File and UploadFile

@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }

