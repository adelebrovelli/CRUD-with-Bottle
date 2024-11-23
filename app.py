from bottle import route, run, template, request, redirect
import datetime
import psycopg2


def get_db_connection(): # me conectando no postgres turma
    conn = psycopg2.connect(database="dbequilibrium", user="postgres", password="9504", host='localhost', port=5432
    )
    return conn


PASSWORD_TABLES = {
    "adele123": "/MedicalAppointments",
    "duda123": "/EventSubscriptions",
    "bruna123": "/Events",
    "sergio123": "/Orders"
}

def credentials(password):
    return PASSWORD_TABLES.get(password)

@route('/', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.forms.get('password')  
        table = credentials(password)  
        if table:
            redirect(f'{table}')  
        else:
            return "<p>Senha incorreta. Tente novamente.</p>"

    return template('views/login.tpl')

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


@route('/MedicalAppointments')
def homeMedicalAppointments():
    tabelaConsultas = showMedicalAppointments()
    return template('views/medicalAppointments.tpl', tabelaConsultas=tabelaConsultas)

@route('/createMedicalAppointments', method=['GET', 'POST'])
def add():
        fk_medico_crm = request.forms.get('fk_medico_crm')
        fk_medico_fk_pessoa_cpf = request.forms.get('fk_medico_fk_pessoa_cpf')
        fk_paciente_id_paciente = request.forms.get('fk_paciente_id_paciente')
        fk_paciente_fk_pessoa_cpf = request.forms.get('fk_paciente_fk_pessoa_cpf')
        sala = int(request.forms.get('sala'))
        data = request.forms.get('data')

        addMedicalAppointments(fk_medico_crm, fk_medico_fk_pessoa_cpf, fk_paciente_id_paciente, fk_paciente_fk_pessoa_cpf, sala, data)

        redirect('/')

@route('/removeMedicalAppointments', method =['GET', 'POST'])
def remove():
    fk_medico_crm = request.forms.get('fk_medico_crm')
    data = request.forms.get('data')

    removeMedicalAppointments(data, fk_medico_crm)

    redirect('/')

@route('/editMedicalAppointments', method=['POST'])
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

def showEventSubscriptions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM E_Assoc_Inscricao;')
    resultados = cursor.fetchall()
    conn.close()
    resultados_formatados = []
    for inscricao in resultados:
        nova_inscricao = []
        for campo in inscricao:
            if isinstance(campo, (datetime.date, datetime.datetime)):
                nova_inscricao.append(str(campo)) 
            else:
                nova_inscricao.append(campo)
        resultados_formatados.append(nova_inscricao)
    
    return resultados_formatados


@route('/EventSubscriptions')
def view_inscricoes():
    tabelaInscricoes = showEventSubscriptions()
    return template('views/Subscriptions.tpl', tabelaInscricoes=tabelaInscricoes)

def addEventSubscriptions(fk_evento_data_evento, fk_participante_cpf):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO E_Assoc_Inscricao 
            (fk_Evento_Data_Evento, fk_Participante_fk_Pessoa_CPF)
            VALUES (%s, %s) RETURNING ID_Inscricao; 
        ''', (fk_evento_data_evento, fk_participante_cpf))
        new_id = cursor.fetchone()[0]  
        conn.commit()
        print(f"Inscrição adicionada com sucesso! ID: {new_id}")
    except Exception as e:
        print(f"Erro ao adicionar inscrição: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


@route('/createEventSubscriptions', method=['POST'])
def add_inscricao():
    fk_evento_data_evento = request.forms.get('fk_evento_data_evento')
    fk_participante_cpf = request.forms.get('fk_participante_cpf')

    addEventSubscriptions(fk_evento_data_evento, fk_participante_cpf)
    redirect('/EventSubscriptions')


def removeEventSubscriptions(id_inscricao):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM E_Assoc_Inscricao WHERE ID_Inscricao = %s', (id_inscricao,))
        conn.commit()
    except Exception as e:
        print(f"Erro ao remover inscrição: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

@route('/removeEventSubscriptions', method=['POST'])
def delete_inscricao():
    id_inscricao = request.forms.get('id_inscricao')
    removeEventSubscriptions(id_inscricao)
    redirect('/EventSubscriptions')


def editEventSubscriptions(id_inscricao, updates):
    conn = get_db_connection()
    cursor = conn.cursor()
    values = []
    valuesFiltered = []
    for column, value in updates.items():
        if value is not None:
            valuesFiltered.append(f"{column} = %s")
            values.append(value)

    if valuesFiltered:
        query = f"UPDATE E_Assoc_Inscricao SET {','.join(valuesFiltered)} WHERE ID_Inscricao = %s"
        values.append(id_inscricao)

        try:
            cursor.execute(query, tuple(values))
            conn.commit()
        except Exception as e:
            print(f"Erro ao editar inscrição: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

@route('/editEventSubscriptions', method=['POST'])
def edit_inscricao():
    id_inscricao = request.forms.get('id_inscricao')
    updates = {
        "fk_Evento_Data_Evento": request.forms.get('fk_evento_data_evento'),
        "fk_Participante_fk_Pessoa_CPF": request.forms.get('fk_participante_cpf'),
        "Frequencia": request.forms.get('frequencia') == 'on',
        "satisfacao_Inscrito": request.forms.get('satisfacao')
    }
    updates = {k: v for k, v in updates.items() if v}
    editEventSubscriptions(id_inscricao, updates)
    redirect('/EventSubscriptions')



if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True) # lembrar de retirar e usar apenas para testes