from bottle import Bottle, template, request, response, redirect
import model


app = Bottle()


@app.route('/')
def index():
    """Main index page of the application"""
    info = dict()

    key = model.get_session(db, request.get_cookie('COOKIE_NAME'))

    info['title'] = "Likes Application"
    info['yourlikes'] = model.get_likes(db, key)

    return template('index', info)

@app.post('/likeform')
def formhandler():

    key = model.get_session(db, request.get_cookie('COOKIE_NAME'))

    if request.forms['like']:
        newlike = request.forms['like']
        newlike = newlike.capitalize()
        model.store_like(db, newlike, key)

    return redirect('/')


@app.post('/deletelikes')
def formhandlerdelete():

    checked = request.POST.getall('checks')

    if checked:
        for check in checked:
            model.delete_like(db, check)

    return redirect('/')

if __name__ == "__main__":
    DB_NAME = model.DATABASE_NAME
    db = model.sqlite3.connect(DB_NAME)
    app.run()