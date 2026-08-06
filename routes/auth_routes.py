from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuarios import validarLogin
from auth import login_required

auth_bp = Blueprint("auth", __name__)


# ======================================
# LOGIN
# ======================================

@auth_bp.route("/", methods=["GET", "POST"])
def login():

    # Si ya inició sesión, enviarlo a su dashboard
    if "id_usuario" in session:

        if session["rol"] == "SUPERADMIN":
            return redirect(url_for("dashboard.dashboard_superadmin"))

        elif session["rol"] == "ADMIN":
            return redirect(url_for("dashboard.dashboard_admin"))

        elif session["rol"] == "EMPLEADO":
            return redirect(url_for("dashboard.dashboard_user"))

    # Procesar login
    if request.method == "POST":

        usuario = request.form["usuario"].strip()
        password = request.form["password"]

        usuarioDB = validarLogin(usuario, password)

        if usuarioDB:

            session["id_usuario"] = usuarioDB["id_usuario"]
            session["nombre_usuario"] = usuarioDB["nombre_usuario"]
            session["rol"] = usuarioDB["rol"]
            session["id_empresa"] = usuarioDB["id_empresa"]

            flash(f"Bienvenido {usuarioDB['nombre_usuario']}.", "success")

            if usuarioDB["rol"] == "SUPERADMIN":
                return redirect(url_for("dashboard.dashboard_superadmin"))

            elif usuarioDB["rol"] == "ADMIN":
                return redirect(url_for("dashboard.dashboard_admin"))

            elif usuarioDB["rol"] == "EMPLEADO":
                return redirect(url_for("dashboard.dashboard_user"))

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html")


# ======================================
# LOGOUT
# ======================================

@auth_bp.route("/logout")
@login_required
def logout():

    session.clear()

    flash("Sesión cerrada correctamente.", "success")

    return redirect(url_for("auth.login"))