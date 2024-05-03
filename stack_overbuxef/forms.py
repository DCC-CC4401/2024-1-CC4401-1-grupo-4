from django import forms
from .models import Consulta, Tag

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['titulo', 'mensaje', 'anonimo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Modificar widgets para personalizar la apariencia
        self.fields['mensaje'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 15})  # Ajustar tamaño de la caja de texto
        
        # Obtener los tags existentes y convertirlos a una lista para usar en el campo de selección
        #existing_tags = Tag.objects.all().values_list('id', 'nombre')
        #self.fields['tag'] = forms.ChoiceField(choices=existing_tags)

        # Cambiar el widget del campo anonimo a un checkbox
        self.fields['anonimo'] = forms.BooleanField(label='Publicación anónima', required=False)
