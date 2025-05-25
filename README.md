## Webová aplikace nad otevřenými daty
Zpracování otevřených dat z informačního systému veřejné správy povodňových čidel. Aplikace byla vypracována pro DCÚK v rámci soutěže Hackathon.

**Autoři:** Tomáš Ladislav Kotek, Patrik Poklop, Matěj Sloup

**Technologie:** 
Jazyk: Python

Backend: FastApi 
Frontend: Nginx , Streamlit, Folium

Běží na Dockeru

**Použití dat ze stránky vlády data.gov.cz**
- Aktuální stav na povodňových čidlech Ústeckého kraje
- Přehled hlásných profilů Ústeckého kraje

#### Spuštění aplikace
Stačí mít docker a v kořenovém adresáři *Open_Data_Web_Api/* zadat do příkazové řádky *docker-compose up --build*.
Docker-compose je rozdělený na backend(Uvicorn) a frontend konteiner(Nginx). Nám stačí spustit frontend na *localhost:8501*. 

### Popis api
![image](https://github.com/user-attachments/assets/815d0469-9c1e-476f-ade7-6f168084ee7e)

Aplikace obsahuje mapu, která zobrazuje jednotlivá měření hladin po ústeckém kraji ze senzorů, která jsou vyznačena jednotlivými body a ty jsou zabarveny podle jejich stavu. Body na mapě se dají filtrovat podle obce, stavu a toku. Ve filtru je možno vybrat více možností najednou. Jednotlivé body na mapě se dají rozkliknout a zobrazit se jejich stav naměřený z čidel, které se online získávají z json souboru z vládních stránek data.gov.cz, který se pravidelně aktualizuje. Při rozkliknutí jednotlivých bodů si můžeme zobrazit název čidla, přesnou adresu, v jaké jsou obci, jaký mají stav, jaký mají tok, výšku jejich hladiny v cm a čas, kdy informace byla naposledy aktualizovaná. Hranice kraje jsou zobrazeny pomocí geoJson souboru obsahujícího souřadnice o hranicích ústeckého kraje, vnitřek hranic je vyznačený světle modrou barvou. Mapa je vytvořena pomocí knihovny Folium. Mapa se v určitém rozmezí přibližovat a oddalovat. Zelené body symbolizují normální stav, žluté suchý stav, červené extrémní stav


