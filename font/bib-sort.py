#!/usr/bin/env python3
"""
Script to process bibliography entries:
1. Remove unused entries from ref.bib that don't appear in main.tex
2. Sort entries in ref.bib by their appearance order in main.tex
3. Export the processed bibliography to ref_output.bib

Use:
python font/bib-sort.py

"""

import re
import sys
from collections import OrderedDict

def extract_citations_from_tex(tex_file):
    """
    Extract all citation keys from a LaTeX file.
    
    Args:
        tex_file (str): Path to the LaTeX file
        
    Returns:
        set: Set of citation keys found in the LaTeX file
    """
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all citation commands
    citation_patterns = [
        r'\\cite\{([^}]+)\}',
        r'\\citep\{([^}]+)\}',
        r'\\citet\{([^}]+)\}',
        r'\\citeauthor\{([^}]+)\}',
        r'\\citeyear\{([^}]+)\}',
        r'\\citeyearpar\{([^}]+)\}',
        r'\\autocite\{([^}]+)\}',
        r'\\nocite\{([^}]+)\}'
    ]
    
    citations = set()
    
    for pattern in citation_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            # Handle multiple citations in one command (e.g., \cite{key1,key2,key3})
            keys = match.split(',')
            for key in keys:
                citations.add(key.strip())
    
    return citations

def parse_bib_file(bib_file):
    """
    Parse a bibliography file and extract entries.
    
    Args:
        bib_file (str): Path to the .bib file
        
    Returns:
        dict: Dictionary with entry names as keys and entry content as values
    """
    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all bibliography entries
    entry_pattern = r'(@\w+\{([^,\n]+),.*?\n\s*\})'
    entries = {}
    
    # Use DOTALL flag to match across multiple lines
    matches = re.findall(entry_pattern, content, re.DOTALL)
    
    for full_entry, entry_name in matches:
        entries[entry_name.strip()] = full_entry
    
    return entries

def filter_and_sort_bib_entries(bib_entries, citation_keys):
    """
    Filter bibliography entries to only include cited ones and sort by appearance order.
    
    Args:
        bib_entries (dict): All bibliography entries
        citation_keys (set): Set of citation keys used in the LaTeX file
        
    Returns:
        OrderedDict: Filtered and sorted bibliography entries
    """
    # Filter entries to only include cited ones
    filtered_entries = {}
    for key in citation_keys:
        if key in bib_entries:
            filtered_entries[key] = bib_entries[key]
    
    # Sort entries by their order of appearance in the citation list
    sorted_entries = OrderedDict()
    for key in citation_keys:
        if key in filtered_entries:
            sorted_entries[key] = filtered_entries[key]
    
    return sorted_entries

def write_bib_file(entries, output_file):
    """
    Write bibliography entries to a file.
    
    Args:
        entries (OrderedDict): Bibliography entries to write
        output_file (str): Path to the output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in entries.values():
            f.write(entry + '\n\n')

def main():
    """
    Main function to process bibliography files.
    """
    # Input and output file names
    tex_file = 'main.tex'
    bib_file = 'ref.bib'
    output_file = 'ref_output.bib'
    
    try:
        # Extract citations from LaTeX file
        print(f"Extracting citations from {tex_file}...")
        citations = extract_citations_from_tex(tex_file)
        print(f"Found {len(citations)} unique citations")
        
        # Parse bibliography file
        print(f"Parsing bibliography entries from {bib_file}...")
        bib_entries = parse_bib_file(bib_file)
        print(f"Found {len(bib_entries)} entries in bibliography")
        
        # Filter and sort entries
        print("Filtering and sorting entries...")
        processed_entries = filter_and_sort_bib_entries(bib_entries, citations)
        print(f"Kept {len(processed_entries)} cited entries")
        
        # Write processed bibliography to output file
        print(f"Writing processed bibliography to {output_file}...")
        write_bib_file(processed_entries, output_file)
        print("Processing complete!")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()