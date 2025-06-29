import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db/studentdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# ---------- Models ----------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    nickname = db.Column(db.String(50))
    student_id = db.Column(db.String(20))
    image = db.Column(db.String(100))
    team = db.Column(db.String(50))

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.String(4))
    image = db.Column(db.String(100))

# ---------- Routes: Student ----------
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        file = request.files['image']
        filename = ''
        if file and file.filename != '':
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        student = Student(
            name=request.form['name'],
            nickname=request.form['nickname'],
            student_id=request.form['student_id'],
            image=filename,
            team=request.form['team']
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.nickname = request.form['nickname']
        student.student_id = request.form['student_id']
        student.team = request.form['team']
        file = request.files['image']
        if file and file.filename != '':
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            student.image = filename
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

# ---------- Routes: Car ----------
@app.route('/cars')
def show_cars():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        file = request.files['image']
        filename = ''
        if file and file.filename != '':
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        car = Car(
            brand=request.form['brand'],
            model=request.form['model'],
            year=request.form['year'],
            image=filename
        )
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('show_cars'))
    return render_template('car_form.html')

@app.route('/edit_car/<int:id>', methods=['GET', 'POST'])
def edit_car(id):
    car = Car.query.get_or_404(id)
    if request.method == 'POST':
        car.brand = request.form['brand']
        car.model = request.form['model']
        car.year = request.form['year']
        file = request.files['image']
        if file and file.filename != '':
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            car.image = filename
        db.session.commit()
        return redirect(url_for('show_cars'))
    return render_template('car_form.html', car=car)

@app.route('/delete_car/<int:id>')
def delete_car(id):
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('show_cars'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
