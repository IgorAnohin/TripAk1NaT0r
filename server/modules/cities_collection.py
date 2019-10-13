import pandas as pd
import json


class CitiesCollection:
    DEFAULT_FP = "data/cities_predict.csv"
    IMAGES_FP = "data/images.json"

    def _load_images(self, filepath):
        return json.load(open(filepath, 'r'))

    def _preprocess_data(self, data):
        def prettify_place(row):
            return ' '.join(map(lambda s: s.capitalize(), row['place_slug'].split('-')[:-row['countries_parts']]))

        data['countries_parts'] = data['country'].str.split().str.len()
        data['city'] = data[['place_slug', 'countries_parts']].apply(prettify_place, axis=1)
        data = data.rename(columns=self._old_new_scored_features_mapping)
        data = data[self._key_features + self._scored_features]
        return data

    def _load_table(self, filepath):
        data = pd.read_csv(filepath)
        return self._preprocess_data(data)

    @staticmethod
    def _get_old_new_scored_features_mapping():
        return {
            'female_friendly': 'female friendly',
            'friendly_to_foreigners': 'friendly to foreigners',
            'fun': 'fun',
            'happiness': 'happiness',
            'healthcare': 'healthcare',
            'lgbt_friendly': 'lgbt friendly',
            'nightlife': 'nightlife',
            'peace': 'peace',
            'quality_of_life': 'quality of life',
            'racial_tolerance': 'racial tolerance',
            'religious_government': 'religious government',
            'safety': 'safety',
            'startup_score': 'startup score',
            'traffic_safety': 'traffic safety',
            'walkability': 'walkability',
            'internet': 'internet'
        }

    @staticmethod
    def _get_old_new_binary_features_mapping():
        return {
            'cashless_society': 'cashless society',
            'safe_tap_water': 'safe tap water',
            'coffee': 'coffee',
            'coca-cola': 'coca cola',
            'lgbt_friendly': 'lgbt friendly',
            'internet': 'internet'
        }

    @staticmethod
    def _get_binary_features_questions_mapping():
        return {
            'cashless society': 'Does society have to be cashless?',
            'safe tap water': 'Do you drink water from the tap?',
            'coffee': 'Do you consume coffee often?',
            'coca cola': 'Do you consume soda often?',
            'lgbt friendly': 'Does the city have to be LGBT friendly?',
            'internet': 'Is the internet speed an important factor for you?'
        }

    @staticmethod
    def _get_numeric_features_questions_mapping():
        return {
            'female friendly': 'How female friendly should the city be?',
            'friendly to foreigners': 'How important is it that the city is friendly to foreigners?',
            'fun': 'How fun should be the city?',
            'happiness': 'Happiness level of the city?',
            'healthcare': 'Healthcare level in the city?',
            'nightlife': 'Nightlife activity in the city.',
            'peace': 'How peaceful is the city required to be?',
            'quality of life': 'How good is the city for life?',
            'racial tolerance': 'Tolerance level towards non-local races?',
            'religious government': 'How religious should be the government?',
            'safety': 'Required safety level?',
            'startup score': 'How good is the city for developing a startup?',
            'traffic safety': 'How safe is the traffic?',
            'walkability': 'How good is the city for walks?',
        }

    def get_main_features(self):
        return ['region', 'country', 'city']

    # only exceptional (!= (0, 5))
    @staticmethod
    def _get_features_ranges_mapping():
        return {}

    def get_cities(self):
        return list(self.data['city'])

    def get_countries(self):
        return list(self.data['country'])

    def get_binary_features(self):
        return self._binary_features

    def get_scored_features(self):
        return self._scored_features

    def get_numeric_question(self, feature):
        return self._features_numeric_questions_mapping.get(feature)

    def get_binary_question(self, feature):
        return self._features_binary_questions_mapping.get(feature)

    def get_image(self, feature):
        return self.images.get(feature)

    def get_range(self, feature):
        return self._features_ranges_mapping.get(feature, (1, 5))

    def __init__(self, cities):
        self._old_new_scored_features_mapping = self._get_old_new_scored_features_mapping()
        self._scored_features = list(self._old_new_scored_features_mapping.values())

        self._old_new_binary_features_mapping = self._get_old_new_binary_features_mapping()
        self._binary_features = list(self._old_new_binary_features_mapping.values())

        self._key_features = self.get_main_features()
        self._features_ranges_mapping = self._get_features_ranges_mapping()
        self._features_numeric_questions_mapping = self._get_numeric_features_questions_mapping()
        self._features_binary_questions_mapping = self._get_binary_features_questions_mapping()

        self.data = self._load_table(self.DEFAULT_FP)
        self.images = self._load_images(self.IMAGES_FP)
        self.data = self.data[self.data['city'].isin(cities)]
