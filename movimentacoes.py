from banco_mysql import get_db_connection
from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime

movimentacoes_bp = Blueprint('movimentacoes', __name__)

@movimentacoes_bp.route('/create', methods=['GET', 'POST'])
def create_movimentacao():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM containers")
    containers = cursor.fetchall()
    if request.method == 'POST':
        ds_tipo_movimentacao = request.form['ds_tipo_movimentacao']
        dt_hr_inicio = request.form['dt_hr_inicio']
        dt_hr_fim = request.form['dt_hr_fim']
        cd_container = request.form['cd_container']

        
        dt_hr_inicio = datetime.strptime(dt_hr_inicio, "%Y-%m-%dT%H:%M:%S")
        dt_hr_fim = datetime.strptime(dt_hr_fim, "%Y-%m-%dT%H:%M:%S")

        if dt_hr_fim <= dt_hr_inicio:
            flash(f"Data do fim tem que ser depois da data do início", 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for("movimentacoes.create_movimentacao"))

        cursor.execute("INSERT INTO movimentacoes(ds_tipo_movimentacao, dt_hr_inicio, dt_hr_fim, cd_container) VALUES(%s, %s, %s, %s)", (ds_tipo_movimentacao, dt_hr_inicio, dt_hr_fim, cd_container,))
        flash(f"Movimentação criada com sucesso", "success")
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("movimentacoes.create_movimentacao"))

    cursor.close()
    conn.close()
    return render_template('movimentacoes/create_movimentacao.html', containers=containers)

@movimentacoes_bp.route('/', methods=['GET', 'POST'])
def read_movimentacao():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT c.nr_container, m.cd_movimentacao, m.ds_tipo_movimentacao, m.dt_hr_inicio, m.dt_hr_fim FROM movimentacoes m JOIN containers c ON c.cd_container = m.cd_container ORDER BY c.nr_container, m.ds_tipo_movimentacao")
    movimentacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("movimentacoes/list_movimentacao.html", movimentacoes=movimentacoes)


@movimentacoes_bp.route("/update/<int:cd_movimentacao>", methods=['GET', 'POST'])
def update_movimentacao(cd_movimentacao):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM containers")
    containers = cursor.fetchall()
    cursor.execute("SELECT * FROM movimentacoes WHERE cd_movimentacao = %s", (cd_movimentacao,))
    movimentacao = cursor.fetchone()

    if request.method == "POST":
        ds_tipo_movimentacao = request.form['ds_tipo_movimentacao']
        dt_hr_inicio = request.form['dt_hr_inicio']
        dt_hr_fim = request.form['dt_hr_fim']
        cd_container = request.form['cd_container']

        
        dt_hr_inicio = datetime.strptime(dt_hr_inicio, "%Y-%m-%dT%H:%M:%S")
        dt_hr_fim = datetime.strptime(dt_hr_fim, "%Y-%m-%dT%H:%M:%S")


        if dt_hr_fim <= dt_hr_inicio:
            flash(f"Data do fim tem que ser depois da data do início", 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for("movimentacoes.update_movimentacao"))
            
        cursor.execute("UPDATE movimentacoes SET ds_tipo_movimentacao = %s, dt_hr_inicio = %s, dt_hr_fim = %s,  cd_container = %s WHERE cd_movimentacao = %s", (ds_tipo_movimentacao, dt_hr_inicio, dt_hr_fim, cd_container, cd_movimentacao,))
        conn.commit()
        flash("Movimentação atualizada com sucesso", "success")
        cursor.close()
        conn.close()
        return redirect(url_for("movimentacoes.read_movimentacao"))

    cursor.close()
    conn.close()
    return render_template("movimentacoes/update_movimentacao.html", movimentacao=movimentacao, containers=containers)


@movimentacoes_bp.route('/delete/<int:cd_movimentacao>', methods=['POST'])
def delete_movimentacao(cd_movimentacao):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM movimentacoes WHERE cd_movimentacao = %s", (cd_movimentacao,))
    flash("Movimentação deletada com sucesso", "success")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("movimentacoes.read_movimentacao"))