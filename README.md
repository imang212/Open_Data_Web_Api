## Webová aplikace nad otevřenými daty
Zpracování otevřených dat z informačního systému veřejné správy  povodňových čidel.

**Použití dat z data.gov.cz**
- Aktuální stav na povodňových čidlech Ústeckého kraje
- Přehled hlásných profilů Ústeckého kraje


**Autoři:** Tomáš Ladislav Kotek, Patrik Poklop, Matěj Sloup

**Technologie:** Python, Backend: FastApi, Frontend: Streamlit, Folium, Docker

#### Spuštění aplikace
Stačí mít docker a v kořenovém adresáři *Open_Data_Web_Api/* zadat do příkazové řádky *docker-compose up --build*.
Docker-compose je rozdělený na backend a frontend konteiner. Nám stačí spustit frontend na *localhost:8501*. 


