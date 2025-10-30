from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

@login_required
def home(request):
    return render(request, 'teacher_avaliation/home.html')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # loga automaticamente depois do cadastro
            return redirect('home')    # redireciona para a home após cadastro
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'teacher_avaliation/signup.html', context)

def adicionar_aluno(request):
    # Esta função simplesmente renderiza o template que você acabou de criar
    return render(request, 'teacher_avaliation/adicionar_aluno.html')

def adicionar_professor(request):
    # Por enquanto, ela apenas renderiza o template
    return render(request, 'teacher_avaliation/adicionar_professor.html')

def adicionar_disciplina(request):
    return render(request, 'teacher_avaliation/adicionar_disciplina.html')