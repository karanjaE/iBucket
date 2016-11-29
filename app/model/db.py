from passlib.apps import custom_app_context as pwd_ctx

from app import db


class BaseModel(db.Model):
    """It creates the base for DB classes"""

    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(BaseModel):
    """It defines the users table"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, default=111000,
                   autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True,
                         index=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)

    def hash_password(self, password):
        """Hashes out passwords before persisting to the db"""
        self.password_hash = pwd_ctx.encrypt(password)

    def verify_password(self, password):
        """Hashes password at login for verification"""
        return pwd_ctx.verify(password, self.password_hash)


class Bucket(BaseModel):
    __tablename__ = "buckets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bucket_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(), default=db.func.now())
    date_modified = db.Column(db.DateTime(), default=db.func.now(),
                              onupdate=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    items = db.relationship("Item", backref="bucket")


class Item(BaseModel):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(200), nullable=False)
    bucket = db.Column(db.Integer, db.ForeignKey("buckets.id"))
    date_created = db.Column(db.DateTime(), default=db.func.now())
    date_modified = db.Column(db.DateTime(), default=db.func.now(),
                              onupdate=db.func.now())
