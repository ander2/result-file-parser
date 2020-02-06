import csv
import couchdb
import json
import sys

from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza
from operator import attrgetter

couch = couchdb.Server('http://admin:HHZ60Et4wxJLhLs@127.0.0.1:5984')
db = couch['test']

kategoriak = ['Haurra', 'Infantila', 'Promesa', 'Kadete', 'Jubenil', 'Absolut', 'Jubenil', 'Senior']

if __name__ == "__main__":
    lekua = None
    id = None
    filename = sys.argv[1]
    izena = sys.argv[2]
    if sys.argv[3]:
        id = sys.argv[3]
    if sys.argv[4]:
        lekua = sys.argv[4]
    with open('./data/2020111_194026_200111_Arraun denborrak.csv', newline='') as csvfile:
        teamreader = csv.reader(csvfile, delimiter=",")

        e = {'izena': izena}
        if id:
            e = db[id]
        if lekua:
            e['lekua'] = lekua
        estropada = Estropada(**e)

        tanda = 0
        kategoria_base = None
        kategoriak_helper = []
        for row in teamreader:
            posizioa = None
            try:
                posizioa = int(row[1])
            except ValueError as e:
                continue
            if posizioa == 1:
                kategoria_base = kategoriak[tanda]
                tanda = tanda + 1
            kategoria = kategoria_base + ' ' + row[3]
            kategoriak_helper.append(kategoria)
            emaitza = {'tanda': tanda,
                       'tanda_postua': posizioa,
                       'kalea': 1,
                       'posizioa': posizioa,
                       'kategoria': kategoria,
                       'denbora': row[8],
                       'puntuazioa': row[10]}
            t = TaldeEmaitza(row[2], **emaitza)
            t.ziaboga_gehitu(row[5])
            estropada.taldeak_add(t)
        estropada.kategoriak = list(set(kategoriak_helper))

    print(estropada.get_json())
    estropada_json = estropada.get_json()
    estropada_obj = json.loads(estropada_json)
    estropada_obj['_rev'] = estropada._rev
    db[estropada.id] = estropada_obj
