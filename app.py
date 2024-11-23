from bottle import route, run, template, request, redirect
import datetime
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

    resultados_formatados = []
    for consulta in resultados:
        nova_consulta = []
        for campo in consulta:
            if isinstance(campo, (datetime.date, datetime.datetime)):
                nova_consulta.append(str(campo)) 
            else:
                nova_consulta.append(campo)
        resultados_formatados.append(nova_consulta)
    
    return resultados_formatados

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

def removeMedicalAppointments(data, fk_medico_crm):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            DELETE FROM ent_consulta_consulta WHERE data = %s AND fk_medico_crm = %s;
        ''', (data, fk_medico_crm))
        conn.commit()
        print("Consulta removida com sucesso")
    except Exception as e:
        print(f"Erro ao remover consulta: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def editMedicalAppointments(data, updates):
    conn = get_db_connection()
    cursor = conn.cursor()
    values = []
    valuesFiltered = []
    for column, value in updates.items():
        if value is not None:  # filtrando dnv
            valuesFiltered.append(f"{column} = %s")
            values.append(value)
    if valuesFiltered:
        query = f"UPDATE ent_consulta_consulta SET {','.join(valuesFiltered)} WHERE data = %s"
        values.append(data)

        try:
            cursor.execute(query, tuple(values))
            conn.commit()
            print("Consulta editada com sucesso!")
        except Exception as e:
            print(f"Erro ao editar consulta: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    else:
        print("Nenhum campo para atualizar")


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

@route('/remove', method =['GET', 'POST'])
def remove():
    fk_medico_crm = request.forms.get('fk_medico_crm')
    data = request.forms.get('data')

    removeMedicalAppointments(data, fk_medico_crm)

    redirect('/')

@route('/edit', method=['POST'])
def edit():
    data = request.forms.get('data')
    updates = {
        "fk_medico_crm": request.forms.get('fk_medico_crm'),
        "fk_medico_fk_pessoa_cpf": request.forms.get('fk_medico_fk_pessoa_cpf'),
        "fk_paciente_id_paciente": request.forms.get('fk_paciente_id_paciente'),
        "fk_paciente_fk_pessoa_cpf": request.forms.get('fk_paciente_fk_pessoa_cpf'),
        "sala": request.forms.get('sala'),
        "data": request.forms.get('data')
    }

    updates = {k: v for k, v in updates.items() if v} # filtro

    editMedicalAppointments(data, updates)

    redirect('/')


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=False) # lembrar de retirar e usar apenas para testes