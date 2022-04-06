# Coursework 2

### Instructions

Before running the app for the first time, please follow these instructions to create the database for each models.

1. In the [models.py](flask_app/models.py) file, uncomment these lines of code under the User class (line 10-15)

```python
     __tablename__ = "user"
   id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.Text, nullable=False)
   last_name = db.Column(db.Text, nullable=False)
   email = db.Column(db.Text, unique=True, nullable=False)
   password = db.Column(db.Text, nullable=False)
```

and also under the Post class (line 29-34)

```python
    __tablename__ = "post"
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), nullable=False)
   date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   content = db.Column(db.Text, nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

2. In the User class, comment this line of code (line 9)

```python
    __table__ = db.Model.metadata.tables['user']
```

and comment this line of code in the Post class (line 28)

```python
    __table__ = db.Model.metadata.tables['post']
```

3. In the [__init.py__](flask_app/__init__.py) file, uncomment line 34 and 35

```python
    from flask_app.models import User, Post
    db.create_all()
```

and comment line 36

```python
db.Model.metadata.reflect(bind=db.engine)
```

4. Run [app.py](flask_app/app.py)
5. If you were to run the app again, please uncomment the commented lines and comment the uncommented lines from the
   previous steps in each file and
6. Run [app.py](flask_app/app.py) again

### Github Repository Link

https://github.com/Jorge-gg7/comp0034_cw2_team10

### Video Link
https://youtu.be/JcxRs1vg4mk