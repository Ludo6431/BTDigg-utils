#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by Ludovic Lacoste <ludolacost@gmail.com>

from enum import Enum
from html.parser import HTMLParser
from re import compile

class ParseState(Enum):
    Unknown = 0
    Init_StartTable = 1
    Init_StartTr = 2
    Init_StartTh = 3
    Init_StartB = 4
    Init_DataHash = 5
    Init_Header = 6
    Row = 7
    Row_DLCount = 8
    Row_Size = 9
    Row_FileCount = 10
    Row_FakeCount = 11
    Row_Name = 12
    
    @staticmethod
    def isParsingRow(s):
        if s == ParseState.Row or s == ParseState.Row_DLCount or s == ParseState.Row_Size or s == ParseState.Row_FileCount or s == ParseState.Row_FakeCount or s == ParseState.Row_Name:
            return 1
        return 0

class BtDiggTop100Entry:
    url = "http://btdigg.org"
    hash_extractor = compile(".*info_hash=([0-9a-fA-F]+)")
    
    def __str__(self):
        return "[rk=" +     str(self.rank) +\
            " ; dlcnt=" +   str(self.dlcount) +\
            " ; size=" +    str(self.size) +\
            " ; filecnt=" + str(self.filecount) +\
            " ; fakecnt=" + str(self.fakecount) +\
            " ; name=" +    str(self.name) +\
            " ; url=" +     str(self.url) + "]"
    
    def to_magnet(self):
        h = self.get_hash()
        return "magnet:?xt=urn:btih:" + h # + "&dn=" + escape(self.name) FIXME add escaped name

    def get_hash(self):
        p = BtDiggTop100Entry.hash_extractor.search(self.url)
        return p.group(1)

class BtDiggTop100Parser(HTMLParser):
    state = ParseState.Unknown
    verbose = 0
    curr_entry = None

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)

    def handle_row(self, e):
        pass

    def handle_starttag(self, tag, attrs):
        if self.verbose > 3:
            print("Encountered a start tag:", tag)
        
        if self.state == ParseState.Unknown and tag == "table":
            self.state = ParseState.Init_StartTable
        elif self.state == ParseState.Init_StartTable and tag == "tr":
            self.state = ParseState.Init_StartTr
        elif self.state == ParseState.Init_StartTr and tag == "th":
            self.state = ParseState.Init_StartTh
        elif self.state == ParseState.Init_StartTh and tag == "b":
            self.state = ParseState.Init_StartB
        elif self.state == ParseState.Init_Header:
            if tag == "tr":
                self.curr_entry = BtDiggTop100Entry()
                self.state = ParseState.Row
        elif ParseState.isParsingRow(self.state):
            if self.state == ParseState.Row_Name and tag == "a":
                d = dict(attrs)
                url = BtDiggTop100Entry.url + d["href"]
                
                if self.verbose > 2:
                    print("url      :", url)
                    
                self.curr_entry.url = url
        else:
            self.state = ParseState.Unknown

    def handle_endtag(self, tag):
        if self.verbose > 3:
            print("Encountered an end tag :", tag)

        if self.state == ParseState.Row and tag == "table":
            self.state = ParseState.Unknown

    def handle_data(self, data):
        if self.verbose > 3:
            print("Encountered some data  :", data)

        if self.state == ParseState.Init_StartB and data == "#":
            self.state = ParseState.Init_Header
        elif self.state == ParseState.Row:
            if self.verbose > 2:
                print("rank     :", data)
                
            self.curr_entry.rank = int(data)
            self.state = ParseState.Row_DLCount
        elif self.state == ParseState.Row_DLCount:
            if self.verbose > 2:
                print("dlcount  :", data)
                
            self.curr_entry.dlcount = int(data)
            self.state = ParseState.Row_Size
        elif self.state == ParseState.Row_Size:
            if self.verbose > 2:
                print("size    :", data)
            
            (sz, ml) = data.split('\xa0') # &nbsp;
            
            self.curr_entry.size = float(sz)
            if ml == "KB":
                self.curr_entry.size = self.curr_entry.size * 1000
            elif ml == "MB":
                self.curr_entry.size = self.curr_entry.size * 1000 * 1000
            elif ml == "GB":
                self.curr_entry.size = self.curr_entry.size * 1000 * 1000 * 1000
            elif ml == "TB":
                self.curr_entry.size = self.curr_entry.size * 1000 * 1000 * 1000 * 1000
            self.state = ParseState.Row_FileCount
        elif self.state == ParseState.Row_FileCount:
            if self.verbose > 2:
                print("filecount:", data)
                
            self.curr_entry.filecount = int(data)
            self.state = ParseState.Row_FakeCount
        elif self.state == ParseState.Row_FakeCount:
            if self.verbose > 2:
                print("fakecount:", data)
                
            self.curr_entry.fakecount = data
            self.state = ParseState.Row_Name
        elif self.state == ParseState.Row_Name:
            if self.verbose > 2:
                print("name     :", data)
                
            self.curr_entry.name = data
            if self.verbose > 1:
                print("entry:", self.curr_entry)
            self.handle_row(self.curr_entry)
            self.curr_entry = BtDiggTop100Entry()
            self.state = ParseState.Row

if __name__ == "__main__":
    from urllib.request import urlopen

    class BtDiggTop100Print(BtDiggTop100Parser):
        def handle_row(self, e):
            print(e)
            
    html = urlopen("http://btdigg.org/top100.html")
    html = str(html.read())
    parser = BtDiggTop100Print()
    parser.feed(html)
