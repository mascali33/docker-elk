#!/usr/bin/env python3

import os
import json

def parse_log_line(line):
    parts = line.strip().split('\t')
    print(f"Parsing line: {line.strip()} -> Parts: {len(parts)}")  # Debug: print parts count
    if len(parts) < 5:
        print("Skipping line: insufficient parts")  # Debug: indicate skipped line
        return None
    log_entry = {
        "code": parts[0],
        "date": parts[1],
        "time": parts[2],
        "side": parts[3],
        "description": parts[4]
    }
    # Add optional fields if present
    if len(parts) > 5:
        log_entry["additional"] = parts[5]
    if len(parts) > 6:
        log_entry["signal_strength"] = parts[6]
    return log_entry


def process_directory(directory):
    logs = []
    for filename in os.listdir(directory):
        if filename.endswith('.his'):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")  # Debug: print file being processed
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        log_entry = parse_log_line(line)
                        if log_entry:
                            logs.append(log_entry)
            except UnicodeDecodeError:
                # Try a different encoding if UTF-8 fails
                with open(file_path, 'r', encoding='iso-8859-1') as file:
                    for line in file:
                        log_entry = parse_log_line(line)
                        if log_entry:
                            logs.append(log_entry)
    if not logs:
        print("No logs were added.")  # Debug: indicate if no logs were collected
    return logs

def save_as_json(logs, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)

# Usage
directory = '.'  # Set to your directory containing .his files
output_json_file = 'billing.json' # Set the desired output JSON file path

logs = process_directory(directory)
save_as_json(logs, output_json_file)

print(f"Processed logs saved to {output_json_file}")

