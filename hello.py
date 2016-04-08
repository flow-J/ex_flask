# coding: utf-8
from datetime import datetime
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import Required, Email, EqualTo
from flask import session, redirect, url_for# 会话，　重定向
from flask import flash
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

#***************************** database **********************************#
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy= 'dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


def make_shell_context():
    return dict(app=app, db=db,User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))









#**************************** decorate************************************#

@app.route('/user/<name>')
def name(name):
    return render_template('user.html', name= name)
#   return app.send_static_file('a.json')

@app.route('/time')
def time():
    return render_template('time.html',
            time = datetime.utcnow())


@app.route('/base/')
def base():
    return render_template('base.html')



@app.errorhandler(404)
def page_not_found(justaword):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(justaword):
    return render_template('500.html'), 500


#***************************************class*****************************#

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])# 文本字段 Required()是个验证函数　如果输入框里为空的话就会提示出错

    submit = SubmitField('Submit') # 表单提交按钮


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = NameForm()
    if form.validate_on_submit():# 首先检查提交的内容是不是为空,或者说检测有没有提交
#       old_name = session.get('name')
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data   #IF TRUE后把data里的值赋给name
        form.name.data = ''
        return redirect(url_for('hello'))     #url_for里的参数是函数名
    return render_template('index.html', form=form, name=session.get('name'),
            known = session.get('known', False),
            time = datetime.utcnow())

#************************** Email ***************************************#
class EmailForm(Form):
    email = StringField('Enter your email.', validators=[Email()])
    password = PasswordField('password', validators=[Required(), EqualTo('confirm_password',message='password')])# 确认密码　然后这里还是linux那种隐藏文本字段
    confirm_password = PasswordField('confirm password', validators=[Required()])

    submit = SubmitField('Submit')


"""　
0 首先用户输入127.0.0.1:7777/email　打开网页
1 然后模板文件被打开　１行email框 ２行password框
2 输入完毕以后用户点击　submit　提交
"""
@app.route('/email/', methods=['GET', 'POST'])
def email():
    email_form = EmailForm()
    return render_template('email.html', form=email_form)






if __name__ == '__main__':
    manager.run()
