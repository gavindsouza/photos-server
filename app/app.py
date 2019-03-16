# imports - standard imports
import os
import json
import datetime

# imports - module imports
from app.config import config

# imports - third party imports
from flask import Flask, url_for, request, redirect, jsonify
from flask import render_template as render
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
import argon2
import werkzeug
import jwt

# global constants
ALLOWED_EXTENSIONS = [
    "ase",
    "art",
    "bmp",
    "blp",
    "cd5",
    "cit",
    "cpt",
    "cr2",
    "cut",
    "dds",
    "dib",
    "djvu",
    "egt",
    "exif",
    "gif",
    "gpl",
    "grf",
    "icns",
    "ico",
    "iff",
    "jng",
    "jpeg",
    "jpg",
    "jfif",
    "jp2",
    "jps",
    "lbm",
    "max",
    "miff",
    "mng",
    "msp",
    "nitf",
    "ota",
    "pbm",
    "pc1",
    "pc2",
    "pc3",
    "pcf",
    "pcx",
    "pdn",
    "pgm",
    "PI1",
    "PI2",
    "PI3",
    "pict",
    "pct",
    "pnm",
    "pns",
    "ppm",
    "psb",
    "psd",
    "pdd",
    "psp",
    "px",
    "pxm",
    "pxr",
    "qfx",
    "raw",
    "rle",
    "sct",
    "sgi",
    "rgb",
    "int",
    "bw",
    "tga",
    "tiff",
    "tif",
    "vtf",
    "xbm",
    "xcf",
    "xpm",
    "3dv",
    "amf",
    "ai",
    "awg",
    "cgm",
    "cdr",
    "cmx",
    "dxf",
    "e2d",
    "egt",
    "eps",
    "fs",
    "gbr",
    "odg",
    "svg",
    "stl",
    "vrml",
    "x3d",
    "sxd",
    "v2d",
    "vnd",
    "wmf",
    "emf",
    "art",
    "xar",
    "png",
    "webp",
    "jxr",
    "hdp",
    "wdp",
    "cur",
    "ecw",
    "iff",
    "lbm",
    "liff",
    "nrrd",
    "pam",
    "pcx",
    "pgf",
    "sgi",
    "rgb",
    "rgba",
    "bw",
    "int",
    "inta",
    "sid",
    "ras",
    "sun",
    "tga"
]
storage_space = 1 * 1024 * 1024
basedir = os.path.abspath(os.path.dirname(__file__))

# setting up Flask instance
app = Flask(__name__)
app.config.update(
    ENV='development',
    SECRET_KEY='kaam_bhari',
    STATIC_FOLDER='static/dist',
    HOST='0.0.0.0',
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'data.sqlite')
)

db = SQLAlchemy(app)
api = Api(app)

# setting up password hasher: REF=> https://argon2-cffi.readthedocs.io/en/stable/api.html
hasher = PasswordHasher()


class User(db.Model):
    __tablename__ = "users"

    # user auth
    username = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(120), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    # application auth
    token = db.Column(db.String(120), unique=True, nullable=False)

    # server allotations
    folder = db.Column(db.String(120), unique=True, nullable=False)
    alloted_space = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password):
        self.username = username
        # salt = uuid.uuid4().hex
        # self.password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        self.password = password
        self.registered_on = datetime.datetime.now()
        self.token = encode_token(self.username)

    def __repr__(self):
        return '<User %r>' % self.username


# standards
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def encode_token(self, username):
    try:
        payload = {
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_token(token):
    try:
        payload = jwt.decode(token, app.config.get('SECRET_KEY'))
        return payload['sub']

    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


# App Routes definitions
@app.route('/hello', methods=['GET'])
def greeting():
    return 'Hello from the other side'


@app.route('/')
def get_authenticated():
    if request.method == 'POST':
        trans_type = request.form['type']
        if trans_type == 'login':
            typed_user_name = request.form['username']
            typed_password = request.form['password']

            query_result = User.query.filter_by(
                username=typed_user_name).first()

            if query_result:
                retrieved_password = query_result.password
                try:
                    corect_password = hasher.verify(
                        typed_password, retrieved_password)
                    if corect_password:
                        return query_result.token

                except argon2.exceptions.VerificationError:
                    return {'Invalid': 'Credentials'}

        if trans_type == 'register':
            typed_name = request.form['name']
            typed_user_name = request.form['username']
            typed_password = request.form['password']

        return storage_space

    return render('index.html', title="Index Page"), storage_space


@app.route('/api/v1/', methods=['POST', 'GET'])
def api():

    if request.method == 'POST':
        prod_name = request.form['prod_name']
        quantity = request.form['prod_quantity']

        transaction_allowed = False

        if transaction_allowed:
            return

    return


# API call definitions
class UploadImage(Resource):
    def post(self, fname):
        file = request.files['file']
        if file and allowed_file(file.filename):
            # From flask uploading tutorial
            filename = werkzeug.secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            # return error
            return {'False'}

# api.add_resource(UploadImage, '/api/v1/upload?token=<token_id>')
