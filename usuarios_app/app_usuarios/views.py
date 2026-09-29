# app_usuarios/views.py
from django.shortcuts import render, get_object_or_404
from .models import Usuario
from .services.usuarios_service import load_usuarios

def lista_usuarios(request):
    
    load_usuarios()
    
    usuarios = Usuario.objects.all()
    return render(request, "app_usuarios/usuario_list.html", {"usuarios": usuarios})

def detalle_usuario(request, uuid):

    usuario = get_object_or_404(Usuario, uuid=uuid)
    return render(request, "app_usuarios/usuario_details.html", {"usuario": usuario})
