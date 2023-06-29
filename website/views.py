import json

from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import current_user, login_required

from . import db
from .models import Note

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])

def home():

    return render_template("home.html", user=current_user)



@views.route('/patient', methods=['GET', 'POST'])
@login_required
def patient():

    return render_template("patient.html", user=current_user)




@views.route('/drpatient', methods=['GET', 'POST'])
@login_required
def drpatient():

    return render_template("drpatient.html", user=current_user)


@views.route('/map', methods=['GET', 'POST'])
@login_required
def map():

    return render_template("map.html", user=current_user)



@views.route('/patient/drlogin', methods=['GET', 'POST'])
@login_required
def doctor():
    if request.method == 'POST':
        note = request.form.get('note')

    return render_template("doctor.html", user=current_user)


@views.route('/home/contactus')

def contactus():

    return render_template("contactus.html", user=current_user)


@views.route('/home/his')

def his():

    return render_template("his.html", user=current_user)


@views.route('/home/appoinment')

def appoinment():

    return render_template("appoinment.html")



@views.route('/home/confirmation')

def confirmation():

    return render_template("confirmation.html")

@views.route('/home/inbox', methods=['GET', 'POST'])
@login_required
def inbox():
    
    return render_template("inbox.html", user=current_user)





@views.route('/home/prescription', methods=['GET', 'POST'])
@login_required
def prescription():
    
    return render_template("prescription.html", user=current_user)

@views.route('/home/index', methods=['GET', 'POST'])
@login_required
def index():
    
    return render_template("index.html", user=current_user)

@views.route('/home/drindex', methods=['GET', 'POST'])
@login_required
def drindex():
    
    return render_template("drindex.html", user=current_user)






@views.route('/home/realtime')
@login_required
def realtime():

    return render_template("realtime.html", user=current_user)



@views.route('/home/dr/patient_details')
@login_required
def patient_details():

    return render_template("patient_details.html", user=current_user)

@views.route('/home/history')
@login_required
def history():

    return render_template("history.html", user=current_user)




@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.user_id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
