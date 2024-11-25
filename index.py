from bottle import route, template, request, redirect, Bottle, run
import datetime
import psycopg2
import os
from dotenv import load_dotenv


app = Bottle()
handler = app

load_dotenv()

@app.route('/favicon.ico')
def serve_favicon():
    return '', 204 


def get_db_connection():
    conn = psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
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

@app.route('/', method=['GET', 'POST'])
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
    for inscricao in resultados:
        nova_inscricao = []
        for campo in inscricao:
            if isinstance(campo, bool): 
                nova_inscricao.append('true' if campo else 'false')
            elif isinstance(campo, (datetime.date, datetime.datetime)):
                nova_inscricao.append(str(campo)) 
            else:
                nova_inscricao.append(campo)
        resultados_formatados.append(nova_inscricao)
    
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


@app.route('/MedicalAppointments')
def homeMedicalAppointments():
    tabelaConsultas = showMedicalAppointments()
    return template('views/medicalAppointments.tpl', tabelaConsultas=tabelaConsultas)

@app.route('/createMedicalAppointments', method=['GET', 'POST'])
def add():
        fk_medico_crm = request.forms.get('fk_medico_crm')
        fk_medico_fk_pessoa_cpf = request.forms.get('fk_medico_fk_pessoa_cpf')
        fk_paciente_id_paciente = request.forms.get('fk_paciente_id_paciente')
        fk_paciente_fk_pessoa_cpf = request.forms.get('fk_paciente_fk_pessoa_cpf')
        sala = int(request.forms.get('sala'))
        data = request.forms.get('data')

        addMedicalAppointments(fk_medico_crm, fk_medico_fk_pessoa_cpf, fk_paciente_id_paciente, fk_paciente_fk_pessoa_cpf, sala, data)

        redirect('/')

@app.route('/removeMedicalAppointments', method =['GET', 'POST'])
def remove():
    fk_medico_crm = request.forms.get('fk_medico_crm')
    data = request.forms.get('data')

    removeMedicalAppointments(data, fk_medico_crm)

    redirect('/')

@app.route('/editMedicalAppointments', method=['POST'])
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

@app.route('/EventSubscriptions')
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

@app.route('/createEventSubscriptions', method=['POST'])
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

@app.route('/removeEventSubscriptions', method=['POST'])
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

@app.route('/editEventSubscriptions', method=['POST'])
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

def showEvents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Evento;')
    resultados = cursor.fetchall()
    conn.close()

    resultados_formatados = []
    for evento in resultados:
        nova_evento = []
        for campo in evento:
            if isinstance(campo, bool): 
                nova_evento.append('true' if campo else 'false')
            elif isinstance(campo, (datetime.date, datetime.datetime)):
                nova_evento.append(str(campo))
            else:
                nova_evento.append(campo)
        resultados_formatados.append(nova_evento)
    
    return resultados_formatados

def addEvent(nome_evento, data_evento, online, fk_local_id_local):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Evento 
            (Nome_Evento, Data_Evento, Online, fk_Local_ID_Local)
            VALUES (%s, %s, %s, %s);
        ''', (nome_evento, data_evento, online, fk_local_id_local))
        conn.commit()
        print("Evento adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar evento: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def removeEvent(data_evento, fk_local_id_local):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM Evento WHERE Data_Evento = %s AND fk_local_id_local = %s', (data_evento, fk_local_id_local))
        conn.commit()
        print("Evento removido com sucesso!")
    except Exception as e:
        print(f"Erro ao remover evento: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def editEvent(data_evento, updates):
    conn = get_db_connection()
    cursor = conn.cursor()
    values = []
    valuesFiltered = []
    for column, value in updates.items():
        if value is not None:
            valuesFiltered.append(f"{column} = %s")
            values.append(value)

    if valuesFiltered:
        query = f"UPDATE Evento SET {','.join(valuesFiltered)} WHERE Data_Evento = %s"
        values.append(data_evento)

        try:
            cursor.execute(query, tuple(values))
            conn.commit()
            print("Evento editado com sucesso!")
        except Exception as e:
            print(f"Erro ao editar evento: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

@app.route('/Events')
def view_events():
    tabelaEventos = showEvents()
    return template('views/Events.tpl', tabelaEventos=tabelaEventos)

@app.route('/createEvent', method=['POST'])
def add_event():
    nome_evento = request.forms.get('nome_evento')
    data_evento = request.forms.get('data_evento')
    online = request.forms.get('online') == 'on'
    fk_local_id_local = request.forms.get('fk_local_id_local')

    addEvent(nome_evento, data_evento, online, fk_local_id_local)
    redirect('/Events')

@app.route('/removeEvent', method=['POST'])
def delete_event():
    data_evento = request.forms.get('data_evento')
    fk_local_id_local = request.forms.get('fk_local_id_local')
    removeEvent(data_evento, fk_local_id_local)
    redirect('/Events')

@app.route('/editEvent', method=['POST'])
def edit_event():
    data_evento = request.forms.get('data_evento')
    updates = {
        "Nome_Evento": request.forms.get('nome_evento'),
        "Online": request.forms.get('online') == 'true',  
        "fk_Local_ID_Local": request.forms.get('fk_local_id_local')
    }
    updates = {k: v for k, v in updates.items() if v is not None}  
    editEvent(data_evento, updates)
    redirect('/Events')

def showOrders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pedido;')
    resultados = cursor.fetchall()
    conn.close()


    resultados_formatados = []
    for pedido in resultados:
        nova_pedido = []
        for campo in pedido:
            if isinstance(campo, bool): 
                nova_pedido.append('true' if campo else 'false')
            elif isinstance(campo, (datetime.date, datetime.datetime)):
                nova_pedido.append(str(campo))
            else:
                nova_pedido.append(campo)
        resultados_formatados.append(nova_pedido)
    
    return resultados_formatados

def addOrder(id_pedido, preco_t, delivery, fk_data_data_pk):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Pedido 
            (ID_Pedido, Preco_t, Delivery, fk_Data_Data_PK)
            VALUES (%s, %s, %s, %s);
        ''', (id_pedido, preco_t, delivery, fk_data_data_pk))
        conn.commit()
        print("Pedido adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar pedido: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def removeOrder(id_pedido):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM Pedido WHERE ID_Pedido = %s;', (id_pedido,))
        conn.commit()
        print("Pedido removido com sucesso!")
    except Exception as e:
        print(f"Erro ao remover pedido: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def ensure_date_exists(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT 1 FROM Data WHERE Data_PK = %s', (data,))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO Data (Data_PK) VALUES (%s)', (data,))
            conn.commit()
    except Exception as e:
        print(f"Erro ao garantir a existência da data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def editOrder(id_pedido, updates):
    conn = get_db_connection()
    cursor = conn.cursor()

    # adiciona nova data se n tiver já
    if "fk_Data_Data_PK" in updates:
        ensure_date_exists(updates["fk_Data_Data_PK"])

    values = []
    valuesFiltered = []
    for column, value in updates.items():
        if value is not None:
            valuesFiltered.append(f"{column} = %s")
            values.append(value)

    if valuesFiltered:
        query = f"UPDATE Pedido SET {','.join(valuesFiltered)} WHERE ID_Pedido = %s"
        values.append(id_pedido)
        try:
            cursor.execute(query, tuple(values))
            conn.commit()
            print("Pedido editado com sucesso!")
        except Exception as e:
            print(f"Erro ao editar pedido: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


@app.route('/Orders')
def view_orders():
    tabelaPedidos = showOrders()
    return template('views/Orders.tpl', tabelaPedidos=tabelaPedidos)

@app.route('/createOrder', method=['POST'])
def add_order():
    id_pedido = request.forms.get('id_pedido')
    preco_t = float(request.forms.get('preco_t'))
    delivery = request.forms.get('delivery') == 'on'
    fk_data_data_pk = request.forms.get('fk_data_data_pk')

    addOrder(id_pedido, preco_t, delivery, fk_data_data_pk)
    redirect('/Orders')

@app.route('/removeOrder', method=['POST'])
def delete_order():
    id_pedido = request.forms.get('id_pedido')
    removeOrder(id_pedido)
    redirect('/Orders')

@app.route('/editOrder', method=['POST'])
def edit_order():
    id_pedido = request.forms.get('id_pedido')
    updates = {
        "Preco_t": request.forms.get('preco_t'),
        "Delivery": request.forms.get('delivery') == 'true', 
        "fk_Data_Data_PK": request.forms.get('fk_data_data_pk')
    }
    updates = {k: v for k, v in updates.items() if v is not None}
    editOrder(id_pedido, updates)
    redirect('/Orders')
