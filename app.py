import os
import requests
import datetime

from flask import Flask, session, render_template, request, redirect, escape, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# EMAIL
# EMAIL
# EMAIL
# EMAIL
app.config['MAIL_SERVER'] = 'send.one.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'thamuzz@brigade.no'
app.config['MAIL_PASSWORD'] = '3v3n8w'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Set up database
engine = create_engine("postgres://ianuevwzbuutrj:42354bdc367180a784f10bd07a57fafb669c4e711515371f4b1f1c9f14a0882a@ec2-54-75-239-237.eu-west-1.compute.amazonaws.com:5432/d9i63cog43kchr")
db = scoped_session(sessionmaker(bind=engine))

# GLOBALS
# GLOBALS
# GLOBALS
# GLOBALS
# Finner alle underkategorier til "koldtbord" og "grill" tablesene
def find_id(id):
    items = db.execute("SELECT * FROM koldtbord_meny WHERE koldtbord_id = :id order by dessert asc, id", {"id":id})
    return items
def find_id_grill(id):
    items = db.execute("SELECT * FROM grill_meny WHERE grill_id = :id order by id asc", {"id":id})
    return items

app.jinja_env.globals.update(find_id=find_id)
app.jinja_env.globals.update(find_id_grill=find_id_grill)

#####################################################################################
# LINKS LINKS LINKS LINKS LINKS LINKS LINKS LINKS LINKS LINKS LINKS LINKS LINKS LINKS

# INDEX
# INDEX
# INDEX
# INDEX
@app.route("/")
def index():
    return render_template("index.html", title="Home")


# KONTAKT OSS
# KONTAKT OSS
# KONTAKT OSS
# KONTAKT OSS
@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html", title="Kontakt oss")

# TJENESTER
# TJENESTER
# TJENESTER
# TJENESTER
@app.route("/tjenester")
def tjenester():
    services = db.execute("SELECT * FROM tjenester order by id asc")
    return render_template("tjenester.html", title="Tjenester", services=services)

# MENU
# MENU
# MENU
# MENU
@app.route("/meny/<item>")
def find_item(item):
    # SJEKK FOR DAGENS
    now = datetime.now()
    day = now.strftime("%a")

    item_dagens = db.execute("SELECT * FROM dagens WHERE day = :day", {"day": day}).fetchone()

    if item_dagens is not None:
        dagens = item_dagens.item
    else:
        dagens = None

    items = db.execute("SELECT * FROM menus WHERE type = :type order by id asc", {"type": item})
    return render_template("menyer.html", items=items, dagens=dagens, type=item, title="Overtidsmat & Meny")

# CATERING
# CATERING
# CATERING
# CATERING
@app.route("/catering/<type>")
def catering(type):
    if type == "koldtbord":
        headers = db.execute("SELECT * FROM koldtbord order by id asc")
        capitalize_type = type.capitalize()
        return render_template("catering.html", headers=headers, type=type)
    else:
        types = db.execute("SELECT * FROM catering WHERE type = :type order by id asc", {"type": type})
        return render_template("catering.html", types=types, type=type, title="Catering")

# GRILL
# GRILL
# GRILL
# GRILL
@app.route("/grill")
def grill():
    headers = db.execute("SELECT * FROM grill order by id asc")
    return render_template("grill.html", title="Grill", headers=headers)

#####################################################################################

# LOGIN
# LOGIN
# LOGIN
# LOGIN
@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("username")

    find_user = db.execute("SELECT * FROM sveins WHERE name = :name", {"name": name}).fetchone()
    if find_user is None:
        return render_template("error.html", message="Feil brukernavn eller passord")

    pw = check_password_hash(find_user.pw, request.form.get("password"))
    if pw:
        session['username'] = find_user.name
        return redirect("/redigering/middag")
    return render_template("error.html", message="Feil brukernavn eller passord")

# LOGOUT
# LOGOUT
# LOGOUT
# LOGOUT
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

#####################################################################################

# EDIT MENU
# EDIT MENU
# EDIT MENU
# EDIT MENU
@app.route("/redigering/<item>")
def redigering(item):
    if 'username' in session and session['username']:
        find_admin = db.execute("SELECT * FROM sveins WHERE name = :name", {"name": session['username']}).fetchone()
        items = db.execute("SELECT * FROM menus WHERE type = :item order by id asc", {"item":item})
        type = item

        return render_template('redigering.html', items=items, type=type, title="Overtidsmat & Meny")
    else:
        return render_template("index.html", title="Home")

# SEND EDIT
@app.route("/edit/<id>", methods=["POST"])
def edit(id):
    name = request.form.get("name")
    price = request.form.get("price")
    description = request.form.get("description")
    type = request.form.get("type")
    db.execute("UPDATE menus SET name = :name, price = :price, description = :description WHERE id = :id", {"name": name, "price": price, "description": description, "id": id})
    db.commit();
    return redirect('/redigering/' + type)
# DELETE ITEM MENU
@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    db.execute("DELETE FROM menus WHERE id = :id", {"id": id})
    db.commit()
    type = request.form.get("type")
    return redirect('/redigering/' + type)
# NEW ITEM MENU
@app.route("/new", methods=["POST"])
def new():
    name = request.form.get("name")
    price = request.form.get("price")
    description = request.form.get("description")
    type = request.form.get("type")
    db.execute("INSERT INTO menus (name, price, description, type) VALUES (:name, :price, :description, :type)", {"name": name, "price": price, "description": description, "type": type})
    db.commit()
    return redirect('/redigering/' + type)

#####################################################################################


# EDIT TJENESTER
# EDIT TJENESTER
# EDIT TJENESTER
# EDIT TJENESTER
@app.route("/rediger_tjenester")
def rediger_tjenester():
    if 'username' in session and session['username']:
        types = db.execute("SELECT * FROM tjenester order by id asc")
        return render_template("rediger_tjenester.html", title="Tjenester", types=types)
    else:
        return render_template("index.html", title="Home")

# SEND EDIT TJENESTER
# SEND EDIT TJENESTER
# SEND EDIT TJENESTER
# SEND EDIT TJENESTER
@app.route("/edit_tjenester/<id>", methods=["POST"])
def edit_tjenester(id):
    name = request.form.get("name")
    price_one = request.form.get("price_one")
    price_two = request.form.get("price_two")
    description = request.form.get("description")
    db.execute("UPDATE tjenester SET name = :name, price_one = :price_one, price_two = :price_two, description = :description WHERE id = :id", {"name": name, "price_one": price_one, "price_two": price_two, "description": description, "id": id})
    db.commit()
    return redirect("/rediger_tjenester")

# DELETE TJENESTER
# DELETE TJENESTER
# DELETE TJENESTER
# DELETE TJENESTER
@app.route("/delete_tjenester/<id>", methods=["POST"])
def delete_tjenester(id):
    db.execute("DELETE FROM tjenester WHERE id = :id", {"id": id})
    db.commit()
    return redirect('/rediger_tjenester')

# NEW TJENESTER
# NEW TJENESTER
# NEW TJENESTER
# NEW TJENESTER
@app.route("/new_tjeneste/", methods=["POST"])
def new_tjeneste():
    name = request.form.get("name")
    price_one = request.form.get("price_one")
    price_two = request.form.get("price_two")
    description = request.form.get("description")

    db.execute("INSERT INTO tjenester (name, price_one, price_two, description) VALUES (:name, :price_one, :price_two, :description)",
            {"name": name, "price_one":price_one,"price_two":price_two,"description":description})
    db.commit()
    return redirect('/rediger_tjenester')

#####################################################################################

# EDIT CATERING
# EDIT CATERING
# EDIT CATERING
# EDIT CATERING
@app.route("/rediger_catering/<type>")
def rediger_catering(type):
    if 'username' in session and session['username']:

        if type == "koldtbord":
            headers = db.execute("SELECT * FROM koldtbord order by id asc")
            capitalize_type = type.capitalize()
            return render_template("edit_catering.html",  title="Catering", headers=headers, type= type)

        types = db.execute("SELECT * FROM catering WHERE type = :type order by id asc", {"type": type})
        return render_template("edit_catering.html", title="Catering", type=type, types=types)
    else:
        return render_template("index.html", title="Home")

# SEND EDIT CATERING
# SEND EDIT CATERING
# SEND EDIT CATERING
# SEND EDIT CATERING
@app.route("/edit_catering/<id>", methods=["POST"])
def edit_catering(id):
    name = request.form.get("name")
    price = request.form.get("price")
    description = request.form.get("description")
    type = request.form.get("type")
    db.execute("UPDATE catering SET name = :name, price_one = :price, description = :description WHERE id = :id", {"name": name, "price": price, "description": description, "id": id})
    db.commit()
    return redirect("/rediger_catering/" + type)

# DELETE CATERING
# DELETE CATERING
# DELETE CATERING
# DELETE CATERING
@app.route("/delete_catering/<id>", methods=["POST"])
def delete_catering(id):
    db.execute("DELETE FROM catering WHERE id = :id", {"id": id})
    db.commit()
    type = request.form.get("type")
    return redirect('/rediger_catering/' + type)

# NEW CATERING
# NEW CATERING
# NEW CATERING
# NEW CATERING
@app.route("/new_catering", methods=["POST"])
def new_catering():
    name = request.form.get("name")
    price_one = request.form.get("price_one")
    price_two = request.form.get("price_two")
    description = request.form.get("description")
    type = request.form.get("type")
    db.execute("INSERT INTO catering (name, price_one, price_two, description, type) VALUES (:name, :price_one, :price_two, :description, :type)", {"name": name, "price_one": price_one, "price_two": price_two, "description": description, "type": type})
    db.commit()
    return redirect('/rediger_catering/' + type)


#####################################################################################


# SEND EDIT KOLDTBORD
# SEND EDIT KOLDTBORD
# SEND EDIT KOLDTBORD
# SEND EDIT KOLDTBORD
@app.route("/edit_koldtbord/<id>", methods=["POST"])
def edit_koldtbord(id):
    name = request.form.get("name")
    description = request.form.get("description")
    type = request.form.get("type")
    db.execute("UPDATE koldtbord_meny SET name = :name, description = :description WHERE id = :id",
                {"name": name, "description": description, "id": id})
    db.commit()
    return redirect("/rediger_catering/" + type)
# SEND EDIT KOLDTBORD HEADERS
# SEND EDIT KOLDTBORD HEADERS
# SEND EDIT KOLDTBORD HEADERS
# SEND EDIT KOLDTBORD HEADERS
@app.route("/edit_koldtbord_headers/<id>", methods=["POST"])
def edit_koldtbord_headers(id):
    name = request.form.get("name")
    price = request.form.get("price")
    db.execute("UPDATE koldtbord SET name = :name, price = :price WHERE id = :id",
                {"name": name, "price": price, "id": id})
    db.commit()
    return redirect("/rediger_catering/koldtbord")
# DELETE KOLDTBORD
# DELETE KOLDTBORD
# DELETE KOLDTBORD
# DELETE KOLDTBORD
@app.route("/delete_koldtbord/<id>", methods=["POST"])
def delete_koldtbord(id):
    db.execute("DELETE FROM koldtbord_meny WHERE id = :id", {"id": id})
    db.commit()
    return redirect('/rediger_catering/koldtbord')

# NEW KOLDTBORD
# NEW KOLDTBORD
# NEW KOLDTBORD
# NEW KOLDTBORD
@app.route("/new_koldtbord/", methods=["POST"])
def new_koldtbord():
    koldtbord_id = request.form.get("koldtbord_id")
    name = request.form.get("name")
    description = request.form.get("description")
    if request.form.get("dessert"):
        dessert = "1"
    else:
        dessert = "0"
    db.execute("INSERT INTO koldtbord_meny (koldtbord_id, name, description, dessert) VALUES (:koldtbord_id, :name, :description, :dessert)",
        {"koldtbord_id":koldtbord_id, "name": name, "description": description, "dessert":dessert})
    db.commit()
    return redirect('/rediger_catering/koldtbord')

#####################################################################################


# EDIT GRILL
# EDIT GRILL
# EDIT GRILL
# EDIT GRILL
@app.route("/rediger_grill/")
def rediger_grill():
    if 'username' in session and session['username']:
        headers = db.execute("SELECT * FROM grill order by id asc")
        return render_template("rediger_grill.html", title="Grill", headers=headers)
    else:
        return render_template("index.html", title="Home")

# SEND EDIT GRILL
# SEND EDIT GRILL
# SEND EDIT GRILL
# SEND EDIT GRILL
@app.route("/edit_grill/<id>", methods=["POST"])
def edit_grill(id):
    name = request.form.get("name")
    db.execute("UPDATE grill_meny SET name = :name WHERE id = :id",
                {"name": name, "id": id})
    db.commit()
    return redirect("/rediger_grill")

# SEND EDIT GRILL HEADERS
# SEND EDIT GRILL HEADERS
# SEND EDIT GRILL HEADERS
# SEND EDIT GRILL HEADERS
@app.route("/edit_grill_headers/<id>", methods=["POST"])
def edit_grill_headers(id):
    name = request.form.get("name")
    price = request.form.get("price")
    db.execute("UPDATE grill SET name = :name, price = :price WHERE id = :id",
                {"name": name, "price": price, "id": id})
    db.commit()
    return redirect("/rediger_grill")

# DELETE GRILL
# DELETE GRILL
@app.route("/delete_grill/<id>", methods=["POST"])
def delete_grill(id):
    db.execute("DELETE FROM grill_meny WHERE id = :id", {"id": id})
    db.commit()
    return redirect('/rediger_grill')

# NEW GRILL
# NEW GRILL
# NEW GRILL
# NEW GRILL
@app.route("/new_grill/", methods=["POST"])
def new_grill():
    grill_id = request.form.get("grill_id")
    name = request.form.get("name")
    db.execute("INSERT INTO grill_meny (grill_id, name) VALUES (:grill_id, :name)",
        {"grill_id":grill_id, "name": name })
    db.commit()
    return redirect('/rediger_grill')

#####################################################################################

# KONTAKTSKJEMA
# KONTAKTSKJEMA
# KONTAKTSKJEMA
# KONTAKTSKJEMA
@app.route("/send", methods=["POST"])
def send():
    name = request.form.get("name")
    email = request.form.get("email")
    number = request.form.get("number")
    body = request.form.get('body')

    msg = Message('mail fra ' + email, sender = 'thamuzz@brigade.no', recipients = ['thomasbw@brigade.no'])
    msg.body = body + '\n' + '\n' + "Navn: " + name + '\n' + "Email: " + email + '\n' + "Telefonnummer: " + number + '\n'
    mail.send(msg)
    return "Sent"
