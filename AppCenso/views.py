from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from AppCenso.forms import formVivienda,formPersona,formDireccion,formFeedback, formImprimir
from AppCenso.models import Vivienda,Persona,Direccion,Feedback, Datos
from usuario.views import EnviarCFN
# Create your views here.

datosToUpload = [] #Para subir los datos de forma mas mela
del datosToUpload[:]  #Toca borrar porque sino la cosa esa se quedaba con los valores pasados siempre
datosToUpload = [None] * 22 #Le asignamos valores nulos a todos los campos, sino las vistas no obtenian adecuadamente el tamaño del vector
formEnviado = [0,0,0,0] #Servira para saber que categoria ya está lista
alertaDireccion = 0 #Definición de todas las alertas que usarán las funciones de Enviar Censo
alertaPersona = 0 
alertaVivienda = 0
alertaFeedback = 0

#Implementación del controlador de cada categoria del censo con su respectivo manejo de envios
#Solo se comentara el de dirección pues los demás siguen exactamente la misma logica
def VistaDireccion(request):
    global formEnviado #Traer las globales necesarias, sino no las reconoce
    global datosToUpload
    global alertaDireccion
    global alertaPersona
    global alertaFeedback
    global alertaVivienda
    validador = formEnviado[0] #Establecemos un validador con el valor actual del vector formEnviado, esto maneja el mensaje de finalización del formulario
    alertaFeedback = 0 #Para que las alertas de formulario no finalizado desaparezcan al irse a otra pagina
    alertaPersona = 0
    alertaVivienda = 0
    if request.method == 'POST':
        formulario = formDireccion(request.POST) 
        if formulario.is_valid():
            info = formulario.cleaned_data
            iterador = 0 #Iterador para ubicarme en la posición del vector datosToUpload que le corresponde 
            try:
                datosToUpload[0] = info['departamento'] #Esta linea es distinta a los demás, un bug hacia que el for siguiente no obtuviera este valor
            except:
                print("muerto")
            for key in info.keys(): 
                for i in range(iterador):
                    datosToUpload[iterador] = info[key] #For para llenar el vector datosToUpload con el contenido del formulario
                iterador += 1
            formEnviado[0] = 1 #setear en 1 el valor de formEnviado correspondiendo para que ya no aparezca el boton de enviar sino el mensaje de enviado
            validador = formEnviado[0]
            contexto = {
                "formulario":formulario,
                "formEnviado":validador,
                "alerta":alertaDireccion
            }
            request.session['form_dataDireccion'] = formulario.cleaned_data #Cargamos los valores enviados a la sesión correspondiente
            
             
            return render(request,"direccion.html",contexto) 
        
    else:
        formulario = formDireccion(initial=request.session.get('form_dataDireccion')) #Se instancia el formulario con este argumento para que cargue con el valor de la sesión dentro
        
        
    contexto = {
        "formulario":formulario,
        "formEnviado":validador,
        "alerta":alertaDireccion
    }
    
    return render(request,"direccion.html",contexto) 

def EnviarDireccion(request): #Está función se encarga de comprobar si ya se completó el censo y enviarlo desde el path de dirección, esto permite que se envie desde cualquier categoria
    global formEnviado #Traer globales necesarias
    global datosToUpload
    global alertaDireccion
    global alertaPersona
    global alertaVivienda
    global alertaFeedback
    n1 = formEnviado[0]
    n2 = formEnviado[1]
    n3 = formEnviado[2]
    n4 = formEnviado[3]
            
    if (n1+n2+n3+n4) == 4: #Si todos los valores estan en 1, significa que todas las categorias están listas y se puede enviar el censo
        
        SubirDatos()
        del request.session['form_dataDireccion'] #Procedo a borrar todos los datos locales estacionales para evitar corrupción
        del request.session['form_dataPersona']
        del request.session['form_dataVivienda']
        del request.session['form_dataFeedback']
        del datosToUpload[:]
        datosToUpload = [None] * 22
        formEnviado = [0,0,0,0]
        alertaDireccion = 0
        alertaPersona = 0
        alertaVivienda = 0
        alertaFeedback = 0
        return render(request,"gracias.html") #Retorna el final del censo
    else:
        alertaDireccion = 1  #Si aun no está listo el censo, esto funciona como alerta para que su respectiva vista imprima el mensaje de que aun no está terminado el censo
        return redirect("/AppCenso/direccion/") #Retorno a la vista original
    

def VistaPersona(request):
    global formEnviado
    global datosToUpload
    global alertaPersona
    global alertaDireccion
    global alertaFeedback
    global alertaVivienda
    validador = formEnviado[1]
    alertaDireccion = 0
    alertaFeedback = 0
    alertaVivienda = 0
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
                "formEnviado":validador,
                "alerta":alertaPersona
            }
            request.session['form_dataPersona'] = formulario.cleaned_data
                        
            return render(request,"persona.html",contexto) 
            
    else:
        formulario = formPersona(initial=request.session.get('form_dataPersona'))
            
    contexto = {
        "formulario":formulario,
        "formEnviado":validador,
        "alerta":alertaPersona
    }
        
    return render(request,"persona.html",contexto) 
        
def EnviarPersona(request):
    global formEnviado
    global datosToUpload
    global alertaDireccion
    global alertaPersona
    global alertaVivienda
    global alertaFeedback
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
        datosToUpload = [None] * 22
        formEnviado = [0,0,0,0]
        alertaDireccion = 0
        alertaPersona = 0
        alertaVivienda = 0
        alertaFeedback = 0
        return render(request,"gracias.html")
    else:
        alertaPersona = 1
        return redirect("/AppCenso/persona/")       


def VistaVivienda(request):
    global formEnviado
    global datosToUpload
    global alertaVivienda
    global alertaDireccion
    global alertaFeedback
    global alertaPersona
    validador = formEnviado[2]
    alertaDireccion = 0
    alertaPersona = 0
    alertaFeedback = 0
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
                "formEnviado":validador,
                "alerta":alertaVivienda
            }
            request.session['form_dataVivienda'] = formulario.cleaned_data
            
            
            return render(request,"vivienda.html",contexto)
        
    else:
        formulario = formVivienda(initial=request.session.get('form_dataVivienda'))
        
    contexto = {
        "formulario":formulario,
        "formEnviado":validador,
        "alerta":alertaVivienda
    }
    
    return render(request,"vivienda.html",contexto) 

def EnviarVivienda(request):
    global formEnviado
    global datosToUpload
    global alertaDireccion
    global alertaPersona
    global alertaVivienda
    global alertaFeedback
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
        datosToUpload = [None] * 22
        formEnviado = [0,0,0,0]
        alertaDireccion = 0
        alertaPersona = 0
        alertaVivienda = 0
        alertaFeedback = 0
        return render(request,"gracias.html")
    else:
        alertaVivienda = 1
        return redirect("/AppCenso/vivienda/") 


def VistaFeedback(request):
    global formEnviado
    global datosToUpload
    global alertaFeedback
    global alertaDireccion
    global alertaPersona
    global alertaVivienda
    validador = formEnviado[3]
    alertaDireccion = 0
    alertaPersona = 0
    alertaVivienda = 0
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
                "formEnviado":validador,
                "alerta":alertaFeedback
            }
            request.session['form_dataFeedback'] = formulario.cleaned_data
            
            return render(request,"feedback.html",contexto)
        
    else:
        formulario = formFeedback(initial=request.session.get('form_dataFeedback'))
        
    contexto = {
        "formulario":formulario,
        "formEnviado":validador,
        "alerta":alertaFeedback
    }
    
    return render(request,"feedback.html",contexto) 
        
def EnviarFeedback(request):
    global formEnviado
    global datosToUpload
    global alertaDireccion
    global alertaPersona
    global alertaVivienda
    global alertaFeedback
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
        datosToUpload = [None] * 22
        formEnviado = [0,0,0,0]
        alertaDireccion = 0
        alertaPersona = 0
        alertaVivienda = 0
        alertaFeedback = 0
        return render(request,"gracias.html")
    else:
        alertaFeedback = 1
        return redirect("/AppCenso/feedback/")


#Está función se encarga de imprimir los datos existentes en la base de datos en función de dos parametros, departamento y ciudad
def ImprimirDatos(request):
    if request.method == 'POST':
        formulario = formImprimir(request.POST)
        
        if formulario.is_valid():
            info = formulario.cleaned_data
            dat = Datos.objects.filter(departamento = info['departamento'], ciudad = info['ciudad']) #Porque se filtra por departamento y ciudad, deben ser iguales
            NumeroRegistros = dat.count() #Para saber cuantos registros hay
            datos = [] #Vector de los registros que recupere la consulta
            
            for registro in dat:
                datos.append(registro) #Agregamos el resultadod de la consulta al vector
            
            contexto = {
                "registros":datos,
                "Numero":NumeroRegistros,
                "departamento":info['departamento'],
                "ciudad":info['ciudad']
            }
            
            return render(request,"imprimir.html",contexto) #El html que imprime los resultados es distinto al que pregunta departamento y ciudad
        
    else:
        formulario = formImprimir()
        
    contexto = {
        "formulario":formulario,       
    }
    
    return render(request,"formImprimir.html",contexto)        
          
            
#Esta función se encarga de subir los datos del vector datosToUpload a la base de datos (usando la tabla "datos"), una vez el usuario finalizó el censo        
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
    