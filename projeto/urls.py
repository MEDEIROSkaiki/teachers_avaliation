
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from teacher_avaliation.forms import LoginForm
from teacher_avaliation import views as teacher_views
from teacher_avaliation import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('teacher_avaliation.urls')),

    # login/logout prontos do Django
    path('login/', auth_views.LoginView.as_view(
        template_name='teacher_avaliation/login.html',
        authentication_form=LoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('adicionar_aluno/', teacher_views.adicionar_aluno, name='adicionar_aluno'),
    path('adicionar_professor/', teacher_views.adicionar_professor, name='adicionar_professor'),
    path('adicionar_disciplina/', teacher_views.adicionar_disciplina, name='adicionar_disciplina'),
    path('disciplinas/', views.listar_disciplinas, name='lista_disciplinas'),
]
