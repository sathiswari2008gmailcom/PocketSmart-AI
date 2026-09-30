from typing import Literal
from pydantic import BaseModel,Field
class RegisterRequest(BaseModel):
    username:str=Field(min_length=3,max_length=80); email:str=Field(min_length=5,max_length=255); password:str=Field(min_length=8,max_length=128)
class LoginRequest(BaseModel): email:str; password:str
class HomeItem(BaseModel): name:str=Field(min_length=1,max_length=100); quantity:int=Field(ge=1,le=50); notes:str=Field(default="",max_length=300)
class HomeRequest(BaseModel): budget:float=Field(gt=0,le=10000000); rooms:list[str]=Field(min_length=1,max_length=10); items:list[HomeItem]=Field(min_length=1,max_length=30); style:str=Field(default="modern",max_length=100)
class PartyRequest(BaseModel): budget:float=Field(gt=0,le=10000000); guests:int=Field(ge=1,le=10000); event_type:str=Field(min_length=2,max_length=100); venue:str=Field(default="",max_length=200); preferences:str=Field(default="",max_length=500)
class JewelryRequest(BaseModel): budget:float=Field(gt=0,le=10000000); occasion:str=Field(min_length=2,max_length=100); style:str=Field(default="elegant",max_length=100); outfit_description:str=Field(default="",max_length=500); preferences:str=Field(default="",max_length=500)
class RecommendationItem(BaseModel): title:str; category:str; estimated_price:float; quantity:int=1; platform:str; search_url:str; reason:str; notes:str=""
class RecommendationResponse(BaseModel):
    planner_type:Literal["home","party","jewelry"]; summary:str; budget:float; estimated_total:float; remaining_budget:float; allocation:dict[str,float]={}; items:list[RecommendationItem]; source:str; disclaimer:str
