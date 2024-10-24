from flask import Flask, render_template
import os
from clientes import clientes_bp
from containers import containers_bp
from movimentacoes import movimentacoes_bp
from banco_mysql import get_db_connection

app = Flask(__name__)
app.secret_key = str(os.urandom(24))
app.register_blueprint(clientes_bp, url_prefix='/clientes')
app.register_blueprint(containers_bp, url_prefix='/containers')
app.register_blueprint(movimentacoes_bp, url_prefix='/movimentacoes')

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/reports')
def reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT cl.nm_cliente AS Cliente, m.ds_tipo_movimentacao AS Tipo, COUNT(cd_movimentacao) AS Total FROM movimentacoes m JOIN containers c ON c.cd_container = m.cd_container JOIN clientes cl ON cl.cd_cliente = c.cd_cliente GROUP BY cl.nm_cliente, m.ds_tipo_movimentacao ORDER BY Total, Cliente")
    reports = cursor.fetchall()
    cursor.execute("SELECT cl.nm_cliente AS Cliente, c.ds_categoria AS Categoria, COUNT(cl.cd_cliente) AS Total FROM containers c JOIN clientes cl ON c.cd_cliente = cl.cd_cliente GROUP BY cl.nm_cliente, c.ds_categoria ORDER BY c.ds_categoria, cl.nm_cliente, Total")
    reports_categoria = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("report.html", reports=reports, categorias=reports_categoria)



if __name__ == "__main__":
    app.run(debug=True)