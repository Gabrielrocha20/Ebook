from unicodedata import category

from decouple import config
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
from django.views.generic.base import TemplateView
from utils.gerador import gerador_token
from utils.pagination import make_pagination

from .models import Categoria, Produto


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')

        return render(request, 'home/pages/Login.html')

    def post(self, request):
        username = request.POST.get('usuario')
        password = request.POST.get('senha')

        user = authenticate(username = username, password = password)

        if user:
            login(request, user = user)
            return redirect('home:home')
        
        
        messages.error(
                request,
                'Usuario ou senha incorretos'
            )
        return redirect('home:login')

class CadastrarConta(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')

        return render(request, 'home/pages/Cadastro.html')

    def post(self, request):
        username = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        btn_token = request.POST.get('btn_token')
        input_token = request.POST.get('token')
        token = gerador_token()

        user = User.objects.filter(Q(username = username) | Q(email=email))

        if user:
            messages.error(
                request,
                'Usuário ou email ja existe'
            )
            return redirect('home:cadastrar')

        if len(senha) < 6:
            messages.error(
                request,
                'Senha precisa ter no minimo 6 digitos'
            )
            return redirect('home:cadastrar')
        
        if len(username) < 8:
            messages.error(
                request,
                'Nome de usuário precisa ter no minimo 8 digitos'
            )
            return redirect('home:cadastrar')

        if btn_token == 'on':
            subject = 'Token de verificação'
            html_message = render_to_string('home/pages/mail.html', {'token': token})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, config('EMAIL_HOST_USER'), [email], html_message=html_message,fail_silently=False,)

            request.session['token'] = token
            messages.success(
                request,
                'Token Enviado para o email'
            )
            return render(request, 'home/pages/Cadastro.html', context={
                'atualCad':True,
                'username': username,
                'email': email,
                'senha': senha,
                'is_verificado': True,
                })

        check_token = request.session['token']
        if input_token == check_token:
            usuario = User.objects.create_user(username=username, email=email, password=senha)
            usuario.save()
            user = authenticate(username = username, password = senha)
            login(request, user = user)
            return redirect('home:home')

        messages.error(
                request,
                'Token de verificação errado'
            )
            
        return redirect('home:cadastrar')

# Create your views here.
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return redirect('home:home')
        

class HomeView(View):
    def get(self, request):
        categorias = Categoria.objects.all().order_by('-id')
        produtos = Produto.objects.all().order_by('-id')
        produtos = produtos[:50]
        return render(request, 'home/pages/index.html', context={
            'categorias': categorias,
            'produtos': produtos,
            'produtos_destaque': produtos[:4]
            })


class SearchView(View):
    def get(self, request):
        categoria = request.GET.get('categoria')
        pesquisa = request.GET.get('q', '').strip()
        if (categoria != "0") and (categoria is not None):
            return redirect('home:categoria', categoria)

        categorias = Categoria.objects.all().order_by('-id')
        produtos = Produto.objects.filter(Q(nome__icontains=pesquisa) | Q(descricao_curta__icontains=pesquisa))
        page_obj, pagination_range = make_pagination(
            request,
            produtos,
            25
        )
        return render(request, 'home/pages/produtos.html', context={
            'produtos': page_obj,
            'categorias': categorias,
            'title': f'{pesquisa} | Produtos',
            'pagination_range': pagination_range,
        })


class CategoriaView(View):
    def get(self, request, id):
        categorias = Categoria.objects.all().order_by('-id')
        categoria = get_object_or_404(Categoria, pk=id, )

        produtos = Produto.objects.filter(categoria__id=id)
        page_obj, pagination_range = make_pagination(
            request,
            produtos,
            50
        )
        
        return render(request, 'home/pages/produtos.html', 
        context={
            'produtos': page_obj,
            'categoria_nome': categoria,
            'categorias': categorias,
            'title': f'{categoria} | Categoria',
            'pagination_range': pagination_range,
            })

