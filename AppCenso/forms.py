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

departamentos = (
    ('Antioquia','Antioquia'),
    ('Atlantico','Atlantico'),
    ('Amazonas','Amazonas'),
)

ciudades = (
    ('Antioquia: Medellin','Antioquia: Medellin'),
    ('Antioquia: Rionegro','Antioquia: Rionegro'),
    ('Antioquia: Bello','Antioquia: Bello'),
    ('Amazonas: Leticia','Amazonas: Leticia'),
    ('Amazonas: Tarapaca','Amazonas: Tarapaca'),
    ('Amazonas: El encanto','Amazonas: El encanto'),
    ('Atlantico: Barranquilla','Atlantico: Barranquilla'),
    ('Atlantico: Puerto Colombia','Atlantico: Puerto Colombia'),
    ('Atlantico: Soledad','Atlantico: Soledad'),
)



class formDireccion(forms.Form):
    departamento = forms.ChoiceField(label="¿En que departamento vive?",widget=forms.Select,choices = departamentos)
    ciudad = forms.ChoiceField(label="¿En que ciudad vive?", widget=forms.Select, choices = ciudades)
    barrio = forms.CharField(label="¿En que barrio vive?")
    direccion = forms.CharField(label="¿Cual es su dirección?")
    estrato = forms.IntegerField(label="¿Cual es el estrato de la zona donde vive?", min_value = 1, max_value = 6)
    codigoPostal = forms.IntegerField(label="¿Cual es el codigo postal de la zona donde vive?", min_value = 1000, max_value=99999)
    
    
    
class formPersona(forms.Form):
    PrimerNombre = forms.CharField(label="Primer nombre")
    SegundoNombre = forms.CharField(label="Segundo nombre (si tiene)",required=False)
    PrimerApellido = forms.CharField(label="Primer apellido")
    SegundoApellido = forms.CharField(label="Segundo apellido")
    edad = forms.IntegerField(label="Edad", min_value = 0, max_value = 150)
    profesion = forms.CharField(label="Profesión actual")
    

class formVivienda(forms.Form):
    area = forms.IntegerField(label="Area en metros cuadrados de su vivienda", max_value=9999, min_value = 1)
    tipo = forms.ChoiceField(label="Tipo de vivienda", widget=forms.Select, choices=tiposVivienda)
    agua = forms.ChoiceField(label="¿Tiene servicio de agua?",widget=forms.Select,choices=opciones)
    luz = forms.ChoiceField(label="¿Tiene servicio de electricidad?",widget=forms.Select,choices=opciones)
    gas = forms.ChoiceField(label="¿Tiene servicio de gas?",widget=forms.Select,choices=opciones)
    internet = forms.ChoiceField(label="¿Tiene servicio de internet?",widget=forms.Select,choices=opciones)
    computador = forms.ChoiceField(label="¿Tiene computador en casa?",widget=forms.Select,choices=opciones)
    propia = forms.ChoiceField(label="¿Su vivienda es propia?",widget=forms.Select,choices=opciones)
    

class formFeedback(forms.Form):
    feedback = forms.CharField(label="Si tiene algún comentario o sugerencia, escribalo a continuación por favor.",required=False,widget=forms.Textarea)


class formImprimir(forms.Form):
    departamento = forms.ChoiceField(label="¿En que departamento vive?",widget=forms.Select,choices = departamentos)
    ciudad = forms.ChoiceField(label="¿En que ciudad vive?", widget=forms.Select, choices = ciudades)