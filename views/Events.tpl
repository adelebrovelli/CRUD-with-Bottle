% import json
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerenciamento de Eventos</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
            padding: 10px;
        }

        header {
            background-color: #2e91b2;
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }

        h1 {
            font-size: 2rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            margin: 20px 0;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }

        th {
            background-color: #2e91b2;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        tr:hover {
            background-color: #ddd;
        }

        ul {
            list-style: none;
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
            padding: 0;
        }

        ul li a, ul li button, table tr td button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #2e91b2;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        ul li button:hover, ul li a:hover {
            background-color: #2c8cac;
        }

        .modal {
            display: none; 
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            justify-content: center;
            align-items: center;
        }

        .modal-content {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            width: 90%;
            max-width: 500px;
            text-align: center;
        }

        .modal-content input, .modal-content button {
            margin: 10px 0;
            padding: 10px;
            width: 90%;
            font-size: 1rem;
            border-radius: 10px;
        }

        .close-modal {
            background-color: red;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
        }

        .close-modal:hover {
            background-color: #2c8cac;
        }
    </style>
</head>
<body>
    <header>
        <h1>Lista de Eventos</h1>
    </header>

    <table border="1">
        <tr>
            <th>Nome do Evento</th>
            <th>Data do Evento</th>
            <th>Online</th>
            <th>Local</th>
            <th></th>
        </tr>
        % for evento in tabelaEventos:
            <tr>
                % for campo in evento:
                    <td>{{campo}}</td>
                % end
                <td>
                    <button onclick="openEditModal({{json.dumps(evento)}})">Editar</button>
                </td>
            </tr>
        % end
    </table>

    <ul>
        <li><button onclick="openAddModal()">Adicionar</button></li>
        <li><button onclick="openRemoveModal()">Remover</button></li>
    </ul>


    <div class="modal" id="addModal">
        <div class="modal-content">
            <h2>Adicionar evento</h2>
            <form action="/createEvent" method="post">
                <input type="text" name="nome_evento" placeholder="Nome do Evento*" required><br>
                <input type="date" name="data_evento" placeholder="Data do evento*" required><br>
                <input type="checkbox" name="online"><label>Evento online?</label><br>
                <input type="text" name="fk_local_id_local" placeholder="ID do Local*" required><br>
                <p>*Campos obrigatórios</p>
                <button type="submit">Adicionar</button>
                <button type="button" class="close-modal" onclick="closeAddModal()">Fechar</button>
            </form>
        </div>
    </div>

    <div class="modal" id="removeModal">
        <div class="modal-content">
            <h2>Remover evento</h2>
            <form action="/removeEvent" method="post">
                <input type="date" name="data_evento" placeholder="Data do evento*" required><br>
                <input type="text" name="fk_local_id_local" placeholder="ID do Local*" required><br>
                <p>*Campos obrigatórios</p>
                <button type="submit">Remover</button>
                <button type="button" class="close-modal" onclick="closeRemoveModal()">Fechar</button>
            </form>
        </div>
    </div>

    <div class="modal" id="editModal">
    <div class="modal-content">
        <h2>Editar Evento</h2>
        <form action="/editEvent" method="post">
            <input type="hidden" name="data_evento" id="editDataEvento">
            <input type="text" name="nome_evento" id="editNomeEvento" placeholder="Nome do Evento"><br>
            
            <label>
                <input type="radio" name="online" id="editOnlineTrue" value="true"> Online
            </label>
            <label>
                <input type="radio" name="online" id="editOnlineFalse" value="false"> Presencial
            </label><br>
            
            <input type="text" name="fk_local_id_local" id="editLocal" placeholder="ID do Local"><br>
            <button type="submit">Salvar</button>
            <button type="button" class="close-modal" onclick="closeEditModal()">Fechar</button>
        </form>
    </div>
</div>


    <script>
        function openAddModal() {
            document.getElementById('addModal').style.display = 'flex';
        }
        
        function closeAddModal() {
            document.getElementById('addModal').style.display = 'none';
        }

        function openRemoveModal() {
            document.getElementById('removeModal').style.display = 'flex';
        }

        function closeRemoveModal() {
            document.getElementById('removeModal').style.display = 'none';
        }
    
        function openEditModal(evento) {
    document.getElementById('editDataEvento').value = evento[1];
    document.getElementById('editNomeEvento').value = evento[0];

    if (evento[2] === 'true') {
        document.getElementById('editOnlineTrue').checked === true;
    } else if (evento[2] === false) {
        document.getElementById('editOnlineFalse').checked === false;
    }

    document.getElementById('editLocal').value = evento[3];
    document.getElementById('editModal').style.display = 'flex';
}

        function closeEditModal() {
            document.getElementById('editModal').style.display = 'none';
        }
    </script>
</body>
</html>
