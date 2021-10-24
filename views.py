

from flask import Blueprint
from flask import render_template, request, jsonify
import requests
from config import API_KEY
views = Blueprint('views', __name__)

BASE_API_URL = 'https://api.yelp.com/v3/businesses/search'
url_params = {'term': 'bubble tea', 'sort_by': 'rating'}
headers = {'Authorization': f"Bearer {API_KEY}"}

# GLOBAL VARS
json_result = None
sorted_list_busi = None
busi_dict = None


def sort_by_distance(user_coords, json_dict) -> list:
    '''
    user_coords is a tuple representing a user's coordinates. (lat, long)
    json_dict is the dictionary containing the data that came back from our API call
    max_distance: max distance to sort by. Maximum distance away from user_coords
    '''
    KM_TO_MILES = 0.621371
    list_valid_bus = []
    bus_list = list(json_dict.values())[0]
    # bus_list is a list of dictionaries with all the business attributes as keys
    # busi is one dictionary
    for busi in bus_list:
        busi_coord = tuple(busi['coordinates'].values())
        dist_in_miles = round(float(busi['distance']) / 1000 * KM_TO_MILES, 2) # distance comes back as meters
        list_valid_bus.append({'name': busi['name'], 'distance': dist_in_miles, 'rating': busi['rating'], 'image': busi['image_url']})

    list_valid_bus = sorted(list_valid_bus, key=lambda x: x['distance'])
    return list_valid_bus # a list of busniess names, sorted by distance


def get_results():
    global busi_dict, sorted_list_busi
    busi_dict = dict()

    for busi in sorted_list_busi:
        busi_name = busi['name']
        busi_img_url = busi['image'] 
        busi_rating = busi['rating']
        # building the dictionary that the results page will read from
        busi_dict[busi_name] = {"name": busi_name, "rating": busi_rating, 'image': busi_img_url}


def api_call(user_coords: tuple, user_options: tuple) -> dict:
    #print("inside api_call")
    MILES_TO_METERS = 1609
    url_params['open_now'] = False if user_options[1] == True else True # will pass 'True' if this option is empty
    url_params['radius'] = (int(user_options[0]) * MILES_TO_METERS)
    url_params['latitude'] = user_coords[0]
    url_params['longitude'] = user_coords[1]
    url_params['limit'] = int(user_options[2])
    # calling the API
    response = None
    response = requests.get(BASE_API_URL, params=url_params, headers=headers)
    if (response.status_code != 200):
        print('STATUS WAS NOT 200')
    json_test = response.json()
    return json_test


@views.route('/', methods=['POST', 'GET'])
def home_page():
    if request.method == 'GET':
        #print('home: GET')
        return render_template('base.html', boolean=True)
    elif request.method == 'POST':
        print('home: POST')

        data = request.get_json() # getting the coordinates and options from the website
        coords = (data['latitude'], data['longitude'])
        options = (data['distance'], data['is_closed'], data['limit'])
        #print('before api_call')
        json_from_api = api_call(coords, options)
        #print(json_from_api)
        global json_result
        json_result = json_from_api
        global sorted_list_busi
        sorted_list_busi = sort_by_distance(coords, json_result)
        #print(sorted_list_busi)
        get_results()

        # print(f"dist: {dict(request.get_json())['is_closed']}")
        #return "the results page"
        return render_template('base.html', boolean=True)

@views.route('/result', methods=['POST', 'GET'])
def results_page():
    global busi_dict, sorted_list_busi
    while True:
        if busi_dict == None and sorted_list_busi == None:
            pass
        elif request.method == "GET" and busi_dict != None and sorted_list_busi != None:
            temp = render_template('result.html', boolean=True,busi_dict = busi_dict, sorted_list_busi = sorted_list_busi)
            busi_dict, sorted_list_busi = None, None
            return temp