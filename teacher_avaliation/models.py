from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# ========================================
# Manager para o nosso Custom User Model (Pessoa)
# ========================================
class PessoaManager(BaseUserManager):
    def create_user(self, cpf, nome, password=None, **extra_fields):
        if not cpf:
            raise ValueError('O CPF é obrigatório')
        
        user = self.model(cpf=cpf, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(cpf, nome, password, **extra_fields)


# ========================================
# Pessoa (Aluno, Professor, Admin)
# ========================================
class Pessoa(AbstractBaseUser, PermissionsMixin):
    TIPO_CHOICES = [
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    ]

    # Campos do seu modelo original
    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)

    # Campos requeridos pelo Django
    is_staff = models.BooleanField(default=False) # Permite acesso ao admin
    is_active = models.BooleanField(default=True) # Usuário ativo pode logar
    date_joined = models.DateTimeField(default=timezone.now)

    # Define o manager e o campo que será usado como "username"
    objects = PessoaManager()
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome'] # Campos pedidos ao criar superuser

    def __str__(self):
        return self.nome


# ========================================
# Disciplina
# ========================================
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    data_inicio = models.DateField()

    def __str__(self):
        return self.nome


# ========================================
# DisciplinaPessoa (Relaciona Pessoa e Disciplina)
# ========================================
class DisciplinaPessoa(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]

    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('disciplina', 'pessoa')

    def __str__(self):
        return f"{self.pessoa} - {self.disciplina}"


# ========================================
# Categoria de Avaliação
# ========================================
class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


# ========================================
# Avaliacao (uma avaliação de um aluno para uma disciplina)
# ========================================
class Avaliacao(models.Model):
    disciplina_pessoa = models.ForeignKey(DisciplinaPessoa, on_delete=models.CASCADE)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.id} - {self.disciplina_pessoa}"


# ========================================
# AvaliacaoCategoria (nota por categoria dentro de uma avaliação)
# ========================================
class AvaliacaoCategoria(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        unique_together = ('avaliacao', 'categoria')

    def __str__(self):
        return f"{self.categoria} - {self.nota}"


# ========================================
# MediaDisciplina
# ========================================
class MediaDisciplina(models.Model):
    disciplina_pessoa = models.ForeignKey(DisciplinaPessoa, on_delete=models.CASCADE)
    media = models.DecimalField(max_digits=4, decimal_places=2)
    qtde_avaliacoes = models.IntegerField()
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.disciplina_pessoa} - {self.media}"


# ========================================
# MediaDisciplinaCategoria
# ========================================
class MediaDisciplinaCategoria(models.Model):
    disciplina_pessoa = models.ForeignKey(DisciplinaPessoa, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    media = models.DecimalField(max_digits=4, decimal_places=2)
    qtde_avaliacoes = models.IntegerField()
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('disciplina_pessoa', 'categoria')

    def __str__(self):
        return f"{self.disciplina_pessoa} - {self.categoria} - {self.media}"


# ========================================
# MediaProfessor
# ========================================
class MediaProfessor(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    media = models.DecimalField(max_digits=4, decimal_places=2)
    qtde_disciplinas = models.IntegerField()
    qtde_avaliacoes = models.IntegerField()
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pessoa} - {self.media}"


# ========================================
# MediaUniversidade
# ========================================
class MediaUniversidade(models.Model):
    media = models.DecimalField(max_digits=4, decimal_places=2)
    qtde_professores = models.IntegerField()
    qtde_disciplinas = models.IntegerField()
    qtde_avaliacoes = models.IntegerField()
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Media Universidade - {self.media}"
