import teradatasql
import requests
from flask import Flask, request, jsonify

# connect = teradatasql.connect(host='192.168.15.4', user='dbc', password='dbc') 
#   CREATE QUERY 
# query = "SELECT * FROM LAB_ESTUDOS.NAVE_FAST_LOAD;"
# query = "SELECT * FROM LAB_ESTUDOS.NAVE_FAST_LOAD;"
#   CREATE DATA FRAME
# df = pd.read_sql(query, connect)
#   PRINT TABLE DATA
# print(df)
 
app = Flask(__name__)
SECRET_KEY='CRYP2023'

def conexao(): 
     
    # Variaveis de conexão
    connect = teradatasql.connect(host='192.168.15.6', user='dbc', password='dbc')
    return connect



@app.route('/', methods=['GET'])
def main():
    query = "SELECT * FROM LAB_ESTUDOS.alunos;"
    con = conexao()
    cursor = con.cursor()
    cursor.execute(query)
    alunos = cursor.fetchall()
    cursor.close()
    if alunos is None:
        api_url = "http://localhost:5000/consulta/externa"
        response = requests.get(api_url)
        retornaApi = response.json()
        return jsonify(retornaApi)
    else:
        return jsonify(alunos)

    
    


@app.route('/Pesquisar', methods=['GET'])
def pesquisar():
    nome = request.args.get('nome')
    # sobrenome = request.args.get('sobrenome')
    # turma = request.args.get('turma')
    query = "SEL * FROM LAB_ESTUDOS.alunos WHERE nome LIKE '{}';".format(nome)
    con = conexao()
    cursor = con.cursor()
    cursor.execute(query)
    aluno = cursor.fetchall()
    cursor.close()
    if aluno is None:
        api_url = "http://localhost:5000/consulta/externa"
        response = requests.get(api_url)
        retornaApi = response.json()
        return jsonify(retornaApi)
    else:
        return jsonify(aluno)
    
  
@app.route('/cadastrar', methods=['POST'])
def inserir():
    input_json = request.get_json(force=True)
    nome = str(input_json['nome'])
    sobrenome = str(input_json['sobrenome'])
    turma = str(input_json['turma'])
    
    query = "INSERT INTO LAB_ESTUDOS.alunos VALUES ('{}', '{}', '{}');".format(nome, sobrenome, turma)
    con = conexao()
    cursor = con.cursor()
    cursor.execute(query)
    cursor.close()
    
    return f'Registro |{nome}|{sobrenome}|{turma}| inserido com sucesso'


@app.route('/Deletar', methods=['DELETE'])
def cadastro():
    nome = request.args.get('nome')
    sobrenome = request.args.get('sobrenome')
    turma = request.args.get('turma')

    query = "DELETE FROM LAB_ESTUDOS.alunos WHERE nome LIKE '{}' AND sobrenome LIKE '{}' AND turma LIKE '{}';".format(nome, sobrenome, turma)

    con = conexao()
    cursor = con.cursor()
    cursor.execute(query)
    cursor.close()

    return f'Registro |{nome}|{sobrenome}|{turma}| deletado com sucesso'


if __name__ == '__main__':
    app.run()