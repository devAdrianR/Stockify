from flask import Blueprint, render_template
from auth import login_required

finanzas_bp = Blueprint("finanzas", __name__)

@finanzas_bp.route("/finanzas")
@login_required
def finanzas():
    return render_template("finanzas/finanzas.html")