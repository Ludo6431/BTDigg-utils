#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by Ludovic Lacoste <ludolacost@gmail.com>

from enum import Enum
from html.parser import HTMLParser
from urllib.request import urlopen

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
    Row_Size1 = 9
    Row_Size2 = 10
    Row_FileCount = 11
    Row_FakeCount = 12
    Row_Name = 13
    
    def isParsingRow(s):
        if s == ParseState.Row or s == ParseState.Row_DLCount or s == ParseState.Row_Size1 or s == ParseState.Row_Size2 or s == ParseState.Row_FileCount or s == ParseState.Row_FakeCount or s == ParseState.Row_Name:
            return 1
        return 0

class BtDiggTop100Entry:
    rank = -1
    dlcount = -1
    size = -1
    filecount = -1
    fakecount = -1
    name = ""
    
    def __str__(self):
        return "[rk=" + str(self.rank) + " ; dlcnt=" + str(self.dlcount) + " ; size=" + str(self.size) + " ; filecnt=" + str(self.filecount) + " ; fakecnt=" + str(self.fakecount) + " ; name=" + str(self.name) + "]"
    
class BtDiggTop100Parser(HTMLParser):
    state = ParseState.Unknown
    verbose = 0
    curr_entry = None

    def handle_row(self, r):
        pass

    def handle_starttag(self, tag, attrs):
        if self.verbose > 2:
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
            pass
        else:
            self.state = ParseState.Unknown

    def handle_endtag(self, tag):
        if self.verbose > 2:
            print("Encountered an end tag :", tag)

        if self.state == ParseState.Row and tag == "table":
            self.state = ParseState.Unknown

    def handle_data(self, data):
        if self.verbose > 2:
            print("Encountered some data  :", data)

        if self.state == ParseState.Init_StartB and data == "#":
            self.state = ParseState.Init_Header
        elif self.state == ParseState.Row:
            if self.verbose > 1:
                print("rank     :", data)
            self.curr_entry.rank = int(data)
            self.state = ParseState.Row_DLCount
        elif self.state == ParseState.Row_DLCount:
            if self.verbose > 1:
                print("dlcount  :", data)
            self.curr_entry.dlcount = int(data)
            self.state = ParseState.Row_Size1
        elif self.state == ParseState.Row_Size1:
            if self.verbose > 1:
                print("size1    :", data)
            self.curr_entry.size = float(data)
            self.state = ParseState.Row_Size2
        elif self.state == ParseState.Row_Size2:
            if self.verbose > 1:
                print("size2    :", data)
            if data == "KB":
                self.curr_entry.size = self.curr_entry.size * 1000
            elif data == "MB":
                self.curr_entry.size = self.curr_entry.size * 1000 * 1000
            elif data == "GB":
                self.curr_entry.size = self.curr_entry.size * 1000 * 1000 * 1000
            elif data == "TB":
                self.curr_entry.size = self.curr_entry.size * 1000 * 1000 * 1000 * 1000
            self.state = ParseState.Row_FileCount
        elif self.state == ParseState.Row_FileCount:
            if self.verbose > 1:
                print("filecount:", data)
            self.curr_entry.filecount = int(data)
            self.state = ParseState.Row_FakeCount
        elif self.state == ParseState.Row_FakeCount:
            if self.verbose > 1:
                print("fakecount:", data)
            self.curr_entry.fakecount = data
            self.state = ParseState.Row_Name
        elif self.state == ParseState.Row_Name:
            if self.verbose > 1:
                print("name     :", data)
            self.curr_entry.name = data
            print("entry:", self.curr_entry)
            self.curr_entry = BtDiggTop100Entry()
            self.state = ParseState.Row

html = urlopen("http://btdigg.org/top100.html")
html = str(html.read())

# print('html=', html)

parser = BtDiggTop100Parser()
parser.feed(html)
