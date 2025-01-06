import os
import urllib.parse

password = "Share1with@"
encoded_password = urllib.parse.quote(password)


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{encoded_password}@localhost/flask_app"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
