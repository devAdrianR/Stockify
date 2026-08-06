from functools import wraps
from flask import session, redirect, url_for, flash


# ======================================
# LOGIN REQUERIDO
# ======================================

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "id_usuario" not in session:

            flash("Debes iniciar sesión.", "error")

            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function


# ======================================
# SUPERADMIN
# ======================================

def superadmin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get("rol") != "SUPERADMIN":

            flash("Acceso no autorizado.", "error")

            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function


# ======================================
# ADMIN
# ======================================

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get("rol") != "ADMIN":

            flash("Acceso no autorizado.", "error")

            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function


# ======================================
# EMPLEADO
# ======================================

def empleado_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get("rol") != "EMPLEADO":

            flash("Acceso no autorizado.", "error")

            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function





# ======================================
# CUALQUIER USUARIO LOGUEADO
# ======================================

def usuario_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get("rol") not in ["SUPERADMIN", "ADMIN", "EMPLEADO"]:

            flash("Acceso no autorizado.", "error")

            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function