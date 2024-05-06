#!/usr/bin/env python3

import os
import json

def check_ndjson(path):
    if not os.path.exists(path):
        print(f"No file found at {path}")
        return

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                try:
                    # Attempt to load each line as a JSON object to check its integrity
                    json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Error in line {i + 1}: {e} - {line.strip()}")
    except Exception as e:
        print(f"An error occurred when trying to read the file: {e}")

# Assuming your NDJSON file is named 'output.ndjson'
check_ndjson('etelm-logs-001.ndjson')

