from bottle import route, run, template, request, redirect
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

# essa é a funcao
def addMedicalAppointments(fk_medico_crm, fk_medico_fk_pessoa_cpf, fk_paciente_id_paciente, fk_paciente_fk_pessoa_cpf, sala, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO ent_consulta_consulta 
            (fk_medico_crm, fk_medico_fk_pessoa_cpf, fk_paciente_id_paciente, fk_paciente_fk_pessoa_cpf, sala, data)
            VALUES (%s, %s, %s, %s, %s, %s);
        ''', (fk_medico_crm, fk_medico_fk_pessoa_cpf, fk_paciente_id_paciente, fk_paciente_fk_pessoa_cpf, sala, data))
        conn.commit()
        print("Consulta adicionada com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar consulta: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

@route('/')
def home():
    tabelaConsultas = showMedicalAppointments()
    return template('views/medicalAppointments.tpl', tabelaConsultas=tabelaConsultas)

@route('/create', method=['GET', 'POST'])
def add():
        fk_medico_crm = request.forms.get('fk_medico_crm')
        fk_medico_fk_pessoa_cpf = request.forms.get('fk_medico_fk_pessoa_cpf')
        fk_paciente_id_paciente = request.forms.get('fk_paciente_id_paciente')
        fk_paciente_fk_pessoa_cpf = request.forms.get('fk_paciente_fk_pessoa_cpf')
        sala = int(request.forms.get('sala'))
        data = request.forms.get('data')

        addMedicalAppointments(fk_medico_crm, fk_medico_fk_pessoa_cpf, fk_paciente_id_paciente, fk_paciente_fk_pessoa_cpf, sala, data)

        redirect('/')

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=False) # lembrar de retirar e usar apenas para testes