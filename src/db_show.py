#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by Ludovic Lacoste <ludolacost@gmail.com>

'''
Created on 27 janv. 2015

@author: ludo6431
'''

import sqlite3

import matplotlib.pyplot as plt


if __name__ == '__main__':
    conn = sqlite3.connect("top100.db", detect_types=sqlite3.PARSE_DECLTYPES)
     
    c1 = conn.cursor()
    c2 = conn.cursor()
    plt.hold(True)

    for t in c1.execute('SELECT * FROM torrent'):
        print("torrent:", t[1])
        l = []
        for r in c2.execute('SELECT rank, dlcount, top_date FROM top_entry WHERE torrent_hash = ?', (t[0],)):
            print("  rank:", r[0], 'dlcount:', r[1])
            l.append(r)
        x = [r[2] for r in l]
        y = [r[1] for r in l]
        plt.plot(x, y)
 
    conn.close()

    plt.show()
