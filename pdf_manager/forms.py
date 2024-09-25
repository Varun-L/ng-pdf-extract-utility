from django import forms
from .models import PdfFile
from django.core.validators import URLValidator

class PdfDownloadForm(forms.Form):
    url = forms.URLField(validators=[URLValidator()])

class PdfParserForm(forms.Form):
    pdf_file = forms.ModelChoiceField(queryset=PdfFile.objects.all())
    page_numbers = forms.CharField(max_length=255)
    search_string = forms.CharField(max_length=255, required=False)
    rect_coords = forms.CharField(max_length=255, required=False)

class RegexExtractorForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    regex_pattern = forms.CharField(max_length=255)