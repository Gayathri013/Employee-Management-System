from pydantic import EmailStr , BaseModel

class UserEmployee(BaseModel):

    user_id : str
    name : str
    password : str
    email : EmailStr
    age : int
    bload_group : str
    stack : str
    badges : int
    interests : str
    address : str
    date_of_birth : str
    hobbies : str
    experiance : float
    image_url : str
    bravo : int
    raises : int
    trumpet : int
    phone_number : str
    security_q : str
    gender : str


class ShowDetails(BaseModel):

    user_id : str
    name : str
    email : EmailStr
    age : int
    bload_group : str
    stack : str
    badges : int
    interests : str
    address : str
    date_of_birth : str
    hobbies : str
    experiance : float
    image_url : str
    bravo : int
    raises : int
    trumpet : int
    phone_number :str
    


    class Config:
        orm_mode = True


class Register(BaseModel):

    user_id : str
    name : str
    email : EmailStr
    blood_group : str
    blood_group : str
    date_of_birth : str
    address : str
    security_q : str
    phone_number : str


    class Config:
        orm_mode = True




