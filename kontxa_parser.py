import csv
import couchdb
import json
import sys
from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza

couch = couchdb.Server('http://admin:admin123@127.0.0.1:5984')
db = couch['estropadak']

if __name__ == "__main__":
    lekua = 'Donostia'
    id = 'kontxa_2020_gizonezko_2_jardunaldia'
    filename = sys.argv[1]
    izena = sys.argv[2]
    # if sys.argv[3]:
    #     id = sys.argv[3]
    with open(filename, newline='') as csvfile:
        teamreader = csv.reader(csvfile, delimiter=",")

        e = {
            'izena': izena,
            'data': '2020-09-13 10:00'
        }
        # if id:
        #     e = db[id]
        if lekua:
            e['lekua'] = lekua
        estropada = Estropada(**e)

        kategoria_base = None
        kategoriak_helper = []
        for row in teamreader:
            print(row)
            # if row[0].startswith('#'):
            #     continue
            posizioa = None
            try:
                tanda = int(row[0])
                tanda_posizioa = int(row[1])
                posizioa = int(row[2])
                kalea = int(row[5])
            except ValueError as e:
                continue
            emaitza = {
                'tanda': tanda,
                'tanda_postua': tanda_posizioa,
                'kalea': kalea,
                'posizioa': posizioa,
                'denbora': row[8],
                'puntuazioa': 0
            }
            t = TaldeEmaitza(row[3], **emaitza)
            t.ziaboga_gehitu(row[6])
            estropada.taldeak_add(t)

    print(estropada.get_json())
    estropada_json = estropada.get_json()
    estropada_obj = json.loads(estropada_json)
    # estropada_obj['_rev'] = estropada._rev
    db[id] = estropada_obj
