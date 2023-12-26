import os
from dotenv import load_dotenv

load_dotenv(dotenv_path = '.env')

class Settings:
    title = "Employee Application"
    description = """
            Used to manage employee details

            It has two routers
            """
    name = "Aman"
    email = "amanfransis@gmail.com"

    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DATABASE")
    
    datadase_url = f"postgresql://{postgres_user}:{postgres_password}@localhost/{postgres_db}"
    secret_key = os.getenv("SECRET_KEY")
    algorithm = "HS256"



    

settings = Settings()