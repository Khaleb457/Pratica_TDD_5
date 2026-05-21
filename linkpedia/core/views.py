from django.shortcuts import render, redirect, get_object_or_404
from core.forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from core.models import LinkModel
from .forms import LinkForm 

def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        context = {'acesso_negado': True}
        return render(request, 'login.html', {'form':form})
    return render(request, 'login.html', {'form':LoginForm()})

        
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    context = {}
    return render(request, 'index.html', context)


@login_required
def cadastro(request):
    form = LinkForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid(): 
            form.save() 
            return redirect('listar') 
            
    return render(request, 'cadastro_link.html', {'form': form})


@login_required
def listar(request):
    links = LinkModel.objects.all()
    return render(request, 'lista_links.html', {'links': links})

@login_required
def editar(request, id):
    links = get_object_or_404(LinkModel, id=id)
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=links)
        if form.is_valid():
            form.save()
            return redirect('listar')
    else:
        form = LinkForm(instance=links)
    return render(request, 'edita_links.html', {'form': form, 'links': links})

@login_required
def deletar(request, id):
    links = get_object_or_404(LinkModel, id=id)
    links.delete() 
    return redirect('listar')
    
