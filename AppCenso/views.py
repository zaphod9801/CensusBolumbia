from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.core.mail import send_mail
from django.conf import settings
from AppCenso.forms import formVivienda,formPersona,formDireccion,formFeedback, formImprimir
from AppCenso.models import Vivienda,Persona,Direccion,Feedback, Datos

# Create your views here.

#Esta función setea valores iniciales que la sesión necesitará todo el tiempo, una alternativa a los globales
def valoresIniciales(request):
    request.session['direccionEnviado'] = 0
    request.session['departamento'] = None
    request.session['ciudad'] = None
    request.session['barrio'] = None
    request.session['direccion'] = None
    request.session['estrato'] = None
    request.session['codigoPostal'] = None
    request.session['alertaDireccion'] = 0
    
    request.session['personaEnviado'] = 0
    request.session['primerNombre'] = None
    request.session['segundoNombre'] = None
    request.session['primerApellido'] = None
    request.session['segundoApellido'] = None
    request.session['edad'] = None
    request.session['profesion'] = None
    request.session['alertaPersona'] = 0
    
    request.session['viviendaEnviado'] = 0
    request.session['area'] = None
    request.session['tipo'] = None
    request.session['agua'] = None
    request.session['luz'] = None
    request.session['gas'] = None
    request.session['internet'] = None
    request.session['computador'] = None
    request.session['propia'] = None
    request.session['alertaVivienda'] = 0
    
    request.session['feedbackEnviado'] = 0
    request.session['feedback'] = None
    request.session['alertaFeedback'] = 0
    
    
    return redirect('/AppCenso/direccion/') #Porque definí que la primer categoria que aparezca al ingresar sea dirección

#Esta función la usaran las de Enviar para setear todo como estaba inicialmente
def eliminarSession(request):    
    request.session['form_dataDireccion'] = None    
    request.session['form_dataPersona'] = None
    request.session['form_dataVivienda'] = None
    request.session['form_dataFeedback'] = None
    
    request.session['direccionEnviado'] = 0
    request.session['departamento'] = None
    request.session['ciudad'] = None
    request.session['barrio'] = None
    request.session['direccion'] = None
    request.session['estrato'] = None
    request.session['codigoPostal'] = None
    request.session['alertaDireccion'] = 0
    
    request.session['personaEnviado'] = 0
    request.session['primerNombre'] = None
    request.session['segundoNombre'] = None
    request.session['primerApellido'] = None
    request.session['segundoApellido'] = None
    request.session['edad'] = None
    request.session['profesion'] = None
    request.session['alertaPersona'] = 0
    
    request.session['viviendaEnviado'] = 0
    request.session['area'] = None
    request.session['tipo'] = None
    request.session['agua'] = None
    request.session['luz'] = None
    request.session['gas'] = None
    request.session['internet'] = None
    request.session['computador'] = None
    request.session['propia'] = None
    request.session['alertaVivienda'] = 0
    
    request.session['feedbackEnviado'] = 0
    request.session['feedback'] = None
    request.session['alertaFeedback'] = 0

def eliminarTodaLaSession(request):
    eliminarSession(request)
    
    return redirect('/')
    


#Implementación del controlador de cada categoria del censo con su respectivo manejo de envios
#Solo se comentara el de dirección pues los demás siguen exactamente la misma logica
def VistaDireccion(request):
    validador = request.session.get('direccionEnviado') #Establecemos un validador con el valor actual del vector formEnviado, esto maneja el mensaje de finalización del formulario
    request.session['alertaFeedback'] = 0 #Para que las alertas de formulario no finalizado desaparezcan al irse a otra pagina
    request.session['alertaPersona'] = 0
    request.session['alertaVivienda'] = 0
    if request.method == 'POST':
        formulario = formDireccion(request.POST) 
        if formulario.is_valid():
            info = formulario.cleaned_data
            request.session['departamento'] = info['departamento']
            request.session['ciudad'] = info['ciudad']
            request.session['barrio'] = info['barrio']
            request.session['direccion'] = info['direccion']
            request.session['estrato'] = info['estrato']
            request.session['codigoPostal'] = info['codigoPostal']
            
            request.session['direccionEnviado'] = 1 #setear en 1 el valor de formEnviado correspondiendo para que ya no aparezca el boton de enviar sino el mensaje de enviado
            validador = request.session.get('direccionEnviado')

            contexto = {
                "formulario":formulario,
                "formEnviado":validador,
                "alerta":request.session.get('alertaDireccion')
            }
            request.session['form_dataDireccion'] = formulario.cleaned_data #Cargamos los valores enviados a la sesión correspondiente
            
             
            return render(request,"direccion.html",contexto) 
        
    else:
        formulario = formDireccion(initial=request.session.get('form_dataDireccion')) #Se instancia el formulario con este argumento para que cargue con el valor de la sesión dentro
          
    contexto = {
        "formulario":formulario,
        "formEnviado":validador,
        "alerta":request.session.get('alertaDireccion')
    }
    
    return render(request,"direccion.html",contexto) 

def EnviarDireccion(request): #Está función se encarga de comprobar si ya se completó el censo y enviarlo desde el path de dirección, esto permite que se envie desde cualquier categoria
    n1 = request.session.get('direccionEnviado')
    n2 = request.session.get('personaEnviado')
    n3 = request.session.get('viviendaEnviado')
    n4 = request.session.get('feedbackEnviado')
            
    if (n1+n2+n3+n4) == 4: #Si todos los valores estan en 1, significa que todas las categorias están listas y se puede enviar el censo
        
        SubirDatos(request)
        del request.session['form_dataDireccion'] #Procedo a borrar todos los datos locales estacionales para evitar corrupción
        del request.session['form_dataPersona']
        del request.session['form_dataVivienda']
        del request.session['form_dataFeedback']
        eliminarSession(request)
        return render(request,"gracias.html") #Retorna el final del censo
    else:
        request.session['alertaDireccion'] = 1  #Si aun no está listo el censo, esto funciona como alerta para que su respectiva vista imprima el mensaje de que aun no está terminado el censo
        return redirect("/AppCenso/direccion/") #Retorno a la vista original
    

def VistaPersona(request):
    validador = request.session.get('personaEnviado') #Establecemos un validador con el valor actual del vector formEnviado, esto maneja el mensaje de finalización del formulario
    request.session['alertaFeedback'] = 0 #Para que las alertas de formulario no finalizado desaparezcan al irse a otra pagina
    request.session['alertaDireccion'] = 0
    request.session['alertaVivienda'] = 0
    if request.method == 'POST':
        formulario = formPersona(request.POST) 
        if formulario.is_valid():
            info = formulario.cleaned_data
            request.session['primerNombre'] = info['PrimerNombre']
            request.session['segundoNombre'] = info['SegundoNombre']
            request.session['primerApellido'] = info['PrimerApellido']
            request.session['segundoApellido'] = info['SegundoApellido']
            request.session['edad'] = info['edad']
            request.session['profesion'] = info['profesion']
            
            request.session['personaEnviado'] = 1 #setear en 1 el valor de formEnviado correspondiendo para que ya no aparezca el boton de enviar sino el mensaje de enviado
            validador = request.session.get('personaEnviado')

            contexto = {
                "formulario":formulario,
                "formEnviado":validador,
                "alerta":request.session.get('alertaPersona')
            }
            request.session['form_dataPersona'] = formulario.cleaned_data #Cargamos los valores enviados a la sesión correspondiente
            
             
            return render(request,"persona.html",contexto) 
        
    else:
        formulario = formPersona(initial=request.session.get('form_dataPersona')) #Se instancia el formulario con este argumento para que cargue con el valor de la sesión dentro
          
    contexto = {
        "formulario":formulario,
        "formEnviado":validador,
        "alerta":request.session.get('alertaPersona')
    }
    
    return render(request,"persona.html",contexto) 
        
def EnviarPersona(request):
    n1 = request.session.get('direccionEnviado')
    n2 = request.session.get('personaEnviado')
    n3 = request.session.get('viviendaEnviado')
    n4 = request.session.get('feedbackEnviado')
            
    if (n1+n2+n3+n4) == 4: #Si todos los valores estan en 1, significa que todas las categorias están listas y se puede enviar el censo
        
        SubirDatos(request)
        del request.session['form_dataDireccion'] #Procedo a borrar todos los datos locales estacionales para evitar corrupción
        del request.session['form_dataPersona']
        del request.session['form_dataVivienda']
        del request.session['form_dataFeedback']
        eliminarSession(request)
        return render(request,"gracias.html") #Retorna el final del censo
    else:
        request.session['alertaPersona'] = 1  #Si aun no está listo el censo, esto funciona como alerta para que su respectiva vista imprima el mensaje de que aun no está terminado el censo
        return redirect("/AppCenso/persona/")       


def VistaVivienda(request):
    validador = request.session.get('viviendaEnviado') #Establecemos un validador con el valor actual del vector formEnviado, esto maneja el mensaje de finalización del formulario
    request.session['alertaFeedback'] = 0 #Para que las alertas de formulario no finalizado desaparezcan al irse a otra pagina
    request.session['alertaDireccion'] = 0
    request.session['alertaPersona'] = 0
    if request.method == 'POST':
        formulario = formVivienda(request.POST) 
        if formulario.is_valid():
            info = formulario.cleaned_data
            request.session['area'] = info['area']
            request.session['tipo'] = info['tipo']
            request.session['agua'] = info['agua']
            request.session['luz'] = info['luz']
            request.session['gas'] = info['gas']
            request.session['internet'] = info['internet']
            request.session['computador'] = info['computador']
            request.session['propia'] = info['propia']
            
            request.session['viviendaEnviado'] = 1 #setear en 1 el valor de formEnviado correspondiendo para que ya no aparezca el boton de enviar sino el mensaje de enviado
            validador = request.session.get('viviendaEnviado')

            contexto = {
                "formulario":formulario,
                "formEnviado":validador,
                "alerta":request.session.get('alertaVivienda')
            }
            request.session['form_dataVivienda'] = formulario.cleaned_data #Cargamos los valores enviados a la sesión correspondiente
            
             
            return render(request,"vivienda.html",contexto) 
        
    else:
        formulario = formVivienda(initial=request.session.get('form_dataVivienda')) #Se instancia el formulario con este argumento para que cargue con el valor de la sesión dentro
          
    contexto = {
        "formulario":formulario,
        "formEnviado":validador,
        "alerta":request.session.get('alertaVivienda')
    }
    
    return render(request,"vivienda.html",contexto) 

def EnviarVivienda(request):
    n1 = request.session.get('direccionEnviado')
    n2 = request.session.get('personaEnviado')
    n3 = request.session.get('viviendaEnviado')
    n4 = request.session.get('feedbackEnviado')
            
    if (n1+n2+n3+n4) == 4: #Si todos los valores estan en 1, significa que todas las categorias están listas y se puede enviar el censo
        
        SubirDatos(request)
        del request.session['form_dataDireccion'] #Procedo a borrar todos los datos locales estacionales para evitar corrupción
        del request.session['form_dataPersona']
        del request.session['form_dataVivienda']
        del request.session['form_dataFeedback']
        eliminarSession(request)
        return render(request,"gracias.html") #Retorna el final del censo
    else:
        request.session['alertaVivienda'] = 1  #Si aun no está listo el censo, esto funciona como alerta para que su respectiva vista imprima el mensaje de que aun no está terminado el censo
        return redirect("/AppCenso/vivienda/") 


def VistaFeedback(request):
    validador = request.session.get('feedbackEnviado') #Establecemos un validador con el valor actual del vector formEnviado, esto maneja el mensaje de finalización del formulario
    request.session['alertaVivienda'] = 0 #Para que las alertas de formulario no finalizado desaparezcan al irse a otra pagina
    request.session['alertaDireccion'] = 0
    request.session['alertaPersona'] = 0
    if request.method == 'POST':
        formulario = formFeedback(request.POST) 
        if formulario.is_valid():
            info = formulario.cleaned_data
            request.session['feedback'] = info['feedback']
            
            request.session['feedbackEnviado'] = 1 #setear en 1 el valor de formEnviado correspondiendo para que ya no aparezca el boton de enviar sino el mensaje de enviado
            validador = request.session.get('feedbackEnviado')

            contexto = {
                "formulario":formulario,
                "formEnviado":validador,
                "alerta":request.session.get('alertaFeedback')
            }
            request.session['form_dataFeedback'] = formulario.cleaned_data #Cargamos los valores enviados a la sesión correspondiente
            
             
            return render(request,"feedback.html",contexto) 
        
    else:
        formulario = formFeedback(initial=request.session.get('form_dataFeedback')) #Se instancia el formulario con este argumento para que cargue con el valor de la sesión dentro
          
    contexto = {
        "formulario":formulario,
        "formEnviado":validador,
        "alerta":request.session.get('alertaFeedback')
    }
    
    return render(request,"feedback.html",contexto) 
        
def EnviarFeedback(request):
    n1 = request.session.get('direccionEnviado')
    n2 = request.session.get('personaEnviado')
    n3 = request.session.get('viviendaEnviado')
    n4 = request.session.get('feedbackEnviado')      
    if (n1+n2+n3+n4) == 4: #Si todos los valores estan en 1, significa que todas las categorias están listas y se puede enviar el censo
        
        SubirDatos(request)
        del request.session['form_dataDireccion'] #Procedo a borrar todos los datos locales estacionales para evitar corrupción
        del request.session['form_dataPersona']
        del request.session['form_dataVivienda']
        del request.session['form_dataFeedback']
        eliminarSession(request)
        return render(request,"gracias.html") #Retorna el final del censo
    else:
        request.session['alertaFeedback'] = 1  #Si aun no está listo el censo, esto funciona como alerta para que su respectiva vista imprima el mensaje de que aun no está terminado el censo
        return redirect("/AppCenso/feedback/")


#Está función se encarga de imprimir los datos existentes en la base de datos en función de dos parametros, departamento y ciudad
def ImprimirDatos(request):
    if request.method == 'POST':
        formulario = formImprimir(request.POST)
        
        if formulario.is_valid():
            info = formulario.cleaned_data
            dat = Datos.objects.filter(ciudad = info['ciudad']) #Porque se filtra por departamento y ciudad, deben ser iguales
            NumeroRegistros = dat.count() #Para saber cuantos registros hay
            datos = [] #Vector de los registros que recupere la consulta
            
            for registro in dat:
                datos.append(registro) #Agregamos el resultadod de la consulta al vector
            
            contexto = {
                "registros":datos,
                "Numero":NumeroRegistros,
                "ciudad":info['ciudad']
            }
            
            return render(request,"imprimir.html",contexto) #El html que imprime los resultados es distinto al que pregunta departamento y ciudad
        
    else:
        formulario = formImprimir()
        
    contexto = {
        "formulario":formulario,       
    }
    
    return render(request,"formImprimir.html",contexto)        


#Esta función se encargará de enviar un correo desde el gmail de prueba cuando un censo virtual se haga    
def CensoVirtual(request):
    CFNt = None #Aveces ocurria un bug en que el CFN no se obtenía adecuadamente
    try:
        CFNt = request.user.username
        
    except:
        CFNt = 0
        
    if CFNt != "":
        asunto = "Censo Virtual llenado"
        mensaje = "El usuario con CFN: "+str(CFNt)+" llenó el censo virtual."
        email_from = settings.EMAIL_HOST_USER
        receptor = ["jsruiza@eafit.edu.co"]
        send_mail(asunto,mensaje,email_from,receptor)    
                  
            
#Esta función se encarga de subir los datos del censo usando lo que está guardado en la sesión a la base de datos (usando la tabla "datos"), una vez el usuario finalizó el censo        
def SubirDatos(request):
    CFNt = None #Aveces ocurria un bug en que el CFN no se obtenía adecuadamente
    try:
        CFNt = int(request.user.username)
        
    except:
        CFNt = 0
    if CFNt == "":
       CFN = 0 
        
    dato = Datos.objects.create(
        departamento = request.session.get('departamento'),
        ciudad = request.session.get('ciudad'),
        barrio = request.session.get('barrio'),
        direccion = request.session.get('direccion'),
        estrato = request.session.get('estrato'),
        codigoPostal = request.session.get('codigoPostal'),        
        CFN = CFNt,
        
        
        PrimerNombre = request.session.get('primerNombre'),
        SegundoNombre = request.session.get('segundoNombre'),
        PrimerApellido = request.session.get('primerApellido'),
        SegundoApellido = request.session.get('segundoApellido'),
        edad = request.session.get('edad'),
        profesion = request.session.get('profesion'),
        
        area = request.session.get('area'),
        tipo = request.session.get('tipo'),
        agua = request.session.get('agua'),
        luz = request.session.get('luz'),
        gas = request.session.get('gas'),
        internet = request.session.get('internet'),
        computador = request.session.get('computador'),
        propia = request.session.get('propia'),
        
        feedback = request.session.get('feedback'),
        
    )
    CensoVirtual(request)
    
    Datos.objects.filter(CFN=0).delete() #Se eliminan los registros con CFN = 0 pues no son validos
    