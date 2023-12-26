from fastapi import APIRouter , Request , Depends , Response , HTTPException , status 
from fastapi.templating import Jinja2Templates
from database import get_db
from sqlalchemy.orm import Session
from models import Register , Employees , Admin
from hashing import Hasher
from jose import jwt
from config import settings
from webapps.routers import support
from schemas import ShowDetails
from sqlalchemy import desc
from hashing import Hasher

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/admin" , tags=["Admin"])
def return_admin_page(request : Request):
    return templates.TemplateResponse("ad_login.html" , { "request" : request})


    
@router.get("/ad_register_employee" , tags=["Admin"])
def employee_page(request : Request , db : Session = Depends(get_db)):
    if support.verify_admin(request):
        employee_details = db.query(Register).order_by(Register.name).all()
        return templates.TemplateResponse("ad_new.html" , { "request" : request , "employee_details" : employee_details} )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")



@router.get("/approve/{user_id}" , tags=["Admin"])
def add_new_employee(user_id : str ,request : Request , db : Session = Depends(get_db)):
    if support.verify_admin(request):
        emp = db.query(Register).filter(Register.user_id == user_id).first()
        emp1 = Employees(
            user_id = emp.user_id , 
            name = emp.name ,
            email = emp.email ,
            address = emp.address ,
            date_of_birth = emp.date_of_birth ,
            blood_group = emp.blood_group ,
            security_q = emp.security_q ,
            phone_number = emp.phone_number,
            stack = emp.stack ,
            password = Hasher.get_hash(emp.password)
        )
        db.add(emp1)
        db.commit()
        db.delete(emp)
        db.commit() 
        employee_details = db.query(Register).order_by(Register.user_id).all()
        return templates.TemplateResponse("ad_new.html" , { "request" : request , "employee_details" : employee_details} )

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")



@router.get("/disaprove/{user_id}" , tags=["Admin"])
def delete_required_employee(user_id : str , request : Request , db : Session = Depends(get_db)):
    if support.verify_admin(request):
        employee_details = db.query(Register).filter(Register.user_id == user_id).first()
        db.delete(employee_details)
        db.commit()
        employee_details = db.query(Register).order_by(Register.user_id).all()
        return templates.TemplateResponse("ad_new.html" , { "request" : request , "employee_details" : employee_details})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    


@router.get("/ad_employee" , tags = ["Admin"])
def employee_page(request : Request , db : Session = Depends(get_db)):
    if support.verify_admin(request):
        employee_details = db.query(Employees).order_by(Employees.name).all()
        total_emp = len(employee_details)
        return templates.TemplateResponse("ad_employee.html" , { "request" : request , "employee_details" : employee_details , "total" : total_emp} )

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    


@router.get("/ad_profile/{id}" , tags=["Admin"])
def display_details(id : str ,request : Request , db : Session =Depends(get_db)):
    if support.verify_admin(request):
        emp = db.query(Employees).filter(Employees.user_id == id).first()
        if emp is not None:
            return templates.TemplateResponse("ad_profile.html" , {"request" : request , "employee" : emp})
        
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")


    
    
@router.get("/ad_search" , tags=["Admin"])
def requested_details(query : str ,request : Request , db : Session =Depends(get_db)):
    if support.verify_admin(request):
        emp = db.query(Employees).filter(Employees.user_id == query).first()
        if emp is None:
            emp = db.query(Employees).filter(Employees.phone_number == query).first()
        
        if emp is not None:
            return templates.TemplateResponse("ad_profile.html" , {"request" : request , "employee" : emp})
        
        return templates.TemplateResponse("demo2.html" , {"request" : request})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")




@router.get("/ad_top" , tags=["Admin"])
def top_performers(request : Request , db : Session = Depends(get_db)):
    if support.verify_admin(request):
        required_employee = db.query(Employees).order_by(desc(Employees.badges)).limit(3).all()
        return templates.TemplateResponse("ad_top.html" , {"request" : request , "employee_details" : required_employee})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    


@router.get("/ad_logout" , tags=["Admin"])
def ad_logout(request : Request , response : Response):
    response.delete_cookie("admin_token")
    return templates.TemplateResponse("ad_login.html" , { "request" : request})
    


@router.get("/delete_employee/{user_id}" , tags=["Admin"])
def delete_required_employee(user_id : str , request : Request , db : Session = Depends(get_db)):
    if support.verify_admin(request):
        employee_details = db.query(Employees).filter(Employees.user_id == user_id).first()
        print(employee_details)
        db.delete(employee_details)
        db.commit()
        employee_details = db.query(Employees).order_by(Employees.name).all()
        total_emp = len(employee_details)
        return templates.TemplateResponse("ad_employee.html" , { "request" : request , "employee_details" : employee_details , "total" : total_emp})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , 
                            detail="Un-authorized request")
    



@router.post("/admin_login" , tags=["Admin"])
async def authenticate_admin(request : Request , db : Session = Depends(get_db) ):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    errors = []
    try:
        emp_details = db.query(Admin).filter(Admin.username == username).first()
        if emp_details is None:
            errors.append("Invalid userID")
            return templates.TemplateResponse("ad_login.html" , { "request" : request , "errors" : errors} )
        else:
            if Hasher.verify_pass(password ,emp_details.password ):
                data = { "sub" : username}
                jwt_token = jwt.encode(data , settings.secret_key , settings.algorithm)
                msg = "Successfully logged in"
                response = templates.TemplateResponse("ad_home.html" , {"request" : request , "msg" : msg})
                response.set_cookie(key = "admin_token" , value = f"Bearer {jwt_token}" , httponly = True)
                return response
            else:
                errors.append("Invalid Password")
                return templates.TemplateResponse("ad_login.html" , { "request" : request , "errors" : errors} )
        
    except Exception as e:
        print(e)
        errors.append("Something went wrong!")
        return templates.TemplateResponse("ad_login.html" , { "request" : request , "errors" : errors} )