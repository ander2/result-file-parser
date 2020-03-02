import couchdb
import os


user = os.environ['COUCH_USER']
passwd = os.environ['COUCH_PASS']
host = os.environ['COUCH_HOST']
couch = couchdb.Server('http://%s:%s@%s' % (user, passwd, host))
db = couch['test']


def get_estropadak(league, date):
    start = ["%s" % league, "%s" % date]
    end = ["%s" % league, "%sz" % date]
    rows = db.view('estropadak/all', None, startkey=start, endkey=end)
    estropada = None
    estropadak = []
    for row in rows:
        estropada = db.get(row.value)
        if estropada.get('puntuagarria', True) is False:
            continue
        if ('Playoff' not in estropada['izena'] and
            'play off' not in estropada['izena'].lower() and
            'play-off' not in estropada['izena'].lower()):
            estropadak.append(estropada)
    return estropadak


def get_sailkapen_orokorra(league, date, category):
    '''Get rank'''
    rank = {}
    try:
        rank = db.get('rank_{}_{}_{}'.format(league, date, category))
    except couchdb.http.ResourceNotFound:
        pass
    return rank


def set_sailkapen_orokorra(league, date, category, rank):
    '''Set rank'''
    key = 'rank_{}_{}_{}'.format(league, date, category)
    db[key] = rank