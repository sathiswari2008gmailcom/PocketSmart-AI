import os,tempfile
os.environ['DATABASE_URL']=f"sqlite:///{tempfile.NamedTemporaryFile(suffix='.db',delete=False).name}"
os.environ['SECRET_KEY']='test-secret';os.environ['GEMINI_API_KEY']=''
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
init_db()
def test_health():
    with TestClient(app) as c: assert c.get('/health').status_code==200
def test_auth_and_home():
    with TestClient(app) as c:
        assert c.post('/api/auth/register',json={'username':'tester','email':'tester@example.com','password':'password123'}).status_code==200
        assert c.post('/api/auth/login',json={'email':'tester@example.com','password':'password123'}).status_code==200
        r=c.post('/api/generate-home',json={'budget':30000,'rooms':['Living Room'],'style':'modern','items':[{'name':'Light','quantity':2,'notes':''}]})
        assert r.status_code==200 and r.json()['planner_type']=='home'
def test_party_and_history():
    with TestClient(app) as c:
        c.post('/api/auth/login',json={'email':'tester@example.com','password':'password123'})
        r=c.post('/api/generate-party',json={'budget':20000,'guests':30,'event_type':'Birthday','venue':'Home','preferences':'Simple'})
        assert r.status_code==200
        assert c.get('/api/history').status_code==200
