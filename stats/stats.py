''' Calculate cummulative points for teams '''
import ast
import logging
import stats_dao


class Stats:
    '''Class for manipulation of diferent stats in estropadak '''

    def __init__(self):
        self.talde_dict = self.load_talde_dict()
        self.talde_izenak = self.load_taldeak()

    def load_talde_dict(self):
        talde_izenak = {}
        return talde_izenak

    def load_taldeak(self):
        talde_izenak = {}
        return talde_izenak  # self.db['talde_izenak']

    def sailkapen_orokorra(self, league, year, category):
        _category = category.replace(' ', '_').lower()
        return stats_dao.get_sailkapen_orokorra(league, year, _category)

    def set_sailkapen_orokorra(self, league, date, category, rank):
        '''Set rank'''
        _category = category.replace(' ', '_').lower()
        stats_dao.set_sailkapen_orokorra(league, date, _category, rank)

    def calculate_posizioak(self, liga, urtea, kategoria):
        '''Calculate position dict for every team'''
        puntuazioa = {}
        estropadak = stats_dao.get_estropadak(liga, urtea)
        for estropada in estropadak:
            logging.info("%s", estropada['izena'])
            try:
                sailkapena = estropada['sailkapena']
                for emaitza in sailkapena:
                    if kategoria != emaitza['kategoria']:
                        continue
                    try:
                        taldea = emaitza['talde_izena']
                    except KeyError:
                        print("No name for {}".format(emaitza['talde_izena']))
                    if taldea in puntuazioa:
                        puntuazioa[taldea].append(emaitza['posizioa'])
                    else:
                        puntuazioa[taldea] = [emaitza['posizioa']]
            except KeyError:
                print("No sailkapena for {}".format(estropada['izena']))
        return puntuazioa

    def calculate_posizioak_per_race(self, liga, urtea, kategoria):
        '''Calculate positions array for every team'''
        posizioak = []
        estropadak = stats_dao.get_estropadak(liga, urtea)
        for estropada in estropadak:
            try:
                sailkapena = estropada['sailkapena']
                talde_sailkapenak = {}
                for emaitza in sailkapena:
                    if kategoria != emaitza['kategoria']:
                        continue
                    try:
                        taldea = emaitza['talde_izena']
                    except KeyError:
                        print("No name for {}".format(emaitza['talde_izena']))
                    talde_sailkapenak[taldea] = emaitza['posizioa']
                posizioak.append(talde_sailkapenak)
            except KeyError:
                print("No sailkapena for {}".format(estropada['izena']))
        return posizioak

    def calculate_cumulative(self, liga, urtea, kategoria):
        ''' Calculate cumulative points in rank'''
        puntuazioa = {}
        estropadak = stats_dao.get_estropadak(liga, urtea)
        for estropada in estropadak:
            logging.info("%s" % estropada['izena'])
            try:
                sailkapena = estropada.get('sailkapena')
                if sailkapena:
                    for emaitza in sailkapena:
                        import pdb; pdb.set_trace()
                        if kategoria.lower() != emaitza['kategoria'].lower():
                            continue
                        taldea = emaitza['talde_izena']
                        if emaitza['puntuazioa'] == '':
                            puntuak_ = 0
                        else:
                            puntuak_ = int(emaitza['puntuazioa'])
                        if 'puntuazioa-rank' in emaitza:
                            puntuak_ = int(emaitza['puntuazioa-rank'])
                        if taldea in puntuazioa:
                            puntuak = puntuak_ + puntuazioa[taldea][-1:][0]
                            puntuazioa[taldea].append(puntuak)
                        else:
                            puntuazioa[taldea] = list([puntuak_])
            except KeyError as e:
                print("No sailkapena for {}".format(estropada['izena']))
                print(e)
        return puntuazioa

    def calculate_points_per_race(self, liga, urtea, kategoria):
        ''' Calculate points per race'''
        puntuazioa = []
        estropadak = stats_dao.get_estropadak(liga, urtea)
        for estropada in estropadak:
            logging.info("%s" % estropada['izena'])
            try:
                sailkapena = estropada['sailkapena']
                talde_puntuazioa = {}
                for emaitza in sailkapena:
                    if kategoria != emaitza['kategoria']:
                        continue
                    taldea = emaitza['talde_izena']
                    if emaitza['puntuazioa'] == '':
                        puntuak_ = 0
                    else:
                        puntuak_ = int(emaitza['puntuazioa'])
                    if 'puntuazioa-rank' in emaitza:
                        puntuak_ = int(emaitza['puntuazioa-rank'])
                    talde_puntuazioa[taldea] = puntuak_
                puntuazioa.append(talde_puntuazioa)
            except KeyError:
                print("No sailkapena for {}".format(estropada['izena']))
        return puntuazioa

    def clean_rank(self, rank):
        keys = []
        for key in rank.keys():
            if (key != '_id' and key != '_rev' and key != 'stats'):
                keys.append(key)
        for key in keys:
            del rank[key]
        return rank
