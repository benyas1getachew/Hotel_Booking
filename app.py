import pandas as pd
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from flask import jsonify

@app.route('/api/top-hotels')
def top_hotels():
    # Code to fetch top hotels from the database
    hotels = [{'name': 'Hotel A', 'location': 'New York'},
              {'name': 'Hotel B', 'location': 'Paris'},
              {'name': 'Hotel C', 'location': 'Tokyo'}]
    # Return the list of top hotels as a JSON response
    return jsonify(hotels)

from flask import request


@app.route('/api/search2', methods=['POST'])
def search2():
    search_query = request.json['query']
    hotels_df = pd.read_csv('hotels.csv')
    # Query the DataFrame for hotels in the given city
    hotels = hotels_df.loc[hotels_df['city'] == search_query]
    if hotels.empty:
        return jsonify({'message': 'No hotels found in the given city'})
    else:
        num_hotels = len(hotels)
        hotels_list = [{'name': row['name'], 'location': row['city']} for index, row in hotels.iterrows()]
        return jsonify({'num_hotels': num_hotels, 'hotels': hotels_list})
@app.route('/api/search', methods=['POST'])
def search():
    print(request.json)
    search_query = request.json['query']
    hotels_df = pd.read_csv('hotels.csv')
    hotels_df['image_link']=hotels_df['name']+hotels_df['city']
    # Check if the search query matches a city in the DataFrame
    cities = hotels_df['city'].unique().tolist()
    if not search_query:
        # Return all hotels for the selected city
        print(request.json)
        city = request.json['city']
        print(city)
        hotels = hotels_df[hotels_df['city'] == city]
        
        if hotels.empty:
            return jsonify({'message': 'No hotels found in the selected city'})
        else:
            hotels_list = [{'name': row['name'], 'city': row['city'], 'image_link': row['image_link']} for index, row in hotels.iterrows()]
            return jsonify({'hotels': hotels_list})
    elif search_query in cities:
        # Return hotels for the selected city
        hotels = hotels_df[hotels_df['city'] == search_query]
        
        if hotels.empty:
            return jsonify({'message': 'No hotels found in the given city'})
        else:
            hotels_list = [{'name': row['name'], 'city': row['city'], 'image_link': row['image_link']} for index, row in hotels.iterrows()]
            return jsonify({'hotels': hotels_list})
    else:
        # Search for hotels with the given name in the selected city
        hotels = hotels_df[hotels_df['name'].str.contains(search_query, case=False)]
        if hotels.empty:
            return jsonify({'message': 'No hotels found with the given name or in the selected city'})
        else:
            hotels_list = [{'name': row['name'], 'city': row['city'], 'image_link': row['image_link']} for index, row in hotels.iterrows()]
            return jsonify({'hotels': hotels_list})

@app.errorhandler(500)
def internal_server_error(error):
    print(error)
    return {'message': 'Internal server error'}, 500
if __name__ == '__main__':
    app.run()
