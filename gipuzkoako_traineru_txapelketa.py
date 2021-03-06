import click
from tabula import read_pdf
from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza


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


def parse_df_neskak(df):
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
        kalea = int(r['TALDEA Kalea'])
        postua = int(r['Postua'][:-1])
        denbora = r['Denbora']
        taldea = r['Unnamed: 0']
        ziabogak = [r['1, Ziabo']]

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


@click.command()
@click.argument('filename')
def parse_emaitzak_doc(filename):
    df = read_pdf(filename, pages=1, stream=True)

    neskak = df[1]
    nesken_emaitza = parse_df_neskak(neskak)
    print(nesken_emaitza.get_json())

    mutilak = df[2]
    mutil_emaitza = parse_df(mutilak)
    print(mutil_emaitza.get_json())


if __name__ == "__main__":
    parse_emaitzak_doc()
