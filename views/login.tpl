<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>

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

        button {
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

    </style>
</head>
<body>
<header>
    <h1>Clínica Equilibrium - Área Restrita</h1>
    </header>
    <form action="/" method="post">
        <label for="password">Senha:</label><br>
        <input type="password" name="password" required><br>
        <button type="submit">Entrar</button>
    </form>
</body>
</html>
