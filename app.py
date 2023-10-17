from flask import Flask, render_template, request, url_for, redirect
import mysql.connector
con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    db='hotel_python'
)
cursor = con.cursor()

app = Flask(__name__)


@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/main', methods=['POST'])
def main():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        sql = 'select * from usuario where nombre = %s and contraseña = %s'
        cursor.execute(sql, (usuario, contraseña, ))
        usuario_encontrado = cursor.fetchone()
        if usuario_encontrado:
            return render_template('menu-principal.html')
        else:
            return 'Usuario no encontrado'


@app.route('/menu_principal')
def menu_principal():
    return render_template('menu-principal.html')


@app.route('/add_reservacion')
def add_reservacion():
    return render_template('registrar-reservacion.html')


@app.route('/procesar_reserva', methods=['POST'])
def guardar_reserva():
    fecha_entrada = request.form['fecha_entrada']
    fecha_salida = request.form['fecha_salida']
    # Calcula el costo total de la reserva
    tarifa_diaria = 20  # Tarifa por día
    from datetime import datetime
    fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d")
    fecha_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
    duracion_estadia = (fecha_salida - fecha_entrada).days
    costo_total = tarifa_diaria * duracion_estadia

    metodo_pago = request.form['metodo_pago']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    nacionalidad = request.form['nacionalidad']
    telefono = request.form['telefono']
    sql = """insert into reservas(fecha_entrada, fecha_salida, valor, forma_pago)
    values(%s,%s,%s,%s)"""
    cursor.execute(sql, (fecha_entrada, fecha_salida,
                   costo_total, metodo_pago, ))
    con.commit()
    reserva_id = cursor.lastrowid

    sql = """insert into huesped(nombre, apellido, fecha_nacimiento, nacionalidad, telefono, id_reserva) 
    Values(%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql, (nombre, apellido, fecha_nacimiento,
                   nacionalidad, telefono, reserva_id, ))
    con.commit()
    return render_template('menu-principal.html')


# mostrar tabla de reservas
@app.route('/mostrar_tabla_reservas')
def mostrarTabla():
    sql = 'select * from reservas'
    cursor.execute(sql)
    datos = cursor.fetchall()
    return render_template('tabla-reservas.html', reservaciones=datos)

# mostrar tabla de huespedes


@app.route('/mostrar_tabla_huesped')
def motrar_tabla_huesped():
    sql = 'select * from huesped'
    cursor.execute(sql)
    datos = cursor.fetchall()
    return render_template('tabla-huesped.html', huespedes=datos)


# eliminar
@app.route('/delete/<string:id>')
def delete(id):
    cursor.execute(
        """DELETE FROM reservas where id_reservas = {0}""".format(id))
    con.commit()
    return redirect(url_for('menu_principal'))


@app.route('/edit/<string:id>')
def get_reserva(id):
    sql = "SELECT * FROM reservas WHERE id_reservas = %s"
    cursor.execute(sql, (id, ))
    data = cursor.fetchall()

    return render_template('editar-reservacion.html', reserva=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_reserva(id):
    if request.method == 'POST':
        fecha_entrada = request.form['fecha_entrada']
        fecha_salida = request.form['fecha_salida']
        # Calcula el costo total de la reserva
        tarifa_diaria = 20  # Tarifa por día
        from datetime import datetime
        fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d")
        fecha_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
        duracion_estadia = (fecha_salida - fecha_entrada).days
        costo_total = tarifa_diaria * duracion_estadia

        metodo_pago = request.form['metodo_pago']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        nacionalidad = request.form['nacionalidad']
        telefono = request.form['telefono']

        sql = """update reservas 
        set fecha_entrada = %s,
        fecha_salida = %s,
        valor = %s,
        forma_pago = %s
        where id_reservas = %s"""
        cursor.execute(sql, (fecha_entrada, fecha_salida,
                       costo_total, metodo_pago, id, ))
        con.commit()
        sql = """update huesped
        set nombre = %s,
        apellido = %s,
        fecha_nacimiento = %s,
        nacionalidad = %s,
        telefono = %s
        where id_reserva = %s"""
        cursor.execute(sql, (nombre, apellido, fecha_nacimiento,
                       nacionalidad, telefono, id, ))
        con.commit()
        return redirect(url_for('menu_principal'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
