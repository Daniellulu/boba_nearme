from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'boba_finder_website'

    from views import views


    app.register_blueprint(views, url_prefix='/')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

    # BASE_API_URL = 'https://api.yelp.com/v3/businesses/search'
    # url_params = {'term': 'bubble tea', 'limit': 5, 'sort_by': 'rating', 'location': 'san francisco'}    # headers = {'Authorization': f"Bearer {API_KEY}"}

    # response = requests.get(BASE_API_URL, params=url_params, headers=headers)
    # print(response.status_code)
    
