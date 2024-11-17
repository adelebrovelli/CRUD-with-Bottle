from bottle import route, run, template
import psycopg2

def get_db_connection(): # me conectando no postgres turma
    conn = psycopg2.connect(database="dbequilibrium", user="postgres", password="9504", host='localhost', port=5432
    )
    return conn

def showMedicalAppointments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ent_consulta_consulta;')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@route('/')
def home():
    tabelaConsultas = showMedicalAppointments()
    return template('views/index.tpl', tabelaConsultas=tabelaConsultas)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=False) # lembrar de retirar e usar apenas para testes