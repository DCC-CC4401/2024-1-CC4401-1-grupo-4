from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .forms import ConsultaForm, AnswerForm
from .models import Consulta, Usuario, Tag, Consulta_tag, Consulta_respuesta, Respuesta
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required(login_url='/')
def publish_message(request):
    if request.method == "GET":
        form = ConsultaForm()  #Si la request es de tipo GET se crea un formulario vacío y se renderiza
        return render(request, 'stack_overbuxef/publish.html', {'form': form})
    if request.method == "POST":
        form = ConsultaForm(request.POST, request.FILES) #Si la request es de tipo POST se crea un formulario con los datos recibidos
        if form.is_valid():
            consulta = form.save(commit= False)
            consulta.creador_id = request.user.id  #Se asigna el creador de la consulta como el usuario que está logueado
            consulta.save() #Se guarda la consulta en la base de datos

            # Guardar los tags seleccionados en la tabla de relación Consulta_tag
            tags = form.cleaned_data.get('tag')
            for tag in tags:
                Consulta_tag.objects.create(consulta=consulta, tag=tag)
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

		# Verificamos que el username ni el email estén ocupados para crear a un nuevo usuario
		if Usuario.objects.filter(username=nombre).exists():
			return render(request, "register_user.html", {"error": f"Nombre {nombre} ya está en uso"})
		elif Usuario.objects.filter(email=mail).exists():
			return render(request, "register_user.html", {"error": f"Email {mail} ya está en uso"})
		else:
			foto = request.FILES.get('foto')
			if foto:
				file_name = default_storage.save(rf"fotos_usuarios/{foto.name}", foto)
			Usuario.objects.create_user(username=nombre, email=mail, password=contrasenha, tipo=tipo, foto=rf"media/{file_name}" if foto else None)

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


@login_required
def profile(request):
	# Diccionario para renderizar adecuadamente el tipo de cuenta en la página
	tipos = {"PR": "Profesor", "ES": "Estudiante", "AD": "Administrador"}

	if request.method == 'GET':
		return render(request, "profile.html", {"tipos": tipos, "error": ""})

	elif request.method == 'POST':
		# Nueva información del usuario
		nombre = request.POST.get('nombre')
		tipo = request.POST.get('tipo')
		correo = request.POST.get('correo')
		foto = request.FILES.get('foto')

		curr_username = request.user.username
		user = Usuario.objects.get(username=curr_username)

		# Verificar que la nueva información de usuario no coincida con algún registro existente
		if nombre:
			if Usuario.objects.filter(username=nombre).exists():
				return render(request, "profile.html", {"tipos": tipos, "error": f"Nombre {nombre} ya está en uso"})
			elif curr_username == nombre:
				return render(request, "profile.html", {"tipos": tipos, "error": f"Elige un nombre de usuario distinto al actual"})
			user.username = nombre
		if correo:
			if Usuario.objects.filter(email=correo).exists():
				return render(request, "profile.html", {"tipos": tipos, "error": f"Email {correo} ya está en uso"})
			elif request.user.email == correo:
				return render(request, "profile.html", {"tipos": tipos, "error": f"Elige un correo distinto al actual"})
			user.email = correo
		if tipo:
			user.tipo = tipo
		if foto:
			file_name = default_storage.save(rf"fotos_usuarios/{foto.name}", foto)
			user.foto = rf"media/{file_name}"
		user.save()

		return HttpResponseRedirect('/forum') 

  
def modalAnswers(request,consult_id):
	consult = get_object_or_404(Consulta, id=consult_id)
	answers = Respuesta.objects.filter(consulta=consult).order_by('votar')
	paginator = Paginator(answers, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'answers.html', {'page_obj': page_obj, 'consult': consult})

@login_required(login_url='/')
def makeModalAnswer(request, consult_id):
	if request.method == 'GET':
		form = AnswerForm
		return render(request, 'publishAnswer.html', {'form': form, 'consult_id': consult_id})

	elif request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			respuesta = form.save(commit=False)
			respuesta.creador = request.user  # Asignar el usuario logueado
			respuesta.consulta = get_object_or_404(Consulta, id=consult_id)  # Obtener la consulta correspondiente
			respuesta.save()
			return redirect('forum')
		else:
			# Manejar el caso donde el formulario no es válido
			# Puedes renderizar nuevamente el formulario con errores si es necesario
			return render(request, 'publishAnswer.html', {'form': form, 'consult_id': consult_id})


@login_required(login_url='/')
def tags(request):
	if request.method == 'GET':
		# Acceder solo si es admin
		if request.user.tipo != 'AD':
			return HttpResponseRedirect('/forum')

		# Renderizar tags
		tags = Tag.objects.all()
		tags = [{'nombre': tag.nombre, 'id': tag.id} for tag in tags]
		return render(request, 'tags.html', {'tags': tags})

	elif request.method == 'POST':
		# Postear solo si es admin
		if request.user.tipo != 'AD':
			return HttpResponseRedirect('/forum')

		# Subir lista de tags a la base de datos
		tags = request.POST.getlist('tag')
		tags = [tag.strip().lower() for tag in tags if tag]
		if not tags:
			return render(request, 'tags.html', {'error': 'Debes subir al menos una tag'})

		for tag in tags:
			# Crear tag si no existe
			if not Tag.objects.filter(nombre=tag).exists():
				Tag.objects.create(nombre=tag)

		return redirect('/forum')


@login_required(login_url='/')
def deleteTag(request, tag_id):
	if request.method == 'POST':
		# Acceder solo si es admin
		if request.user.tipo != 'AD':
			return HttpResponseRedirect('/forum')

		tag = Tag.objects.get(id=tag_id)
		tag.delete()
		return redirect('/tags')


@login_required(login_url='/')
def deleteComment(request, consult_id):
	if request.method == 'GET':
		# Acceder solo si es admin
		if request.user.tipo != 'AD':
			return HttpResponseRedirect('/forum')

		# Borrar primero las respuestas
		respuestas = Respuesta.objects.filter(consulta_id=consult_id)
		for respuesta in respuestas:
			respuesta.delete()

		# Borrar comentario
		comentario = Consulta.objects.get(id=consult_id)
		comentario.delete()
		return redirect('/forum')


@login_required(login_url='/')
def deleteReply(request, reply_id):
	if request.method == 'GET':
		# Acceder solo si es admin
		if request.user.tipo != 'AD':
			return HttpResponseRedirect('/forum')

		# Borrar respuesta
		respuesta = Respuesta.objects.get(id=reply_id)
		respuesta.delete()
		return redirect('/forum')

@login_required

@login_required
def like_answer(request, answer_id):
    # Obtiene la respuesta con el ID proporcionado, o devuelve un error 404 si no se encuentra
    answer = get_object_or_404(Respuesta, id=answer_id)
    # Incrementa el contador de votos de la respuesta en 1
    answer.votar += 1
    # Guarda los cambios en la base de datos
    answer.save()
    # Devuelve una respuesta JSON indicando éxito y el nuevo conteo de votos
    return JsonResponse({'status': 'success', 'new_vote_count': answer.votar})

@login_required
def dislike_answer(request, answer_id):
    # Obtiene la respuesta con el ID proporcionado, o devuelve un error 404 si no se encuentra
    answer = get_object_or_404(Respuesta, id=answer_id)
    # Decrementa el contador de votos de la respuesta en 1
    answer.votar -= 1
    # Guarda los cambios en la base de datos
    answer.save()
    # Devuelve una respuesta JSON indicando éxito y el nuevo conteo de votos
    return JsonResponse({'status': 'success', 'new_vote_count': answer.votar})