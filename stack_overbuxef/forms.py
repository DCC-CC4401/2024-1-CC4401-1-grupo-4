from django import forms
from .models import Consulta, Tag
from django_select2.forms import Select2MultipleWidget

#Clase formulario para la creación de una consulta
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['titulo', 'mensaje', 'anonimo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Modificar widgets para personalizar la apariencia
        self.fields['mensaje'].widget = forms.Textarea(attrs={'rows': 15, 'cols': 30})  # Ajustar tamaño de la caja de texto
        

        self.fields['tag'] = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=Select2MultipleWidget,  # O puedes usar forms.SelectMultiple para un cuadro de selección múltiple
            required=False
        )

        self.fields['tag'].widget.attrs.update({'class': 'select2'})


        # Cambiar el widget del campo anonimo a un checkbox
        self.fields['anonimo'] = forms.BooleanField(label='Publicación anónima', required=False)
