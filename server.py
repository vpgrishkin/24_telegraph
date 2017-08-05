from flask import Flask, render_template, request, make_response, redirect
from uuid import getnode
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    header = db.Column(db.String(80))
    signature = db.Column(db.String(100))
    body = db.Column(db.String(2000))
    user_id = db.Column(db.String(48))

    def __init__(self, header, signature, body, user_id):
        self.header = header
        self.signature = signature
        self.body = body
        self.user_id = user_id

    def __repr__(self):
        return '{}'.format(self.header)


@app.route('/', methods=['GET'])
def form():
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = getnode()
    res = make_response(render_template('form.html', can_post='True', disablet=''))
    res.set_cookie('user_id', str(user_id))
    return res


@app.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    cookies_user_id = request.cookies.get('user_id')
    post_dict = post.__dict__
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
    db.create_all()
    app.run()
