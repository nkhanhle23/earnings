#!/bin/sh
dolt sql-server -u root &
python app.py
