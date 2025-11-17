from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # -------------------------
    # PayPal webhook route
    # -------------------------
    from flask import request, jsonify
    from .auth import grant_bot_access, revoke_bot_access  # make sure these exist

    @app.route("/paypal-webhook", methods=["POST"])
    def paypal_webhook():
        data = request.json
        print("Webhook received:", data)  # logs webhook payload

        if "event_type" in data:
            event = data["event_type"]
            email = data.get("resource", {}).get("subscriber", {}).get("email_address")
            
            if email:
                if event == "BILLING.SUBSCRIPTION.ACTIVATED":
                    grant_bot_access(email, plan="Basic")  # or dynamic plan
                elif event == "BILLING.SUBSCRIPTION.CANCELLED":
                    revoke_bot_access(email)
                # add more events as needed

        return jsonify({"status": "ok"})

    return app



def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')