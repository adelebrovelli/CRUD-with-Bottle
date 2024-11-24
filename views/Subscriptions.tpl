% import json
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Histórico de Inscrições</title>
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
            background-color: #6fbb9d;
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
            background-color: #6fbb9d;
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
            background-color: #6fbb9d;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        ul li button:hover, ul li a:hover {
            background-color: #6fbb9d;
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
            background-color: #6fbb9d;
        }
    </style>
</head>
<body>
    <header>
        <h1>Histórico de Inscrições</h1>
    </header>

    <table border="1">
        <tr>
            <th>Data do Evento</th>
            <th>CPF do Participante</th>
            <th>ID da Inscrição</th>
            <th>Frequência</th>
            <th>Satisfação</th>
            <th> </th>
        </tr>
        % for inscricao in tabelaInscricoes:
            <tr>
                % for campo in inscricao:
                    <td>{{campo}}</td>
                % end
                <td>
                    <button onclick="openEditModal({{json.dumps(inscricao)}})">Editar</button>
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
            <h2>Adicionar nova inscrição</h2>
            <form action="/createEventSubscriptions" method="post">
                <input type="date" name="fk_evento_data_evento" placeholder="Data do Evento*" required><br>
                <input type="text" name="fk_participante_cpf" maxlength="11" placeholder="CPF do Participante*" required><br>
                <p>*Campos obrigatórios</p>
                <button type="submit">Adicionar</button>
                <button type="button" class="close-modal" onclick="closeAddModal()">Fechar</button>
            </form>
        </div>
    </div>

    <div class="modal" id="removeModal">
        <div class="modal-content">
            <h2>Remover inscrição</h2>
            <form action="/removeEventSubscriptions" method="post">
                <input type="text" name="id_inscricao" maxlength="255" placeholder="ID da Inscrição*" required><br>
                <p>*Campos obrigatórios</p>
                <button type="submit">Remover</button>
                <button type="button" class="close-modal" onclick="closeRemoveModal()">Fechar</button>
            </form>
        </div>
    </div>

    <div class="modal" id="editModal">
        <div class="modal-content">
            <h2>Editar inscrição</h2>
            <form action="/editEventSubscriptions" method="post">
                <input type="hidden" name="id_inscricao" id="editIdInscricao">
                <input type="date" name="fk_evento_data_evento" id="editEventoData" placeholder="Data do Evento"><br>
                <input type="text" name="fk_participante_cpf" id="editParticipanteCpf" maxlength="11" placeholder="CPF do Participante"><br>
                <label>
                    <input type="checkbox" name="frequencia" id="editFrequencia"> Presente no Evento?
                </label><br>
                <input type="number" name="satisfacao" id="editSatisfacao" min="1" max="5" placeholder="Satisfação (1 a 5)"><br>
                <button type="submit">Salvar Alterações</button>
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

        function openEditModal(inscricao) { 
            document.getElementById('editIdInscricao').value = inscricao[2]; 
            document.getElementById('editEventoData').value = inscricao[0]; 
            document.getElementById('editParticipanteCpf').value = inscricao[1];
            document.getElementById('editFrequencia').checked = inscricao[3] === true; 
            document.getElementById('editSatisfacao').value = inscricao[4];
            document.getElementById('editModal').style.display = 'flex';
        }

        function closeEditModal() {
            document.getElementById('editModal').style.display = 'none';
        }
    </script>
</body>

</html>