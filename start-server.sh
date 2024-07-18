#!/bin/bash
source env/bin/activate
pip install -r requirements.txt
python3 src/api.py
