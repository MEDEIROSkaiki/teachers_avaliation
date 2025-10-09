from django.db import models

# ========================================
# Pessoa (Aluno, Professor, Admin)
# ========================================
class Pessoa(models.Model):
    TIPO_CHOICES = [
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    ]

    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    admin = models.BooleanField(default=False)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)

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
