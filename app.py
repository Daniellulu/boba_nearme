from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'boba_finder_website'

    from views import views


    app.register_blueprint(views, url_prefix='/')

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
