#postgres://ickgfmvvrrhudz:e1a43f386f74485fb3e274b05fedf1d0b906d50e7b927f0a999385f000911329@ec2-52-202-22-140.compute-1.amazonaws.com:5432/d3jjct6cthq3tr
from flask import Flask, render_template, session, flash
from flask import request, make_response, redirect, url_for
from flask_wtf import CsrfProtect
from werkzeug.exceptions import  default_exceptions
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import login_forms
import registro_forms



app = Flask(__name__)

engine = create_engine("postgres://ickgfmvvrrhudz:e1a43f386f74485fb3e274b05fedf1d0b906d50e7b927f0a999385f000911329@ec2-52-202-22-140.compute-1.amazonaws.com:5432/d3jjct6cthq3tr")
db = scoped_session(sessionmaker(bind=engine))
#db = SQL("postgres://ickgfmvvrrhudz:e1a43f386f74485fb3e274b05fedf1d0b906d50e7b927f0a999385f000911329@ec2-52-202-22-140.compute-1.amazonaws.com:5432/d3jjct6cthq3tr")

#app.secret_key = 'elliderdelaspromesasrotas'
#csrf = CsrfProtect(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route('/')
def index():
    try:
        session["usuario_id"]
    except:
        lugares = db.execute("select lugar_id, nombre, telefono, ruta_foto, nombre_cat from lugar l inner join categoria c on l.categoria_id = c.categoria_id ORDER BY RANDOM() limit 6").fetchall()
        return render_template('index.html', lugares=lugares)

    user = db.execute ("SELECT * FROM usuario WHERE usuario_id=:user_id", {"user_id": session["usuario_id"]}).fetchone()
    lugares = db.execute("select lugar_id, nombre, telefono, ruta_foto, nombre_cat from lugar l inner join categoria c on l.categoria_id = c.categoria_id ORDER BY RANDOM() limit 6").fetchall()
    return render_template('index.html', lugares=lugares, user = user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out')
    return redirect(url_for("layouts"))

@app.route('/infoform/<int:lugar_id>')
def infoform(lugar_id):
    if "usuario_id" not in session:
        #seleccion del lugar
        lugar = db.execute("select lugar_id, nombre, descr, telefono, ruta_foto, direccion_ref, municipio, departamento, mapa_src, nombre_cat from lugar l inner join direccion d on l.direccion_id = d.direccion_id inner join categoria c on l.categoria_id = c.categoria_id where lugar_id=:lugar_id",
                    {"lugar_id": lugar_id}).fetchone()
        #seleccion de los productos

        #seleccion de los comentarios

        return render_template("infopro.html", lugar=lugar)
    else:
        #seleccion del nombredeusuario

        #seleccion del lugar
        lugar = db.execute("select lugar_id, nombre, descr, telefono, ruta_foto, direccion_ref, municipio, departamento, mapa_src, nombre_cat from lugar l inner join direccion d on l.direccion_id = d.direccion_id inner join categoria c on l.categoria_id = c.categoria_id where lugar_id=:lugar_id",
                    {"lugar_id": lugar_id}).fetchone()
        #seleccion de los productos

        #seleccion de los comentarios




@app.route('/commentform')
def commentform():
    return render_template('comment.html')


@app.route('/loginform', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_form = login_forms.LoginForm(request.form)
        if login_form.validate():
            rows = db.execute ("SELECT * FROM usuario WHERE username=:username", {"username": login_form.username.data}).fetchone()
            if not rows or not check_password_hash(rows.password, login_form.password.data):
                flash("Usuario o contraseña incorrecta")
                return render_template("login.html")
            session["usuario_id"] = rows.usuario_id
            return redirect(url_for("index"))
        else:
            for field, error in login_form.errors.items():
                flash(str(error))
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route('/registroform', methods = ['GET', 'POST'])
def registro():

    if request.method =='POST':
        registro_form = registro_forms.RegistroForm(request.form)
        if registro_form.validate():
            #print (registro_form.p_nombre.data)
            #print (registro_form.s_nombre.data)
            #print (registro_form.p_apellido.data)
            #print (registro_form.s_apellido.data)
            #print (registro_form.correo.data)
            #print (registro_form.tel.data)
            #print (registro_form.username.data)
            #print (registro_form.password.data)
            #print (registro_form.confirm.data)

            try:
                response = db.execute ("INSERT INTO usuario(p_nombre, s_nombre, p_apellido, s_apellido, correo, tel, username, password) VALUES(:p_nombre, :s_nombre, :p_apellido, :s_apellido, :correo, :tel, :username, :password)",
                {"p_nombre" : registro_form.p_nombre.data, "s_nombre" : registro_form.s_nombre.data, "p_apellido" : registro_form.p_apellido.data, "s_apellido" : registro_form.s_apellido.data , "correo" : registro_form.correo.data, "tel" : registro_form.tel.data , "username" : registro_form.username.data, "password" : generate_password_hash(registro_form.password.data)})
                db.commit()
            except Exception:
                flash("El usuario ya existe")
                return render_template("registro.html", form=registro_form)

            session["usuario_id"] = response
            return redirect(url_for('layouts'))
        else:
            for field, error in registro_form.errors.items():
                flash(str(error))
            return render_template("registro.html", form = registro_form)
    else:
        registro_form = registro_forms.RegistroForm()
        return render_template('registro.html', form = registro_form)


@app.route("/comment", methods = ['GET', 'POST'])
def comment():
    com=request.form.get("reseña")
    star=request.form.get("starrating")
    db.execute("INSET INTO resena (comentario, puntuacion, resena_id, usuario_id, lugar_id) VALUES(:comentario, :puntuacion, :resena_id, :usuario_id, :lugar_id)",
    {"comentario": reseña, "puntuacion": strarrating, "resena_id": resena_id, "usuario_id": session["usuario_id"]}).comit()
    return redirect(url_for("infoform"))


#TODO: maquetado de vista de producto, correccion de estilo de formularios (margenes, padding, columnado)
#TODO: popular tabla de productos, corrección layout en logeado ver nombre de usuario estilo dropdown con la opcion cerrar sesión, quitar links
#TODO: corregir maquetado de formulario de comentario
#TODO: CSRF de formulario de comentario
#TODO: (opcional) modo de búsqueda


if __name__ == '_main_':
    app.run(debug = True, port = 8000)