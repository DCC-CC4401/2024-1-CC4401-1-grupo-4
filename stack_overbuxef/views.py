from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import ConsultaForm
from .models import Usuario
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
    if request.method == "GET":
        return render(request, "forum.html")


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
