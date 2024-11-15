import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML para la página de inicio de sesión, búsqueda de contacto y menú de formularios
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Best Work - Iniciar Sesión</title>
    <style>
        body, html {
            font-family: Arial, sans-serif;
            background-color: #f7f8fc;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            width: 100vw;
        }
        .container {
            width: 100%;
            max-width: 400px;
            background: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }
        input[type="text"], input[type="password"], button, select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            box-sizing: border-box;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        #result, #copyButton {
            padding: 10px;
            margin-top: 10px;
            background-color: #f0f0f0;
            border-radius: 5px;
        }
        button {
            background-color: #ff7f50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #e06a3d;
        }
        .logo {
            max-width: 150px;
            margin: 0 auto 20px;
        }
        #iframeContainer {
            width: 100vw;
            height: 100vh;
            border: none;
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
        }
        .full-screen-button {
            display: none;
            margin-top: 10px;
            padding: 10px 20px;
            background-color: #ff7f50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1100;
        }
        .full-screen-button:hover {
            background-color: #e06a3d;
        }
    </style>
</head>
<body>

<div class="container" id="mainContainer">
    <img src="https://bestwork.cl/wp-content/uploads/2023/05/Logo.png" alt="Best Work Logo" class="logo">
    <h2>Iniciar Sesión</h2>
    <form id="loginForm" style="display: block;">
        <input type="text" id="username" placeholder="Usuario" required>
        <input type="password" id="password" placeholder="Contraseña" required>
        <button type="submit">Ingresar</button>
    </form>

    <div id="searchSection" style="display: none;">
        <h2>Buscar Contacto</h2>
        <form id="searchForm">
            <label for="email">Correo electrónico:</label>
            <input type="email" id="email" placeholder="Introduce el correo" required>
            <button type="submit">Buscar</button>
        </form>
        <div id="result"></div>
        <button id="copyButton" style="display: none;" onclick="copyEmail()">Copiar correo</button>
    </div>

    <div id="formSelection" style="display: none;">
        <h2>Elija su Formulario</h2>
        <select id="formSelect">
            <option value="">Seleccione un formulario</option>
            <option value="contacto">Formulario Contacto</option>
            <option value="cotizacion">Formulario Cotización</option>
            <option value="creado">Formulario Creado</option>
        </select>
        <button onclick="showForm()">Ir al Formulario</button>
    </div>
</div>

<iframe id="iframeContainer"></iframe>
<button class="full-screen-button" id="exitFullScreenButton" onclick="exitFullScreen()">Salir de pantalla completa</button>

<script>
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        if (username === "BESTWOR ADM" && password === "BESTWORKK2024") {
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('searchSection').style.display = 'block';
        } else {
            alert("Usuario o contraseña incorrectos");
        }
    });

    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const resultDiv = document.getElementById('result');
        const copyButton = document.getElementById('copyButton');

        fetch(`/search?email=${encodeURIComponent(email)}`)
            .then(response => response.json())
            .then(data => {
                if (data.message && data.message.includes("Contacto encontrado")) {
                    resultDiv.textContent = data.message;
                    copyButton.style.display = 'block';
                    document.getElementById('formSelection').style.display = 'block';
                } else {
                    resultDiv.textContent = "El contacto no existe.";
                    copyButton.style.display = 'none';
                    document.getElementById('formSelection').style.display = 'none';
                }
            })
            .catch(error => {
                resultDiv.textContent = "Error al conectar con la API.";
                console.error("Error:", error);
            });
    });

    function showForm() {
        const selectedForm = document.getElementById('formSelect').value;
        const iframe = document.getElementById('iframeContainer');
        const exitFullScreenButton = document.getElementById('exitFullScreenButton');
        let formURL = "";
        switch (selectedForm) {
            case "contacto":
                formURL = "https://bestwork.cl/";
                break;
            case "cotizacion":
                formURL = "https://bestwork.cl/ielts/";
                break;
            case "creado":
                formURL = "https://bestwork.cl/#contacto";
                break;
            default:
                alert("Seleccione un formulario válido.");
                return;
        }
        iframe.style.display = 'block';
        exitFullScreenButton.style.display = 'block';
        iframe.src = formURL;
        document.getElementById('mainContainer').style.display = 'none';
    }

    function exitFullScreen() {
        document.getElementById('iframeContainer').style.display = 'none';
        document.getElementById('exitFullScreenButton').style.display = 'none';
        document.getElementById('mainContainer').style.display = 'block';
    }

    function copyEmail() {
        const email = document.getElementById('email').value;
        navigator.clipboard.writeText(email).then(() => {
            alert("Correo copiado al portapapeles");
        }).catch(err => {
            console.error("Error al copiar el correo: ", err);
        });
    }
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_code)

# Credenciales para la API externa
API_KEY = 'd2830a151e2d5ae79ee56b3bf8035c9728d27a1c75fbd2fe89eff5f11c57f078c0f93ae1'
API_URL = 'https://sedsa.api-us1.com'
headers = {'Api-Token': API_KEY}

@app.route('/search', methods=['GET'])
def search_contact():
    email = request.args.get('email')
    params = {'email': email}
    response = requests.get(f'{API_URL}/api/3/contacts', headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get('contacts'):
            return jsonify({"message": f"Contacto encontrado: {email}"}), 200
        else:
            return jsonify({"message": "El contacto no existe."}), 404
    else:
        return jsonify({"message": f"Error en la solicitud: {response.status_code}"}), 500

# Inicia la aplicación
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
