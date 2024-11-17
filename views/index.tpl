<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página Inicial</title>
</head>
<body>
    <h1>bem-vindo! insira a opção desejada</h1>
    <p>Histórico de consultas(ou eventos, pedidos e consultas.)</p>
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
        <li><a href="/create">Adicionar novo (?)</a></li>
        <li><a href="/read">Ver lista de tarefas</a></li>
    </ul>
</body>
</html>
