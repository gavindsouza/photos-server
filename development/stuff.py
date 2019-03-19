import requests
import sqlite3


def create_user():
    url = 'http://0.0.0.0:5000/'
    payload = {
        'type': 'register',
        'name' : 'gavin',
        'username' : 'gavin',
        'password' : 'gavin'
    }
    response = requests.post(url=url, data=payload)
    print(response.text)

def upload_image():
    url = 'http://0.0.0.0:5000/api/v1/upload?' 
    files = {
        'media': open('/home/gavin/Downloads/J2BCOGS.jpg', 'rb'),
        'token': 'something'
        }
    requests.post(url, files=files)

def create_table():
    query = "CREATE TABLE IF NOT EXISTS User (username TEXT, name TEXT, password TEXT, registered_on TEXT)"
    db = sqlite3.connect('data.sqlite')
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()
