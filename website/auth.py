import weakref
from flask import Blueprint, Flask, render_template, request, flash, redirect, url_for
from .models import Doctor, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_socketio import join_room, leave_room
# from main import socketio
from website import create_app

from flask_mail import Mail, Message
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)




@auth.route('/', methods=['GET', 'POST'])
def home():
    
   
    return render_template('home.html')




@auth.route('/contact')
def contact():
   

     return redirect(url_for('views.contactus'))


@auth.route('/his')
def his():
   

     return redirect(url_for('views.his'))

@auth.route('/appoinment')
def appoinment():
   

     return redirect(url_for('views.appoinment'))



@auth.route('/confirmation')
def confirmation():
     return redirect(url_for('views.confirmation'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.patient'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/drlogin', methods=['GET', 'POST'])
def drlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        doctor = Doctor.query.filter_by(email=email).first()
        if doctor:
            if check_password_hash(doctor.password, password):
             
                login_user(doctor, remember=True)
                return redirect(url_for('views.doctor'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("drlogin.html", user=current_user)

@auth.route('/doctor')
def doctor():
   

     return redirect(url_for('views.doctor'))


@auth.route('/realtime')
def realtime():
   

     return redirect(url_for('views.realtime'))


@auth.route('/history')
def history():
   

     return redirect(url_for('views.history'))


# @auth.route('/map')
# def map_func():
# 	return render_template('map.html')



@auth.route('/prescription')
def prescription():
   

     return redirect(url_for('views.prescription'))

@auth.route('/index')
def index():
   

     return redirect(url_for('views.index'))
    
@auth.route('/drindex')
def drindex():
   

     return redirect(url_for('views.drindex'))
     

@auth.route('/inbox')
def inbox():
   

     return redirect(url_for('views.inbox'))


@auth.route('/doctor/patient details')
def drpatient():
   

     return redirect(url_for('views.drpatient'))


@auth.route('/doctor/map')
def map():
   

     return redirect(url_for('views.map'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        
        first_name = request.form.get('firstName')
        email = request.form.get('email')
        age = request.form.get('age')
        address = request.form.get('address')
        doctor_id= request.form.get('doctor_id')
        gender = request.form.get('gender')
        bg = request.form.get('bg')
        phone = request.form.get('phone')
        relative = request.form.get('relative')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(first_name=first_name, email=email, age=age,doctor_id=doctor_id,gender=gender,address=address, bg=bg, phone=phone, relative=relative, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.patient'))

    return render_template("sign_up.html", user=current_user)

#dr login login

@auth.route('/drsignup', methods=['GET', 'POST'])
def dr_signup():
    if request.method == 'POST':
        name = request.form.get('firstName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        doctor = Doctor.query.filter_by(email=email).first()
        if doctor:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')  
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Doctor(name=name, email=email, phone=phone, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.doctor'))
    return render_template("drsignup.html", doctor=current_user)





#write details

@auth.route('/patient/<style>')
def patient_details(style):
    try:
        user = User.query.filter_by(style=style).order_by(User.name).all()
        return render_template('patient.html', user=user, style=style)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

#chat
@auth.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    return render_template('chat.html', username=username, room=room)

@auth.route('/drchat')
def drchat():
    username = request.args.get('username')
    room = request.args.get('room')

    return render_template('drchat.html', username=username, room=room)
  















