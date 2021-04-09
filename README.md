# INF142 Project - Fictional Meteorological Institute (FMI)

---

### Mandatory assignment 2

**Authors:** Tor Anders, Eirin, Rakel, Thea og Sindre

## Build & Run

---
- Clone project from github
- Once downloaded, run the files:
  - [weather_station.py](src/weather_station/weather_station.py)
    - the station will begin transmitting as soon as it's run, and will continue to do so until it is stopped
  - [storage_server.py](src/storage_server/storage_server.py)
    - Does not need [weather_station.py](src/weather_station/weather_station.py) to function, only to get new data 
  - [fmi.py](src/app/fmi.py)
    - Both [fmi.py](src/app/fmi.py) and [storage_server.py](src/storage_server/storage_server.py) needs to be running to be able to view data in browser (`localhost:5000`)
    - Some issues with this script, see known bugs section.

---
## Extra features

- Using MongoDB for cloud-database storage
- Flask to generate HTML based on template

---
## Known bugs
- The user-agent ([fmi.py](src/app/fmi.py) is only able to get data once each run. Refreshing the page in the browser will not work
  as the connection to [storage_server.py](src/storage_server/storage_server.py) gets denied when doing this. Our temporary fix to this
  is to restart both scripts.
