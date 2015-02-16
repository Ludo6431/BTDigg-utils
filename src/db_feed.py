#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by Ludovic Lacoste <ludolacost@gmail.com>

import sqlite3
from sqlite3.dbapi2 import Timestamp
from urllib.request import urlopen,Request

from btdigg.top100parser import BtDiggTop100Parser


class ParserAddToDB(BtDiggTop100Parser):
    def __init__(self, ts, dbc):
        BtDiggTop100Parser.__init__(self)
    
        self.count = 0
        self.ts = ts
        self.dbc = dbc
        self.dbc.execute('INSERT INTO top VALUES(?, ?)', (self.ts, ""))
    
    def handle_row(self, e):
        self.count = self.count + 1
        self.dbc.execute('INSERT OR IGNORE INTO torrent(hash, name) VALUES (?, ?)', (e.get_hash(), e.name))
        self.dbc.execute('INSERT INTO top_entry(torrent_hash,top_date,rank,dlcount) VALUES (?, ?, ?, ?)', (e.get_hash(), self.ts, e.rank, e.dlcount))

if __name__ == '__main__':
    conn = sqlite3.connect("top100.db", detect_types=sqlite3.PARSE_DECLTYPES)
    d = Timestamp.utcnow()
    
    html = str(urlopen(Request("http://btdigg.org/top100.html", headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0"})).read())

    p = ParserAddToDB(d, conn.cursor())
    p.feed(html)
    
    if p.count != 100:
        print("Did not encountered the expected 100 results:", str(p.count))

    conn.commit()
    conn.close()
