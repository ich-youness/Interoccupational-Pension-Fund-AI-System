# PDF to Markdown Converter

This script automatically converts all PDF files in the Knowledge folder to Markdown format for easier text processing and analysis.

## Features

- **Automatic PDF Detection**: Finds all PDF files in the current directory
- **Dual Extraction Methods**: Uses both pdfplumber and PyPDF2 for maximum compatibility
- **Clean Filename Generation**: Converts PDF filenames to valid markdown filenames
- **Structured Output**: Creates organized markdown with page headers
- **Comprehensive Logging**: Tracks conversion progress and errors
- **Conversion Statistics**: Provides detailed summary of results

## Quick Start

### Option 1: Windows Batch File (Recommended)
1. Double-click `convert_pdfs.bat`
2. The script will automatically install dependencies and run the conversion
3. Check the `markdown_output` folder for converted files

### Option 2: Manual Python Execution
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the converter:
   ```bash
   python pdf_to_markdown_converter.py
   ```

## Output

- **Markdown Files**: Saved in `markdown_output/` folder
- **Log File**: `pdf_conversion.log` contains detailed conversion logs
- **Console Output**: Real-time progress and summary statistics

## File Naming

Original PDF files are converted to clean markdown filenames:
- `Brochure Questions-réponses AGO 2018 -.pdf` → `Brochure_Questions-réponses_AGO_2018.md`
- `Charte de Communication Responsable.pdf` → `Charte_de_Communication_Responsable.md`

## Markdown Structure

Each converted file includes:
- Document title (from original filename)
- Conversion timestamp
- Page-by-page content with headers
- Clean formatting for readability

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Run: `pip install -r requirements.txt`

2. **Permission Errors**
   - Ensure you have write permissions in the Knowledge folder
   - Run as administrator if needed

3. **PDF Extraction Failures**
   - Some PDFs may have complex layouts or be image-based
   - Check the log file for specific error details

4. **Encoding Issues**
   - The script uses UTF-8 encoding for maximum compatibility
   - Special characters in French text are preserved

### Log Files

Check `pdf_conversion.log` for detailed information about:
- Which files were processed
- Any extraction errors
- Conversion statistics
- Performance metrics

## Technical Details

### Dependencies
- **PyPDF2**: Primary PDF text extraction
- **pdfplumber**: Advanced PDF processing for complex layouts
- **pathlib**: Modern file path handling
- **logging**: Comprehensive error tracking

### Extraction Methods
1. **pdfplumber**: Attempts extraction first (better for complex layouts)
2. **PyPDF2**: Fallback method (more reliable for simple PDFs)

### Error Handling
- Graceful fallback between extraction methods
- Detailed error logging
- Continues processing even if individual files fail
- Comprehensive conversion statistics

## Customization

To modify the script behavior, edit `pdf_to_markdown_converter.py`:

- **Output Format**: Modify `format_as_markdown()` method
- **File Naming**: Adjust `clean_filename()` method
- **Text Processing**: Customize text extraction in the extraction methods
- **Logging**: Modify logging configuration at the top of the script

## Support

For issues or questions:
1. Check the log file for error details
2. Verify all dependencies are installed
3. Ensure PDF files are not corrupted or password-protected
4. Check file permissions in the Knowledge folder
