from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api 
from models import kamera as kameraModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

session = Session(engine)

app = Flask(__name__)
api = Api(app)        

class BaseMethod():

    def __init__(self):
        self.raw_weight = {'penyimpanan_memori': 4, 'kapasitas_baterai': 4, 'harga': 3, 'berat': 5, 'kualitas_hasil': 3}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(kameraModel.nama_kamera, kameraModel.penyimpanan_memori, kameraModel.kapasitas_baterai, kameraModel.harga, kameraModel.berat, kameraModel.kualitas_hasil)
        result = session.execute(query).fetchall()
        print(result)
        return [{'nama_kamera': kamera.nama_kamera, 'penyimpanan_memori': kamera.penyimpanan_memori, 'kapasitas_baterai': kamera.kapasitas_baterai, 'harga': kamera.harga, 'berat': kamera.berat, 'kualitas_hasil': kamera.kualitas_hasil} for kamera in result]

    @property
    def normalized_data(self):
        penyimpanan_memori_values = []
        kapasitas_baterai_values = []
        harga_values = []
        berat_values = []
        kualitas_hasil_values = []

        for data in self.data:
            penyimpanan_memori_values.append(data['penyimpanan_memori'])
            kapasitas_baterai_values.append(data['kapasitas_baterai'])
            harga_values.append(data['harga'])
            berat_values.append(data['berat'])
            kualitas_hasil_values.append(data['kualitas_hasil'])

        return [
            {'nama_kamera': data['nama_kamera'],
             'penyimpanan_memori': min(penyimpanan_memori_values) / data['penyimpanan_memori'],
             'kapasitas_baterai': data['kapasitas_baterai'] / max(kapasitas_baterai_values),
             'harga': data['harga'] / max(harga_values),
             'berat': data['berat'] / max(berat_values),
             'kualitas_hasil': data['kualitas_hasil'] / max(kualitas_hasil_values)
             }
            for data in self.data
        ]

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = []

        for row in normalized_data:
            product_score = (
                row['penyimpanan_memori'] ** self.raw_weight['penyimpanan_memori'] *
                row['kapasitas_baterai'] ** self.raw_weight['kapasitas_baterai'] *
                row['harga'] ** self.raw_weight['harga'] *
                row['berat'] ** self.raw_weight['berat'] *
                row['kualitas_hasil'] ** self.raw_weight['kualitas_hasil']
            )

            produk.append({
                'nama_kamera': row['nama_kamera'],
                'produk': product_score
            })

        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)

        sorted_data = []

        for product in sorted_produk:
            sorted_data.append({
                'nama_kamera': product['nama_kamera'],
                'score': product['produk']
            })

        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return result, HTTPStatus.OK.value
    
    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'data': result}, HTTPStatus.OK.value
    

class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['nama_kamera']:
                  round(row['penyimpanan_memori'] * weight['penyimpanan_memori'] +
                        row['kapasitas_baterai'] * weight['kapasitas_baterai'] +
                        row['harga'] * weight['harga'] +
                        row['berat'] * weight['berat'] +
                        row['kualitas_hasil'] * weight['kualitas_hasil'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return result, HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'data': result}, HTTPStatus.OK.value


class kamera(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None
        
        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.') 
        return {
            'page': page, 
            'page_size': page_size,
            'next': next_page, 
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = select(kameraModel)
        data = [{'nama_kamera': kamera.nama_kamera, 'penyimpanan_memori': kamera.penyimpanan_memori, 'kapasitas_baterai': kamera.kapasitas_baterai, 'harga': kamera.harga, 'berat': kamera.berat, 'kualitas_hasil': kamera.kualitas_hasil} for kamera in session.scalars(query)]
        return self.get_paginated_result('kamera/', data, request.args), HTTPStatus.OK.value


api.add_resource(kamera, '/kamera')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)