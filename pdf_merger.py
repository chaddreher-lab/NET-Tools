from PyPDF2 import PdfMerger

def merge_pdfs(pdf_list, output_name):
    """Merge multiple PDFs into one."""
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_name)
    merger.close()
    print(f"Merged PDFs into {output_name}")
