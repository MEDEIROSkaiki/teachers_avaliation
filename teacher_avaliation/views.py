from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from .models import Disciplina

# 1. IMPORTE OS SEUS NOVOS FORMULÁRIOS NO TOPO
from .forms import PessoaCreationForm, DisciplinaForm, LoginForm # (O LoginForm será usado depois)


# ========================================
# Home (Está OK)
# ========================================
@login_required
def home(request):
    return render(request, 'teacher_avaliation/home.html')


# ========================================
# Signup (CORRIGIDO)
# ========================================
def signup(request):
    if request.method == "POST":
        # 2. USA O SEU FORMULÁRIO CUSTOMIZADO (PessoaCreationForm)
        form = PessoaCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()           # Salva o novo usuário Pessoa no banco
            auth_login(request, user)  # loga automaticamente depois do cadastro
            return redirect('home')    # redireciona para a home após cadastro
    else:
        # 2. USA O SEU FORMULÁRIO CUSTOMIZADO (PessoaCreationForm)
        form = PessoaCreationForm()

    context = {
        'form': form
    }
    return render(request, 'teacher_avaliation/signup.html', context)


# ========================================
# Adicionar Disciplina (CORRIGIDO)
# ========================================
@login_required # Boa prática, apenas usuários logados podem adicionar
def adicionar_disciplina(request):
    if request.method == 'POST':
        # 3. USA O SEU FORMULÁRIO (DisciplinaForm) com dados do POST
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save() # <-- SALVA A NOVA DISCIPLINA NO POSTGRESQL
            return redirect('home') # Ou para 'listar_disciplinas'
    
    else:
        # 3. Se for GET, apenas mostra um form vazio
        form = DisciplinaForm()

    contexto = {'form': form}
    # 4. LEMBRE-SE DO CAMINHO CORRETO DO TEMPLATE (com /)
    return render(request, 'teacher_avaliation/adicionar_disciplina.html', contexto)


# ========================================
# Listar Disciplinas (CORRIGIDO)
# ========================================
@login_required
def listar_disciplinas(request):
    
    disciplinas = Disciplina.objects.all() 
    contexto = {
        'lista_disciplinas': disciplinas
    }

    # 4. LEMBRE-SE DO CAMINHO CORRETO DO TEMPLATE (com /)
    return render(request, 'teacher_avaliation/listar_disciplinas.html', contexto)


# ========================================
# Adicionar Aluno / Professor (Ainda sem lógica de salvar)
# ========================================
@login_required
def adicionar_aluno(request):
    # (Futuramente você precisará de um AlunoForm aqui,
    #  mas por enquanto apenas renderiza o HTML)
    return render(request, 'teacher_avaliation/adicionar_aluno.html')

@login_required
def adicionar_professor(request):
    
    # 1. BUSCA NO BANCO DE DADOS:
    #    Pega todas as disciplinas (incluindo "Japonês")
    todas_as_disciplinas = Disciplina.objects.all()

    # 2. CRIA O CONTEXTO PARA ENVIAR AO TEMPLATE:
    contexto = {
        'lista_disciplinas_do_banco': todas_as_disciplinas
    }

    # 3. ENVIA A LISTA PARA O HTML:
    return render(request, 'teacher_avaliation/adicionar_professor.html', contexto)