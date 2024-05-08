# Create your views here.
from django.shortcuts import render, redirect
from .forms import ConsultaForm
from .models import Usuario
# Create your views here.
from django.http import HttpResponseRedirect

def publish_message(request):
    if request.method == "GET":
        form = ConsultaForm()
        return render(request, 'publish.html', {'form': form})

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

        #Redireccionar la página /tareas
        return HttpResponseRedirect('/')

from django.contrib.auth import authenticate, login
def login_user(request):
    if request.method == 'GET':
        return render(request, "login.html")
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        usuario = authenticate(username=username, password=contraseña)
        if usuario is not None:
            login(request, usuario)
            return HttpResponseRedirect('/forum')
        else:
            return HttpResponseRedirect('/register')
