# Spotify Visualizations

## Requirements
- [Anaconda](https://docs.anaconda.com/anaconda/install/) (this project uses `conda` commands for maintaining viritual environments)
- python 3.6+

## Setup
In the root directory of the repository run the following commands:

```Shell
>> conda env create -f environment.yml  
>> conda deactivate
>> conda activate spotify 
```

Copy config.template.py to config.py and enter your spotify developer credentials

---

## Run analysis

```Shell
>> python data.py
```

## Spotify's Documentation
To get more details on what the Y axis means on some of the graphs
look [here](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/) at Spotify's developer documentation.
