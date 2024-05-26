from .models import CodigoPedido
from random import randint
import secrets
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from PIL import Image, ImageDraw
import aspose.words as aw
from pathlib import Path




def gera_num_pedido(paciente) -> str:
    while True:
        formato = f'NUTRI({paciente}):'
        pedido = secrets.choice(range(200,500000))
        juncao = randint(1, 10000000)
        pedido += juncao
        codigo = formato + str(pedido)
        pedido_db = CodigoPedido.objects.filter(pedido=codigo)
        if not pedido_db:
            pedido_db = CodigoPedido.objects.create(pedido=codigo, paciente=paciente)
            try:
                pedido_db.save()
            except Exception as e:
                return 'Erro ao salvar no DB'
            break
        continue

    return pedido_db

def envia_email(path_template: str, assunto: str, para: list, **kwargs) -> bool:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return True

def valida_campo_branco(*args):
    for arg in args:
        if len(arg.strip()) == 0:
            return False
        return True
    
def gera_comprovante(nome: str, sobrenome: str,  cpf: str, data_consulta: dict, periodo:str, local: str, token: str, nutri: str, data_emissao: dict):
    #em desenvolvimento
    nome_completo = nome + sobrenome
    caminho_projeto = Path(__file__).parent.parent
    caminho_img = caminho_projeto / 'templates/static/consultas/img/comprovante.png'
    comprovante = Image.open(caminho_img)
    personalizar_comprovante = ImageDraw.Draw(comprovante)
    personalizar_comprovante.text((3000,800), nome_completo, fill='white')
    personalizar_comprovante.text((400,800), cpf, fill='white')
    personalizar_comprovante.text((600,1000), data_consulta['dia'], fill='white')
    personalizar_comprovante.text((630,1000), data_consulta['mes'], fill='white')
    personalizar_comprovante.text((660,1000), data_consulta['ano'], fill='white')
    personalizar_comprovante.text((800,1200), periodo, fill='white')
    personalizar_comprovante.text((10000,1400), local, fill='white')
    personalizar_comprovante.text((1200,1600), data_emissao['dia'], fill='white')
    personalizar_comprovante.text((1200,1600), data_emissao['mes'], fill='white')
    personalizar_comprovante.text((1200,1600), data_emissao['ano'], fill='white')
    personalizar_comprovante.text((1400,1800), nutri, fill='white')
    caminho_comprovante = caminho_projeto / 'media/comprovantes'
    comprovante.save(f'{caminho_comprovante}/{token}.png', 'png')

    caminho_comprovante = str(caminho_comprovante) + '/' + token + '.png'
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)

    builder.insert_image(caminho_comprovante)

    doc.save(f'{nome_completo}-{token}.pdf')
    
    Path(caminho_comprovante).unlink(missing_ok=True)

    return doc

      

