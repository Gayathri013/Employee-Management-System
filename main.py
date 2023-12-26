from fastapi import FastAPI
from config import settings
from webapps.routers import user , support , admin
from fastapi.staticfiles import StaticFiles

tags = [
    {
      "name" : "User" ,
      "description" : "Managed by user"
    } , 
    {
       "name" : "Admin" ,
       "description" : "Managed by Admin of Organisation"
    }
]

app = FastAPI(
    title = settings.title , 
    description = settings.description ,
    contact = {
    "name" : settings.name ,
    "email" : settings.email
    } ,
    openapi_tags=tags
)

app.mount("/static" , StaticFiles(directory="static") , name="static")


app.include_router(user.router)
app.include_router(admin.router)
app.include_router(support.router)
