from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

# Models go here!
class Card(db.Model, SerializerMixin):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    suit = db.Column(db.String)
    value = db.Column(db.Integer)
    # This is the image column
    image = db.Column(db.String)

    def __repr__(self):
        return f'<Card: {self.name}, suit: {self.suit}, id: {self.id}>'

class Icon(db.Model, SerializerMixin):
    __tablename__ = "icons"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    content = db.Column(db.String)
    price = db.Column(db.Integer)

    usericons = db.relationship("UserIcon", backref="icon", cascade="all, delete-orphan")
    # users = db.relationship("User", back_populates="icon")

    serialize_rules = ("-usericons.icon",)

class Tag(db.Model, SerializerMixin):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)

    usertags = db.relationship("UserTag", backref="tag", cascade="all, delete-orphan")

    serialize_rules = ("-usertags.tag",)

class Emote(db.Model, SerializerMixin):
    __tablename__ = "emotes"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    content = db.Column(db.String)

    useremotes = db.relationship("UserEmote", backref="emote", cascade="all, delete-orphan")

    serialize_rules = ("-useremotes.emote",)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    user_id = db.Column(db.String)
    points = db.Column(db.Integer)
    total_points = db.Column(db.Integer)
    tag = db.Column(db.String)

    usericons = db.relationship("UserIcon",  backref="user", cascade="all, delete-orphan")
    usertags = db.relationship("UserTag", backref="user", cascade="all, delete-orphan")
    useremotes = db.relationship("UserEmote", backref="user", cascade="all, delete-orphan")

    serialize_rules = ("-usericons.user", "-usertags.user", "-useremotes.user",)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be visible")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))
    
    def __repr__(self):
        return f"<username: {self.username}, id: {self.id}, password: {self._password_hash}, image_url: {self.image_url}, user_id: {self.user_id}, points: {self.points}, total_points: {self.total_points}>"
        

# Join table for User and Icon
class UserIcon(db.Model, SerializerMixin):
    __tablename__ = "usericons"

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    icon_id = db.Column(db.Integer, db.ForeignKey("icons.id"))

    serialize_rules = ("-user.usericons", "-icon.usericons",)

# Join table for User and Tag
class UserTag(db.Model, SerializerMixin):
    __tablename__ = "usertags"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))

    serialize_rules = ("-user.usertags", "-tag.usertags",)

class UserEmote(db.Model, SerializerMixin):
    __tablename__ = "useremotes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    emote_id = db.Column(db.Integer, db.ForeignKey("emotes.id"))

    serialize_rules = ("-user.useremotes", "-emotes.useremotes",)