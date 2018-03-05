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
import redis
import config
#import requests
#import requests_cache
#requests_cache.install_cache('sc', expire_after=60)

from ..constants import *


class ScrutiniesRow:
    def __init__(self, raw):
        self.type = raw['tipo_riga']
        self.candidate = raw['cand_descr_riga']
        self.party = raw['descr_lista']
        self.votes = raw['voti']
        self.percentage = raw['perc']
        self.eletto = raw['eletto']
        self.list_percentage = raw['perc_voti_liste']
        self.seats = raw['seggi']


class ScrutiniesView:
    def __init__(self, section_id=''):
        self.section_id = section_id
        self.url = HOST + '/politiche/camera20180304/scrutiniCI{href}'.format(href=self.section_id)
        self.raw, self.rows, self.notes = {}, [], []
        self.reload()
        self.status = self.raw['status']
        self.electors = self.raw['elettori']
        self.voters = self.raw['votanti']
        self.voters_percentage = self.raw['perc_votanti']
        self.sections = self.raw['sezioni']
        self.received_sections = self.raw['sezioni_perv']
        self.white_cards = self.raw['sk_bianche']
        self.null_cards = self.raw['sk_nulle']
        self.disputed_cards = self.raw['sk_contestate']

        for note in self.raw['note']:
            if note['testo'] != "":
                self.notes.append(note['testo'])

        for row in self.raw['righe']:
            self.rows.append(ScrutiniesRow(row))

    def reload(self):
        re = redis.StrictRedis(host=config.REDIS_HOST,
                               port=config.REDIS_PORT,
                               db=config.REDIS_DB,
                               password=config.REDIS_PASSWORD)
        try:
            self.raw = json.loads(re.hget("dati","scrutiniescam").decode("utf-8"))
        except json.decoder.JSONDecodeError:
            raise

    def format(self):
        text = ''
        index = 0
        for row in self.rows:
            if row.type == 'CA':
                text += (
                    '\n➖➖ 👤 <b>{candidate}</b>'
                    '\n{votes} voti, ({percentage}%)'
                    .format(
                        candidate=row.cand_descr_riga,
                        votes=row.votes if row.votes else '-',
                        percentage=row.percentage if row.votes else '-')
                )
            elif row.type == 'LI':
                text += (
                    '\n🔹 <b>{name}</b>'
                    '\n{votes} voti ({percentage}%); {seats} seggi'
                    .format(
                            name=row.party.title(),
                            votes=row.votes if row.votes else '-',
                            percentage=row.percentage if row.percentage else '-',
                            seats=row.seats if row.seats else '-')
                )
            elif row.type == 'CU':
                parties = 0
                for _row in self.rows[index + 1:]:
                    if _row.type == 'LI':
                        parties += 1
                    if _row.type == 'CU':
                        break
                if parties > 1:
                    text += (
                        '\n➖➖ <b>Coalizione</b>'
                        '\n{votes} voti, ({percentage}%)'
                        .format(
                            votes=row.votes if row.votes else '-',
                            percentage=row.percentage if row.votes else '-'
                        )
                    )
            elif row.type == 'XX':
                text += '\n'

            index += 1

        return text
