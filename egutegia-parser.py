import csv
import couchdb
import json
from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza
from operator import attrgetter

couch = couchdb.Server('http://admin:HHZ60Et4wxJLhLs@127.0.0.1:5984')
db = couch['test']

def month_index(month):
    if month.startswith('Enero'):
        return '01'
    elif month.startswith('Otsaila'):
        return '02'
    elif month.startswith('Martxo'):
        return '03'
    elif month.startswith('Apirila'):
        return '04'

if __name__ == "__main__":
    with open('./data/batel-egutegia.csv', newline='') as csvfile:
        estropadakreader = csv.reader(csvfile, delimiter=",")
        tanda = 0
        kategoria_base = None
        kategoriak_helper = []
        for row in estropadakreader:
            eguna = row[3]
            if int(row[3]) < 10:
                eguna = f'0{row[3]}'
            data = f'2020-{month_index(row[1])}-{eguna}'
            print(row[5][0:2])
            try:
                jardunaldia = int(row[5][0:2])
            except ValueError:
                try:
                    jardunaldia = int(row[5][0])
                except ValueError:
                    jardunaldia = None
            # print(f'{jardunaldia} [{data}] - {row[4]} - {row[5]}')
            datuak = {
                'id': f'2020_GBL_{jardunaldia:02}',
                'jardunaldia': jardunaldia,
                'data': data,
                'liga': 'GBL',
                'lekua': row[4]
            }
            estropada = Estropada(f'Gipuzkoako batel liga, {jardunaldia}. Jardunaldia', **datuak)

            # print_pretty(estropada)
            print(estropada.get_json())
            estropada_json = estropada.get_json()
            db[estropada.id] = json.loads(estropada_json)

