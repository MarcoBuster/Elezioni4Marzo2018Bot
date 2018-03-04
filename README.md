# Elezioni 4 Marzo 2018 Bot
**Elezioni 4 Marzo 2018** è un **bot per Telegram** per ricevere i risultati dello spoglio delle schede elettorali delle 
**Elezioni politiche del 4 marzo 2018**

### Funzionalità e utilizzo
Il bot utilizza le API interne di [elezioni.interno.gov.it][Interno]

### Installazione
Per installare questo bot sulla tua macchina, esegui:

    $ git clone https://www.github.com/MarcoBuster/ReferendumCostituzionaleBot.git && cd ReferendumCostituzionaleBot 
    $ python3 -m pip install -r requirements.txt
    $ python3 start.py

> Attenzione! Modificare il file di configurazione `config.sample.py` e rinominarlo in `config.py`

### Licenza e crediti
Il bot è stato programmato da [Marco Aceti][Marco] e rilasciato sotto licenza [MIT][MIT], raggiungibile su Telegram tramite [questo indirizzo][Bot].

[Bot]: https://t.me/Elezioni4Marzo2018Bot
[Marco]: https://www.github.com/MarcoBuster
[MIT]: https://opensource.org/licenses/MIT
[Interno]: http://elezioni.interno.gov.it
