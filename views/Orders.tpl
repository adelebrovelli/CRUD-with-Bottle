% import json
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Gerenciamento de pedidos</title>
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
            background-color: #1c5870;
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
            background-color: #1c5870;
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
            background-color: #1c5870;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        ul li button:hover, ul li a:hover {
            background-color: #1c5870;
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
            background-color: #1c5870;
        }
    </style>
</head>
<body>
    <header>
        <h1>Gerenciamento de pedidos</h1>
    </header>

    <table>
        <tr>
            <th>ID do Cliente</th>
            <th>Preço Total</th>
            <th>Delivery</th>
            <th>Data do Pedido</th>
            <th> </th>
        </tr>
        % for pedido in tabelaPedidos:
        <tr>
            % for campo in pedido:
            <td>{{campo}}</td>
            % end
            <td>
                <button onclick="openEditModal({{json.dumps(pedido)}})">Editar</button>
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
            <h2>Adicionar Pedido</h2>
            <form action="/createOrder" method="post">
                <input type="text" name="id_pedido" placeholder="ID do Pedido*" required>
                <input type="number" step="0.01" name="preco_t" placeholder="Preço Total*" required>
                <label><input type="checkbox" name="delivery"> Delivery?</label><br>
                <input type="date" name="fk_data_data_pk" placeholder="Data*" required>
                <button type="submit">Adicionar</button>
                <button type="button" class="close-modal" onclick="closeAddModal()">Fechar</button>
            </form>
        </div>
    </div>

    <div class="modal" id="removeModal">
        <div class="modal-content">
            <h2>Remover Pedido</h2>
            <form action="/removeOrder" method="post">
                <input type="text" name="id_pedido" placeholder="ID do Pedido*" required>
                <button type="submit">Remover</button>
                <button type="button" class="close-modal" onclick="closeRemoveModal()">Fechar</button>
            </form>
        </div>
    </div>

    <div class="modal" id="editModal">
    <div class="modal-content">
        <h2>Editar Pedido</h2>
        <form action="/editOrder" method="post">
            <input type="hidden" name="id_pedido" id="editPedidoId">
            <input type="number" step="0.01" name="preco_t" id="editPrecoT" placeholder="Preço Total">
            <label>Delivery?</label>
            <div style="display: flex; justify-content: center; gap: 10px; margin-bottom: 10px;">
                <label>
                    <input type="radio" name="delivery" value="true" id="editDeliveryYes"> Sim
                </label>
                <label>
                    <input type="radio" name="delivery" value="false" id="editDeliveryNo"> Não
                </label>
            </div>
            <input type="date" name="fk_data_data_pk" id="editData" placeholder="Data">
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
            document.getElementById('addModal').style.display = 'none'; }
        function openRemoveModal() 
        {
             document.getElementById('removeModal').style.display = 'flex'; }
        function closeRemoveModal() 
        { 
            document.getElementById('removeModal').style.display = 'none'; }
       function openEditModal(pedido) 
       {

    document.getElementById('editPedidoId').value = pedido[0];
    document.getElementById('editPrecoT').value = pedido[1];
    document.getElementById('editData').value = pedido[3];

    if (pedido[2] === 'true') {
        document.getElementById('editDeliveryYes').checked = true;
    } else {
        document.getElementById('editDeliveryNo').checked = false;
    }

    document.getElementById('editModal').style.display = 'flex';
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

    </script>
</body>
</html>
