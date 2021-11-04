#File and UploadFile

# Ya hemos aprendido mucho sobre transferencia de datos en API, con path y query parameters, request body, formularios, headers y cookies, pero nos falta algo mas que ver. Los archivos.
# Por ejemplo si tenemos una aplicación donde tenemos que subir un video, tendremos que subir un archivo.
# La palabras claves son en FastAPI, File y UploadFile, ambos son clases. Ambas sirven para controlar el flujo de entrada de archivos desde el cliente hasta el sevidor.
# UploadFile tiene una serie de parámetros:
# -Filename: nombre del archivo. Con este tendremos control del nombre del archivo
# -Content_type: el tipo de archivo que puede ser por ejemeplo jpg, mp4, gif.
# -File: Se corresponde al archivo en si mismo, es decir, acceder a todos los datos del archivo.


# Antes que nada un nuevo git checkout -b “File_and_UploadFile”.
# 1.	Crearemos un nuevo path operation que será de método .post, porque vamos a trabajar enviando datos desde el cliente hasta el servidor.
# El path será /post-image. Es decir que si las personas entran a este endpoint, van a ser capaces de subir una imagen.
# 2.	Importaremos de fastapi las clases UploadFile(que será el tipo) y File(que será la clase)
# 3.	La P. O Function será post_image y como parámetros:
# image que será de tipo UploadFile y será igual a la clase File
# 4.	En la funcion retornaremos un diccionario que será convertido por FastAPI a JSON, que contenga las siguientes llaves y valores.
# Las llaves seran los parámetros que vimos en la clase anterior de UploadFile
# “Filename”: image.filename,
# “Format: image.content_type,
# “Size(kb)”: len(image.file.read()),  #Para poder acceder al tamaño de este archivo, además de acceder al archivo con el método .file utilizaremos la funcion .read() nativa de Python, y con la funcion len(), vamos a envolver a toda la funcion para obtener la cantidad de bytes del archivo.
# 5.	Si nos vamos a la documentación interactiva veremos ya el path operation en /post-image
# Veremos que no tenemos parámetros y que el Request Body es un multipart/form-data y no un application/json o un form.
# Cuando le damos try it out, vemos que Swagger UI ya nos da una herramienta para poder elegir el archivo desde el pc. Nos da un botón como si ya estuviera perfectamente trabajado desde el frontend.
 
# Si subimos un archivo y le damos execute, nuestra path operation debería subirnos el archivo y darnos un response body con lo que pedimos retornar, que es Filename, Format y Size(kb).
 

# Sin embargo, vemos que el response nos esta mostrando el tamaño en bytes y nosotros lo pedimos en kilobytes. Para corregir esto, hacemos una operación matemática.
# Envolvemos el valor del diccionario Size(kb), en un round(), función nativa se Python que nos permite redondear números, pero además para poder que nos muestre cuantos kilobytes son, a partir de los bytes del mismo tenemos que dividir la cantidad de bytes entre 1024, esto nos dara la cantidad de kilobytes.
# Ademas a la funcion round le vamos a pasar el parámetro ndigits= , es decir cuántos dígitos despues de la coma quiero visualizar dentro de la API. Y le daremos un valor de 2.
# Y ahora si nos mostrara lo que pesa en kb nuestra imagen

#Con esto terminamos todos los tipos de entradas de datos que tenemos en FastAPI

#Python
from typing import Optional
from enum import Enum
from fastapi.datastructures import Default

#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, status, Form, Header, Cookie, File, UploadFile



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

