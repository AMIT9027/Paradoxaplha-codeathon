from flask import Flask,render_template,flash,url_for,redirect,request,Blueprint
import secrets
import pickle
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os
import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
from PIL import Image
import json
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf.file import FileField,FileAllowed
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail,Message
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
app=Flask(__name__,template_folder="C:\\Users\\acer\\Desktop\\Social media")
errors=Blueprint(__name__,"total product")
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///C:/Users/acer/Desktop/Social media/sitess.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config["RECAPTCHA_PUBLIC_KEY"]="6Lc7dfgUAAAAAFWGvBsNlAiYxhMQxRyTQp17EAsk"
app.config["RECAPTCHA_PRIVATE_KEY"]="6Lc7dfgUAAAAADC3pepyGWO6lmrG_Yao2IPpJaJF"
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'amitshah.tulas@gmail.com'
app.config['MAIL_PASSWORD'] = 'fcewcyuskzpwytiw'
mail = Mail(app)

cascPath = "haarcascade_frontalface_default.xml"
#######                                                                    COMMENT FORM CLASSSSSSSS                                                                    ###########################################################
class P(FlaskForm):
    submit = SubmitField('Login')

###################################################################################################################################################################################
class SURVEY(FlaskForm):
    Firstname = StringField('Firstname',
                           validators=[DataRequired()])
    Lastname = StringField('Lastname',
                        validators=[DataRequired()])
    Address=  StringField('Address',
                                  validators=[DataRequired(), Length(min=8, max=30)])
    Socia=SelectField('SELECT SOCIAL MEDIA',choices=[('Facebook','Facebook'),('Twitter','Twitter'),
    ('LinkedIn','LinkedIn'),('Instagram','Instagram'),
    ('Snapchat','Snapchat'),('Pinterest','Pinterest'),
    ('YouTube','YouTube'),('WhatsApp','WhatsApp'),
    ('Messenger','Messenger'),('WeChat','WeChat'),
    ('QQ','QQ'),('Tumblr','Tumblr'),
    ('Qzone','Qzone'),('TikTok','TikTok'),
    ('Reddit','Reddit'),('Skype','Skype'),
    ('Baidu Tieba','Baidu Tieba'),('Viber','Viber'),
    ('Line','Line'),('Telegram','Telegram'),
    ('Medium','Medium'),('Tagged','Tagged'),
    ('Renren','Renren'),('Badoo','Badoo'),
    ('Myspace','Myspace'),('StumbleUpon','StumbleUpon'),
    ('The Dots','The Dots'),('Kiwibox','Kiwibox'),
    ('Skyrock','Skyrock'),('Delicious','Delicious'),
    ('Snapfish','Snapfish'),('ReverbNation','ReverbNation'),
    ('Flixster','Flixster'),('Ravelry','Ravelry'),
    ('Wayn','Wayn'),('Vine','Vine'),
    ('Classmates','Classmates'),('Discord','Discord')])
    submit=SubmitField('Submit')
    
    
    def validate_username(self, username):
        user = Social.query.filter_by(Name=Name.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Social.query.filter_by(Names=Names.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

#############################################                       Registration form start                   #################################################################################

class RegistrationForm(FlaskForm):
    recaptcha=RecaptchaField()
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

#############################################                            registration  file end                      #################################################################################
#############################################                           Login file start                     #################################################################################
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
#############################################                            login file end                      #################################################################################
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
#############################################                            Update form file end                      #################################################################################
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.user_loader
def load_user(user_ids):
    return User.query.get(int(user_ids))

#############################################                          Update  Form file end                      ###########################
#############################################                          Model file start                     ###########################
#############################################                          User file start                    ###########################
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

####################################################################################################################################################################################
class S(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name=db.Column(db.String(100), unique=True, nullable=False)
    Names=db.Column(db.String(100), unique=True, nullable=False)
    Address=db.Column(db.String(100),unique=True, nullable=False)
    Social=db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"Social('{self.Name}', '{self.Names}', '{self.Address}', '{self.Social}')"


##########################################################################################################################################################################################
def Amit():
    data={}
    us=S.query.all()
    for u in us:
        data['data']={
            'Firstname':u.Name,
            'Lastname':u.Names,
            'Address':u.Address,
            'Social':u.Social,

            }

        s=json.dumps(data)
        with open('dataas.json',"w")as f:
            f.write(s)

#############################################                          Post  file start                    ###########################
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

#############################################                          notifier  file start                     ###########################


#############################################                          notifier file end                      ###########################
#############################################                          Post file end                      ###########################

#############################################                         Route file open                   ###########################

#############################################                          Route post file start                     ###########################


posts=[{

'author':'Amit shah',
'title':'Medicines',
'content':'First post content',
'date_posted':'april 20,2018'



},
{

'author':'Yashasvi Agarawal',
'title':'Testing',
'content':'second post content',
'date_posted':'april 21,2018'
}
]

#############################################                          Route post file end                ############################################
#############################################                         App route Form file start                      ###########################
@app.route('/')
@app.route('/index')
def index():
   
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #return redirect(url_for("ink.html'))
    return render_template('ind.html',posts=posts)
   # return "hello world"
cascPath = "haarcascade_frontalface_default.xml"
@app.route("/AMITS",methods=['GET', 'POST'])
def AMITS():
            var=input("Enter name")

            faceCascade = cv2.CascadeClassifier(cascPath)
            log.basicConfig(filename='webcam.log',level=log.INFO)

            video_capture = cv2.VideoCapture(0)
            anterior = 0

            while True:
                if not video_capture.isOpened():
                    print('Unable to load camera.')
                    sleep(5)
                    pass

                # Capture frame-by-frame
                ret, frame = video_capture.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )

                # Draw a rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                if anterior != len(faces):
                    anterior = len(faces)
                    log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


                # Display the resulting frame
                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('s'): 

                    check, frame = video_capture.read()
                    cv2.imshow("Capturing", frame)
                    cv2.imwrite(filename='C:\\Users\\acer\\Desktop\\Social media\\collect\\'+var+'.jpg', img=frame)
                    video_capture.release()
                    img_new = cv2.imread('C:\\Users\\acer\\Desktop\\Social media\\collect\\'+var+'.jpg', cv2.IMREAD_GRAYSCALE)
                    img_new = cv2.imshow('C:\\Users\\acer\\Desktop\\Social media\\collect\\'+var+'.jpg', img_new)
                    cv2.waitKey(1650)
                    print("Image Saved")
                    print("Program End")
                    cv2.destroyAllWindows()

                    break
                elif cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Turning off camera.")
                    video_capture.release()
                    print("Camera off.")
                    print("Program ended.")
                    cv2.destroyAllWindows()
                    break

                # Display the resulting frame
                cv2.imshow('Video', frame)

            # When everything is done, release the capture
            video_capture.release()
            cv2.destroyAllWindows()
            flash('HAS BEEN REGISTER', 'success')
            return redirect(url_for('index')) 
        
@app.route('/Social', methods=['GET', 'POST'])
def Social():
    form=SURVEY()
    if form.validate_on_submit():
        Amit=S(Name=form.Firstname.data, Names=form.Lastname.data, Address=form.Address.data, Social=form.Socia.data)
        db.session.add(Amit)
        db.session.commit()
        flash('Your data has been register!', 'success')
        return redirect(url_for('Social'))  
    return render_template('Social.html', title='Social',form=form)

@app.route('/pppp', methods=['GET', 'POST'])
def pppp():
    form=P()
    if form.validate_on_submit():
        Amit()
        return redirect(url_for('maps'))  
    return render_template('new.html', title='Social',form=form)

@app.route('/maps')
def maps():
   
    return render_template('maps.html')


@app.route('/map')
def map():
   
    return render_template('map.html')
@app.route('/f')
def f():
   return render_template('ink.html',title='About')
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('Login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('ind'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile picture', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/account",methods=['GET',"POST"])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file=url_for('static',filename='profile picture/'+current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file,form=form)


#############################################                          Route post function file start                    ###########################

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
    
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
    



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='amitshah.tulas@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: 
    {url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('Login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('Login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500


@app.route('/pre')
def pre():
    return render_template('buttons.html',title='precautions')

@app.route('/btn1')
def btn1():
    return render_template('basic.html',title='precautions')

@app.route('/btn2')
def btn2():
    return render_template('yogic.html',title='precautions')    

    #############################################                          Route post function file end                      ###########################

#############################################                          APP Route file end                      ###########################
#############################################                          Route  file end                      ###########################

#############################################                          Main file start                   ###########################

if __name__ == '__main__':
    app.run(debug=True)


#############################################                          Main file end                      ###########################