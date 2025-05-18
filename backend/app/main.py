from fastapi import FastAPI
from pydantic import BaseModel
import requests, re, math
from bs4 import BeautifulSoup
from skyfield.api import EarthSatellite, load, wgs84
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
                title = item.text
                link = item.attrs['href']
                events.append({"title":title, "link":link})
            obj['events'] = events
            result.append(obj)
        return result
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {"error": "Произошла ошибка, повторите попытку позже"}


@app.get('/api/satellites')
def Satellites():
    try:
        response = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP=last-30-days&FORMAT=tle")
        lines = response.text.strip().split("\n")
        satellites = []
        ts = load.timescale()
        now = ts.now()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()

            satellite = EarthSatellite(line1, line2, name, ts)
            geocentric = satellite.at(now)
            subpoint = wgs84.subpoint(geocentric)

            lat = subpoint.latitude.degrees
            lon = subpoint.longitude.degrees
            alt = subpoint.elevation.km

            if any(math.isnan(x) or math.isinf(x) for x in [lat, lon, alt]):
                continue  
        
            satellites.append({
                "name": name,
                "lat": lat,
                "lng": lon
            })
        return satellites[:100]
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {"error": "Произошла ошибка, повторите попытку позже"}


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
                    date = 'Not earlier ' + date.split('NET')[1]
                elif 'TBD' in date:
                    date = 'The time will be determined ' + date.split('TBD')[1]
                name = datename[i].find('span', class_='mission').text
                info = missiondata[i].text.replace('Launch site: ', '').replace('Launch time:', '').strip()
                info = "The time will be determined\n" + info.split('TBD')[1] if "TBD" in info else info
                info = re.sub(r'\n+', '\n', info)
                description = re.sub(r'\n+', '\n', missdescrip[i].text.strip())
                missions.append({
                    "date": date,
                    "name": name,
                    "info": info,
                    "description": description
                })
            except: print("Возникла ошибка")
        return missions
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {"error": "Произошла ошибка, повторите попытку позже"}