from fastapi import FastAPI
from pydantic import BaseModel
import requests, re
from bs4 import BeautifulSoup
import argostranslate.package
import argostranslate.translate
# http POST http://localhost:8000/api/calendar year="2025" month="05"
app = FastAPI()

argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == "en" and x.to_code == "ru", available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

class DateModel(BaseModel):
    year: str
    month: str

def translate_text(text):
    try:
        return argostranslate.translate.translate(text, "en", "ru")
    except:
        return "Ошибка перевода"

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
    try:
        response = requests.get('https://spaceflightnow.com/launch-schedule/')
        soup =  BeautifulSoup(response.text, 'lxml')
        missions = []
        datename = soup.find_all('div', class_="datename")
        missiondata = soup.find_all('div', class_="missiondata")
        missdescrip = soup.find_all('div', class_="missdescrip")
        for i in range(len(datename)):
            try:
                date = datename[i].find('span', class_="launchdate").text
                if 'NET' in date:
                    date = 'Не ранее ' + translate_text(date.split('NET')[1])
                elif 'TBD' in date:
                    date = 'Будет определено ' + translate_text(date.split('TBD')[1])
                name = datename[i].find('span', class_='mission').text
                info = missiondata[i].text.replace('Launch site: ', '').replace('Launch time:', '').strip()
                info = "Время будет определено\n" + translate_text(info.split('TBD')[1]) if "TBD" in info else translate_text(info)
                info = re.sub(r'\n+', '\n', info)
                description = translate_text(re.sub(r'\n+', '\n', missdescrip[i].text.strip()))
                missions.append({
                    "date": date,
                    "name": name,
                    "info": info,
                    "description": description
                })
            except: print("Возникла ошибка")
        return missions
    except: 
        return {"error": "Произошла ошибка, повторите попытку позже"}