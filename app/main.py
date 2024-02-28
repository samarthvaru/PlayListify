import pathlib, json
from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cassandra.cqlengine.management import sync_table
from . import config, db,utils
from .users.models import User
from .users.schemas import UserSignupSchema, UserLoginSchema

BASE_DIR = pathlib.Path(__file__).resolve().parent # app/
TEMPLATE_DIR = BASE_DIR / "templates"


app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

DB_SESSION = None

#settings = config.get_settings()

@app.on_event("startup")
def on_startup():
    #triggered when fastapi calls
    print("hello")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)

@app.get("/",response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        "request":request,
        "abc": 123
    }
    return templates.TemplateResponse("home.html",context)
 
@app.get("/login",response_class=HTMLResponse)
def login_get_view(request: Request):
    return templates.TemplateResponse("auth/login.html",{
        "request": request
    })

@app.post("/login",response_class=HTMLResponse)
def login_post_view(request: Request,
                    email: str = Form(...), 
                    password: str = Form(...)):
    raw_data = {
        "email": email,
        "password": password
    }
    data,errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
        
    return templates.TemplateResponse("auth/login.html",{
        "request": request,
        "data": data,
        "errors": errors
    })
    
@app.get("/signup",response_class=HTMLResponse)
def signup_get_view(request: Request):
    return templates.TemplateResponse("auth/signup.html",{
        "request": request
    })

@app.post("/signup",response_class=HTMLResponse)
def signup_post_view(request: Request,
                    email: str = Form(...), 
                    password: str = Form(...),
                    password_confirm: str = Form(...)
                    ):
    raw_data = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm
    }
    data,errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    
    return templates.TemplateResponse("auth/signup.html",{
        "request": request,
        "data": data,
        "errors": errors
    })
 
@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)
    