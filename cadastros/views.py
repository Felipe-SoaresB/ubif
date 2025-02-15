from django.shortcuts import redirect, render
from django.contrib import messages
from cadastros.models import OfertaCarona, Usuario
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def cadastro_usuario(request):
    if request.method == 'POST':
        acao = request.POST.get('btnAcao')
    
        if acao == "Novo_Usuario":
            nome = request.POST.get('txtNome')
            email = request.POST.get('txtEmail')
            senha = request.POST.get('txtSenha')
            telefone = request.POST.get('txtTelefone')
            
            # Verificando se o e-mail já está cadastrado
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Usuário já cadastrado com esse Email!')
                return redirect('cadastros:cadastro_usuario')
            
            confirmar_senha = request.POST.get('confirmar_senha')

            # Verificando se as senhas coincidem
            if senha != confirmar_senha:
                messages.error(request, 'As senhas não coincidem!')
                return redirect('cadastros:cadastro_usuario')

            # Criando uma nova instância do usuário com os campos obrigatórios
            usuario = Usuario(nome=nome, telefone=telefone, email=email, is_active=True, is_admin=False)
            
            # Salvando a senha de forma segura
            usuario.set_password(senha)
            try:
                usuario.save()
                messages.success(request, 'Usuário cadastrado com sucesso!')
                return redirect('autenticacao:login')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao salvar o usuário: {str(e)}')
    
    return render(request, 'cadastro_usuario.html')

@login_required
def oferta_carona(request):
    if request.method == 'POST':
        acao = request.POST.get('btnAcao')
        if acao == "oferecer_carona":
            motorista = request.user  # Já temos o usuário autenticado, não precisa buscar de novo

            # Obtendo os dados do formulário
            origem = request.POST.get('txtOrigem')
            destino = request.POST.get('txtDestino')
            data = request.POST.get('txtData_hora')
            num_vagas = request.POST.get('txtVagas')
            descricao = request.POST.get('txtDescricao')

            # Criando a oferta de carona
            oferta = OfertaCarona(
                motorista=motorista,  # Agora corretamente associado ao usuário logado
                origem=origem,
                destino=destino,
                data_hora=data,
                vagas_ofertadas=num_vagas,
                descricao=descricao,
                status='Aberta'
            )
            oferta.save()

            messages.success(request, 'Oferta de Carona cadastrada com sucesso!')
            return redirect('core:main')  # Redirecionamento correto após o cadastro

    return render(request, 'oferta_carona.html')

def listar_caronas(request):
    ofertas = OfertaCarona.objects.filter(status='Aberta').exclude(motorista=request.user).order_by('data_hora')
    return render(request, 'lista_ofertas.html', {'ofertas': ofertas})

def home(request):
    return render(request, 'home.html')

