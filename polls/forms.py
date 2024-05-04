# from django import forms
# from .models import Rectangle

from django import forms
from .models import Rectangle, SVGImage

class RectangleForm(forms.ModelForm):
    rectangle_id = forms.IntegerField(widget=forms.HiddenInput, required=False)  # Dodanie pola na ID prostokąta
    image_id = forms.IntegerField(widget=forms.HiddenInput, required=False)  # Dodanie pola na ID prostokąta

    class Meta:
        model = Rectangle
        fields = ['image_id','rectangle_id', 'x', 'y', 'width', 'height', 'fill']