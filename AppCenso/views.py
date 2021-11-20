from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from AppCenso.forms import formVivienda,formPersona,formDireccion,formFeedback
from AppCenso.models import Vivienda,Persona,Direccion,Feedback, Datos
from usuario.views import EnviarCFN
# Create your views here.

dato = None
idSupreme = None
datosToUpload = [] #Para subir los datos de forma mas mela
datosToUpload2 = [] #Para subir otras personas
del datosToUpload[:]
del datosToUpload2[:]  #Toca borrar porque sino la cosa esa se quedaba con los valores pasados siempre
datosToUpload = [None] * 22
formEnviado = [0,0,0,0]


def VistaDireccion(request):
    global formEnviado
    global datosToUpload
    validador = formEnviado[0]
    if request.method == 'POST':
        formulario = formDireccion(request.POST)
        if formulario.is_valid():
            info = formulario.cleaned_data
            iterador = 0
            datosToUpload[0] = info['departamento']
            for key in info.keys():
                for i in range(iterador):
                    datosToUpload[iterador] = info[key]
                iterador += 1
            formEnviado[0] = 1
            validador = formEnviado[0]
            contexto = {
                "formulario":formulario,
                "formEnviado":validador
            }
            request.session['form_dataDireccion'] = formulario.cleaned_data
            
            n1 = formEnviado[0]
            n2 = formEnviado[1]
            n3 = formEnviado[2]
            n4 = formEnviado[3]
            
            if (n1+n2+n3+n4) == 4:
        
                SubirDatos()
                del request.session['form_dataDireccion']
                del request.session['form_dataPersona']
                del request.session['form_dataVivienda']
                del request.session['form_dataFeedback']
                del datosToUpload[:]
                formEnviado = [0,0,0,0]
                return render(request,"gracias.html")
            else: 
                return render(request,"direccion.html",contexto) 
        
    else:
        formulario = formDireccion(initial=request.session.get('form_dataDireccion'))
        
        
    contexto = {
        "formulario":formulario,
        "formEnviado":validador
    }
    
    return render(request,"direccion.html",contexto) 

    

def VistaPersona(request):
    global formEnviado
    global datosToUpload
    validador = formEnviado[1]

    if request.method == 'POST':
        formulario = formPersona(request.POST)
        
        if formulario.is_valid():
            info = formulario.cleaned_data
            iterador = 6   
            for key in info.keys():
                i = 6
                for i in range(iterador):
                    datosToUpload[iterador] = info[key]
                iterador += 1        
                
            formEnviado[1] = 1
            validador = formEnviado[1]
            contexto = {
                "formulario":formulario,
                "formEnviado":validador
            }
            request.session['form_dataPersona'] = formulario.cleaned_data
            
            n1 = formEnviado[0]
            n2 = formEnviado[1]
            n3 = formEnviado[2]
            n4 = formEnviado[3]
                
            if (n1+n2+n3+n4) == 4:
        
                SubirDatos()
                del request.session['form_dataDireccion']
                del request.session['form_dataPersona']
                del request.session['form_dataVivienda']
                del request.session['form_dataFeedback']
                del datosToUpload[:]
                formEnviado = [0,0,0,0]
                return render(request,"gracias.html")
            else: 
                return render(request,"persona.html",contexto) 
            
    else:
        formulario = formPersona(initial=request.session.get('form_dataPersona'))
            
    contexto = {
        "formulario":formulario,
        "formEnviado":validador
    }
        
    return render(request,"persona.html",contexto) 
        
        

def VistaVivienda(request):
    global formEnviado
    global datosToUpload
    validador = formEnviado[2]
    if request.method == 'POST':
        formulario = formVivienda(request.POST)
        
        if formulario.is_valid():
            info = formulario.cleaned_data
            
            iterador = 13   
            for key in info.keys():
                i = 13
                for i in range(iterador):
                    datosToUpload[iterador] = info[key]
                iterador += 1
                
            formEnviado[2] = 1
            validador = formEnviado[2]
            contexto = {
                "formulario":formulario,
                "formEnviado":validador
            }
            request.session['form_dataVivienda'] = formulario.cleaned_data
            
            n1 = formEnviado[0]
            n2 = formEnviado[1]
            n3 = formEnviado[2]
            n4 = formEnviado[3]
            
            if (n1+n2+n3+n4) == 4:
                SubirDatos()
                del request.session['form_dataDireccion']
                del request.session['form_dataPersona']
                del request.session['form_dataVivienda']
                del request.session['form_dataFeedback']
                del datosToUpload[:]
                formEnviado = [0,0,0,0]
                return render(request,"gracias.html")
            else: 
                return render(request,"vivienda.html",contexto)
        
    else:
        formulario = formVivienda(initial=request.session.get('form_dataVivienda'))
        
    contexto = {
        "formulario":formulario,
        "formEnviado":validador
    }
    
    return render(request,"vivienda.html",contexto) 



def VistaFeedback(request):
    global formEnviado
    global datosToUpload
    validador = formEnviado[3]
    if request.method == 'POST':
        formulario = formFeedback(request.POST)
        
        if formulario.is_valid():
            info = formulario.cleaned_data
            
            iterador = 21   
            for key in info.keys():
                i = 21
                for i in range(iterador):
                    datosToUpload[iterador] = info[key]
            formEnviado[3] = 1
            validador = formEnviado[3]
            contexto = {
                "formulario":formulario,
                "formEnviado":validador
            }
            request.session['form_dataFeedback'] = formulario.cleaned_data
            
            n1 = formEnviado[0]
            n2 = formEnviado[1]
            n3 = formEnviado[2]
            n4 = formEnviado[3]
            
            if (n1+n2+n3+n4) == 4:
        
                SubirDatos()
                del request.session['form_dataDireccion']
                del request.session['form_dataPersona']
                del request.session['form_dataVivienda']
                del request.session['form_dataFeedback']
                del datosToUpload[:]
                formEnviado = [0,0,0,0]
                return render(request,"gracias.html")
            else: 
                return render(request,"feedback.html",contexto)
        
    else:
        formulario = formFeedback(initial=request.session.get('form_dataFeedback'))
        
    contexto = {
        "formulario":formulario,
        "formEnviado":validador
    }
    
    return render(request,"feedback.html",contexto) 
        
        
def SubirDatos():
    dato = Datos.objects.create(
        departamento = datosToUpload[0],
        ciudad = datosToUpload[1],
        barrio = datosToUpload[2],
        direccion = datosToUpload[3],
        estrato = datosToUpload[4],
        codigoPostal = datosToUpload[5],
        CFN = EnviarCFN(),
        
        PrimerNombre = datosToUpload[6],
        SegundoNombre = datosToUpload[7],
        PrimerApellido = datosToUpload[8],
        SegundoApellido = datosToUpload[9],
        edad = datosToUpload[10],
        profesion = datosToUpload[11],
        
        area = datosToUpload[13],
        tipo = datosToUpload[14],
        agua = datosToUpload[15],
        luz = datosToUpload[16],
        gas = datosToUpload[17],
        internet = datosToUpload[18],
        computador = datosToUpload[19],
        propia = datosToUpload[20],
        
        feedback = datosToUpload[21],
        
    )
    