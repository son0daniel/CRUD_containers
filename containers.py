from banco_mysql import get_db_connection
from flask import Blueprint, render_template, request, flash, redirect, url_for

containers_bp = Blueprint('containers', __name__)

@containers_bp.route('/create', methods=['GET', 'POST'])
def create_container():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    if request.method == 'POST':
        nr_container = request.form['nr_container']
        qt_tipo = request.form['qt_tipo']
        ds_status = request.form['ds_status']
        ds_categoria = request.form['ds_categoria']
        cd_cliente = request.form['cd_cliente']

        cursor.execute("SELECT COUNT(*) FROM containers WHERE nr_container = %s", (nr_container,))
        count = cursor.fetchone()

        if count['COUNT(*)'] > 0:
            flash(f"Container {nr_container} já existe", 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for("containers.create_container"))

        cursor.execute("INSERT INTO containers(nr_container, qt_tipo, ds_status, ds_categoria, cd_cliente) VALUES(%s, %s, %s, %s, %s)", (nr_container, qt_tipo, ds_status, ds_categoria, cd_cliente,))
        flash(f"Container {nr_container} criado com sucesso", "success")
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("containers.create_container"))

    cursor.close()
    conn.close()
    return render_template('containers/create_container.html', clientes=clientes)

@containers_bp.route('/', methods=['GET', 'POST'])
def read_container():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT c.cd_container, c.nr_container, c.qt_tipo, c.ds_status, c.ds_categoria, cl.nm_cliente, cl.cd_cnpj FROM containers c JOIN clientes cl ON c.cd_cliente = cl.cd_cliente ORDER BY c.nr_container, cl.nm_cliente")
    containers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("containers/list_container.html", containers=containers)

@containers_bp.route("/update/<int:cd_container>", methods=['GET', 'POST'])
def update_container(cd_container):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.execute("SELECT * FROM containers WHERE cd_container = %s", (cd_container,))
    container = cursor.fetchone()

    if request.method == "POST":
        nr_container = request.form['nr_container']
        qt_tipo = request.form['qt_tipo']
        ds_status = request.form['ds_status']
        ds_categoria = request.form['ds_categoria']
        cd_cliente = request.form['cd_cliente']


        if container['nr_container'] != nr_container:
            cursor.execute("SELECT COUNT(*) FROM containers WHERE nr_container = %s", (nr_container,))
            count = cursor.fetchone()
            if count['COUNT(*)'] > 0:
                if count['COUNT(*)'] > 0:
                    flash(f"Já existe um container com número {nr_container}", 'danger')
                    cursor.close()
                    conn.close()
                    return redirect(url_for("containers.update_container", cd_container=cd_container))
            
        cursor.execute("UPDATE containers SET nr_container = %s, qt_tipo = %s, ds_status = %s,  ds_categoria = %s, cd_cliente = %s WHERE cd_container = %s", (nr_container, qt_tipo, ds_status, ds_categoria, cd_cliente, cd_container,))
        conn.commit()
        flash("Container atualizado com sucesso", "success")
        cursor.close()
        conn.close()
        return redirect(url_for("containers.read_container"))

    cursor.close()
    conn.close()
    return render_template("containers/update_container.html", container=container, clientes=clientes)

@containers_bp.route('/delete/<int:cd_container>', methods=['POST'])
def delete_container(cd_container):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM containers WHERE cd_container = %s", (cd_container,))
    flash("Container deletado com sucesso", "success")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("containers.read_container"))