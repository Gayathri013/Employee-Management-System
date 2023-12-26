from fastapi import APIRouter , Request , Depends , Response , HTTPException , status
from fastapi.templating import Jinja2Templates
from database import get_db
from sqlalchemy.orm import Session
from models import Register , Employees
from hashing import Hasher
from jose import jwt
from config import settings
from sqlalchemy import and_


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/forgotpassword")
def return_page(request : Request):
    return templates.TemplateResponse("forgot.html" , {"request" : request})


@router.get("/passwordsetting")
async def resetpassword(request : Request , user_id : str , answer : str, db : Session = Depends(get_db) ):
    print(user_id , answer)
    emp = db.query(Employees).filter(Employees.user_id == user_id).first()
    if emp is not None:
        if emp.security_q == answer:
            return templates.TemplateResponse("reset.html" , {"request" : request , "employee" : emp })
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                        detail="Incorrect Answer")


@router.get("/reset/{id}")
async def reset(request : Request, id : str ,newPassword: str , confirmPassword : str, db : Session = Depends(get_db)):
   
    if newPassword == confirmPassword:
        emp = db.query(Employees).filter(Employees.user_id == id).first()
        emp.password = Hasher.get_hash(newPassword)
        db.commit()
        return templates.TemplateResponse("login.html" , {"request" : request})



@router.post("/admin_auth")
async def storing_for_authentication(request : Request , db : Session = Depends(get_db) ):
    form = await request.form()
    user_id = form.get("user_id")
    username = form.get("name")
    email = form.get("email")
    password = form.get("password")
    blood_group = form.get("blood_group")
    date_of_birth = form.get("dob")
    address = form.get("address")
    security_q = form.get("answer")
    phone_number = form.get("phone")
    stack = form.get("stack")

    new_emp = Register(
        user_id = user_id ,
        name = username , 
        password = password ,
        stack = stack ,
        email = email ,
        blood_group = blood_group ,
        date_of_birth = date_of_birth ,
        address = address ,
        security_q = security_q , 
        phone_number = phone_number
    )

    existing_employee = db.query(Employees).filter(Employees.user_id == username).first()

    if existing_employee is None:
        db.add(new_emp)
        db.commit()
        return templates.TemplateResponse("demo.html", {"request" : request})
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE , 
                            detail="User is alredy exists")
    


        


def verify_user(request : Request):
    try:
        token  = request.cookies.get("access_token")
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                                detail="User Not LoggedIn")
        else:
            scheme , _ , path = token.partition(" ")
            payload = jwt.decode(path , settings.secret_key , settings.algorithm)
            return True

    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , 
                            detail = "Bad request ")


def verify_admin(request : Request):
    try:
        token  = request.cookies.get("admin_token")
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                                detail="User Not LoggedIn")
        else:
            scheme , _ , path = token.partition(" ")
            payload = jwt.decode(path , settings.secret_key , settings.algorithm)
            return True

    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , 
                            detail = "Bad request ")
