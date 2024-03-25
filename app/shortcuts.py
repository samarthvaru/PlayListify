from app import config

from cassandra.cqlengine.query import DoesNotExist,MultipleObjectsReturned

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from starlette.exceptions import HTTPException as StarletteHTTPException

settings = config.get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))

print(f"Templates directory: {settings.templates_dir}")

def is_htmx(request:Request):
    """Checks if the request is an HTMX request."""
    return request.headers.get("hx-request") == 'true'

def get_object_or_404(KlassName,**kwargs):
    """Gets an object from the database or raises a 404 exception if not found."""
    obj = None
    try:
        obj = KlassName.objects.get(**kwargs)
    except DoesNotExist:
        raise StarletteHTTPException(status_code=404)
    except MultipleObjectsReturned:
        raise StarletteHTTPException(status_code=400)
    except:
        raise StarletteHTTPException(status_code=500)
    return obj


def redirect(path, cookies:dict={},remove_session=False):
    """Redirects the user to a new path with optional cookies."""
    response = RedirectResponse(path,status_code=302)
    for k,v in cookies.items():
        response.set_cookie(key=k,value=v,httponly=True)
    if remove_session:
        response.set_cookie(key="session_ended",value=1,httponly=True)
        response.delete_cookie("session_id") 
    return response
    

def render(request,template_name,context={},status_code:int=200,cookies:dict = {}):
    """Renders a Jinja2 template with optional context and cookies."""
    ctx = context.copy()
    ctx.update({"request":request})
    
    #set httponly cookies
    t = templates.get_template(template_name)
    print(t, template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str,status_code=status_code)
    if len(cookies.keys()) > 0:
        for k,v in cookies.items():
            response.set_cookie(key=k,value=v,httponly=True)
    # #delete cookies
    # for key in request.cookies.keys():
    #     response.delete_cookie(key)
    return response