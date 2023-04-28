# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 14:32:31 2023

@author: Benyas
"""

import pandas as pd
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from flask import jsonify
from sqlalchemy import create_engine, text

# Replace 'username', 'password', 'localhost', 'database_name' with the appropriate values
engine = create_engine('mysql+mysqldb://newuser:password@localhost:3308/hotel_sys')

# Create a connection object
conn = engine.connect()
print("haaa")
# Define your query
query = text('SELECT * from hotels')

# Execute the query
result = conn.execute(query)
hotels_df = pd.read_sql(query, conn)
# Fetch all the rows
rows = result.fetchall()
"""
# Print the rows
for row in rows:
    print(row)
"""
# Close the connection
conn.close()
hotels_df['city']=hotels_df['City_id']
hotels_df['name']=hotels_df['Name']
print(hotels_df)
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
    das=pd.read_csv('hotel_images12.csv')
    #give imagelink from das by using randomly
    import random as ran
    def get_image_link(row):
        try:
            return das.loc[das['hotel_id'] == row['id'], 'image_link'].iloc[5]
        except:
            return das['image_url'].iloc[ran.randint(1, len(das) - 1)]

    hotels_df['image_link'] = hotels_df.apply(get_image_link, axis=1)

    #hotels_df['image_link'] = hotels_df.apply(lambda row: das['image_url'].iloc[ran.randint(1,len(das)-1)], axis=1)
    #hotels_df['image_link'] = hotels_df.apply(lambda row: das.loc[das['hotel_id'] == row['id'], 'image_link'].iloc[0], axis=1)
    #hotels_df['image_link'] = hotels_df.apply(lambda row: f"https://via.placeholder.com/150x150?text={row['name']} {row['city']}" , axis=1)
    
    
    # Check if the search query matches a city in the DataFrame
    cities = hotels_df['city'].unique().tolist()
    
    if not search_query:
        # Return all hotels for the selected city
        print(request.json)
        city = request.json['city']
        print(city)
        hotels = hotels_df[hotels_df['city'] == city]
        print(hotels)
        if len(hotels)==0:
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
