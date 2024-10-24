from banco_mysql import get_db_connection
from flask import Blueprint, render_template, request, flash, redirect, url_for

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/create', methods=['GET', 'POST'])
def create_cliente():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nm_cliente = request.form['nm_cliente'].capitalize()
        cd_cnpj = request.form['cd_cnpj']

        cursor.execute("SELECT COUNT(*) FROM clientes WHERE cd_cnpj = %s", (cd_cnpj,))
        count = cursor.fetchone()

        if count['COUNT(*)'] > 0:
            flash(f"Já existe um cliente cadastrado com o CNPJ {cd_cnpj}", 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for("clientes.create_cliente"))

        cursor.execute("INSERT INTO clientes(nm_cliente, cd_cnpj) VALUES(%s, %s)", (nm_cliente, cd_cnpj,))
        flash(f"Cliente {nm_cliente} criado com sucesso", "success")
        conn.commit()

    cursor.close()
    conn.close()
    return render_template('clientes/create_cliente.html')

@clientes_bp.route('/')
def read_cliente():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("clientes/list_cliente.html", clientes=clientes)

@clientes_bp.route("/update/<int:cd_cliente>", methods=['GET', 'POST'])
def update_cliente(cd_cliente):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE cd_cliente = %s", (cd_cliente,))
    cliente = cursor.fetchone()

    if request.method == "POST":
        nm_cliente = request.form['nm_cliente'].capitalize()
        cd_cnpj = request.form['cd_cnpj']

        if cd_cnpj != cliente['cd_cnpj']:
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE cd_cnpj = %s", (cd_cnpj,))
            count = cursor.fetchone()
            if count['COUNT(*)'] > 0:
                flash(f"Já existe um cliente cadastrado com o CNPJ {cd_cnpj}", 'danger')
                cursor.close()
                conn.close()
                return redirect(url_for("clientes.update_cliente", cd_cliente=cd_cliente))
            
        cursor.execute("UPDATE clientes SET nm_cliente = %s, cd_cnpj = %s WHERE cd_cliente = %s", (nm_cliente, cd_cnpj, cd_cliente,))
        conn.commit()
        flash("Cliente atualizado com sucesso", "success")
        cursor.close()
        conn.close()
        return redirect(url_for("clientes.read_cliente"))


    cursor.close()
    conn.close()
    return render_template("clientes/update_cliente.html", cliente=cliente)

@clientes_bp.route('/delete/<int:cd_cliente>', methods=['POST'])
def delete_cliente(cd_cliente):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM clientes WHERE cd_cliente = %s", (cd_cliente,))
    flash("Cliente deletado com sucesso", "success")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("clientes.read_cliente"))