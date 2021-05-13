from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from studyeasy.models import User
from flask_wtf.file import FileField, FileAllowed


class Register(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)], 
    render_kw={'class':"form-control", 'placeholder':"Name"})

    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=99)], 
    render_kw={'class':"form-control", 'placeholder':"Age"})

    email = StringField('Email', validators=[DataRequired(), Email()],
    render_kw={'class':"form-control", 'placeholder':"Email"})

    def validate_email(self, email_from_form):
        result = User.query.filter_by(email=email_from_form.data).first()
        if result:
            raise ValidationError('Email address already regitered')

    password = PasswordField('Password', validators=[DataRequired()],
    render_kw={'class':"form-control", 'placeholder':"Password"})

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
    render_kw={'class':"form-control", 'placeholder':"Confirm Passord"})

    submit = SubmitField('Sign Up')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()],
    render_kw={'class':"form-control", 'placeholder':"Email"})
    
    password = PasswordField('Password', validators=[DataRequired()],
    render_kw={'class':"form-control", 'placeholder':"Password"})

    submit = SubmitField('Login')

    remember = BooleanField('Remember Me')
    

class Account(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)], 
    render_kw={'class':"form-control", 'placeholder':"Name"})

    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=99)], 
    render_kw={'class':"form-control", 'placeholder':"Age"})

    email = StringField('Email', validators=[DataRequired(), Email()],
    render_kw={'class':"form-control", 'placeholder':"email"})


    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')],
    render_kw={'class':"form-control", 'placeholder':"profile_pic"})

    def validate_email(self, email_from_form):
        result = User.query.filter_by(email=email_from_form.data).count()
        if result > 1:
            raise ValidationError('Email address already regitered')


    submit = SubmitField('Update details')
   

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)],
    render_kw={'class':"form-control", 'placeholder':"Title"})
    
    content = TextAreaField('Article Content', validators=[DataRequired()],
    render_kw={'class':"form-control", 'placeholder':"Article Content", 'rows':'15'})

    submit = SubmitField('Post')

