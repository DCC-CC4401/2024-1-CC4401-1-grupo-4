# Create your views here.
from django.shortcuts import render, redirect
from .forms import ConsultaForm
# Create your views here.
from django.http import HttpResponse

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

# def register_user(request):
#     if request.method == 'GET': #Si estamos cargando la página
#         return render(request, "todoapp/register_user.html") #Mostrar el template

#     elif request.method == 'POST': #Si estamos recibiendo el form de registro

#         #Tomar los elementos del formulario que vienen en request.POST
#         nombre = request.POST['nombre']
#         contraseña = request.POST['contraseña']
#         apodo = request.POST['apodo']
#         pronombre = request.POST['pronombre']
#         mail = request.POST['mail']

#         #Crear el nuevo usuario
#         user = User.objects.create_user(username=nombre, password=contraseña, email=mail, apodo=apodo, pronombre=pronombre)

#         #Redireccionar la página /tareas
#         return HttpResponseRedirect('/tareas')

# from django.contrib.auth import authenticate, login,logout
# def login_user(request):
#     if request.method == 'GET':
#         return render(request,"todoapp/login.html")
#     if request.method == 'POST':
#         username = request.POST['username']
#         contraseña = request.POST['contraseña']
#         usuario = authenticate(username=username,password=contraseña)
#         if usuario is not None:
#             login(request,usuario)
#             return HttpResponseRedirect('/tareas')
#         else:
#             return HttpResponseRedirect('/register')


def forum(request):
    return HttpResponse("Hello world")

# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect('/tareas')