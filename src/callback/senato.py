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


import botogram
from datetime import datetime

from ..parser import affluence_senato, scrutinies_senato


def process(query, data, message):
    # TODO: Results from every electoral section
    affluence = affluence_senato.AffluenceView()
    scrutinies = scrutinies_senato.ScrutiniesView()

    keyboard = botogram.Buttons()
    keyboard[0].callback('🔄 Aggiorna', 'senato', 'update')
    keyboard[1].callback('🔙 Torna indietro', 'home')

    try:
        message.edit(
            "🗳 <b>Senato della Repubblica</b>"
            "{scrutinies}"
            "\n👥 <b>Votanti</b>: {voters}"
            "\n⚪️ <b>Bianche</b>: {white}"
            "\n✖️ <b>Nulle</b>: {null}"
            "\n⁉️ <b>Contestate</b>: {disputed}"
            "\n🕚 <b>Affluenza ore 23</b>: {affluence_23}%"
            "\n<i>Scrutinate {received_sections} sezioni su {sections}</i>"
            "\nUltimo aggiornamento: {last_update}"
            .format(
                scrutinies=scrutinies.format(),
                voters=scrutinies.voters,
                white=scrutinies.white_cards,
                null=scrutinies.null_cards,
                disputed=scrutinies.disputed_cards,
                affluence_23=affluence.elements[0].affluence_23,
                received_sections=scrutinies.received_sections,
                sections=scrutinies.sections,
#                sections_percentage=round(int(scrutinies.received_sections.replace('.', ''))/int(scrutinies.sections.replace('.','')),2),
                last_update=datetime.now().strftime("%H:%M %d/%m/%y")
            ),
            syntax="HTML", preview=False, attach=keyboard
        )
        if data == 'update':
            query.notify('✅ Informazioni aggiornate')
    except Exception as e:
        print(e)
        query.notify('❎ Le informazioni sono rimaste invariate', alert=True)
