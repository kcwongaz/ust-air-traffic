# This Project

Using historical flight trajectory data, can you come up with a quantitive strategy for mitigating flight delay?

This is a project I have worked on with Prof. Michael K. Y. Wong and Prof. Rhea Liem during my MPhil at HKUST. A detailed description of this project can be found in Chapter 4 of my [MPhil thesis](https://drive.google.com/file/d/1wgr3l9psxnW8qiUr-FL-vXN2wRbjcxAC/view?usp=sharing).

This repo contains the code I developed for analyzing historical flight trajectories around the Hong Kong International Airport (HKIA). The flight data used was originally obtained by Prof. Lishuai Li from the City University of Hong Kong and shared with us. Special thanks to Prof. Li for allowing me to release part of the flight data in this repo.

Some example analyses can be found in the notebooks.

<br>

# Getting Started

## 1 - Setting up
I suggest installing the code locally, e.g.

```bash
git clone https://github.com/kcwongaz/ust-air-traffic
cd ust-air-traffic
pip -e install .  # -e flag for editable mode
```

This project requires the standard scientific packages, `numpy`, `scipy`, `matplotlib` and `pandas`. In addition, `Cartopy` is needed for drawing maps, and `geopy` is used to compute geodesic distances.

<br>

## 2 - Data
An example dataset can be downloaded here. 

The example dataset contains the flight data in Jan 2017. Decompressing the data to `data/` at the project root should get the jupyter notebooks to run.

If you are interested to see the raw data, here is an example dataset. The raw data is quite large in file size, so I can only provide 3 days of data. To process the raw data, decompress the raw data to `raw/` at the project root, then run

```bash
. ./pipeline/start.sh 
```

The scripts in `pipeline/` perform successive processing to prepare the data, e.g. by computing various useful statistics, for further analysis.

<br>

## 3 - Quick walkthrough

`air_traffic/`: main package
 - `FR24Writer.py`, `filters.py`:  for processing raw data
 - `io.py`:  I/O handlers
 - `loop.py`:  module for analyzing holding patterns and rescheduling
 - `temporal.py`:  module for analyzing from a time-series perspective
 - `trajectory.py`:  utility functions for working with flight trajectories
 - `visual.py`:  utility functions for drawing
