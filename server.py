from flask import Flask, render_template, request, make_response, redirect
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy


HEADER_LENGTH = 80
SIGNATURE_LENGTH = 100
BODY_LENGTH = 2000
USERID_LENGTH = 48


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    header = db.Column(db.String(HEADER_LENGTH))
    signature = db.Column(db.String(SIGNATURE_LENGTH))
    body = db.Column(db.String(BODY_LENGTH))
    user_id = db.Column(db.String(USERID_LENGTH))

    def __init__(self, header, signature, body, user_id):
        self.header = header
        self.signature = signature
        self.body = body
        self.user_id = user_id

    def __repr__(self):
        return '{}'.format(self.header)

db.create_all()
db.session.commit()


@app.route('/', methods=['GET'])
def form():
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = uuid4()
    res = make_response(render_template('form.html', can_post='True', disablet='', body_length=BODY_LENGTH))
    res.set_cookie('user_id', str(user_id))
    return res


@app.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    cookies_user_id = request.cookies.get('user_id')
    post_dict = {}
    post_dict['header'] = post.header
    post_dict['signature'] = post.signature
    post_dict['body'] = post.body
    post_dict[body_length] = BODY_LENGTH
    if (cookies_user_id == post.user_id):
        post_dict['can_post'] = 'True'
        post_dict['disabled'] = ''
    else:
        post_dict['disabled'] = 'disabled'
    return render_template('form.html', **post_dict)


@app.route('/', methods=['POST'])
@app.route('/<int:post_id>', methods=['POST'])
def add_post(post_id=None):
    user_id = request.cookies.get('user_id')
    if user_id is None:
        return render_template('error.html')
    if post_id:
        post = Post.query.get_or_404(post_id)
    else:
        post = Post('', '', '', user_id)
    
    post.header = request.form['header']
    post.signature = request.form['signature']
    post.body = request.form['body']

    if user_id == post.user_id:
        db.session.add(post)
        db.session.commit()
        return redirect('/{}'.format(post.id))
    else:
        return render_template('error.html')


if __name__ == "__main__":
    app.run()
