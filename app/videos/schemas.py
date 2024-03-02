import uuid
from pydantic import BaseModel,validator,root_validator
from .extractors import extract_video_id
from app.users.exceptions import InvalidUserIDException
from app.videos.exceptions import InvalidYouTubeVideoURLException, VideoAlreadyAddedException 
from .models import Video

class VideoCreateSchema(BaseModel):
    url: str #user generated
    title: str
    user_id: uuid.UUID # request.session user_id
    
    @validator("url")
    def validate_youtube_url(cls,v,values,**kwargs):
        url = v
        video_id = extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not valid")
        return url
    
    @root_validator(skip_on_failure=True)
    def validate_data(cls,values):
        url = values.get("url")
        title = values.get("title")
        
        if url is None:
            raise ValueError("A valid url is required")
        
        user_id = values.get("user_id")
        
        video_obj = None
        try:
            video_obj = Video.add_video(url,user_id=user_id)
        except InvalidUserIDException:
            raise ValueError("Theres a problem with your account. Please try again.")
        except VideoAlreadyAddedException:
            raise ValueError(f"{url} already added")
        except InvalidYouTubeVideoURLException:
            raise ValueError(f"{url} is not valid")
        except:
            raise ValueError("Theres a problem with your account. Please try again.")
        if video_obj is None:
            raise ValueError("Theres a problem with your account. Please try again.")
        if not isinstance(video_obj,Video):
            raise ValueError("Theres a problem with your account. Please try again.")
        
        video_obj.title = title
        video_obj.save()
            
        return video_obj.as_data()
            
            
    