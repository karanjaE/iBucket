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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True,
                         index=True)
    password = db.Column(db.String(200), nullable=False)
    bucket = db.relationship("Bucket", backref="users", lazy="dynamic",
                             cascade="all, delete-orphan")


class Bucket(BaseModel):
    """It creates the buckets table"""

    __tablename__ = "buckets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bucket_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(), default=db.func.now())
    date_modified = db.Column(db.DateTime(), default=db.func.now(),
                              onupdate=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    items = db.relationship("Item", backref="buckets",lazy="dynamic",
                            cascade="all, delete-orphan")


class Item(BaseModel):
    """It creates the items table"""

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    done  = db.Column(db.Boolean, nullable=False)
    bucket = db.Column(db.Integer, db.ForeignKey("buckets.id"))
    date_created = db.Column(db.DateTime(), default=db.func.now())
    date_modified = db.Column(db.DateTime(), default=db.func.now(),
                              onupdate=db.func.now())
