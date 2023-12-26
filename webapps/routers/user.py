from fastapi import APIRouter , Request , Depends , Response , HTTPException , status , File , UploadFile , Path
from fastapi.templating import Jinja2Templates
from database import get_db
from sqlalchemy.orm import Session
from models import Employees
from hashing import Hasher
from jose import jwt
from config import settings
from webapps.routers import support
from schemas import UserEmployee
from sqlalchemy import desc
import shutil
import math

router = APIRouter()

templates = Jinja2Templates(directory="templates")



@router.get("/home_page" , tags=["User"])
def home_page(request : Request):
    if support.verify_user(request):
        return templates.TemplateResponse("home.html" , { "request" : request})
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    



@router.get("/employee_profile/{id}" , tags=["User"])
def employee_profile(request : Request,id : str  , db : Session = Depends(get_db)):
    if support.verify_user(request):
        employee_details = db.query(Employees).filter(Employees.user_id == id).first()
        return templates.TemplateResponse("view_profile.html" , {"request" : request , "employee" : employee_details})
    



@router.get("/employee_details" , tags = ["User"])
def employee_page(request : Request , db : Session = Depends(get_db)):
    if support.verify_user(request):
        employee_details = db.query(Employees).order_by(Employees.name).all()
        total_emp = len(employee_details)
        return templates.TemplateResponse("employee.html" , { "request" : request , "employee_details" : employee_details , "total" : total_emp} )

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    



@router.get("/details" , tags=["User"])
def requested_details(query : str ,request : Request , db : Session =Depends(get_db)):
    if support.verify_user(request):
        emp = db.query(Employees).filter(Employees.user_id == query).first()
        if emp is None:
            emp = db.query(Employees).filter(Employees.phone_number == query).first()
        
        if emp is not None:
            return templates.TemplateResponse("view_profile.html" , {"request" : request , "employee" : emp})
        
        return templates.TemplateResponse("demo2.html" , {"request" : request})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    



@router.get("/")
def home(request : Request ):
    return templates.TemplateResponse("login.html" , { "request" : request })



@router.get("/register" , tags = ["User"])
def home(request : Request ):
    return templates.TemplateResponse("register.html" , { "request" : request })



@router.get("/update_profile" , tags = ["User"])
def return_profile_template(request : Request , db : Session = Depends(get_db)):
    if support.verify_user(request):
        token  = request.cookies.get("access_token")
        scheme , _ , path = token.partition(" ")
        payload = jwt.decode(path , settings.secret_key , settings.algorithm)
        user_id = payload.get("sub")
        emp = db.query(Employees).filter(Employees.user_id == user_id).first()
        return templates.TemplateResponse("profile.html" , { "request" : request  , "employee" : emp})
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    



@router.get("/contact" , tags = ["User"])
def return_profile_template(request : Request , db : Session = Depends(get_db)):
    if support.verify_user(request):
        return templates.TemplateResponse("contact.html" , { "request" : request })
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    



@router.get("/top_performers")
def top_performers(request : Request , db : Session = Depends(get_db)):
    if support.verify_user(request):
        required_employee = db.query(Employees).order_by(desc(Employees.badges)).limit(3).all()
        return templates.TemplateResponse("top.html" , {"request" : request , "employee_details" : required_employee})
   
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    



@router.get("/logout")
def ad_logout(request : Request , response : Response):
    if support.verify_user(request):
        response.delete_cookie("access_token")
        return templates.TemplateResponse("login.html" , { "request" : request })
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    
    


@router.post("/login_auth" , tags = ["User"])
async def validate_emp_details(request : Request , response : Response , db : Session = Depends(get_db)):
    form = await request.form()
    user_id = form.get("user_id")
    password = form.get("password")
    errors = []
    try:
        emp_details = db.query(Employees).filter(Employees.user_id == user_id).first()
        if emp_details is None:
            errors.append("Invalid userID")
            return templates.TemplateResponse("login.html" , { "request" : request , "errors" : errors} )
        else:
            if Hasher.verify_pass(password ,emp_details.password ):
                data = { "sub" : user_id}
                jwt_token = jwt.encode(data , settings.secret_key , settings.algorithm)
                msg = "Successfully logged in"
                response = templates.TemplateResponse("home.html" , {"request" : request , "msg" : msg , "emp" : emp_details})
                response.set_cookie(key = "access_token" , value = f"Bearer {jwt_token}" , httponly = True)
                return response
            else:
                errors.append("Invalid Password")
                return templates.TemplateResponse("login.html" , { "request" : request , "errors" : errors} )
            

    except Exception as e:
        print(e)
        errors.append("Something went wrong!")
        return templates.TemplateResponse("login.html" , { "request" : request , "errors" : errors} )
    


    

@router.post("/profile_update" , tags=["User"])
async def update_data(request : Request , file: UploadFile=File(...) , db : Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    email = form.get("email")
    blood_group = form.get("blood_group")
    date_of_birth = form.get("date_of_birth")
    phone_number = form.get("phn_number")
    experiance = form.get("experiance")
    role = form.get("role")
    bravo = form.get("bravo")
    raises = form.get("raises")
    trumpet = form.get("trumpet")
    address = form.get("address")
    stack = form.get("stack")
    intersts = form.get("interests")
    hobbies = form.get("hobbies")
    url = await file.read()
    file_location = "static/user_images/"
    with open(f"{file_location}{file.filename}", "wb") as f:
        f.write(url)
    
    image_url = f"{file_location}{file.filename}"


    if support.verify_user(request):
        token  = request.cookies.get("access_token")
        scheme , _ , path = token.partition(" ")
        payload = jwt.decode(path , settings.secret_key , settings.algorithm)
        user_id = payload.get("sub")
        emp_updated = db.query(Employees).filter(Employees.user_id == user_id).first()
        if emp_updated:
            emp_updated.name = name
            emp_updated.email = email
            emp_updated.blood_group = blood_group
            emp_updated.date_of_birth = date_of_birth
            emp_updated.address = address
            emp_updated.experiance = float(experiance)
            emp_updated.phone_number = phone_number
            emp_updated.bravo = int(bravo)
            emp_updated.trumpet = int(trumpet)
            emp_updated.raises = int(raises)
            emp_updated.badges = int((int(trumpet)*20)+(int(bravo)*10)+int(raises))
            emp_updated.stack = stack
            emp_updated.interests = intersts
            emp_updated.hobbies = hobbies
            emp_updated.image_url = image_url
            db.commit()
            return templates.TemplateResponse("home.html" , {"request" : request})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                                detail= " No employee with that userID ")
        
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
