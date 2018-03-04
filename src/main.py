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
import redis
from datetime import datetime

from .callback import camera, senato
import config

bot = botogram.create(config.TOKEN)
r = redis.StrictRedis(host=config.REDIS_HOST,
                      port=config.REDIS_PORT,
                      db=config.REDIS_DB,
                      password=config.REDIS_PASSWORD)


@bot.before_processing
def analytics(message):
    rhash = 'user:' + str(message.sender.id)
    r.hset(rhash, 'id', message.sender.id)
    r.hset(rhash, 'username', message.sender.username)
    r.hset(rhash, 'last_access', str(datetime.now()))


@bot.command("start")
def start(message):
    keyboard = botogram.Buttons()
    keyboard[0].callback('🔴 Camera dei Deputati', 'camera')
    keyboard[1].callback('🔵 Senato della Repubblica', 'camera')
    keyboard[2].callback('ℹ️ Informazioni', 'info')
    message.chat.send(
        "<b>🗳 Elezioni politiche del 4 marzo 2018</b>"
        "\nBot <b>non ufficiale</b> per i dati sull'affluenza ed "
        "i risultati delle elezioni politiche di Camera e Senato"
        "\n\nℹ️ I dati sono aggiornati automaticamente dal "
        "<a href=\"http://elezioni.interno.gov.it/\">"
        "sito del Ministero dell'Interno</a>",
        syntax="HTML", preview=False, attach=keyboard,
    )


@bot.callback('home')
def home_callback(message):
    keyboard = botogram.Buttons()
    keyboard[0].callback('🔴 Camera dei Deputati', 'camera')
    keyboard[1].callback('🔵 Senato della Repubblica', 'senato')
    keyboard[2].callback('ℹ️ Informazioni', 'info')
    message.edit(
        "<b>🗳 Elezioni politiche del 4 marzo 2018</b>"
        "\nBot <b>non ufficiale</b> per i dati sull'affluenza ed "
        "i risultati delle elezioni politiche di Camera e Senato"
        "\n\nℹ️ I dati sono aggiornati automaticamente dal "
        "<a href=\"http://elezioni.interno.gov.it/\">"
        "sito del Ministero dell'Interno</a>",
        syntax="HTML", preview=False, attach=keyboard,
    )


@bot.callback("camera")
def camera_callback(query, data, message):
    camera.process(query, data, message)


@bot.callback("senato")
def senato_callback(query, data, message):
    senato.process(query, data, message)


@bot.callback("info")
def info_callback(_, __, message):
    keyboard = botogram.Buttons()
    keyboard[0].url("👤 Sviluppatore", "https://t.me/MarcoBuster")
    keyboard[0].url("👥 Gruppo di supporto", "https://t.me/MarcoBusterGroup")
    keyboard[1].url("🖥 Codice sorgente", "https://github.com/MarcoBuster/Elezioni4Marzo2018Bot")
    keyboard[2].callback("🔙 Torna indietro", "home")
    message.edit(
        "ℹ️ <b>Informazioni</b>"
        "\nIl bot è stato programmato da <a href=\"https://t.me/MarcoBuster\">Marco Aceti</a> (studente di informatica)"
        " per puro scopo didattico. È rilasciato sotto licenza libera per permettere lo studio del codice a tutti.",
        syntax="HTML", preview=False, attach=keyboard
    )
