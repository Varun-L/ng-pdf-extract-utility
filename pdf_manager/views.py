import fitz
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PdfDownloadForm, PdfParserForm, RegexExtractorForm
from .models import PdfFile
import requests
from django.core.files import File
from io import BytesIO

def index(request):
    pdf_files = PdfFile.objects.all()
    return render(request, 'pdf_manager/index.html', {'pdf_files': pdf_files})

def download_pdf(request):
    if request.method == 'POST':
        form = PdfDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            response = requests.get(url)
            pdf_file = PdfFile(name=url.split('/')[-1], file=File(BytesIO(response.content), name=url.split('/')[-1]))
            pdf_file.save()
            messages.success(request, 'PDF downloaded successfully!')
            return redirect('index')
    else:
        form = PdfDownloadForm()
    return render(request, 'pdf_manager/download_pdf.html', {'form': form})

def pdf_parser(request):
    if request.method == 'POST':
        form = PdfParserForm(request.POST)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            page_numbers = form.cleaned_data['page_numbers']
            search_string = form.cleaned_data['search_string']
            rect_coords = form.cleaned_data['rect_coords']

            doc = fitz.open(pdf_file.file.path)
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

            return render(request, 'pdf_manager/pdf_parser.html', {'form': form, 'text': text})
    else:
        form = PdfParserForm()
    return render(request, 'pdf_manager/pdf_parser.html', {'form': form})

def regex_extractor(request):
    if request.method == 'POST':
        form = RegexExtractorForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            regex_pattern = form.cleaned_data['regex_pattern']
            try:
                matches = re.findall(regex_pattern, text)
                return render(request, 'pdf_manager/regex_extractor.html', {'form': form, 'matches': matches})
            except re.error as e:
                messages.error(request, f'Invalid regex pattern: {e}')
    else:
        form = RegexExtractorForm()
    return render(request, 'pdf_manager/regex_extractor.html', {'form': form})