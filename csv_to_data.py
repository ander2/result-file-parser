import csv
from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza
from operator import attrgetter

kategoriak = ['Haurra', 'Infantila', 'Promesa', 'Kadete', 'Jubenil', 'Absolut', 'Jubenil', 'Senior']

def print_pretty(estropada: Estropada):
    sailkapena = sorted(estropada.sailkapena, key=attrgetter('posizioa'))
    for talde in sorted(sailkapena, key=attrgetter('tanda')):
        print(u'{0:<6}\t{1:^5}\t{2:^5}\t{3:<30}\t{4:<25}\t{5:<8}\t{6:<12}'.format(
                    str(talde.posizioa), talde.tanda, talde.kalea,
                    talde.talde_izena, u'\t'.join(talde.ziabogak),
                    talde.denbora, talde.kategoria))


if __name__ == "__main__":
    with open('./data/2020111_194026_200111_Arraun denborrak.csv', newline='') as csvfile:
        teamreader = csv.reader(csvfile, delimiter=",")

        estropada = Estropada('Gipuzkoako batel liga, 1. Jardunaldia', **{'data': '2020-01-11 15:30', 'lekua': 'Martutene (Donostia)'})

        tanda = 0
        kategoria_base = None
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
            t = TaldeEmaitza(row[2], **{'tanda': tanda, 'kalea': 1, 'posizioa': posizioa, 'kategoria': kategoria, 'denbora':row[8], 'puntuak': row[10] })
            estropada.taldeak_add(t)

    print_pretty(estropada)

