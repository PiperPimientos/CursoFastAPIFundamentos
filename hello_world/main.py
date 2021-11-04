#Cookie and Header parameters

# Ya aprendimos como ingresar datos a la API mediante path parameters, query parameters, request bodys y formularios. Hay fuentes de datos todavía mas exóticas. Son dos cookies y headers parameters.
# Por ejemplos header ya los hemos visto, es una parte de una petición o respuesta http que contiene datos sobre ella, como por ejemplo la fecha en que se hizo, en que formato viene, siendo esto último por ejemplo que vimos que swagger UI nos muestra si la application era un JSON o era un formulario. Tambien existen otros, como el user agent que nos dice quien esta entrando a nuestra web y quien esta usando nuestra API. 
# Una cookie es una pieza de código pequeña que un servidor mete en el PC cuando estamos navegando en el PC, esos datos van a ser útiles para facilitar la navegación en una pagina web despues de la primera vez.
# Las clases para trabajar con cookies y headers en FastAPI, son esas mismas, cookies y headers.
# Crearemos un git checkout -b “cookie_and_headers_parameters”.
# 1.	Vamos a crear los Cookies and Headers Parameters. Vamos a crear toda la path operation.
# 2.	El path operation decorator será de tipo .post porque vamos a trabajar con un envio de información desde el frontend hacia el servidor.
# El path será /contact, pues vamos a crear un formulario de contacto de la pagina web.
# El status code de esta response será 200
# 3.	Ahora haremos nuestro path operation function.
# En sus parámetros necesitaremos el first_name, que es el nombre de la persona, y como viene de un formulario será entonces un Form. Dentro de los parámetros de este form tendremos que es obligatorio . . ., max_Length=20, min_length=1.
# Haremos el otro parámetro que será last_name, con las mismas propiedades del anterior.
# Vamos a pedir también el email, para ello utilizaremos ese tipo de dato exotico de pydantic que es EmailStr y que igual será un Form, que a su vez tendra parámetro de ser obligatorio.
# Luego Sigue el Message que será un str y también va ser un Form, que será obligatorio, tendra un min_length=20. Este será el mensaje que nos envie el usuario
# Ahora agregaremos el primer header, que será el user_agent, que nos dira quien esta intentando usar a esta parte de la API. Por el momento colocaremos que será Optional[str] y que será un = Header. Para ello tendremos que importar esta clase de fastapi y de paso también vamos a importar Cookie. El valor por default de Header va ser None, porque a veces puede venir y a veces no.
# Por ultimo tendremos un parámetro llamado ads que va a controlar las cookies que nos envia el servidor que esta trabajando con la API. el ads será de tipo Optional[str] y será una = Cookie, con parámetro default None.
# Ahora, dentro de la funcion, simplemente retornaremos user_agent
# Nota: Recordemos que ppara utilizar el EmailStr tenemos que tener instalado el pydantic email en la terminal con “pip install pydantic[email]”
# 4.	Si vamos a nuestra documentación interactiva encontraremos que tenemos un nuevo path operation que será de tipo post y estará en /contact. Tendra dos parámetros que ingresar, que corresponderán al de header y cookie. En user_agent no le pondremos nada, lo capturara por defecto. En ads colocaremos “This is the info that is tracking you”.
# Luego podremos ver el formulario con el first name, last name, email, message, en message por ejemplo “I am Felipe and Im trying to learn FastAPI in python”.
# Si vemos el response body veremos que nos retorna, tal y como dijimos en el código, el user_agent. Nos aparece el valor de la cabecera http user_agent de la petición post de la PC de la persona que esta usando la API. Nos dice por ejemplo si estamos en Windows.


#Python
from typing import Optional
from enum import Enum
from fastapi.datastructures import Default

#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, status, Form, Header, Cookie



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