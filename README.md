
[![Python 3.8](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

![tftfi00](./assets/tft_feature_importances_12.12.450.4196.png)
 <!-- ![tftfi](./assets/tft_feature_importances.png) -->
 

##
Datasets publish @
https://www.kaggle.com/datasets/teckmengwong/team-fight-tactics-matches

## Requirements

To develop and use this code, you will need:

- a Riot Games Developer account at <https://developer.riotgames.com/>
- a Riot Games API key

In your `.bashrc`, `.zshrc`, or equivalet, export the Riot Games API key as `RIOT_API_KEY`.
For windows, in your sys/user environment.

```
export RIOT_API_KEY="RGAPI-blah-blah-blah"
```

- Python >= `3.10`
- Packages included in `requirements.txt` file
- (Anaconda for easy installation)

### Python virtual env setup
For local setup, I recommend to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html), a minimal version of the popular [Anaconda](https://www.anaconda.com/) distribution that contains only the package manager `conda` and Python. Follow the installation instructions on the [Miniconda Homepage](https://docs.conda.io/en/latest/miniconda.html).

After installation of Anaconda/Miniconda, run the following command(s) from the project directory:

### Install dependencies
Conda virtual environment:
```sh
conda create --name myenv python=3.10
conda activate myenv
conda install --file requirements.txt -c conda-forge
```

As **Conda has limited package support for python 3.10** activate your virtual environment and install the dependencies using

```sh
pip install -r requirements.txt
```

## Usage for Jupyter Notebook
Activate and install the correct python3 virtual environment before proceeding.

```sh
jupyter notebook
```

## Scraping script /backend/app/scrape.py

Config:
```
SERVER = 'na1'  # euw1 na1 kr oc1
LEAGUE='challengers'
MAX_COUNT = 30
```

To run:
```
cd backend/app
python3 scrape.py
```