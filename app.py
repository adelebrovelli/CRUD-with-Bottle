from bottle import route, run, template


@route('/')
def home():
    entrada = 'bem-vindo. insira a opção desejada'
    return template('views/index.tpl', entrada=entrada)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=False) # lembrar de retirar e usar apenas para testes