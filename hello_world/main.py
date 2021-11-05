#Ordenar los Tags

# Si vemos nuestra documentación interactiva, veremos que hay algo que no tiene ningún tipo de sentido:
 
# Esto es que las etiquetas no tienen ningún tipo de orden. Las path operation están todas desordenadas.
# Haremos, primero que todo, un nuevo Branch llamado tags.
# 1.	Vamos a tomar todas las path operations de personas y las vamos a clasificar bajo un nuevo parámetro del path operation decorator.
# por ejemplo, si nos vamos al path operation /person/new, justo del status_code, vamos a colocar un nuevo parámetro que será
# tags=[“Persons”]
# Alli contenemos un nombre que servirá para clasificar.
# Copy y luego vamos a pegarla en todas las path operation que contegan person
# Si recargamos la pagina de nuestra documentación interactiva veremos que ahora tenemos una sección de etiquetas llamada persons
 
# RETO: Colocar etiquetas a todos los demás path operations.



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
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def home():
    return {"Hello": "World"}

#Request and Response body

@app.post(
    "/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get(
    "/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
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
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
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
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
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
    status_code=status.HTTP_200_OK,
    tags=["Login"]
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

#Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Cookies and Headers"]
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
    path="/post-image",
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }

