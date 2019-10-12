import configparser

from flask import Flask, jsonify, request

from modules.images_getter import ImageGetterCached
from modules.price_finder import PriceFinder
from modules.cities_funnel import CitiesFunnel


CONFIG_FP = 'config.conf'
config = configparser.ConfigParser()
config.read(CONFIG_FP)

app = Flask(__name__)

img_getter = ImageGetterCached(config['google.api']['developer_key'], config['google.api']['cx'])
funnel = CitiesFunnel(img_getter)
price_finder = PriceFinder(config['skyscanner.api']['api_key'])


def merge_with_flights(cities):
    flights = [price_finder.get_price(city, max_results=1) for city in cities]
    min_prices = [flight['MinPrice'] for flight in flights]
    urls = [img_getter.get(city, 'sightseeing', count=1) for city in cities]
    return [{'city': city, 'min_price': min_price, 'url': url} for (city, min_price, url) in zip(min_prices, min_prices, urls)]


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return jsonify(funnel.get_next_question().to_json())
    elif request.method == 'POST':
        if request.args.get('image') == 1:
            feature = request.args.get('city_key')
            score = 1
        else:
            feature = request.args.get('question_perk')
            score = request.args.get('value')

        resulted_cities = funnel.set_rating(feature, score)
        json = {'status': 'confirmed'}
        if resulted_cities is not None:
            json['flights'] = merge_with_flights(resulted_cities)
        return jsonify(json)


@app.route('/final', methods=['GET'])
def final_result():
    cities = funnel.find_best(3)
    return jsonify({'flights': merge_with_flights(cities)})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
