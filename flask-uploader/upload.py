import os.path
from flask import Flask, redirect, request, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.storage import get_default_storage_class
from flask.ext.uploads import delete, init, save, Upload

# app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
# app.config['UPLOADS_FOLDER'] = os.path.realpath('.') + '/static/'
# app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
# # init(SQLAlchemy(app), get_default_storage_class(app))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.config['UPLOADS_FOLDER'] = os.path.realpath('.') + '/static/'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
db = SQLAlchemy(app)

Storage = get_default_storage_class(app)

init(db, Storage)

db.create_all()


@app.route('/')
def index():
    uploads = Upload.query.all()
    #return render_template('uploads.html')
    # return render_template('uploads.html', uploads=[1,1,2,3,5])
    return render_template('uploads.html', uploads=uploads)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a new file."""
    if request.method == 'POST':
        print 'saving'
        save(request.files['upload'])
        return redirect(url_for('index'))
    return (
        u'<form method="POST" enctype="multipart/form-data">'
        u'  <input name="upload" type="file">'
        u'  <button type="submit">Upload</button>'
        u'</form>'
    )

@app.route('/delete/<int:id>', methods=['POST'])
def remove(id):
    upload = Upload.query.get_or_404(id)
    delete(upload)
    return redirect(url_for('index'))



if __name__ == '__main__':
	app.debug = True
	app.run()