from functools import wraps
from flask import session,redirect,url_for,flash

def login_required(f):

    @wraps(f)
    def decorated_function(*args,**kwargs):

        if "id_usuario" not in session:
            flash("Debes iniciar sesión.","error")
            return redirect(url_for("login"))

        return f(*args,**kwargs)

    return decorated_function

def admin_required(f):

    @wraps(f)
    def decorated_function(*args,**kwargs):

        if session.get("rol")!="Administrador":
            session.clear()
            flash("Acceso no autorizado.","error")
            return redirect(url_for("login"))

        return f(*args,**kwargs)

    return decorated_function

def empleado_required(f):

    @wraps(f)
    def decorated_function(*args,**kwargs):

        if session.get("rol")!="Empleado":
            session.clear()
            flash("Acceso no autorizado.","error")
            return redirect(url_for("login"))

        return f(*args,**kwargs)

    return decorated_function