from flask import Flask, render_template, request, redirect, url_for
from models import db, Image
import os

app = Flask(__name__, template_folder='views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_gallery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Ensure the upload folder exists
os.makedirs('uploads', exist_ok=True)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        comment = request.form.get('comment', '')

        if file:
            filename = file.filename
            file.save(os.path.join('uploads', filename))

            # Store image metadata in the database
            new_image = Image(filename=filename, comment=comment)
            db.session.add(new_image)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/student', methods=['GET', 'POST'])
def student_view():
    if request.method == 'POST':
        # Handle comment submission
        image_id = request.form.get('image_id')
        comment = request.form.get('comment', '')

        if image_id and comment:
            # Store student comment in the database
            image = Image.query.get(image_id)
            if image:
                image.comment += f" | Student: {comment}"  # Append student comment
                db.session.commit()

            return redirect(url_for('student_view'))

    # Retrieve images from the database
    images = Image.query.all()
    return render_template('student_view.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
