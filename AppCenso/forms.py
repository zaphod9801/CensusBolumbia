from django import forms

opciones = (
    ('Si','Si'),
    ('No','No'),
)

tiposVivienda = (
    ('Mansión','Mansión'),
    ('Casa','Casa'),
    ('Apartamento','Apartamento'),
    ('Apartaestudio','Apartaestudio'),
    ('Cuarto','Cuarto'),    
    ('Otro','Otro'),
)

class formDireccion(forms.Form):
    departamento = forms.CharField(label="¿En que departamento vive?")
    ciudad = forms.CharField(label="¿En que ciudad vive?")
    barrio = forms.CharField(label="¿En que barrio vive?")
    direccion = forms.CharField(label="¿Cual es su dirección?")
    estrato = forms.IntegerField(label="¿Cual es el estrato de la zona donde vive?")
    codigoPostal = forms.IntegerField(label="¿Cual es el codigo postal de la zona donde vive?")
    
    
    
class formPersona(forms.Form):
    PrimerNombre = forms.CharField(label="Primer nombre")
    SegundoNombre = forms.CharField(label="Segundo nombre (si tiene)",required=False)
    PrimerApellido = forms.CharField(label="Primer apellido")
    SegundoApellido = forms.CharField(label="Segundo apellido")
    edad = forms.IntegerField(label="Edad")
    profesion = forms.CharField(label="Profesión actual")
    agregarPersona = forms.ChoiceField(label="Desea agregar otra persona?",widget=forms.Select,choices=opciones)
    

class formVivienda(forms.Form):
    area = forms.IntegerField(label="Area en metros cuadrados de su vivienda")
    tipo = forms.ChoiceField(label="Tipo de vivienda", widget=forms.Select, choices=tiposVivienda)
    agua = forms.ChoiceField(label="¿Tiene servicio de agua?",widget=forms.Select,choices=opciones)
    luz = forms.ChoiceField(label="¿Tiene servicio de electricidad?",widget=forms.Select,choices=opciones)
    gas = forms.ChoiceField(label="¿Tiene servicio de gas?",widget=forms.Select,choices=opciones)
    internet = forms.ChoiceField(label="¿Tiene servicio de internet?",widget=forms.Select,choices=opciones)
    computador = forms.ChoiceField(label="¿Tiene computador en casa?",widget=forms.Select,choices=opciones)
    propia = forms.ChoiceField(label="¿Su vivienda es propia?",widget=forms.Select,choices=opciones)
    

class formFeedback(forms.Form):
    feedback = forms.CharField(label="Si tiene algún comentario o sugerencia, escribalo a continuación por favor.",required=False,widget=forms.Textarea)