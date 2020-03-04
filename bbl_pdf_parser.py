import sys
from tabula import read_pdf
from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza


def parse_senior_data(orrialdea, kategoria):
    df = read_pdf(filename, pages=orrialdea, stream=True)
    if kategoria in ['JG', 'JN']:
        df[0].drop(df[0].columns[[2]], axis=1, inplace=True)
    df[0].columns = ['TandaPostua', 'BalizaKlub', 'Ziab1', 'Ziab23', 'Denbora', 'Ezdakit', 'Diferentzia']
    sailkapena = df[0].iloc[1::2]

    for i, r in sailkapena.iterrows():
        (posizioa, _, tanda) = r['TandaPostua'].partition('o')
        (kalea, _, taldea) =  r['BalizaKlub'].partition(' ')
        (ziab2, _, ziab3) =  r['Ziab23'].partition(' ')
        tanda = int(tanda)
        kalea = int(kalea)
        denbora =  r['Denbora']
        emaitza = {
            'tanda': tanda,
            'tanda_postua': posizioa,
            'kalea': kalea,
            'posizioa': posizioa,
            'kategoria': kategoria,
            'denbora': denbora,
            'puntuazioa': 0}
        t = TaldeEmaitza(taldea, **emaitza)
        t.ziaboga_gehitu(r['Ziab1'])
        t.ziaboga_gehitu(ziab2)
        t.ziaboga_gehitu(ziab3)
        estropada.taldeak_add(t)

def parse_kadete_data(orrialdea, kategoria):
    df = read_pdf(filename, pages=orrialdea, stream=True)
    df[0].columns = ['TandaPostua', 'BalizaKlub', 'Ezdakit', 'Ziab1', 'Ziab2Denbora', 'Ezdakit2', 'Diferentzia']
    sailkapena = df[0].iloc[1::2]

    for i, r in sailkapena.iterrows():
        (posizioa, _, tanda) = r['TandaPostua'].partition('o')
        (kalea, _, taldea) =  r['BalizaKlub'].partition(' ')
        ziab1 = r['Ziab1']
        (ziab2, _, denbora) =  r['Ziab2Denbora'].partition(' ')
        tanda = int(tanda)
        kalea = int(kalea)
        emaitza = {
            'tanda': tanda,
            'tanda_postua': posizioa,
            'kalea': kalea,
            'posizioa': posizioa,
            'kategoria': kategoria,
            'denbora': denbora,
            'puntuazioa': 0}
        t = TaldeEmaitza(taldea, **emaitza)
        t.ziaboga_gehitu(ziab1)
        t.ziaboga_gehitu(ziab2)
        estropada.taldeak_add(t)

def parse_infantil_data(orrialdea, kategoria):
    df = read_pdf(filename, pages=orrialdea, stream=True)
    df[0].columns = ['TandaPostua', 'BalizaKlub', 'Ezdakit', 'Ziab1', 'Denbora', 'Diferentzia']
    sailkapena = df[0].iloc[1::2]

    for i, r in sailkapena.iterrows():
        (posizioa, _, tanda) = r['TandaPostua'].partition('o')
        (kalea, _, taldea) =  r['BalizaKlub'].partition(' ')
        ziab1 = r['Ziab1']
        denbora =  r['Denbora']
        emaitza = {
            'tanda': tanda,
            'tanda_postua': posizioa,
            'kalea': kalea,
            'posizioa': posizioa,
            'kategoria': kategoria,
            'denbora': denbora,
            'puntuazioa': 0}
        t = TaldeEmaitza(taldea, **emaitza)
        estropada.taldeak_add(t)
        t.ziaboga_gehitu(ziab1)

def parse_data(orrialdea, kategoria):
    df = read_pdf(filename, pages=orrialdea, stream=True)
    if kategoria[1] == 'N':
        df[0].drop(df[0].columns[[2]], axis=1, inplace=True)
    if kategoria[1] == 'G':
        df[0].drop(df[0].columns[[3]], axis=1, inplace=True)
    df[0].columns = ['TandaPostua', 'BalizaKlub', 'Denbora', 'Diferentzia']
    sailkapena = df[0].iloc[1::2]

    for i, r in sailkapena.iterrows():
        (posizioa, _, tanda) = r['TandaPostua'].partition('o')
        (kalea, _, taldea) =  r['BalizaKlub'].partition(' ')
        denbora =  r['Denbora']
        emaitza = {
            'tanda': tanda,
            'tanda_postua': posizioa,
            'kalea': kalea,
            'posizioa': posizioa,
            'kategoria': kategoria,
            'denbora': denbora,
            'puntuazioa': 0}
        t = TaldeEmaitza(taldea, **emaitza)
        estropada.taldeak_add(t)


filename = sys.argv[1]
# @ToDo Lehen estropadak kateagoria bat gehiago dago:
# 3. orrialdean Alebin Mixto
# Saltatu egin behar da...
skip = sys.argv[2]

structure = [(1, 'SG'), (2, 'AN'), (3, 'AG'), (4, 'IN'), (5, 'IG'), (6, 'IG'), (7, 'KN'), (8, 'KG'), (9, 'JN'), (10, 'JG'), (11, 'SN')]

e = {
    'izena': 'Bizkaiako batel liga, 3.jardunaldia',
    'data': '2020-02-29',
    'lekua': 'Sestao'
}
estropada = Estropada(**e)

for kategoria in structure:
    print(f'Reading page {kategoria[0]} for cat {kategoria[1]}')
    if kategoria[1][0] in ['S', 'J']:
        parse_senior_data(kategoria[0], kategoria[1])
    elif kategoria[1][0] in ['K']:
        parse_kadete_data(kategoria[0], kategoria[1])
    elif kategoria[1][0] in ['I']:
        parse_infantil_data(kategoria[0], kategoria[1])
    else:
        parse_data(kategoria[0], kategoria[1])

estropada.dump_json()