from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage for comments
comments = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Get comments from the form
            comment = request.form.get('comment', '')
            comments[filename] = comments.get(filename, []) + [comment]

            return redirect(url_for('index'))

    # List uploaded files and their comments
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
