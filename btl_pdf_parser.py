"""
Parser for Bizkaiako trainerila liga. Tries to create Estropada model
based on CSV files derived from PDF result files.
"""
import click
import logging
import json
import pandas as pd
import os

from tabula import read_pdf
from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza

logger = logging.getLogger('estropadak')
logger.debug('Start logging')

def puntuazioak_kalkulatu(estropada):
    kategoriak = ['JN', 'JG', 'SN', 'SG' ]
    for kategoria in kategoriak:
        taldeak = [taldea for taldea in estropada.sailkapena if taldea.kategoria == kategoria]
        liga_taldeak = [taldea for taldea in taldeak if 'nesk' not in taldea.talde_izena.lower() and 'mx' not in taldea.talde_izena.lower() and 'NM' not in taldea.talde_izena]
        liga_taldeak = [taldea for taldea in liga_taldeak if "Ez aurkeztua" not in taldea.denbora]
        liga_taldeak = [taldea for taldea in liga_taldeak if "Fortfait" not in taldea.denbora]
        max_points = 12
        if len(liga_taldeak) > 12:
            max_points = len(liga_taldeak)
        logger.debug(f'Kategoria: {kategoria}')
        for posizioa, taldea in enumerate(liga_taldeak):
            logger.debug(f'Puntuazioa:{taldea.talde_izena}\t{max_points}-{taldea.posizioa} + 1')
            if 'kanporatua' in taldea.denbora.lower() or 'deskalifikatua' in taldea.denbora.lower():
                taldea.puntuazioa = 0
            else:
                taldea.puntuazioa = max_points - posizioa

def read_columns(df):
    columns = []
    for col in df.columns:
        columns.append(df[col][0])
    return columns

def parse_pdf_to_csv(filename, orrialdea, kategoria, data):
    df = read_pdf(filename, pages=orrialdea, stream=True)
    cols = read_columns(df[0])
    df[0].columns = cols
    sailkapena = df[0][df[0][cols[0]].notna()].iloc[1:]
    try:
        os.mkdir(f'./data/btl/{data}/')
    except FileExistsError:
        pass
    sailkapena.to_csv(f'./data/btl/{data}/{kategoria}_{orrialdea}.csv')

def parse_data(orrialdea, kategoria, data):
    sailkapena = pd.read_csv(f'./data/btl/{data}/{kategoria}_{orrialdea}.csv')
    cols = sailkapena.columns
    tanda = 0
    talde_emaitzak = []
    ziab1 = None
    ziab2 = None
    ziab3 = None
    denbora = ''

    for i, r in sailkapena.iterrows():
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
        if 'Ciaboga 1 Ciaboga 2 Ciaboga 3 Final' in cols:
            denborak =  str(r['Ciaboga 1 Ciaboga 2 Ciaboga 3 Final']).split(' ')
            if len(denborak) < 3:
                ziab1 = ''
                ziab2 = ''
                ziab3 = ''
                denbora = denborak[0]
            else:
                (ziab1, ziab2, ziab3, denbora) = denborak
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
            'kategoria': kategoria,
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
@click.option('--docid', help='ID of doc in DB')
@click.option('--izena', help='Race name')
@click.option('--data', help='Race date')
@click.option('--lekua', help='Race place')
@click.option('--import-to-db', is_flag=True, help='Import result to the DB')
@click.option('--parse-to-csv', is_flag=True, help='Create CSV files with parsed data')
@click.argument('filename')
def gtl_pdf_parser(docid, izena, data, lekua, import_to_db, filename, parse_to_csv):
    structure = [(1, 'JN'), (2, 'JG'), (3, 'SN'), (4, 'SG'), (5, 'SG')]

    e = None
    if import_to_db:
        import adaptors.couch as couchdb
        try:
            e = couchdb.getdoc(docid)
            del e['sailkapena']
        except KeyError as err:
            e = {
                'izena': izena,
                'data': data,
                'lekua': lekua
            }
    else:
        e = {
            'izena': izena,
            'data': data,
            'lekua': lekua
        }
    estropada = Estropada(**e)
    kategoriak = []

    if parse_to_csv:
        for kategoria in structure:
            logger.info(f'Reading page {kategoria[0]} for cat {kategoria[1]}')
            try:
                kategoria_emaitzak = parse_pdf_to_csv(filename, kategoria[0], kategoria[1], data)
            except Exception as e:
                print(f"Cannot parse {kategoria[0]} orrialdea")
                logger.error(e)

    else:
        for kategoria in structure:
            logger.info(f'Reading page {kategoria[0]} for cat {kategoria[1]}')
            try:
                kategoria_emaitzak = parse_data(kategoria[0], kategoria[1], data)
                kategoriak.append(kategoria[1])
                for t in kategoria_emaitzak:
                    estropada.taldeak_add(t)
            except Exception as e:
                print(f"Cannot parse {kategoria[0]} orrialdea")
                logger.error(e)


        estropada.kategoriak = kategoriak
        puntuazioak_kalkulatu(estropada)

        if import_to_db:
            estropada_json = estropada.get_json()
            estropada_obj = json.loads(estropada_json)
            if hasattr(estropada, '_rev'):
                estropada_obj['_rev'] = estropada._rev
            couchdb.setdoc(docid, estropada_obj)
        else:
            estropada.dump_json()

if __name__ == "__main__":
    logging.basicConfig(filename='btl.log', level=logging.DEBUG)
    gtl_pdf_parser()