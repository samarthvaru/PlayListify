import pathlib, json
from typing import Optional
from fastapi import FastAPI,Request,Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
from cassandra.cqlengine.management import sync_table
from . import config, db,utils
from .indexing.client import (
    update_index,
    search_index
)
from .playlists.routers import router as playlist_router
from .playlists.models import Playlist
from .shortcuts import redirect,render
from .users.backends import JWTCookieBackend
from .users.decorators import login_required
from .users.models import User
from .users.schemas import UserSignupSchema, UserLoginSchema
from .videos.models import Video
from .videos.routers import router as video_router
from .watch_events.models import WatchEvent
from .watch_events.schemas import WatchEventSchema
from .watch_events.routers import router as watch_event_router

app = FastAPI()

app.add_middleware(AuthenticationMiddleware,backend= JWTCookieBackend())

app.include_router(playlist_router)
app.include_router(video_router)
app.include_router(watch_event_router)

settings = config.get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))

print(f"Templates directory: {settings.templates_dir}")

DB_SESSION = None

from .handlers import * #noqa
#settings = config.get_settings()

@app.on_event("startup")
def on_startup():
    #triggered when fastapi calls
    print("hello")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)
    sync_table(WatchEvent)
    sync_table(Playlist)

@app.get("/",response_class=HTMLResponse)
def homepage(request: Request):
    """Render the homepage."""
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {}, status_code=200)
    return render(request,"home.html",{})

@app.get("/account",response_class=HTMLResponse)
@login_required
def account_view(request: Request):
    """Render the account view."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400)
    context = {}
    return render(request,"account.html",context)
 
@app.get("/login",response_class=HTMLResponse)
def login_get_view(request: Request):
    """Render the login form."""
#    session_id = request.cookies.get("session_id") or None
 #   return render(request,"auth/login.html",{"logged_in": session_id is not None})
    return render(request, "auth/login.html", {})

@app.post("/login",response_class=HTMLResponse)
def login_post_view(request: Request,
                    email: str = Form(...), 
                        password: str = Form(...),
    next: Optional[str] = "/"
    ):
    
    """Handle login form submission."""
    
    raw_data = {
        "email": email,
        "password": password,
    }
    data,errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    
    context = {
            "data": data,
            "errors": errors,
        }
    if len(errors) > 0:
        return render(request,"auth/login.html",context, status_code=400)
    print(data)
    if "http://127.0.0.1" not in next:
        next = '/'
    return redirect(next, cookies=data)


@app.get("/logout", response_class=HTMLResponse)
def logout_get_view(request: Request):
    """Render the logout confirmation."""
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, "auth/logout.html", {})

@app.post("/logout", response_class=HTMLResponse)
def logout_post_view(request: Request):
    """Handle logout form submission."""
    return redirect("/login", remove_session=True)

    
@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    """Render the signup form."""
    return render(request, "auth/signup.html")


@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request, 
    email: str=Form(...), 
    password: str = Form(...),
    password_confirm: str = Form(...)
    ):
    """Handle signup form submission."""
    
    raw_data  = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    context = {
            "data": data,
            "errors": errors,
        }
    if len(errors) > 0:
        return render(request, "auth/signup.html", status_code=400)
    User.create_user(data.get('email'),data.get('password').get_secret_value())
    return redirect("/login")

@app.post('/update-index', response_class=HTMLResponse)
def htmx_update_index_view(request:Request):
    """Update the search index."""
    count = update_index()
    return HTMLResponse(f"({count}) Refreshed")
 
 
@app.get("/users")
def users_list_view():
    """List users."""
    q = User.objects.all().limit(10)
    return list(q)

@app.get("/search", response_class=HTMLResponse)
@login_required
def search_detail_view(request:Request, q:Optional[str] = None):
    """Render the search results."""
    query = None
    context = {}
    if q is not None:
        query = q
        results = search_index(query)
        hits = results.get('hits') or []
        num_hits = results.get('nbHits')
        context = {
            "query": query,
            "hits": hits,
            "num_hits": num_hits
        }
    return render(request, "search/detail.html", context)

@app.post("/watch-event", response_model=WatchEventSchema)
@login_required
def watch_event_view(request: Request, watch_event: WatchEventSchema):
    cleaned_data = watch_event.dict()
    data = cleaned_data.copy()
    data.update({
        "user_id": request.user.username
    })
    print("data", data)
    if (request.user.is_authenticated):
        WatchEvent.objects.create(**data)
        return watch_event
    return watch_event