''' Calculate Stats for league and year '''
import json
import sys
from stats import Stats


def calculate_stats(posizioak, puntuazioak, sailkapena, kategoria):
    '''Calculate stats for league and year'''
    stats_lib = Stats()
    TALDE_DICT = stats_lib.load_talde_dict()
    stats = {}
    if sailkapena is not None:
        for taldea in sailkapena['stats']:
            if kategoria != taldea['kategoria']:
                continue
            talde_norm = TALDE_DICT.get(taldea, taldea)
            stats[talde_norm] = {
                'position': len([tal for tal in sailkapena['stats'].keys()
                                 if (puntuazioak[tal][-1] > puntuazioak[taldea][-1])]) + 1,
                'points': puntuazioak[taldea][-1],
                'wins': posizioak[talde_norm].count(1),
                'best': min(posizioak[talde_norm]),
                'worst': max(posizioak[talde_norm]),
                'positions': posizioak[talde_norm],
                'cumulative': puntuazioak[taldea]
            }
            if min(posizioak[talde_norm]) < 0:
                raise ValueError('{} out of min bound({}): {}'.format(talde_norm,
                                                                      sailkapena['_id'],
                                                                      posizioak[talde_norm]))
            if min(posizioak[talde_norm]) > len(posizioak):
                raise ValueError('{} out of max bound({}): {}'.format(talde_norm,
                                                                      sailkapena['_id'],
                                                                      posizioak[talde_norm]))
    else:
       for taldea in puntuazioak.keys():
            talde_norm = taldea
            stats[talde_norm] = {
                "position": len([tal for tal in puntuazioak.keys()
                                 if (puntuazioak[tal] > puntuazioak[taldea])]) + 1,
                'points': puntuazioak[talde_norm][-1],
                'wins': posizioak[talde_norm].count(1),
                'best': min(posizioak[talde_norm]),
                'worst': max(posizioak[talde_norm]),
                'positions': posizioak[talde_norm],
                'cumulative': puntuazioak[taldea]
            }
    return stats

def update_stats(league, year, category):
    stats = Stats()
    positions = stats.calculate_posizioak(league, year, category)
    puntuazioak = stats.calculate_cumulative(league, year, category)
    rank = stats.sailkapen_orokorra(league, year)
    if rank:
        rank['stats'] = calculate_stats(positions, puntuazioak, rank, category)
    else:
        rank = {
            '_id': 'rank_{}_{}'.format(league, year),
            'stats': calculate_stats(positions, puntuazioak, rank, category)
        }
    print(json.dumps(rank['stats']))
    stats.set_sailkapen_orokorra(league, year, rank)


if __name__ == "__main__":
    league = sys.argv[1]
    year = sys.argv[2]
    category = sys.argv[3]
    update_stats(league, year, category)