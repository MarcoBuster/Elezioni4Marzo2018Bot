# Copyright (c) 2018 Marco Aceti <mail@marcoaceti.it>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import json
import requests

from ..constants import *


class AffluenceElement:
    def __init__(self, raw):
        self.level = raw['livello']
        self.body = raw['ente']
        self.href = raw['href']
        self.received_municipalities = raw['comuni_perv']
        self.municipalities = raw['comuni']
        self.affluence_23 = raw['perc_ore23']
        self.previous_affluence_23 = raw['percprec_ore23']

    def click(self):
        return AffluenceView(section_href=self.href)


class AffluenceView:
    def __init__(self, section_href='votantiSI'):
        self.section_href = section_href
        self.url = HOST + '/votanti/votanti20180304/{href}'.format(href=self.section_href)
        self.raw, self.elements, self.notes = {}, [], []
        self.reload()
        self.status = self.raw['status']

        for note in self.raw['note']:
            if note['testo'] != "":
                self.notes.append(note['testo'])

        for element in self.raw['righe']:
            self.elements.append(AffluenceElement(element))

    def reload(self):
        r = requests.get(self.url, headers=HEADERS)
        try:
            self.raw = r.json()
        except json.decoder.JSONDecodeError:
            raise
