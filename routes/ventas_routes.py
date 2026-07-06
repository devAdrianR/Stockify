from flask import Blueprint, render_template
from auth import login_required

ventas_bp = Blueprint("ventas", __name__)

@ventas_bp.route("/ventas")
@login_required
def ventas():
    return render_template("ventas/ventas.html")