import os
import secrets
from PIL import Image
from datetime import datetime
from flask import render_template, url_for, redirect, request,flash
from main_app import app, db, current_user,login_user, logout_user,login_required
from main_app.models import Message, Announcement, Testimony, Book, Gallery, User


#middleware - save audiofiles
def save_audio(media):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(media.filename)
    media_fn = random_hex + f_ext
    media_path = os.path.join(app.root_path, 'static/message_audios', media_fn)
    media.save(media_path)
    return media_fn

#middleware - save image files
def save_img(img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(img.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/church_img', picture_fn)
    img.save(picture_path)
    return picture_fn

def fake(img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(img.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/church_img', picture_fn)
    
    compression_layer = (400,400)
    img_file = Image.open(img)
    img_file.thumbnail(compression_layer)
    img_file.save(picture_path)
    
    return picture_fn

#middleware - save books/pdf files
def save_book(book):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(book.filename)
    book_fn = random_hex + f_ext
    book_path = os.path.join(app.root_path, 'static/books', book_fn)
    book.save(book_path)
    return book_fn



#dashboard routes
@app.route("/admin")
@login_required
def admin_index():
    galleries = Gallery.query.order_by(Gallery.id.desc()).limit(3).all()
    messages = Message.query.order_by(Message.id.desc()).limit(3).all()
    return render_template("admin/index.html", messages=messages, galleries=galleries, title="Home")

@app.route("/admin/announcement", methods=['GET','POST'])
@login_required
def announcement():
    announcements = Announcement.query.all()
    if request.method == "POST":
        image = save_img(request.files['imganounc'])
        new_announcement = Announcement(annouce=request.form['announce'], image=image, content=request.form['content'])
        new_announcement.save_to_database()
        flash("Annoucement Created Successfully", "success")
        return redirect(url_for('announcement'))
    return render_template('admin/announcement.html', announcements=announcements,title="Announcements")

@app.route('/admin/announcement/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit_announcement(id):
    announcement = Announcement.find_by_id(id)
    if request.method == "POST":
        if request.form['announce'] and request.form['content'] and request.files['imganounc']:
            image = save_img(request.files['imganounc'])
            announcement.annouce = request.form['announce']
            announcement.image = image
            announcement.content = request.form['content']
            db.session.commit()
            flash('Announcement Updated', "success")
            return redirect(url_for('announcement'))
        elif request.form['announce'] and request.form['content']:
            announcement.annouce = request.form['announce']
            announcement.content = request.form['content']
            db.session.commit()
            flash('Announcement Updated', "success")
            return redirect(url_for('announcement'))
    return render_template('admin/edit_announcement.html', announcement=announcement, title="Edit Annoucement")

@app.route('/admin/announcement/<int:id>/delete')
@login_required
def delete_announcement(id):
    announce = Announcement.find_by_id(id)
    os.remove(app.root_path + url_for('static', filename="church_img/"+announce.image))
    announce.remove_from_database()
    flash("Annoucement Deleted Successfully","danger")
    return redirect(url_for('announcement'))

@app.route('/admin/books', methods=['GET','POST'])
@login_required
def books():
    books = Book.query.all()
    if request.method == "POST":
        book = save_book(request.files['book'])
        new_book = Book(title=request.form['title'], name=book, author=request.form['author'])
        new_book.save_to_database()
        flash("Book Added Successfully", "success")
        return redirect(url_for('books'))
    return render_template('admin/books.html', books=books,title="Add Books")

@app.route('/admin/books/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit_book(id):
    book = Book.find_by_id(id)
    if request.method == "POST":
        if request.form['author'] and request.form['title']  and request.files['book']:
            book_file = save_book(request.files['book'])
            book.author = request.form['author']
            book.title = request.form['title']
            book.name = book_file
            db.session.commit()
            flash('Book Updated', "success")
            return redirect(url_for('books'))
        elif request.form['author'] and request.form['title']:
            book.author = request.form['author']
            book.title = request.form['title']
            db.session.commit()
            flash('Book Updated', "success")
            return redirect(url_for('books'))
    return render_template('admin/edit_book.html', book=book, title="Edit Books")

@app.route('/admin/books/<int:id>/delete')
@login_required
def delete_book(id):
    book = Book.find_by_id(id)
    os.remove(app.root_path + url_for('static', filename="books/"+book.name))
    print("Book Deleted Successfully!")
    book.remove_from_database()
    flash("Book Deleted Successfully","danger")
    return redirect(url_for('books'))

@app.route('/admin/gallery', methods=['GET','POST'])
@login_required
def gallery():
    galleries = Gallery.query.all()
    if request.method == "POST":
        for pic in request.files.getlist('image'):
            image = save_img(pic)
            fake_img = fake(pic)
            new_gallery = Gallery(tag=request.form['tag'],image=image, org_img=fake_img)
            new_gallery.save_to_database()
        flash("Picture Added Sucessfully", "success")
        return redirect(url_for('gallery'))
    return render_template('admin/gallery.html', galleries=galleries,title="Gallery")

@app.route('/admin/gallery/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit_gallery(id):
    gallery = Gallery.find_by_id(id)
    if request.method == "POST":
        if request.form['tag'] and request.files['image']:
            os.remove(app.root_path + url_for('static', filename="church_img/"+gallery.image))
        os.remove(app.root_path + url_for('static', filename="church_img/"+gallery.org_img))
            image = save_img(request.files['image'])
            gallery.tag = request.form['tag']
            gallery.image = image
            db.session.commit()
            flash('Picture Updated', "success")
            return redirect(url_for('gallery'))
        elif request.form['tag']:
            gallery.tag = request.form['tag']
            db.session.commit()
            flash('Picture Updated', "success")
            return redirect(url_for('gallery'))
    return render_template('admin/edit_gallery.html', gallery=gallery,title="Edit Image")

@app.route('/admin/gallery/<int:id>/delete')
@login_required
def delete_gallery(id):
    gallery = Gallery.find_by_id(id)
    os.remove(app.root_path + url_for('static', filename="church_img/"+gallery.image))
    os.remove(app.root_path + url_for('static', filename="church_img/"+gallery.org_img))
    gallery.remove_from_database()
    flash("Gallery Deleted Successfully","danger")
    return redirect(url_for('gallery'))

@app.route('/admin/messages', methods=['GET','POST'])
@login_required
def messages():
    messages = Message.query.all()
    if request.method == "POST":
        print(request.form['date'])
        message_audio = save_audio(request.files['audio'])
        message = Message(
            minister=request.form['author'], 
            title=request.form['title'], 
            tag=request.form['tag'], 
            message=request.form['message'],
            audio=message_audio
            )
        message.save_to_database()
        flash("Message Added Successfully", "success")
        return redirect(url_for('messages'))
    return render_template('admin/message.html', messages=messages,title="Sermons")

@app.route('/admin/messages/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit_message(id):
    message = Message.find_by_id(id)
    print(message.audio)
    if request.method == "POST":
        if request.form['author'] and request.form['title'] and request.form['tag'] and request.files['audio'] and request.form['message']:
            message_audio = save_audio(request.files['audio'])
            message.minister = request.form['author']
            message.title = request.form['title']
            message.tag = request.form['tag']
            message.audio = message_audio
            message.message = request.form['message']
            db.session.commit()
            flash('Message Updated', "success")
            return redirect(url_for('messages'))
        elif request.form['author'] and request.form['title'] and request.form['tag'] and request.form['message']:
            message.minister = request.form['author']
            message.title = request.form['title']
            message.tag = request.form['tag']
            message.message = request.form['message']
            db.session.commit()
            flash('Message Updated', "success")
            return redirect(url_for('messages'))
    return render_template('admin/edit_message.html', message=message, title="Edit Sermon")

@app.route('/admin/messages/<int:id>/delete')
@login_required
def delete_message(id):
    message = Message.find_by_id(id)
    os.remove(app.root_path + url_for('static', filename="message_audios/"+message.audio))
    message.remove_from_database()
    flash("Message Deleted Successfully","danger")
    return redirect(url_for('messages'))

@app.route('/admin/testimonies', methods=['GET', 'POST'])
@login_required
def testimony():
    testimonies = Testimony.query.all()
    if request.method == "POST":
        testimony = Testimony(name=request.form['name'], testimony=request.form['testi'])
        testimony.save_to_database()
        flash("Testimony added successfully", "success")
        return redirect(url_for('testimony'))
    return render_template('admin/testimony.html', testimonies=testimonies, title="Testimonies")

@app.route('/admin/testimonies/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit_testimony(id):
    testimony = Testimony.find_by_id(id)
    if request.method == "POST":
        testimony.name = request.form['name']
        testimony.testimony = request.form['testi']
        db.session.commit()
        flash('Testimony Updated', "success")
        return redirect(url_for('testimony'))
    return render_template('admin/edit_testimony.html', testimony=testimony,title="Edit testimony")

@app.route('/admin/testimonies/<int:id>/delete')
@login_required
def delete_testimony(id):
    testimony = Testimony.find_by_id(id)
    testimony.remove_from_database()
    flash("Testimony Deleted Successfully","danger")
    return redirect(url_for('testimony'))

@app.route('/admin/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username="admin@rcffutminna1234").first()
        if request.form['username'] == user.username and request.form['password'] == user.password:
            login_user(user)
            next_page = request.args.get('next')
            flash("Login Successfull", "success")
            return redirect(next_page) if next_page else redirect(url_for('admin_index'))
        else:
            flash("Invalid Username or Password","danger")
            return redirect(url_for('login'))
    return render_template("admin/login.html",title="DashBoard Login")


@app.route('/admin/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

