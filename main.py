from flask import Flask, jsonify, request
from flask_mysql import MySQL

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'autorack.proxy.rlwy.net'
app.config['MYSQL_PORT'] = 56092
app.config['MYSQL_USER'] = 'all_user'
app.config['MYSQL_PASSWORD'] = '8765'
app.config['MYSQL_DB'] = 'bd_project'

# Inicializar la extensión MySQL
mysql = MySQL(app)

# Función para obtener movimientos permitidos desde la base de datos
def obtener_informacion_movimientos():
    with app.app_context():  # Establecer el contexto de la aplicación
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT id_historial, decision, nivel, posicion_x, posicion_y
            FROM historial
            ORDER BY id_historial DESC
            LIMIT 1
        ''')
        movimientos_permitidos = cursor.fetchall()  # Devuelve una lista de tuplas
        cursor.close()

    if movimientos_permitidos:
        return movimientos_permitidos[0]
    return None

# Función para actualizar el registro en la base de datos
def actualizar_registro(voto, historial_id, nivel, x, y):
    with app.app_context():  # Establecer el contexto de la aplicación
        cursor = mysql.connection.cursor()
        # Llamar a un procedimiento almacenado
        cursor.callproc('registrar_voto', (voto, historial_id, nivel, x, y))
        mysql.connection.commit()
        cursor.close()

# Rutas de la API
@app.route('/obtener_movimientos', methods=['GET'])
def obtener_movimientos():
    movimientos = obtener_informacion_movimientos()
    if movimientos:
        return jsonify(movimientos), 200
    else:
        return jsonify({"error": "No se pudieron obtener movimientos"}), 500

@app.route('/actualizar_registro', methods=['POST'])
def actualizar_registro_endpoint():
    data = request.json
    voto = data.get('voto')
    historial_id = data.get('historial_id')
    nivel = data.get('nivel')
    x = data.get('x')
    y = data.get('y')
    actualizar_registro(voto, historial_id, nivel, x, y)
    return jsonify({"success": True}), 200

@app.route('/')
def hello_world():
    return 'Hello from Flask with MySQL!'
