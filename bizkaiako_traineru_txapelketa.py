import click
import pandas as pd
import json

from tabula import read_pdf
from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza


def read_columns(df):
    columns = []
    for col in df.columns:
        columns.append(df[col][0])
    return columns


def parse_df(df):
    e = {
        'izena': 'Gipuzkoako traineru txapelketa',
        'data': '2020-07-15 18:00',
        'lekua': 'Orio'
    }
    estropada = Estropada(**e)
    for i, r in df.iterrows():
        # tanda = int(tanda)
        if not isinstance(r['Postua'], type('str')):
            break
        tanda = 1
        kalea = int(r['Kalea'])
        postua = int(r['Postua'][:-1])
        denbora = r['Denbora']
        taldea = r['TALDEA']
        ziabogak = [r['1, Ziabo']]
        if '2, Ziabo' in df.columns:
            ziabogak.extend([r['2, Ziabo'], r['3, Ziabo']])

        emaitza = {
            'tanda': tanda,
            'tanda_postua': postua,
            'kalea': int(kalea),
            'posizioa': postua,
            'denbora': denbora,
            'puntuazioa': postua,
            'ziabogak': ziabogak
        }
        t = TaldeEmaitza(taldea, **emaitza)
        estropada.taldeak_add(t)
    return estropada


def parse_data(sailkapena):
    # cols = sailkapena.columns
    # read_pdf(filename, pages=orrialdea, stream=True)
    cols = read_columns(sailkapena)
    sailkapena.columns = cols
    # sailkapena = df[0][df[0][cols[0]].notna()].iloc[1:]
    tanda = 0
    kalea = 1
    talde_emaitzak = []
    ziab1 = None
    ziab2 = None
    ziab3 = None

    for i, r in sailkapena.iterrows():
        if not isinstance(r['Puesto Tanda Baliza'], type('str')):
            continue
        if i == 0:
            continue
        if 'Puesto Tanda Baliza Club' in  cols:
            (posizioa, _, rest) =  str(r['Puesto Tanda Baliza Club']).partition('o')
            (tanda, _, rest) =  rest.lstrip().partition(' ')
            (kalea, _, taldea) =  rest.lstrip().partition(' ')
        if 'Puesto Tanda Baliza' in  cols:
            (posizioa, _, rest) =  str(r['Puesto Tanda Baliza']).partition('o')
            (tanda, _, kalea) =  rest.lstrip().partition(' ')
        if 'Club' in cols:
            taldea =  str(r['Club']).strip()
        if 'Puesto Tanda' in cols:
            (posizioa, _, tanda) = r['Puesto Tanda'].partition('o')
        if 'Baliza Club' in cols:
            (kalea, _, taldea) =  r['Baliza Club'].partition(' ')
        if 'Ciaboga 1' in cols:
            ziab1 = r['Ciaboga 1']
        if 'Ciaboga 1 Final' in cols:
            (ziab1, _, denbora) = r['Ciaboga 1 Final'].partition(' ')
        if 'Ciaboga 1 Ciaboga 2' in cols:
            (ziab1, _, ziab2) =  r['Ciaboga 1 Ciaboga 2'].partition(' ')
        if 'Ciaboga 1 Ciaboga 2 Final' in cols:
            denborak =  str(r['Ciaboga 1 Ciaboga 2 Final']).split(' ')
            if len(denborak) < 3:
                ziab1 = ''
                ziab2 = ''
                denbora = denborak[0]
            else:
                (ziab1, ziab2, denbora) = denborak
        if 'Ciaboga 2' in cols:
            ziab2 =  r['Ciaboga 2']
        if 'Ciaboga 2 Final' in cols:
            (ziab2, _, denbora) =  str(r['Ciaboga 2 Final']).partition(' ')
        if 'Ciaboga 2 Ciaboga 3' in cols:
            (ziab2, _, ziab3) =  r['Ciaboga 2 Ciaboga 3'].partition(' ')
        if 'Ciaboga 3 Final' in cols:
            (ziab3, _, denbora) =  str(r['Ciaboga 3 Final']).partition(' ')
        if 'Final' in cols:
            denbora =  r['Final']
            if pd.isna(denbora) and ziab1:
                (ziab1, _, denbora) = ziab1.partition(' ')
        tanda = int(tanda)
        kalea = int(kalea)
        emaitza = {
            'tanda': tanda,
            'tanda_postua': int(posizioa),
            'kalea': int(kalea),
            'posizioa': int(posizioa),
            'denbora': denbora,
            'puntuazioa': 0
        }
        t = TaldeEmaitza(taldea, **emaitza)
        if ziab1 and pd.notna(ziab1):
            t.ziaboga_gehitu(ziab1)
        if ziab2 and pd.notna(ziab2):
            t.ziaboga_gehitu(ziab2)
        if ziab3 and pd.notna(ziab3):
            t.ziaboga_gehitu(ziab3)
        talde_emaitzak.append(t)
    return talde_emaitzak


@click.command()
@click.argument('filename')
def parse_emaitzak_doc(filename):
    df = read_pdf(filename, pages=1, stream=True)

    neskak = df[0]
    nesken_emaitza = parse_data(neskak)
    e = {
        'izena': 'Bizkaiako traineru txapelketa',
        'data': '2020-07-15 18:00',
        'lekua': 'Orio'
    }
    estropada = Estropada(**e)
    for e in nesken_emaitza:
        estropada.taldeak_add(e)
    print(estropada.get_json())
    # mutilak = df[2]
    # mutil_emaitza = parse_df(mutilak)
    # print(mutil_emaitza.get_json())


if __name__ == "__main__":
    parse_emaitzak_doc()
