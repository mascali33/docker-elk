#!/usr/bin/env python3

import os
import json
import re
from datetime import datetime

def process_file(file_path, output_file):
    counter = 1
    logs = []
    try:
        with open(file_path, 'r', encoding='iso-8859-1') as file:  # Directly use ISO-8859-1
            for line in file:
                log_entry = parse_log_line(line, counter)
                if log_entry:
                    logs.append(json.dumps(log_entry) + '\n')
                    counter += 1
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

    # Write the logs to the output file after processing
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(logs)

def parse_type_details(type_str):
    details = {}
    if type_str.startswith("Appel:"):
        details['type'] = 'appel'
        regex = r"Appel:(\d+) MS:(\d+) vers GRP:(\d+) Type:(.*?/.*?/.*?) BS:(.*?) dBm:(.*?)$"
        match = re.match(regex, type_str)
        if match:
            details.update({
                'call_number': match.group(1),
                'ms': match.group(2),
                'grp': match.group(3),
                'call_type': match.group(4).replace('/', '-'),
                'bs': match.group(5),
                'dbm': match.group(6)
            })

    elif type_str.startswith("Etabl Com:"):
        details['type'] = 'com'
        regex = r"Etabl Com:(\d+) MS:(\d+) vers GRP:(\d+) Type:(.*?/.*?/.*?) BS:(.*?),(.*?)$"
        match = re.match(regex, type_str)
        if match:
            details.update({
                'com_number': match.group(1),
                'ms': match.group(2),
                'grp': match.group(3),
                'call_type': match.group(4).replace('/', '-'),
                'bs': match.group(5) + ',' + match.group(6)
            })

    # Ajoutez d'autres motifs selon le même schéma ici...

    return details

def parse_log_line(line, counter):
    parts = line.strip().split('\t')
    if len(parts) < 5:
        print("Skipping line: insufficient parts")
        return None

    try:
        date_obj = datetime.strptime(parts[1] + ' ' + parts[2], '%y-%m-%d %H:%M:%S')
        formatted_date_time = datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print(f"Date format error: {e} in line: {line.strip()}")
        return None

    log_entry = {
        "id": counter,
        "timestamp": formatted_date_time,
        "event": parts[0][0] if parts[0] else None,
        "code": parts[0],
        "switch": parts[3],
    }

    type_str = parts[4]
    # Regular expressions for various type formats
    patterns = {
        'appel': re.compile(r"Appel:(\d+) MS:(\d+) vers .* Type:(.+?) BS:(.+?) dBm:(.+)"),
        'com': re.compile(r"Etabl Com:(\d+) MS:(\d+) vers .* Type:(.+?) BS:(.+)"),
        'inscription': re.compile(r"Inscr MS:(\d+) BS:(.+?) accepté +dBm:(.+)"),
        'assGr': re.compile(r"AssGr MS:(\d+) GRP:(\d+)"),
        'DesAssGr': re.compile(r"DesAssGr MS:(\d+) GRP:(\d+)"),
        'liber_com': re.compile(r"Liber Com:(\d+) : Déconnexion demandée par le (.*)$"),
        'xcell': re.compile(r"Xcell MS:(\d+) BS:(.+)"),
        'sds': re.compile(r"SDS de MS:(\d+) vers PO:(\d+) bits:(\d+) BS:(.+) dBm:(.+)"),
        'status': re.compile(r"Status:(\d+)\(Appel Normal\) MS:(\d+) vers Dispatch:(\d+)"),
        'assDynGrp': re.compile(r"AssDynGrp MS:(\d  +) GRP:(\d+)"),
        'desassociationGrp': re.compile(r"DésassDynGrp MS:(\d+) GRP:(\d+)")
    }

    # Check each pattern and extract data
    try:
    # Extraction logic
        for type_key, pattern in patterns.items():
            match = pattern.search(type_str)
            if match:
                log_entry['type'] = type_key
                if type_key in ['appel', 'com', 'inscription', 'xcell', 'sds', 'status']:
                    log_entry.update({
                        'ms': match.group(2),
                        'bs': match.group(4)
                    })
                    if type_key == 'appel':
                        log_entry.update({
                            'call_number': match.group(1),
                            'call_type': match.group(3),
                            'dbm': match.group(5)
                        })
                    elif type_key == 'com':
                        log_entry.update({
                            'com_number': match.group(1),
                            'call_type': match.group(3)
                        })
                    elif type_key == 'inscription':
                        log_entry.update({
                            'dbm': match.group(3)
                        })
                    elif type_key == 'sds':
                        log_entry.update({
                            'po': match.group(3),
                            'bits': match.group(4),
                            'dbm': match.group(5)
                        })
                    elif type_key == 'status':
                        log_entry.update({
                            'status_number': match.group(1),
                            'dispatch': match.group(3)
                        })
                elif type_key in ['assGr', 'assDynGrp', 'desassociationGrp']:
                    log_entry.update({
                        'grp': match.group(2)
                    })
                elif type_key == 'liber_com':
                    log_entry.update({
                        'com_number': match.group(1),
                        'disconnect_order': match.group(2)
                    })
                break
    except AttributeError:  # Typical error thrown when regex match fails
        print(f"Failed to parse line {counter}: {line}")
        return None
    
    return log_entry

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.his'):
            file_path = os.path.join(directory, filename)
            output_ndjson_file = f"{filename[:-4]}.ndjson"
            print(f"Processing file: {file_path}")
            process_file(file_path, os.path.join(directory, output_ndjson_file))
            print(f"Processed logs saved to {output_ndjson_file}")

# Usage
directory = '.'  # Set to your directory containing .his files
process_directory(directory)
