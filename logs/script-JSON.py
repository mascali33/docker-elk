#!/usr/bin/env python3

import os
import json

def parse_log_line(line, counter):
    parts = line.strip().split('\t')
    print(f"Parsing line: {line.strip()} -> Parts: {len(parts)}")  # Debug: print parts count
    if len(parts) < 5:
        print("Skipping line: insufficient parts")  # Debug: indicate skipped line
        return None
    log_entry = {
    	"id": counter,
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

def process_file(file_path):
    logs = []
    counter = 1
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                log_entry = parse_log_line(line, counter)
                if log_entry:
                    logs.append(log_entry)
                    counter += 1
    except UnicodeDecodeError:
        # Try a different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            for line in file:
                log_entry = parse_log_line(line, counter)
                if log_entry:
                    logs.append(log_entry)
                    counter += 1
    return logs

def save_as_json(logs, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.his'):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")  # Debug: print file being processed
            logs = process_file(file_path)
            if logs:
                output_json_file = f"{filename[:-4]}.json"  # Create JSON file name based on HIS file
                save_as_json(logs, os.path.join(directory, output_json_file))
                print(f"Processed logs saved to {output_json_file}")
            else:
                print(f"No logs were added for {filename}.")  # Debug: indicate if no logs were collected

# Usage
directory = '.'  # Set to your directory containing .his files
process_directory(directory)

