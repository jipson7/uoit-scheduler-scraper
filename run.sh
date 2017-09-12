#!/bin/bash

source env/bin/activate

export SCRAPE_DATABASE=sqlite:///schedule.db 
#export SCRAPE_DATABASE=postgres://fuxkqlurxyswbe:YlAF78BEc4V1gI4iTPvDW3p08J@ec2-54-225-165-132.compute-1.amazonaws.com:5432/dk2124iurbta4

python scraper/scrape.py $1
