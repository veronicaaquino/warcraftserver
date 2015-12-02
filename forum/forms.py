from django import forms

class PostForm(forms.Form):
    body = forms.
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    
