import json
from io import BytesIO
from fastapi import APIRouter,Depends,File,Form,HTTPException,UploadFile
from PIL import Image,UnidentifiedImageError
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import current_user
from ..models import RecommendationHistory
from ..schemas import HomeRequest,PartyRequest,RecommendationResponse
from ..services.gemini_service import generate_home,generate_party,generate_jewelry
router=APIRouter(prefix="/api",tags=["Planners"])
def save(db,user,kind,request_data,result):
    r=RecommendationHistory(user_id=user.id,planner_type=kind,request_json=json.dumps(request_data),response_json=json.dumps(result)); db.add(r); db.commit(); db.refresh(r); return r.id
@router.post("/generate-home",response_model=RecommendationResponse)
def home(p:HomeRequest,user=Depends(current_user),db:Session=Depends(get_db)):
    d=p.model_dump(); result=generate_home(d); save(db,user,"home",d,result); return result
@router.post("/generate-party",response_model=RecommendationResponse)
def party(p:PartyRequest,user=Depends(current_user),db:Session=Depends(get_db)):
    d=p.model_dump(); result=generate_party(d); save(db,user,"party",d,result); return result
@router.post("/generate-jewelry",response_model=RecommendationResponse)
async def jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form("elegant"),outfit_description:str=Form(""),preferences:str=Form(""),outfit_image:UploadFile|None=File(None),user=Depends(current_user),db:Session=Depends(get_db)):
    if budget<=0 or len(occasion)>100 or len(style)>100 or len(outfit_description)>500 or len(preferences)>500: raise HTTPException(422,"Invalid input")
    image=None
    if outfit_image:
        if outfit_image.content_type not in {"image/jpeg","image/png","image/webp"}: raise HTTPException(400,"Only JPG, PNG or WEBP images are allowed")
        raw=await outfit_image.read()
        if len(raw)>5*1024*1024: raise HTTPException(413,"Image must be 5 MB or smaller")
        try: image=Image.open(BytesIO(raw)).convert("RGB")
        except (UnidentifiedImageError,OSError): raise HTTPException(400,"Invalid image file")
    d={"budget":budget,"occasion":occasion,"style":style,"outfit_description":outfit_description,"preferences":preferences,"image_uploaded":bool(image)}
    result=generate_jewelry(d,image); save(db,user,"jewelry",d,result); return result
@router.get("/history")
def history(user=Depends(current_user),db:Session=Depends(get_db)):
    rows=db.query(RecommendationHistory).filter_by(user_id=user.id).order_by(RecommendationHistory.created_at.desc()).limit(50).all()
    return [{"id":r.id,"planner_type":r.planner_type,"created_at":r.created_at.isoformat()} for r in rows]
@router.get("/recommendations/{rid}")
def details(rid:int,user=Depends(current_user),db:Session=Depends(get_db)):
    r=db.query(RecommendationHistory).filter_by(id=rid,user_id=user.id).first()
    if not r: raise HTTPException(404,"Recommendation not found")
    return json.loads(r.response_json)
@router.get("/session-data")
def session_data(user=Depends(current_user),db:Session=Depends(get_db)):
    count=db.query(RecommendationHistory).filter_by(user_id=user.id).count(); return {"user_id":user.id,"recommendation_count":count}
