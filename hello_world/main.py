#Summary and Description. Docstrings


# Si vamos por ejemplo al path operation de /person/new, que vemos que este mal? Que podríamos ordenar para que esto este ordenado y prolijo?
 
# Necesitamos explicarle al usuario de la API como utilizar esta path operation. Pues la persona que llegue y vea el código, que quiera usar la API, se va preguntar que tiene que hacer.
# Dentro de Python hay un concepto llamado docstring, que es la documentación de las funciones. Es un concepto que se puede extrapolar a cualquier aspecto de Python. Es una muy buena practica.
# Para crear un docstring, antes del contenido de la funcion introducimos las triple comillas  ‘ ‘ ‘. Esto lo vimos en pensamiento computacional, además. 
# La estructura de un docstring es, Titulo, Descripcion, Parametros, Resultado.
# Antes que nada, haremos una nueva Branch que será git checkout -b “summary_and_description”
# Vamos a hacer el ejemplo sobre /person/new
# 1.	Agregaremos las pautas mencionadas para el docstring, justo despues de la definición de la path operation function:
# ‘ ‘ ‘
# 1-	Titulo: Create Person
# 2-	Descripcion: This path operation creates a person in the app and save the information in the database
# 3-	Parametros: 
# -	Request Body parameter:
#        -**person: Person** -> A person model with first, last name,                age, haricolor, ismarried.
# 4-	Resultado: returns a person model with first name, last name, age, hair color and marital status.
# ‘ ‘ ‘
# Este es el docstring.
# Ademas veremos un nuevo parámetro para la path operation decorator que se llama summary=, que nos permite colocarle un titulo personalizado a esta funcion.
# Por ejemplo, agregaremos summary=”Create person in the app”..
# Ahora nos vamos a ir a nuestra documentación interactiva. Y si vamos a person/new, veremos que por ejemplo ya esta el titulo personalizado de summary que nosotros le colocamos
# RETO: Documentar todas las demás path operations



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
    '''
    1-	Titulo: Home

    2-	Descripcion: This path operation take us to home page
    
    3-	Parametros: No parameters
        
    
    4-	Resultado: returns hello world in home page.
    '''
    return {"Hello": "World"}

#Request and Response body

@app.post(
    "/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create person in the app"
    )
def create_person(person: Person = Body(...)):
    '''
    1-	Titulo: Create Person

    2-	Descripcion: This path operation creates a person in the app and save the information in the database
    
    3-	Parametros: 
        -	Request Body parameter:
            - **person: Person** -> A person model with first, last name, age, haricolor, ismarried.
    
    4-	Resultado: returns a person model with first name, last name, age, hair color and marital status.
    '''
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
    '''
    1-	Titulo: Person details

    2-	Descripcion: This path operation query the person details
    
    3-	Parametros: 
        
        -Query parameter: name: Optional[str] -> Person name with min and max length.
        
        -Query parameter: name: str -> mandatory, its the person age.
        
    
    4-	Resultado: returns a JSON with name: age.
    '''
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
    '''
    1-	Titulo: Person_id

    2-	Descripcion: This path operation shows the person_id
    
    3-	Parametros: 
        
        -Path parameter: person_id: int -> mandatory, minimum 1 as a value
        
    
    4-	Resultado: If person_id is not in list persons, raise a exception "This person doesnt exist". Else, returns a JSON with the int and message "It exists".
    '''
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
    '''
    1-	Titulo: Update Person

    2-	Descripcion: This path operation updates Person data
    
    3-	Parametros: 
        
        -Path parameter: person_id: int -> mandatory, shows Person by the id (int)
        
        -Body request: person: Person -> Require, fill the Person model data
    
    4-	Resultado: returns a JSON with Person model data filled.
    '''
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
    '''
    1-	Titulo: Login Form

    2-	Descripcion: This path operation is for the Login Form
    
    3-	Parametros: 
        
        -Form: username: str -> require, str of the username

        -Form: password: sstr -> require, str of the password
        
    
    4-	Resultado: returns only the username.
    '''
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
    '''
    1-	Titulo: Cookies and Headers parameters

    2-	Descripcion: This path operation sends a contact message from client data
    
    3-	Parametros: 
        
        -Form: first_name: str -> require first, str, name of client with max and min length.

        -Form: last_name: str -> require last, str, name of client with max and min length.

        -Form: email: EmailStr -> require email of client

        -Form: message: str -> require the message of client with min length.

        -Header: user_agent: str -> user_agent of client, optional.

        -Cookie: ads: str -> Cookie of client, optional.
            
    4-	Resultado: returns header of user_agent.
    '''
    return user_agent


#File and UploadFile

@app.post(
    path="/post-image",
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...)
):
    '''
    1-	Titulo: Post Image, File

    2-	Descripcion: This path operation post a file image
    
    3-	Parametros: 
        
        -File: image: UploadFile -> require the user to upload a file image from his PC
            
    4-	Resultado: returns the file name, the format of file, and the size in kb.
    '''
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }

