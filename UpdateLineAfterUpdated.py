import os
import re
import json
from difflib import SequenceMatcher

STRING_PATTERN = re.compile(r'"((?:\\"|\\\\|\\[^"]|[^"\\])*)"')

def calculate_line_mapping(original_lines, modified_lines):
    matcher = SequenceMatcher(None, original_lines, modified_lines)
    line_map = {}
    for op in matcher.get_opcodes():
        tag, i1, i2, j1, j2 = op
        if tag == 'equal':
            for delta in range(i2 - i1):
                line_map[i1 + delta] = j1 + delta
    return line_map

def write(original, after, jsonn, output):
    with open(jsonn, mode="r", encoding="utf-8") as f:
        old_mappings = json.load(f)
    
    print(f"\nProcessing file: {os.path.basename(after)}")
    
    with open(original, "r", encoding="utf-8") as f:
        orig_lines = f.readlines()
    with open(after, "r", encoding="utf-8") as f:
        after_lines = f.readlines()
    
    line_mapping = calculate_line_mapping(orig_lines, after_lines)
    new_mappings = {}
    
    for old_key, value in old_mappings.items():
        try:
            if old_key.count(":") != 1:
                raise ValueError
            filename, orig_lineno = old_key.split(":")
            orig_lineno = int(orig_lineno)
        except:
            print(f"Invalid key format: {old_key}")
            continue

        if orig_lineno >= len(orig_lines):
            print(f"Original line out of range: {old_key}")
            continue
            
        new_lineno = line_mapping.get(orig_lineno)
        if new_lineno is None:
            print(f"No line mapping for: {old_key}")
            continue
            
        try:
            orig_line = orig_lines[orig_lineno]
            new_line = after_lines[new_lineno]
        except IndexError:
            print(f"Line number out of bounds: {old_key}")
            continue

        orig_match = STRING_PATTERN.search(orig_line)
        if not orig_match:
            print(f"No string found in original line: {old_key}")
            continue
            
        target_str = orig_match.group(1)
        print(f"Found string '{target_str}' at original line {orig_lineno}")

        new_match = STRING_PATTERN.search(new_line)
        if not new_match:
            print(f"No string in new line: {old_key}")
            continue
            
        if new_match.group(1) != target_str:
            print(f"String mismatch: {old_key} | Original: '{target_str}' New: '{new_match.group(1)}'")
            continue

        new_key = f"{filename}:{new_lineno}"
        new_mappings[new_key] = value
        print(f"Mapped to new position: {new_key}")

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        f.write(json.dumps(new_mappings, indent=4, separators=(",", ": "), ensure_ascii=False))
    print(f"\nSuccessfully generated: {output}")

original = input("Original file: ").replace("\\", "/")
after = input("Current file: ").replace("\\", "/")
jsonn = input("JSON file: ").replace("\\", "/")
output = input("Output file (default in Repacked folder next to JSON file): ").replace("\\", "/")
if not output:
    output = os.path.join(os.path.dirname(jsonn), "Repacked", os.path.basename(jsonn))

write(original, after, jsonn, output)