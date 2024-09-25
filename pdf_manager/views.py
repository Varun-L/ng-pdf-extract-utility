import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import requests
from django.core.files import File
from io import BytesIO

PDF_STORAGE_DIR = 'pdf_storage'

def index(request):
    pdf_files = []
    for filename in os.listdir(PDF_STORAGE_DIR):
        pdf_files.append(filename)
    return render(request, 'pdf_manager/index.html', {'pdf_files': pdf_files})

def download_pdf(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        response = requests.get(url,verify = False)
        pdf_file_name = url.split('/')[-1]
        with open(os.path.join(PDF_STORAGE_DIR, pdf_file_name), 'wb+') as destination:
            for chunk in response.iter_content(1024):
                destination.write(chunk)
        return redirect('index')
    else:
        return render(request, 'pdf_manager/download_pdf.html')

def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage(location=PDF_STORAGE_DIR)
        filename = fs.save(pdf_file.name, pdf_file)
        return redirect('index')
    return render(request, 'pdf_manager/upload_pdf.html')

def pdf_parser(request):
    if request.method == 'POST':
        pdf_file_name = request.POST.get('pdf_file_name')
        page_numbers = request.POST.get('page_numbers')
        search_string = request.POST.get('search_string')
        rect_coords = request.POST.get('rect_coords')

        # PyMuPDF integration
        import fitz
        doc = fitz.open(os.path.join(PDF_STORAGE_DIR, pdf_file_name))
        pages = [doc.load_page(int(i)) for i in page_numbers.split(',')]
        text = ''
        for page in pages:
            text += page.get_text()

        if search_string:
            for page in pages:
                rect = page.search_for(search_string)
                if rect:
                    text += f'\nSearch result: {rect[0]}'

        if rect_coords:
            x1, y1, x2, y2 = map(float, rect_coords.split(','))
            rect = fitz.Rect(x1, y1, x2, y2)
            for page in pages:
                text += f'\nRect text: {page.get_text("text", clip=rect)}'

        return render(request, 'pdf_manager/pdf_parser.html', {'text': text})
    return render(request, 'pdf_manager/pdf_parser.html')

def regex_extractor(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        regex_pattern = request.POST.get('regex_pattern')
        try:
            import re
            matches = re.findall(regex_pattern, text)
            return render(request, 'pdf_manager/regex_extractor.html', {'matches': matches})
        except re.error as e:
            return render(request, 'pdf_manager/regex_extractor.html', {'error': f'Invalid regex pattern: {e}'})
    return render(request, 'pdf_manager/regex_extractor.html')