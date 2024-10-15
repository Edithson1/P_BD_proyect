from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

# Función para conectarse a la base de datos
def get_db_connection():
    return pymysql.connect(
        host='autorack.proxy.rlwy.net',
        port=56092,
        user='all_user',
        password='8765',
        database='bd_project'
    )

# Ruta para obtener el último movimiento desde la base de datos
@app.route('/movimientos', methods=['GET'])
def obtener_movimientos():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT id_historial, time_insert, nivel, orientation, posicion_x, posicion_y
                FROM historial
                ORDER BY id_historial DESC
                LIMIT 1
            ''')
            movimiento = cursor.fetchone()
            return jsonify({
                'id_historial': movimiento[0],
                'time_insert': movimiento[1],
                'nivel': movimiento[2],
                'orientation': movimiento[3],
                'posicion_x': movimiento[4],
                'posicion_y': movimiento[5]
            })
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)})
    finally:
        connection.close()

# Ruta para actualizar el registro en la base de datos
@app.route('/actualizar', methods=['POST'])
def actualizar_registro():
    data = request.json
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc('registrar_voto', (data['voto'], data['historial_id'], data['nivel'], data['orientation'], data['posicion_x'], data['posicion_y']))
            connection.commit()
            return jsonify({"status": "success"})
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)})
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
