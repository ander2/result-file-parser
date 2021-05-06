""" Parse text from Gipuzkoako trainerila txapelketa into data """
import csv
import json
import sys
import collections

from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza
from operator import attrgetter

kategoriak = collections.deque(['JG', 'SN', 'SG', 'SG'])

if __name__ == "__main__":
    lekua = None
    id = None
    filename = sys.argv[1]
    izena = sys.argv[2]
    data = sys.argv[3]
    lekua = sys.argv[4]

    with open(filename, newline='') as csvfile:
        teamreader = csv.reader(csvfile, delimiter=",")

        e = {
            'izena': izena, 
            'data': data,
            'liga': 'GTL',
            'puntuagarria': False
        }
        if lekua:
            e['lekua'] = lekua
        estropada = Estropada(**e)

        tanda = 1
        kalea = 1
        count = 0
        kategoria_base = kategoriak.popleft()
        kategoriak_helper = []
        puntuagarria = None
        for row in teamreader:
            try:
                posizioa = int(row[0])
                count = count + 1
            except IndexError as e:
                kategoria_base = kategoriak.popleft()
                count = 0
                continue
            kategoria = kategoria_base
            kategoriak_helper.append(kategoria)
            denbora = row[5]
            if kategoria_base == 'SG' and count < 2:
                puntuazioa = 0
            else:
                if posizioa == 1:
                    puntuazioa = row[6]
                else:
                    puntuazioa = row[7]
            emaitza = {'tanda': tanda,
                       'tanda_postua': posizioa,
                       'kalea': kalea,
                       'posizioa': posizioa,
                       'kategoria': kategoria,
                       'denbora': denbora,
                       'puntuazioa': int(puntuazioa)
                       }
            t = TaldeEmaitza(row[1], **emaitza)
            t.ziaboga_gehitu(row[4])
            # if row[13] != '':
            #     t.ziaboga_gehitu(row[13])
            # if row[15] != '':
            #     t.ziaboga_gehitu(row[15])
            estropada.taldeak_add(t)
        estropada.kategoriak = list(set(kategoriak_helper))

    print(estropada.get_json())


