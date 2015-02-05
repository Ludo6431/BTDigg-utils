'''
Created on 27 janv. 2015

@author: ludo6431
'''

import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect("top100.db", detect_types=sqlite3.PARSE_DECLTYPES)
    
    c1 = conn.cursor()
    c2 = conn.cursor()
    
    for t in c1.execute('SELECT * FROM torrent'):
        print("torrent:", t[1])
        for r in c2.execute('SELECT rank, dlcount FROM top_entry WHERE torrent_hash = ?', (t[0],)):
            print("  rank:", r[0], 'dlcount:', r[1])

    conn.close()
