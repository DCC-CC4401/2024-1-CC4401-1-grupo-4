from django import forms
from .models import Consulta, Tag

#Clase formulario para la creación de una consulta
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['titulo', 'mensaje', 'anonimo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Modificar widgets para personalizar la apariencia
        self.fields['mensaje'].widget = forms.Textarea(attrs={'rows': 15, 'cols': 30})  # Ajustar tamaño de la caja de texto
    
        # Cambiar el widget del campo anonimo a un checkbox
        self.fields['anonimo'] = forms.BooleanField(label='Publicación anónima', required=False)
