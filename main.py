from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://all_user:8765@autorack.proxy.rlwy.net:56092/bd_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar la modificación de seguimiento

# Inicializar la extensión SQLAlchemy
db = SQLAlchemy(app)

# Definir la tabla 'historial' usando SQLAlchemy ORM
class Historial(db.Model):
    __tablename__ = 'historial'
    
    id_historial = db.Column(db.Integer, primary_key=True)
    time_insert = db.Column(db.String(255))
    nivel = db.Column(db.Integer)
    orientation = db.Column(db.String(255))
    posicion_x = db.Column(db.Float)
    posicion_y = db.Column(db.Float)

# Función para obtener movimientos permitidos desde la base de datos
def obtener_informacion_movimientos():
    movimiento = Historial.query.order_by(Historial.id_historial.desc()).first()
    if movimiento:
        return {
            "id_historial": movimiento.id_historial,
            "time_insert": movimiento.time_insert,
            "nivel": movimiento.nivel,
            "orientation": movimiento.orientation,
            "posicion_x": movimiento.posicion_x,
            "posicion_y": movimiento.posicion_y
        }
    return None

# Función para actualizar el registro en la base de datos
def actualizar_registro(voto, historial_id, nivel, x, y):
    # Aquí puedes usar el modelo o un procedimiento almacenado como prefieras
    # Para este ejemplo, supongamos que solo registras el voto en una nueva entrada
    nuevo_voto = Historial(id_historial=historial_id, nivel=nivel, posicion_x=x, posicion_y=y)
    db.session.add(nuevo_voto)
    db.session.commit()

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
    return 'Hello from Flask with SQLAlchemy!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
