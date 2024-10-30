# from django.apps import AppConfig


# class AccommodationConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'Accommodation'
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue dans l'application SmartBooking !"

if __name__ == "__main__":
    app.run(debug=True)

