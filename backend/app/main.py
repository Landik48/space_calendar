from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from app.functions import *
# http POST http://localhost:8000/api/calendar year="2025" month="05"
app = FastAPI()

class DateModel(BaseModel):
    year: str
    month: str

@app.post('/api/calendar')
def Calendar(data: DateModel):
    try:
        response = requests.get(f'https://in-the-sky.org/newscal.php?year={data.year}&month={data.month}')
        soup =  BeautifulSoup(response.text, 'lxml')
        els = soup.find_all('div', class_='newscalday')
        result = []
        for el in els:
            obj = {}
            obj['num'] = el.find('p', class_="lefttitle").text
            items = el.find_all('a', href=True)
            events = []
            for item in items:
                title = translate_text(item.text)
                link = item.attrs['href']
                events.append({"title":title, "link":link})
            obj['events'] = events
            result.append(obj)
        return result
    except:
        return {"error": "Произошла ошибка, повторите попытку позже"}

@app.get('/api/satellites')
def Satellites() :
    return {"message": "Календарь"}

@app.get('/api/missions')
def Missions() :
    return {"message": "Миссии"}