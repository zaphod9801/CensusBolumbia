from django.db import models

# Create your models here.
class Direccion(models.Model):
    departamento = models.TextField(default="")
    ciudad = models.TextField(default="")
    barrio = models.TextField(default="")
    direccion = models.TextField(default="")
    estrato = models.IntegerField(default=0)
    codigoPostal = models.IntegerField(default=0)
    CFN = models.IntegerField(default=0)
    
    
class Persona(models.Model):
    PrimerNombre = models.TextField(default="")
    SegundoNombre = models.TextField(default="",null=True)
    PrimerApellido = models.TextField(default="")
    SegundoApellido = models.TextField(default="")
    edad = models.IntegerField(default=0)
    profesion = models.TextField(default="")
    

class Vivienda(models.Model):
    area = models.DecimalField(default=0,max_digits=5,decimal_places=1)
    tipo = models.TextField(default="")
    agua = models.TextField(default="No")
    luz = models.TextField(default="No")
    gas = models.TextField(default="No")
    internet = models.TextField(default="No")
    computador = models.TextField(default="No")
    propia = models.TextField(default="No")
    

class Feedback(models.Model):
    feedback = models.TextField(default="")
    

class Datos(models.Model):
    departamento = models.TextField(default="")
    ciudad = models.TextField(default="")
    barrio = models.TextField(default="")
    direccion = models.TextField(default="")
    estrato = models.IntegerField(default=0)
    codigoPostal = models.IntegerField(default=0)
    CFN = models.IntegerField(default=0)
    
    PrimerNombre = models.TextField(default="")
    SegundoNombre = models.TextField(default="",null=True)
    PrimerApellido = models.TextField(default="")
    SegundoApellido = models.TextField(default="")
    edad = models.IntegerField(default=0)
    profesion = models.TextField(default="")
    
    area = models.DecimalField(default=0,max_digits=5,decimal_places=1)
    tipo = models.TextField(default="")
    agua = models.TextField(default="No")
    luz = models.TextField(default="No")
    gas = models.TextField(default="No")
    internet = models.TextField(default="No")
    computador = models.TextField(default="No")
    propia = models.TextField(default="No")
    
    feedback = models.TextField(default="")

class Dato(models.Model):
    claveDireccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    clavePersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    claveVivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE)
    claveFeedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
