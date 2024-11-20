<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Histórico de Consultas</title>
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
            background-color: #4CAF50;
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
            background-color: #4CAF50;
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

        ul li a, ul li button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        ul li button:hover, ul li a:hover {
            background-color: #45a049;
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
        }

        .close-modal {
            background-color: red;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
        }

        .close-modal:hover {
            background-color: darkred;
        }
    </style>
</head>
<body>
    <header>
        <h1>Histórico de Consultas</h1>
    </header>

    <table border="1">
        <tr>
            <th>CRM do Médico</th>
            <th>CPF do Médico</th>
            <th>ID do Paciente</th>
            <th>CPF do Paciente</th>
            <th>Sala</th>
            <th>Data</th>
        </tr>
        % for consulta in tabelaConsultas:
            <tr>
                % for campo in consulta:
                    <td>{{campo}}</td>
                % end
            </tr>
        % end
    </table>

    <ul>
        <li><button onclick="openAddModal()">+</button></li>
        <li><button onclick="openRemoveModal()">-</button></li>
    </ul>

    <div class="modal" id="addModal">
        <div class="modal-content">
            <h2>Adicionar nova consulta</h2>
            <form action="/create" method="post">
                <input type="text" name="fk_medico_crm" maxlength="8" placeholder="CRM do Médico*" required><br>
                <input type="text" name="fk_medico_fk_pessoa_cpf" maxlength="11" placeholder="CPF do Médico*" required><br>
                <input type="text" name="fk_paciente_id_paciente" placeholder="ID do Paciente*" required><br>
                <input type="text" name="fk_paciente_fk_pessoa_cpf" maxlength="11" placeholder="CPF do Paciente*" required><br>
                <input type="number" name="sala" placeholder="Sala" min="1" required><br>
                <input type="date" name="data" required><br>
                <p>*Campos obrigatórios</p style="color:red">
                <button>Adicionar</button>
                <button type="button" class="close-modal" onclick="closeAddModal()">Fechar</button>
            </form>
        </div> 
    </div>
    <div class="modal" id="removeModal">
        <div class="modal-content">
            <h2>Remover consulta</h2>
            <form action="/remove" method="post">
                <input type="text" name="fk_medico_crm" maxlength="8" placeholder="CRM do Médico*" required><br>
                <input type="date" name="data" placeholder="Data*" required><br>
                <p>*Campos obrigatórios</p style="color:red">
                <button>Remover</button>
                <button type="button" class="close-modal" onclick="closeRemoveModal()">Fechar</button>
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
    </script>
</body>
</html>