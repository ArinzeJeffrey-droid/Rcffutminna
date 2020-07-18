import os
import secrets
from datetime import datetime
from flask import render_template, url_for, redirect, request,flash
from main_app import app, db, current_user,login_user, logout_user,login_required
from main_app.models import Message, Announcement, Testimony, Book, Gallery, User, Contact, Alumni


#index page
@app.route("/", methods=['GET',"POST"])
def index():
    if request.method == "POST":
        add_contact = Contact(name=request.form['fullname'], email=request.form['email'], message=request.form['message'])
        add_contact.save_to_database()
        flash("Message Received!, We'll Contact You", "Success")
        return redirect(url_for('index'))
    return render_template("user/index.html",title="The official website of Redeemed Christian fellowship Futminna chapter")


#gallery page
@app.route("/galleries", methods=['GET','POST'])
def view_gallery():
    page = request.args.get('page', 1, type=int)
    galleries = Gallery.query.order_by(Gallery.id.desc()).paginate(page=page,per_page=9)
    return render_template("user/gallery.html",galleries=galleries, title="Galleries")


@app.route("/alumni", methods=['GET',"POST"])
def alumni():
    if request.method == "POST":
        if request.form['alumni-unit']:
            check_email = Alumni.query.filter_by(email=request.form['alumni-email']).first()
            if check_email:
                flash("Alumni with that email already exists","danger")
                return redirect(url_for('alumni'))
            add_alumni = Alumni(
                first_name=request.form['firstName'],
                last_name=request.form['lastName'],
                email=request.form['alumni-email'],
                phone_number=request.form['alumni-number'],
                unit=request.form['alumni-unit'],
                role=request.form['unit']
                )
            add_alumni.save_to_database()
            flash("Submitted Successfully","success")
            return redirect(url_for('alumni'))
        else:
            add_alumni = Alumni(
                first_name=request.form['firstName'],
                last_name=request.form['lastName'],
                email=request.form['alumni-email'],
                phone_number=request.form['alumni-number'],
                role=request.form['unit']
                )
            add_alumni.save_to_database()
            flash("Submitted Successfully","success")
            return redirect(url_for('alumni'))
    return render_template('user/alumni.html', title="Alumni Connect")

@app.route("/events")
def events():
    return render_template("user/event.html", title="Events")

@app.route("/sermons")
def sermons():
    page = request.args.get('page', 1, type=int)
    messages = Message.query.order_by(Message.id.desc()).paginate(page=page,per_page=9)
    return render_template("user/sermon.html", title="Sermons", messages=messages)

@app.route("/books")
def user_books():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.id.desc()).paginate(page=page,per_page=9)
    return render_template("user/books.html", title="Books", books=books)


