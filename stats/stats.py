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
        return talde_izenak #self.db['talde_izenak']


    def sailkapen_orokorra(self, league, year):
        return stats_dao.get_sailkapen_orokorra(league, year)


    def set_sailkapen_orokorra(self, league, date, rank):
        '''Set rank'''
        stats_dao.set_sailkapen_orokorra(league, date, rank)

    def calculate_posizioak(self, liga, urtea, kategoria):
        '''Calculate position array for every team'''
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

    def calculate_cumulative(self, liga, urtea, kategoria):
        ''' Calculate cumulative points in rank'''
        puntuazioa = {}
        estropadak = stats_dao.get_estropadak(liga, urtea)
        for estropada in estropadak:
            logging.info("%s" % estropada['izena'])
            try:
                sailkapena = estropada['sailkapena']
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
                    if taldea in puntuazioa:
                        puntuak = puntuak_ + puntuazioa[taldea][-1:][0]
                        puntuazioa[taldea].append(puntuak)
                    else:
                        puntuazioa[taldea] = list([puntuak_])
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
