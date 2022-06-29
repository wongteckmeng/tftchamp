
[![Python 3.8](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

![tftfi00](./assets/tft_feature_importances_12.12.450.4196.png)
 <!-- ![tftfi](./assets/tft_feature_importances.png) -->
 
## Requirements

To develop and use this code, you will need:

- a Riot Games Developer account at <https://developer.riotgames.com/>
- a Riot Games API key

In your `.bashrc`, `.zshrc`, or equivalet, export the Riot Games API key as `RIOT_API_KEY`.

```
export RIOT_API_KEY="RGAPI-blah-blah-blah"
```

```
SERVER = 'na1'  # euw1 na1 kr oc1
LEAGUE='challengers'
MAX_COUNT = 30
```

```
cd backend/app
python3 scape.py
```