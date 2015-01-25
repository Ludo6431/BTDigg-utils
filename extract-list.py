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

class BtDiggTop100Parser(HTMLParser):
    state = ParseState.Unknown
    verbose = 0

    def handle_row(self, r):
        pass

    def handle_starttag(self, tag, attrs):
        if self.verbose > 1:
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
                self.state = ParseState.Row
        elif self.state == ParseState.Row:
            pass
        else:
            self.state = ParseState.Unknown

    def handle_endtag(self, tag):
        if self.verbose > 1:
            print("Encountered an end tag :", tag)
        
        if self.state == ParseState.Row and tag == "table":
            self.state = ParseState.Unknown

    def handle_data(self, data):
        if self.verbose > 1:
            print("Encountered some data  :", data)
        
        if self.state == ParseState.Init_StartB and data == "#":
            self.state = ParseState.Init_Header
        elif self.state == ParseState.Row:
            print("data:", data)

html = urlopen("http://btdigg.org/top100.html")
html = str(html.read())

# print('html=', html)

parser = BtDiggTop100Parser()
parser.feed(html)
