#!/usr/bin/env python3
"""
PDF to Markdown Converter Script
Converts all PDF files in the Knowledge folder to Markdown format.

Requirements:
- pip install PyPDF2 pdfplumber
- pip install python-docx (if handling other document types)

Usage:
    python pdf_to_markdown_converter.py
"""

import os
import sys
import re
from pathlib import Path
import logging
from datetime import datetime

try:
    import PyPDF2
    import pdfplumber
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Please install required packages:")
    print("pip install PyPDF2 pdfplumber")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PDFToMarkdownConverter:
    def __init__(self, knowledge_folder_path):
        self.knowledge_folder = Path(knowledge_folder_path)
        self.output_folder = self.knowledge_folder / "markdown_output"
        self.conversion_stats = {
            'total_files': 0,
            'successful_conversions': 0,
            'failed_conversions': 0,
            'errors': []
        }
        
        # Create output directory if it doesn't exist
        self.output_folder.mkdir(exist_ok=True)
        
    def clean_filename(self, filename):
        """Clean filename for valid markdown file naming."""
        # Remove .pdf extension
        name = filename.replace('.pdf', '')
        # Replace spaces with underscores
        name = name.replace(' ', '_')
        # Remove special characters except underscores and hyphens
        name = re.sub(r'[^\w\-_]', '', name)
        # Ensure it doesn't start with a number
        if name and name[0].isdigit():
            name = f"doc_{name}"
        return f"{name}.md"
    
    def extract_text_with_pdfplumber(self, pdf_path):
        """Extract text using pdfplumber (better for complex layouts)."""
        text_content = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        text_content.append(f"## Page {page_num}\n\n{text}\n")
                    else:
                        text_content.append(f"## Page {page_num}\n\n*[No text content found on this page]*\n")
        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber from {pdf_path}: {e}")
            return None
            
        return "\n".join(text_content)
    
    def extract_text_with_pypdf2(self, pdf_path):
        """Extract text using PyPDF2 (fallback method)."""
        text_content = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"## Page {page_num}\n\n{text}\n")
                    else:
                        text_content.append(f"## Page {page_num}\n\n*[No text content found on this page]*\n")
        except Exception as e:
            logger.error(f"Error extracting text with PyPDF2 from {pdf_path}: {e}")
            return None
            
        return "\n".join(text_content)
    
    def format_as_markdown(self, text, original_filename):
        """Format extracted text as proper markdown."""
        if not text:
            return None
            
        # Create markdown header
        markdown_content = f"""# {original_filename.replace('.pdf', '')}

*Converted from PDF on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

{text}

---

*End of document*
"""
        return markdown_content
    
    def convert_pdf_to_markdown(self, pdf_path):
        """Convert a single PDF file to Markdown."""
        logger.info(f"Converting: {pdf_path.name}")
        
        # Try pdfplumber first (better for complex layouts)
        text = self.extract_text_with_pdfplumber(pdf_path)
        
        # Fallback to PyPDF2 if pdfplumber fails
        if not text or not text.strip():
            logger.info(f"pdfplumber failed for {pdf_path.name}, trying PyPDF2...")
            text = self.extract_text_with_pypdf2(pdf_path)
        
        if not text or not text.strip():
            error_msg = f"Failed to extract text from {pdf_path.name}"
            logger.error(error_msg)
            self.conversion_stats['errors'].append(error_msg)
            return False
        
        # Format as markdown
        markdown_content = self.format_as_markdown(text, pdf_path.name)
        
        if not markdown_content:
            error_msg = f"Failed to format markdown for {pdf_path.name}"
            logger.error(error_msg)
            self.conversion_stats['errors'].append(error_msg)
            return False
        
        # Save markdown file
        output_filename = self.clean_filename(pdf_path.name)
        output_path = self.output_folder / output_filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            logger.info(f"Successfully converted: {pdf_path.name} -> {output_filename}")
            return True
        except Exception as e:
            error_msg = f"Failed to save markdown file for {pdf_path.name}: {e}"
            logger.error(error_msg)
            self.conversion_stats['errors'].append(error_msg)
            return False
    
    def convert_all_pdfs(self):
        """Convert all PDF files in the Knowledge folder."""
        logger.info(f"Starting PDF to Markdown conversion in: {self.knowledge_folder}")
        
        # Find all PDF files
        pdf_files = list(self.knowledge_folder.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning("No PDF files found in the Knowledge folder")
            return
        
        self.conversion_stats['total_files'] = len(pdf_files)
        logger.info(f"Found {len(pdf_files)} PDF files to convert")
        
        # Convert each PDF
        for pdf_file in pdf_files:
            if self.convert_pdf_to_markdown(pdf_file):
                self.conversion_stats['successful_conversions'] += 1
            else:
                self.conversion_stats['failed_conversions'] += 1
        
        # Print summary
        self.print_conversion_summary()
    
    def print_conversion_summary(self):
        """Print conversion summary."""
        stats = self.conversion_stats
        
        print("\n" + "="*60)
        print("PDF TO MARKDOWN CONVERSION SUMMARY")
        print("="*60)
        print(f"Total PDF files found: {stats['total_files']}")
        print(f"Successfully converted: {stats['successful_conversions']}")
        print(f"Failed conversions: {stats['failed_conversions']}")
        print(f"Success rate: {(stats['successful_conversions']/stats['total_files']*100):.1f}%")
        
        if stats['errors']:
            print(f"\nErrors encountered:")
            for error in stats['errors']:
                print(f"  - {error}")
        
        print(f"\nMarkdown files saved to: {self.output_folder}")
        print("="*60)

def main():
    """Main function to run the PDF to Markdown converter."""
    # Get the script directory (Knowledge folder)
    script_dir = Path(__file__).parent
    knowledge_folder = script_dir
    
    # Check if we're in the right directory
    if not knowledge_folder.exists():
        logger.error(f"Knowledge folder not found: {knowledge_folder}")
        sys.exit(1)
    
    # Initialize converter
    converter = PDFToMarkdownConverter(knowledge_folder)
    
    # Run conversion
    try:
        converter.convert_all_pdfs()
    except KeyboardInterrupt:
        logger.info("Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
