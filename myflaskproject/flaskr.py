from flask import Flask,render_template,g,request,redirect,url_for
import os   
import database,validateimg

app=Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path,'info.db'),
    DEBUG=True
))


def get_db():
    if not hasattr(g,'db'):
        g.db=database.Db(app.config['DATABASE'])
    return g.db 

@app.before_request
def before_request():
    get_db()

@app.teardown_appcontext
def close_db(error):
    g.db.close()


@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    assert request.path=='/login'
    assert request.method=='POST'   
    name=request.form['username']
    password=request.form['password']
    rs=g.db.checkUsr(name,password)
    if len(rs) > 0:
        return render_template('login.html',errmsg=rs)
    else:
        return redirect(url_for('books'))

@app.route('/books')
def books():
    return render_template('books.html')

 
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/checkimg')
def checkimg():
    s,img=validateimg.gen()
    img=img.getvalue()
    response=app.make_response(img)
    response.headers['content-type']='image/gif'
    return response

if __name__=='__main__':
    app.run(debug=True)
