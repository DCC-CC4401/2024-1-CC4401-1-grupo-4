from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import ConsultaForm
from .models import Consulta
from .models import Usuario
from django.core.paginator import Paginator
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def publish_message(request):
    if request.method == "GET":
        form = ConsultaForm()  #Si la request es de tipo GET se crea un formulario vacío y se renderiza
        return render(request, 'stack_overbuxef/publish.html', {'form': form})
    if request.method == "POST":
        form = ConsultaForm(request.POST) #Si la request es de tipo POST se crea un formulario con los datos recibidos
        if form.is_valid():
            consulta = form.save(commit= False)
            consulta.creador_id = request.user.id  #Se asigna el creador de la consulta como el usuario que está logueado
            consulta.save() #Se guarda la consulta en la base de datos
            return redirect('forum')
        return render(request, 'stack_overbuxef/publish.html', {'form': form}) # Si el formulario no es válido se renderiza nuevamente el formulario con los errores

@login_required(login_url='/')
def forum(request):
    query = request.GET.get('q', '') # Devuelve el término ingresado en el input de "Busqué una pregunta"
    if query: # Si hay algo ingresado en el buscador
        consultas = Consulta.objects.filter(titulo__icontains=query) # Filtra las consultas por el título de estas
    else: # Si no
        consultas = Consulta.objects.all() # Se devuelven todas las consultas
    
    paginator = Paginator(consultas, 10)  # Muestra 10 consultas por página

    page_number = request.GET.get('page') # Obtengo el número de la página que se esta mostrando
    page_obj = paginator.get_page(page_number) # Obtengo el objeto página

    context = { # Se crea un diccionario el cual se le va entregar al html para obtener las referencias necesarias
        'page_obj': page_obj, # Objeto página
        'query': query, # Lo ingresado en el campo de la búsqueda. Esto es necesario para mantenerlo al cambiar de página
    }
    return render(request, 'forum.html', context) # Se muestra el template cuyo contexto es context


def register_user(request):
    if request.method == 'GET':
        return render(request, "register_user.html")

    elif request.method == 'POST':
        # Obtener los elementos del formulario
        nombre = request.POST['nombre']
        contrasenha = request.POST['contraseña']
        tipo = request.POST['tipo_usuario']
        mail = request.POST['mail']
        foto = request.POST['foto']

        # Verificamos que el username ni el email estén ocupados para crear a un nuevo usuario
        if Usuario.objects.filter(username=nombre).exists():
            return render(request, "register_user.html", {"error": f"Nombre {nombre} ya está en uso"})
        elif Usuario.objects.filter(email=mail).exists():
            return render(request, "register_user.html", {"error": f"Email {mail} ya está en uso"})
        else:
            Usuario.objects.create_user(username=nombre, email=mail, password=contrasenha, tipo=tipo, foto=foto)

        # Redireccionar a la página de /login
        return HttpResponseRedirect('/')

def login_user(request):
    if request.method == 'GET':
        return render(request, "login.html")

    elif request.method == 'POST':
        username = request.POST['username']
        contrasenha = request.POST['contraseña']

        # Autentificar al usuario
        usuario = authenticate(username=username, password=contrasenha)
        if usuario is not None:
            login(request, usuario)
            return HttpResponseRedirect('/forum') 
        return HttpResponseRedirect('/register')
