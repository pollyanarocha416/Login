from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from usuarios.models import Fotografia

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()
        
        usuario = auth.authenticate(
            request,
            username=nome,
            password=senha
            )
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f"{nome} logado(a) com sucesso!")
            return redirect ('index')

        else:
            messages.error(request, "Erro ao efetuar login")
            return redirect('login')


    return render(request, "usuarios/login.html", {"form": form})

def cadastro(request):
    form = CadastroForms()
    
    if request.method == 'POST':
        form = CadastroForms(request.POST)

        
        if form.is_valid():
           
            
            nome=form["nome_cadastro"].value()
            email=form["email"].value()
            senha=form["senha_1"].value()

            if User.objects.filter(username=nome).exists():
                messages.error(request, "Usuario já existente")
                return redirect('cadastro')
            
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.save()
            messages.success(request, "Cadastro feito com sucesso")
            return redirect('login')
    return render(request, "usuarios/cadastro.html", {"form": form})

def logout(request):
    
    auth.logout(request)
    messages.success(request, "Logout feito com sucesso!")
    return redirect('login')


def buscar(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuario nao logado")
        return redirect('login')
    fotografias = Fotografia.objects.order_by("-data_fotografia").filter(publicada=True)
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar)

    return render(request, "galeria/buscar.html", {"cards": fotografias})
