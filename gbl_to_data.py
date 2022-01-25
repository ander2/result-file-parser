""" 
    Parse text from Gipuzkoako batel liga into data. 
    PDF result files doesn't generate well-formed CSV
    files, so the CSVs have to be cleaned.
    Returns an Estropada object in json format
"""
import csv
import sys

from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza

kategoriak = [
    'IG',
    'IN',
    'PG',
    'PN',
    'JG',
    'JN',
    'SG',
    'SN',
]


def parse_csv_file(filename: str):
    with open(filename, newline='') as csvfile:
        teamreader = csv.reader(csvfile, delimiter=",")

        e = {
            'izena': izena, 
            'data': data,
            'liga': 'GBL',
            'puntuagarria': True
        }

        estropada = Estropada(**e)

        tanda = 1
        for row in teamreader:
            tanda = 1
            try:
                posizioa = int(row[1])
            except ValueError:
                continue
            try:
                kalea=int(row[5])
            except ValueError as e:
                if row[9] == 'FORFAIT':
                    continue
                else:
                    print("Errorea kalea parseatzen")
                    print(row)
                    raise e
            denbora=row[9]
            try:
                puntuak=int(row[11])
            except ValueError:
                puntuak = 0
            except IndexError as e:
                print("Errorea puntuazioa parseatzen")
                print(row)
                raise e
            taldea = row[3]
            if posizioa == 1:
                kategoria = kategoriak.pop(0)
            try:
                posizioa = int(row[1])
            except ValueError as e:
                continue
            emaitza = {'tanda': tanda,
                       'tanda_postua': posizioa,
                       'kalea': kalea,
                       'posizioa': posizioa,
                       'kategoria': kategoria,
                       'denbora': denbora,
                       'puntuazioa': puntuak
                       }
            t = TaldeEmaitza(taldea, **emaitza)
            t.ziaboga_gehitu(row[6])
            if row[7] != '':
                t.ziaboga_gehitu(row[7])
            if row[8] != '':
                t.ziaboga_gehitu(row[8])
            estropada.taldeak_add(t)

    print(estropada.get_json())

if __name__ == "__main__":
    lekua = None
    id = None
    filename = sys.argv[1]
    izena = sys.argv[2]
    data = sys.argv[3]
    lekua = sys.argv[4]

    parse_csv_file(filename)
