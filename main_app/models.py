from main_app import db, login_manager, UserMixin
from datetime import datetime


@login_manager.user_loader
def admin(id):
    return User.query.get(int(id))

#message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    minister = db.Column(db.String(50))
    title = db.Column(db.String(100), nullable=False)
    tag = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.Text, nullable=False)
    audio = db.Column(db.String(100))
    
    def __str__(self):
        return f"Message('{self.minister}', '{self.title}')"
    
    @classmethod
    def find_by_title(cls, title:str):
        return cls.query.filter_by(title=title).first()
    
    @classmethod
    def find_by_id(cls, id:int):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_minister(cls, minister:str):
        return cls.query.filter_by(minister=minister).first()
    
    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()

#Announcement model
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    annouce = db.Column(db.String(50))
    image = db.Column(db.String(50), default="default.jpg")
    content = db.Column(db.Text, nullable=False)
    
    @classmethod
    def find_by_id(cls, id:int):
        return cls.query.filter_by(id=id).first()
    
    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()

#testimony model
class Testimony(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    testimony = db.Column(db.Text)
    
    @classmethod
    def find_by_id(cls, id:int):
        return cls.query.filter_by(id=id).first()
    
    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()

#books model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    
    def __str__(self):
        return self.title
    
    @classmethod
    def find_by_id(cls, id:int):
        return cls.query.filter_by(id=id).first()
    
    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()

#gallery model
class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), default="default.jpg")
    org_img = db.Column(db.String(50), default="default.jpg")
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def find_by_id(cls, id:int):
        return cls.query.filter_by(id=id).first()
    
    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()

#ADMIN USER MODEL
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()


#ALUMNI MODEL
class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    phone_number = db.Column(db.String(20))
    unit = db.Column(db.String(20), default=None)
    role = db.Column(db.String(50))
    
    def __str__(self):
        return self.first_name
    
    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()

#CONTACT MODEL
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)
    
    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()