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
        form = ConsultaForm()
        return render(request, 'stack_overbuxef/publish.html', {'form': form})
    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit= False)
            consulta.creador_id = 1
            consulta.tag_id = 1
            consulta.save()
            return redirect('forum')
        return "It was not valid"
    else:
        return "It was not a POST request"

@login_required(login_url='/')
def forum(request):
    query = request.GET.get('q')
    if query:
        consultas = Consulta.objects.filter(titulo__icontains=query)
    else:
        consultas = Consulta.objects.all()
    
    paginator = Paginator(consultas, 10)  # Muestra 10 consultas por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'forum.html', context)


def register_user(request):
    if request.method == 'GET': #Si estamos cargando la página
        return render(request, "register_user.html") #Mostrar el template

    elif request.method == 'POST': #Si estamos recibiendo el form de registro

        #Tomar los elementos del formulario que vienen en request.POST
        nombre = request.POST['nombre']
        contrasenha = request.POST['contraseña']
        tipo = request.POST['tipo_usuario']
        mail = request.POST['mail']
        foto = request.POST['foto']

        #Crear el nuevo usuario
        user = Usuario.objects.create_user(username=nombre, email=mail, password=contrasenha, tipo=tipo, foto=foto)

        #Redireccionar la página de /login
        return HttpResponseRedirect('/')

def login_user(request):
    if request.method == 'GET':
        return render(request, "login.html")
    if request.method == 'POST':
        username = request.POST['username']
        contrasenha = request.POST['contraseña']
        usuario = authenticate(username=username, password=contrasenha)
        if usuario is not None:
            login(request, usuario)
            # Por mientras va directamente a message, debe ser cambiado a '/forum' cuando este implementado
            return HttpResponseRedirect('/message') 
        else:
            return HttpResponseRedirect('/register')
        