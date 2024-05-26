from django.contrib import messages
from random import randint, choice, uniform
from datetime import datetime, time
from .models import Pacientes, DadosPaciente, Refeicao, Opcao
from consultas.models import Consulta, DadosConsulta, Cancelamento, CodigoPedido
import secrets
from pathlib import Path
from django.conf import settings
from PIL import Image
import os
from datetime import date

def valida_campos_nulos(*args) -> bool:
    for x in args:
        if len(x.strip()) == 0:
            return False
    return True

def valida_campos(request, *args):
    for x in args:
        if len(x.strip()) == 0 or not x.isnumeric() :
            messages.add_message(request, messages.ERROR, 'todos os campos são numeros e obrigatorios!')
            return False
    return True
        
def gera_cpf():                                                        
    cpf = [randint(0, 9) for x in range(9)]                              
                                                                                
    for _ in range(2):                                                          
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                
        cpf.append(11 - val if val > 1 else 0)                                  
                                                                                
    return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)

def basal(pessoa: dict) -> int:
    if pessoa['sexo'] == 'F':
        calculo = 10* pessoa['peso']+6.25*pessoa['altura']-(5*pessoa['idade'])-161
    else:
        calculo = 10 * pessoa['peso'] + 6.25 * pessoa['altura'] - (5 * pessoa['idade']) + 5

    return f'{calculo:.0f}'


class Geradora:
    def __init__(self, nutri_id: int, qtd_dados=40, limite=40):
        self.nutri_id = nutri_id
        self.qtd_dados = qtd_dados
        self.limite = limite

    @classmethod
    def gera_telefone(cls) -> str:
        digitos = ['9']
        telefone = []
        ddd_estado = ['82','71','85','98','83','81','86','84','79','68','96','92','97','91','69','95','63','27','31','21','11','41','51','47']
        for i in range(0,8):
            digitos += str(randint(0, 9))    
        
        digitos.insert(5, '-')
        ddd = choice(ddd_estado)
        digitos.insert(0, ddd)
        digitos.insert(1, '-')

        telefone = ''.join(digitos)

    
        return telefone

    @classmethod
    def gera_idade(cls) -> int:
        idade = randint(5,80)

        return idade
    
    @classmethod
    def gera_email(cls, nome: str, sobrenome: str) -> str:
        nome_completo = nome + sobrenome
        numero_aleatorio = randint(1000,50000)
        provedores = ['_@gmail.com', '_@outlook.com', '_@Yahoo.com']
        provedor = choice(provedores)
        email =  nome_completo + '_' + str(numero_aleatorio) + provedor

        return email

    @classmethod
    def gera_cpf(cls):                                                        
        cpf = [randint(0, 9) for x in range(9)]                              
                                                                                    
        for _ in range(2):                                                          
            val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                    
            cpf.append(11 - val if val > 1 else 0)                                  
                                                                                    
        return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)
    
    @classmethod
    def gera_sexo(cls)  -> str:
        sexos = ['M', 'F']
        sexo = choice(sexos)

        return sexo
    
    @classmethod
    def gera_peso(cls, idade: int) -> int:
        if idade > 4 and idade <18:
            peso =  randint(14,90)
        else:
            peso = randint(50,160)
        
        return peso

    @classmethod
    def gera_altura(cls, idade: int) -> int:
        if idade > 4 and idade <18:
            altura = randint(99, 182)
        else: 
            altura = randint(100, 200)

        return altura

    @classmethod
    def gera_basal(cls, sexo: str, peso: int, altura: int, idade: int) -> float:
        if sexo == 'F':
            calculo = 10* peso + 6.25 * altura - (5* idade) - 161
        else:
            calculo = 10 * peso + 6.25 * altura - (5 * idade) + 5

        return f'{calculo:.0f}'

    @classmethod
    def gera_percentual_gordura(cls) -> int:
        p_gordura = randint(10, 60)

        return p_gordura
    
    @classmethod
    def gera_percentual_musculo(cls) -> int:
        p_musculo = randint(20, 60)

        return p_musculo
    
    @classmethod
    def gera_colesterol_hdl(cls) -> int:
        colesterol_hdl = randint(30, 100)

        return colesterol_hdl
    
    @classmethod
    def gera_colesterol_ldl(cls) -> int:
        colesterol_ldl = randint(60, 170)

        return colesterol_ldl
    
    @classmethod
    def gera_colesterol_total(cls) -> int:
        colesterol_total = randint(30, 200)

        return colesterol_total
    @classmethod

    @classmethod
    def gera_endereco(cls) -> str:
        locais = ['São Paulo, Toninho Cerezo 820, andar 8', 'São Paulo, rua batalhao teodoro 536', 'São Paulo, Paulista candida, andar 2']
        local = choice(locais)

        return local

    @classmethod
    def gera_datas(cls, data_atual = datetime.now()) -> list:
        status_list = ['C', 'F', 'A']
        status_escolha = choice(status_list)

        aleatorio_mes = [1,2,3]

        meses = [x for x in range(1,13)]
        dias = [x for x in range(1,28)]
        
        horas = ['10', '11', '12', '14', '15', '16', '17', '18']
        ano = data_atual.year
        minutos = 00
        segundos = 00

        mes_atual = data_atual.month
        dia_atual = data_atual.day
        mes_aleatorio = choice(aleatorio_mes)
        data_horario = []
        hora = choice(horas)

        if status_escolha == 'C':
            mes = choice(meses)
            if mes < mes_atual:
                mes = mes_atual - mes_aleatorio
            dia = choice(dias)
            data = datetime(ano,mes,dia,int(hora),minutos,segundos)
            data.strftime('%d/%m/%Y %H:%M:%S')
            

            data_horario.append(data)
            data_horario.append(status_escolha)

            return data_horario
        
        elif status_escolha == 'F':
            mes = choice(meses)
            if mes > mes_atual:
                mes = mes_atual - mes_aleatorio
            dia = choice(dias)
            data = datetime(ano,mes,dia,int(hora),minutos,segundos)
            data.strftime('%d/%m/%Y %H:%M:%S')
            

            data_horario.append(data)
            data_horario.append(status_escolha)

            return data_horario
        
        elif status_escolha == 'A':
            mes = choice(meses)
            if mes < mes_atual:
                mes = mes_atual + mes_aleatorio
            dia = choice(dias)
            data = datetime(ano,mes,dia,int(hora),minutos,segundos)
            data.strftime('%d/%m/%Y %H:%M:%S')
            

            data_horario.append(data)
            data_horario.append(status_escolha)

            return data_horario

    @classmethod
    def gera_cancelamento(cls, consulta: Consulta) -> Cancelamento:
        motivos = ['E', 'I', 'O']
        detalhes = ['imprevisto na agenda', 'Paciente cancelou', 'Atraso do paciente', 'Fiquei Doente', 'Problema técnico']
        detalhe = choice(detalhes)
        motivo = choice(motivos)
        try: 
            cancela = Cancelamento.objects.create(consulta=consulta, detalhes=detalhe, motivo=motivo)     
            cancela.save()
            return cancela
        except Exception as e:
              print(e)
              return False

    @classmethod
    def gera_codigo(cls, paciente) -> CodigoPedido:
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
                return pedido_db
            except Exception as e:
                print(e)
                return False

    @classmethod
    def gera_trigliceridios(cls) -> int:
        trigliceridios = randint(100, 500)

        return trigliceridios
    
    def gera_paciente(self, qtd) -> Pacientes:
        nutri = self.nutri_id
        nomes = ['Helena', 'Miguel', 'Alice',	'Arthur', 'Laura', 'Heitor', 'Manuela',	'Bernardo', 'Valentina', 'Davi', 'Sophia', 'Théo', 'Isabella',
                'Lorenzo', 'Heloísa', 'Gabriel', 'Luiza',	'Pedro', 'Júlia', 'Benjamin', 'Lorena', 'Matheus', 'Lívia', 'Lucas', 'MariaLuiza', 'Nicolas',
                'Cecília', 'Joaquim', 'Eloá', 'Samuel','Giovanna',	'Henrique', 'Maria Clara', 'Rafael', 'Maria Eduarda','Guilherme', 'Mariana Enzo', 
                'Lara',	'Murilo', 'Beatriz',	'Benício', 'Antonella',	'Gustavo', 'Maria Júlia', 'Isaac', 'Emanuelly',	'João Miguel', 'Isadora	Lucca',
               ' Ana Clara',' Enzo Gabriel', 'Melissa','	Pedro Henrique','Ana Luiza',' Felipe','Ana Júlia', 'João Pedro', 'Esther', 'Pietro',  
               'Lavínia Anthony','Maitê Daniel', 'Maria Cecília','Bryan', 'Maria Alice', 'Davi Lucca', 'Sarah',	'Leonardo', 'Elisa',	'Vicente','Liz',
                'Eduardo', 'Yasmin', 'Gael', 'Isabelly', 'Antônio', 'Alícia', 'Vitor', 'Clara',	'Noah', 'Isis', 'Caio', 'Rebeca',	'João', 'Rafaela',
                'Emanuel', 'Marina', 'Cauã', 'Ana Laura', 'João Lucas', 'Maria Helena', 'Calebe', 'Agatha', 'Enrico', 'Gabriela', 'Vinícius', 'Catarina',
                'Bento']
        sobrenomes = ['Rossi', 'Ferrari', 'Mello', 'Melo', 'Merlo', 'Russo', 'Casagrande', 'Basso', 'Fontana', 'Fontaine', 'Martinelli', 'Martini', 
                    'Martinus', 'Silva', 'Santos','Ferreira', 'Pereira', 'Oliveira', 'Costa', 'Rodrigues', 'Martins', 'Jesus', 'Sousa', 'Fernandes', 'Gonçalves',
                    'Gomes', 'Lopes', 'Marques', 'Alves', 'Almeida', 'Ribeiro', 'Pinto', 'Carvalho', 'Teixeira', 'Moreira', 'Correia', 'Mendes', 'Nunes']
        
        for x in range(qtd):
            nome = choice(nomes)
            sobrenome = choice(sobrenomes)
            cpf = self.gera_cpf()
            sexo = self.gera_sexo()
            idade = self.gera_idade()
            email = self.gera_email(nome, sobrenome)
            telefone = self.gera_telefone()
            try:
                paciente = Pacientes.objects.create(nome=nome, sobrenome=sobrenome, cpf=cpf, sexo=sexo, idade=idade, telefone=telefone, email=email, nutri=nutri)
                paciente.save()
                return paciente 
            except Exception as e:
                print(e)
                return False
            
    def gera_dados_paciente(self) -> DadosPaciente:
        qtd = self.qtd_dados

        for x in range(qtd):
            paciente = self.gera_paciente(qtd)
            data = datetime.now()
            peso = self.gera_peso(paciente.idade)
            altura = self.gera_altura(paciente.idade)
            taxa_basal = self.gera_basal(paciente.sexo, peso, altura, paciente.idade)
            p_gordura = self.gera_percentual_gordura()
            p_musculo = self.gera_percentual_musculo()
            colesterol_hdl = self.gera_colesterol_hdl()
            colesterol_ldl = self.gera_colesterol_ldl()
            colesterol_total = self.gera_colesterol_total()
            trigliceridios = self.gera_trigliceridios()

            try:
                dados_paciente = DadosPaciente.objects.create(
                    paciente=paciente, data=data, peso=peso, altura=altura, taxa_metabolismo_basal=taxa_basal, percentual_gordura = p_gordura,
                    percentual_musculo = p_musculo, colesterol_hdl = colesterol_hdl, colesterol_ldl = colesterol_ldl, colesterol_total = colesterol_total,
                    trigliceridios = trigliceridios
                    )
                dados_paciente.save()
                return dados_paciente
            except Exception as e:
                print(e)
                return False

    def gera_consulta(self) -> Consulta:
        qtd = self.qtd_dados

        for x in range(qtd):
            paciente = self.gera_dados_paciente()
            print(self.gera_plano_alimentar(paciente.paciente))
            nutri = self.nutri_id
            paciente_db = Pacientes.objects.filter(cpf=paciente.paciente.cpf).first()
            local= self.gera_endereco()
            data_horario = self.gera_datas()
            codigo = self.gera_codigo(paciente_db)


            try:
                consulta = Consulta.objects.create(paciente=paciente_db, nutri=nutri, local=local, data_horario=data_horario[0], status=data_horario[1], codigo=codigo)
                consulta.save()

                if data_horario[1] == 'C':
                    self.gera_cancelamento(consulta)
                if data_horario[1] == 'F':
                    self.gera_dados_consulta(consulta)

            except Exception as e:
                print(e)
                return False
            
        return consulta

    def gera_dados_consulta(self, consulta: Consulta) -> DadosConsulta:
        qtd = self.qtd_dados
        resumos = ['Paciente expressou interesse em adotar uma dieta mais equilibrada para apoiar seus objetivos de saúde e condicionamento físico',
                   'Durante a consulta, o paciente mencionou o desejo de melhorar seus hábitos alimentares para alcançar um estilo de vida mais saudável.',
                   'O paciente solicitou orientações nutricionais para complementar seu novo regime de exercícios e maximizar os benefícios para a saúde.',
                   'Durante a consulta, o paciente expressou preocupação com sua dieta atual e deseja fazer mudanças para melhorar sua energia e bem-estar geral.',
                   'O paciente manifestou interesse em aprender mais sobre como a nutrição pode impactar sua saúde e qualidade de vida, e busca orientações para fazer escolhas alimentares mais saudáveis.'
                   ,'Durante a consulta, o paciente expressou o desejo de adotar uma dieta específica para auxiliar no controle do diabetes e melhorar sua qualidade de vida',
                   'O paciente relatou problemas de digestão e busca orientações nutricionais para ajudar a aliviar sintomas digestivos desconfortáveis.',
                   'Durante a consulta, o paciente mencionou o desejo de seguir uma dieta vegetariana ou vegana para apoiar seus valores éticos e de sustentabilidade.',
                   'O paciente está procurando estratégias nutricionais para melhorar sua saúde cardiovascular e reduzir fatores de risco associados, como pressão alta e colesterol elevado'
                   ]
        objetivos = ['M','D','S']
        preferencias_alimentares = ['O paciente prefere iniciar o dia com um café da manhã rico em proteínas, como ovos mexidos ou iogurte com frutas.',
                                    'Durante a consulta, o paciente mencionou que tem preferência por refeições leves no almoço, como saladas ou sanduíches com proteínas magras.',
                                    'O paciente expressou gosto por lanches à tarde, como frutas frescas ou barras de cereais, para manter a energia ao longo do dia',
                                    'Durante a consulta, o paciente compartilhou sua preferência por jantares caseiros preparados com ingredientes frescos e naturais, como peixes grelhados e vegetais assados.',
                                    'O paciente admitiu ter uma queda por doces e lanches pouco saudáveis, mas está interessado em encontrar alternativas mais nutritivas para satisfazer seus desejos sem comprometer sua saúde'
                                    ]
        
        opcoes = ['S', 'N']
        freq_tabagismo = ['1M', '2M', 'M+', 'M-']
        atividades = ['O', 'A', 'L', 'N', 'C']
        dias_semana = [x for x in range(1,8)]

        horas= [x for x in range(6, 22)]
        hora = choice(horas)
        minuto = 00
        segundo =00
        hora_fome = time(hora,minuto,segundo)
        horas_atv = time(hora + 1 ,minuto + 30, segundo)

       
        for x in range(qtd):

            resumo = choice(resumos)
            objetivo = choice(objetivos)
            preferencia_alimentar = choice(preferencias_alimentares)
            horario_fome = hora_fome
            horas_sono = randint(4,12)
            tabagismo = choice(opcoes)
            if tabagismo == 'S':
                frequencia_tabagismo = choice(freq_tabagismo)
            else:
                frequencia_tabagismo = None
            atividade_fisica = choice(opcoes)
            if atividade_fisica == 'S':
                atividade = choice(atividades)
                horario_atividade = horas_atv
                qtd_dias_atividade = choice(dias_semana)
            else:
                atividade = None
                horario_atividade = None
                qtd_dias_atividade = None

            try:
                dados_consulta = DadosConsulta.objects.create(
                    consulta=consulta, resumo=resumo, objetivo=objetivo, preferencia_alimentar=preferencia_alimentar, horario_fome=horario_fome,
                    horas_sono=horas_sono, tabagismo=tabagismo, frequencia_tabagismo=frequencia_tabagismo, atividade_fisica=atividade_fisica,
                    atividade=atividade, horario_atividade=horario_atividade, qtd_dias_atividade = qtd_dias_atividade
                )
                dados_consulta.save()
                return dados_consulta
            except Exception as e:
                print(e)
                return False

    def gera_plano_alimentar(self, paciente: Pacientes) -> Refeicao:
        qtd = self.qtd_dados
        descricao_cafe = ['Ovo mexido com pão na chapa e chá verde', 'Vitamina de frutas com banana, morango e leite desnatado', 
                          'Tapioca recheada com queijo branco e peito de peru, acompanhada de suco de abacaxi natural', 
                          'Omelete de claras de ovos com espinafre e queijo cottage, acompanhado de uma fatia de pão integral e suco de melancia', 
                          'Panquecas de aveia com banana e mel, acompanhadas de chá de hortelã', 
                          'Iogurte natural com granola caseira, frutas vermelhas e uma colher de sopa de mel, acompanhado de uma maçã']
        descricao_almoco = ['Salada de quinoa com legumes grelhados (abobrinha, pimentão, berinjela) e frango marinado ao limão, acompanhada de água com gás e limão.',
                            'Filé de peixe assado com molho de ervas frescas, arroz integral e salada de folhas verdes com tomate, pepino e azeitonas, regada com azeite de oliva',
                            'Espaguete integral com molho de tomate caseiro, almôndegas de carne magra e brócolis no vapor, acompanhado de chá de camomila.', 
                            '2 fatias de pão integral com 2 ovos mexidos e 400 ml de suco de laranja natural',
                            'Salada de folhas verdes com tomate cereja, cenoura ralada e molho de iogurte, acompanhada de filé de frango grelhado e arroz integral.',
                            'Macarrão integral com molho de tomate caseiro, brócolis e frango desfiado, acompanhado de água com limão.'] 
        descricao_janta = ['Sopa de lentilhas com legumes variados (cenoura, abóbora, batata) e cubos de tofu, acompanhada de pão integral.', 
                           'Risoto de cogumelos com arroz integral, ervilhas e queijo parmesão, acompanhado de salada de rúcula, tomate seco e nozes.',
                           'Espetinhos de frango com legumes (pimentão, cebola, abobrinha) grelhados, servidos com couscous marroquino e chá verde gelado.'
                           ,'200 gramas de arroz, 100 gramas de feijão, 120 gramas de filé de peixe grelhado e 400 ml de suco de uva integral',
                           'Sopa de legumes com quinoa e frango desfiado, acompanhada de torradas integrais.', 
                           'Salada de quinoa com vegetais assados (abobrinha, pimentão, cebola) e peito de frango grelhado, regada com vinagrete de limão.']
        titulos = ['Café da manha', 'Almoço', 'Café da Tarde',  'Janta', 'Ceia']
        horarios_manha = ['05:00', '06:00', '07:00', '08:00','09:00', '10:00', '11:00']
        horarios_tarde = ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']
        horarios_noite = [ '19:00', '20:00', '21:00', '22:00', '23:00'] 
        
        
        carboidrato = [x for x in range(35,110)]
        proteina = [x for x in range(20,110)]
        gordura = [x for x in range(10, 50)]
        ''''
        path = os.path.join(settings.BASE_DIR, f'media/-{date.today}-dado-gerado-automaticamente')

        path_projeto = Path(__file__).parent.parent
        path_imagens = path_projeto / 'templates/static/plataforma/img/opcoes'
        path_imagens_manha = path_imagens / 'manha'

        imagems_manha = []
        imagems_tarde = []

        for img in path_imagens_manha.glob('*'):
            imagems_manha.append(str(img))
        
        for img in path_imagens.glob('*'):
            imagems_tarde.append(str(img))
        '''

        for x in range(qtd):
            titulo = choice(titulos)
            if titulo == 'Café da manha':
                horario = choice(horarios_manha)      

            elif titulo == 'Almoço':
                horario = choice(horarios_tarde)

            elif titulo == 'Café da Tarde':
                horario = choice(horarios_tarde)
            else:
                horario = choice(horarios_noite)
               
            carboidratos = choice(carboidrato)
            proteinas = choice(proteina)
            gorduras = choice(gordura)

            try:
                ref = Refeicao.objects.create(paciente=paciente, titulo=titulo, horario=horario, carboidratos=carboidratos, proteinas=proteinas, gorduras=gorduras)
                ref.save()
                for x in range(2):

                    if ref.titulo in ['Café da manha', 'Café da Tarde']:
                        descricao = choice(descricao_cafe)
                        imagem = 'opcao/cafe-da-manha-1642012355257_v2_450x450.jpg'
                        '''
                        imagem = choice(imagems_manha)
                        print(f'imagem NN format {imagem}')
                        pil_img = Image.open(imagem)
                        pil_img.save(path)
                        imagem.replace('C%3A/Users/vinic/OneDrive/%C3%81rea%20de%20Trabalho/Python_Full/nutri_lab/templates/static/plataforma/img/opcoes/', 'opcao/')
                        descricao = choice(descricao_cafe)
                        print(f'imagem format {imagem}')
                        '''
                    elif ref.titulo == 'Almoço':
                        #imagem = choice(imagems_tarde)
                        descricao = choice(descricao_almoco)
                        imagem = 'opcao/janta.webp'
                        
                    else:
                        imagem = 'opcao/jantar-fitness.jpg'
                        #imagem = choice(imagems_tarde)
                        descricao = choice(descricao_janta)
                        
                    

                    op1 = Opcao.objects.create(refeicao=ref, imagem=imagem, descricao=descricao)
                    op1.save()

                return ref
            except Exception as e:
                print(e)
                return False


    



