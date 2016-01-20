#!/bin/bash

source env/bin/activate

export SCRAPE_DATABASE=sqlite:///schedule.db 

python scraper/scrape.py $1
