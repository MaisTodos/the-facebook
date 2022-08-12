#!/bin/bash
cd thefacebook
python dynamodb_create_tables.py
chalice local --host 0.0.0.0 --port 8108
