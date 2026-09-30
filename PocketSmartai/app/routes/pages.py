from fastapi import APIRouter,Depends,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from ..dependencies import current_user_optional
router=APIRouter(); templates=Jinja2Templates(directory="templates")
def page(request,name,user=None,**ctx): return templates.TemplateResponse(request=request,name=name,context={"user":user,**ctx})
@router.get("/",response_class=HTMLResponse)
def home(request:Request,user=Depends(current_user_optional)): return page(request,"index.html",user)
@router.get("/register",response_class=HTMLResponse)
def reg(request:Request): return page(request,"register.html")
@router.get("/login",response_class=HTMLResponse)
def login(request:Request): return page(request,"login.html")
@router.get("/dashboard",response_class=HTMLResponse)
def dash(request:Request,user=Depends(current_user_optional)):
    return page(request,"dashboard.html",user) if user else RedirectResponse("/login",303)
@router.get("/history",response_class=HTMLResponse)
def hist(request:Request,user=Depends(current_user_optional)): return page(request,"history.html",user) if user else RedirectResponse("/login",303)
@router.get("/planner/{kind}",response_class=HTMLResponse)
def planner(kind:str,request:Request,user=Depends(current_user_optional)):
    if not user:return RedirectResponse("/login",303)
    names={"home":"home_planner.html","party":"party_planner.html","jewelry":"jewelry_planner.html"}
    if kind not in names:return RedirectResponse("/dashboard",303)
    return page(request,names[kind],user)
@router.get("/recommendations/{rid}",response_class=HTMLResponse)
def recommendation(request:Request,rid:int,user=Depends(current_user_optional)):
    return page(request,"recommendations.html",user,recommendation_id=rid) if user else RedirectResponse("/login",303)
