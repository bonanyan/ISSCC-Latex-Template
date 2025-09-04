import sys
import importlib
import os

def check_requirements():
    """
    Check if required modules are installed
    """
    missing_modules = []
    
    # shutil is part of standard library, so it should always be available
    try:
        import shutil
    except ImportError:
        missing_modules.append('shutil')
    
    # Check for PyPDF2
    try:
        import PyPDF2
    except ImportError:
        missing_modules.append('PyPDF2')
    
    return missing_modules

def process_pdf(pdf_name):
    """
    Process the PDF file - copy and truncate to first 5 pages
    """
    import shutil
    from PyPDF2 import PdfReader, PdfWriter
    
    # Remove .pdf extension if provided
    base_name = pdf_name.replace('.pdf', '') if pdf_name.endswith('.pdf') else pdf_name
    
    input_file = f"{base_name}.pdf"
    backup_file = f"{base_name}_with_ref.pdf"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        sys.exit(1)
    
    # Step 1: Copy main.pdf to main_with_ref.pdf
    shutil.copy2(input_file, backup_file)
    print(f"Copied {input_file} to {backup_file}")
    
    # Step 2: Read the original file and keep only first 5 pages
    reader = PdfReader(backup_file)
    writer = PdfWriter()
    
    # Add only the first 5 pages (or all pages if less than 5)
    num_pages = min(len(reader.pages), 5)
    for page_num in range(num_pages):
        writer.add_page(reader.pages[page_num])
    
    # Step 3: Export to original filename
    with open(input_file, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"Success! Kept {num_pages} pages in {input_file}")

def main():
    # Check if PDF name is provided as argument
    if len(sys.argv) < 2:
        print("Usage: python split-pdf.py <pdf_name>")
        print("Example: python split-pdf.py main.pdf")
        sys.exit(1)
    
    pdf_name = sys.argv[1]
    
    # Check requirements
    missing = check_requirements()
    
    if missing:
        print("Missing required modules:")
        for module in missing:
            print(f"  - {module}")
        
        if 'PyPDF2' in missing:
            print("\nPlease install PyPDF2 using:")
            print("  pip install PyPDF2")
        sys.exit(1)
    else:
        print("All requirements satisfied.")
        process_pdf(pdf_name)

if __name__ == "__main__":
    main()