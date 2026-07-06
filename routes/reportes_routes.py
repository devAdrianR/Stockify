from flask import Blueprint, render_template
from auth import login_required

reportes_bp = Blueprint("reportes", __name__)

@reportes_bp.route("/reportes")
@login_required
def reportes():
    return render_template("reportes/reportes.html")