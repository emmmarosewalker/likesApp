from bottle import Bottle, template, request, response, redirect, static_file
import model
import string


app = Bottle()


@app.route('/')
def index():
    """Main index page of the application"""
    info = dict()

    info['title'] = "Likes Application"

    return template('index', info)


@app.post('/likes')
def likeshandler():
    """Handles the /likes post request from JSON submission"""

    key = model.get_session(db, request.get_cookie('COOKIE_NAME'))

    if 'likes' in request.json:
        likes = request.json['likes']

    else:
        likes = []

    for like in likes:
        if like != "":
            like.upper()
            model.store_like(db, like ,key)

    return "Success"


@app.get('/likes')
def likesgethandler():
    """Handles a get request to /likes and returns JSON version of the likes data"""

    key = model.get_session(db, request.get_cookie('COOKIE_NAME'))

    info = dict()

    info['likes'] = model.get_likes(db, key)

    return info



@app.post('/deletelikes')
def formhandlerdelete():

    checked = request.POST.getall('checks')

    if checked:
        for check in checked:
            model.delete_like(db, check)

    return redirect('/')


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


if __name__ == "__main__":
    DB_NAME = model.DATABASE_NAME
    db = model.sqlite3.connect(DB_NAME)
    app.run()