from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


# for demonstration purposes, we won't actually need this for our little project
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class DownloadVideoForm(FlaskForm):
    video_url = StringField("Video URL", validators=[DataRequired()])
    quality = SelectField(
        "Quality",
        choices=[
            ("high", "High quality"),
            ("med", "Medium quality"),
            ("low", "Low quality"),
        ],
    )
    download_type = SelectField(
        "Download Type",
        choices=[
            ("m4a", "Audio (.m4a)"),
            ("mp3", "Audio (.mp3)"),
            ("mp4", "Video (.mp4)"),
        ],
    )

    submit = SubmitField("Download")
