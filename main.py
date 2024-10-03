from flask import Flask,  render_template, redirect, request #jsonify, send_from_directory <-- conhecimento
import mysql.connector
import os

from funcs_internas.functionsSQL import banco
from funcs_internas.user import user
create_banco = banco()
create_user = None


app = Flask(__name__)



#Diretorio banco de imagens 
diretorio = 'C:\\Users\\davir\\OneDrive\\Área de Trabalho\\Gestão O.S\\banco de fotos\\'
    
#banco de dados


#variaveis globais
gb_usuario = None
gb_senha = None
gb_id = None
flag_log = False
gb_cargo = 'gestor'

#Global maquina -- 
gb_sta = ''
gb_tag = ''
gb_modelo = ''
gb_rg = ''




#função de teste
@app.route('/mostrar', methods=['POST'])
def mostrar():
    print('mostrado')


#page de login
@app.route('/')
def index():
    global flag_log, gb_id,gb_usuario, gb_senha
    
    gb_usuario = None
    gb_senha = None
    gb_id = None
    flag_log = False
    flag_log = False
    return render_template('index.html')


@app.route('/autenticar', methods=['POST'])
def authenticar():
    
    global gb_usuario, gb_senha, gb_id, conexao, flag_log, create_banco, gb_cargo, create_user
    create_banco.open_Banco()
    create_banco.mostrar()
    create_banco.close_Banco()
    usuario_informado = request.form.get('login')
    senha_informada = request.form.get('senha')
    gb_usuario = usuario_informado
    gb_senha = senha_informada
    
    
    create_banco.open_Banco()
    flag_log = create_banco.autenthicar_Banco(usuario_informado,senha_informada,tabela='usuarios')
    gb_id = create_banco.buscar_Banco('usuarios',usuario_informado)
    
    create_banco.close_Banco()
    create_user = user(gb_usuario,gb_senha,gb_id,gb_cargo)
    if flag_log == True:
        return redirect('home')
    else:
        displ = 'block'
        msg = 'Usuario ou senha invalida!'
        return render_template('index.html',  login=usuario_informado,senha=senha_informada, msg=msg, displ=displ)
 

#Verificação de login            
@app.route('/home')
def home_page():
     if flag_log == True:
         return render_template('home.html')
     else:
         return redirect('/')
   
#contrutor da pagina onde a maquina sera exibida
@app.route('/maquina', methods = ['POST'])
def maquina():
    global gb_sta, create_banco, gb_usuario, flag_log

    if flag_log == True:

        create_banco.open_Banco()
        lista_maquinas = create_banco.buscar_Banco('t_equipamentos')
        maquina_selecionada = []
        #Codigo importante -----------------------
        tag_btn = request.form.keys()#------------
        #Codigo importante -----------------------
        print('lista maquina', lista_maquinas)

        print('--------',tag_btn)
        for maquina in lista_maquinas:
            if maquina[1] in tag_btn:
                maquina_selecionada.append(maquina)
                print(maquina_selecionada[0][1])
        
        create_banco.close_Banco()

        return render_template('maquina.html', maquina_selecionada=maquina_selecionada)
    else:
        return redirect('/')

        
#buscador de maquinas no home page
#tentar filtrar com pandas sla
@app.route('/buscar', methods = ['POST'])
def buscar():
    global flag_log, gb_sta, gb_modelo, gb_tag, gb_rg, gb_usuario
    
    gb_sta = request.form.get('sta')
    gb_rg = request.form.get('rg')
    gb_modelo = request.form.get('modelo')
    gb_tag =  request.form.get('tag')
    if flag_log == True:
        conexao = mysql.connector.connect(
            host='doce-gelato.cfey060w0r7y.us-east-2.rds.amazonaws.com',
            database='doce_gelato',
            user='astrodocegelato',
            password='Doce-gelato226')

        if conexao.is_connected():
            cursor = conexao.cursor()
            cursor.execute('Select * from t_equipamentos')
            lista_maquinas = cursor.fetchall()
            maquinas = []
            parametro = request.form.get('sta')
            for maquina in lista_maquinas:
                maquinas.append(maquina)
            
            print(parametro, f'<-- parametro {type(parametro)}')
            
            #caso nada seja informado motras todas as maquinas no banco
            if len(gb_sta) <=0 and len(gb_modelo) <=0 and  len(gb_tag) <=0 and len(gb_rg) <=0: 
                print('Entrei')
               
                return render_template('home.html', maquinas=maquinas, gb_usuario=gb_usuario)
            else :
                print('else')
                parametros = [gb_sta, gb_modelo, gb_tag, gb_rg]
                cont = 0
                for paramentro in parametros:
                    if len(paramentro) >= 3:
                        for maquina in maquinas:
                            if  paramentro in maquina:
                                print(maquina)
                    
            # if len(gb_rg)  <= 0:
            #      for maquina in lista_maquinas:        
            #         maquinas.append(maquina)
                
                return render_template('home.html', maquinas=maquinas)

    else:
        return redirect('/')


@app.route('/cadastrar')
def cadastrar():# rota de verificação de login
    global flag_log
    print(flag_log)
    if flag_log == False:
        return redirect("/")
    if flag_log == True:  
        return render_template('cadastrar.html')
    

@app.route('/cadastrar_sql', methods = ['POST'])
def cadastrar_sql():#Cadastro de maquina. (Fotos(criação de pagina e dowload de arquivos) e dados de texto(salvaos no banco de dados))
    global conexao,gb_usuario, gb_id,gb_cargo,create_user
    
    #verificação de login
    create_banco.open_Banco()
    flag_log = create_banco.autenthicar_Banco(gb_usuario, gb_senha, 'usuarios')
    create_banco.close_Banco()
    #verificação de login */
    
    #Verificar status de logado
    if flag_log == False:#Acesso negado
        return redirect("/")
    
    if flag_log == True:#LIBERADO
        #Verificar nivel de permissão
        #if create_user.ver_requisitos('gestor') == True:
        
        #Pegando todos os dados de textos    
        tag = request.form.get('cad_tag')
        rg  = request.form.get('cad_rg')
        sta = request.form.get('cad_sta')
        voltagem = request.form.get('cad_voltagem')
        largura = request.form.get('cad_largura')
        altura = request.form.get('cad_altura')
        comprimento = request.form.get('cad_comprimento')
        capacidade = request.form.get('cad_capacidade')
        modelo = request.form.get('cad_modelo')
        lista_dados = [tag, rg,sta,voltagem,largura,altura,comprimento,capacidade,modelo,gb_id]
        #----------------------------------------------------- 
        
        #Abaixo é tratado os dados de texto de imagens
        # 1 verificando se a tag já foi cadastrada(DUPLICIDADE)
        create_banco.open_Banco()
        flag_tag = create_banco.buscar_Banco('t_equipamentos', tag)
        create_banco.close_Banco()
       


        if flag_tag == tag:
            #maquina duplicada
            print('ERROR | Maquina duplicada | ERROR')
            return redirect('/cadastrar')    
        else:
            #Tag liberada para cadastro    
            
            #Verificando se a tag existe na lista de tags(pre geradas)
            create_banco.open_Banco()
            lista_tag = create_banco.buscar_Banco('t_tags_geradas')
            for taglist in lista_tag:
                if tag == taglist[1]:#Tag está aprovada para ser cadastrada
                    
                    print(f'Tag aprovada para cadastro')
                
                    #Pegando fotos
                    foto_tag = request.files.get('img_tag')
                    foto_etiqueta = request.files.get('img_etiqueta')
                    foto_maquina1 = request.files.get('img_maquina1')
                    foto_maquina2 = request.files.get('img_maquina2')
                    
                    #Criando pasta com nome da tag
                    pasta_alvo = f'past_{tag}/'
                    if(not os.path.exists(diretorio+pasta_alvo)): #Caso a pasta não exista ela é criada e salva as imagens
                        os.makedirs(diretorio+pasta_alvo)
                        diretorio_banco = diretorio+pasta_alvo
                        print(f'DIRETORIO BANCO = {diretorio_banco} --------------------------')

                        #Verificar se realmnte é uma foto
                        nome_foto_tag = foto_tag.filename
                        foto_tag.save(os.path.join(diretorio_banco, 'foto tag -'+nome_foto_tag))
                            
                        nome_foto_etiqueta = foto_etiqueta.filename
                        foto_etiqueta.save(os.path.join(diretorio_banco, 'foto etiqueta -'+nome_foto_etiqueta))

                        nome_foto_maquina1 = foto_maquina1.filename
                        foto_maquina1.save(os.path.join(diretorio_banco, 'foto maquina 1 -'+nome_foto_maquina1))

                        nome_foto_maquina2 = foto_maquina2.filename
                        foto_maquina2.save(os.path.join(diretorio_banco, 'foto maquina 2 -'+nome_foto_maquina2)) 
                        print('fotos salvas')

                        #Inseindo dados de texto no banco(SALVANDO)
                        create_banco.open_Banco()
                        create_banco.cadastrar_maquina_Banco(lista_dados)
                        create_banco.close_Banco()
                        print('dados salvos')
                    return redirect('/cadastrar')

                else:
                    print('TAG NÃO EXISTENTE')

        return redirect('/cadastrar')


@app.route('/arquivos2')
def post_arquivo1():
    return redirect('/home')


@app.route('/arquivos1', methods=['POST'])
def post_arquivo():
    global flag_log
    arquivo = request.files.get('img_tag')
    nome_arquivo = arquivo.filename
    arquivo.save(os.path.join(diretorio, nome_arquivo))
    print('CARA CHEGUEI AQUI')
    return redirect('/cadastrar')


if __name__ == '__main__':
    app.run(debug=True)
