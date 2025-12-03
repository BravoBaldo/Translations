# Documentazione


## Building

Il "building" [creazione] della documentazione è semplice.  Compilare la documentazione è semplice.

- Doxygen
- Python >= 3.10
- Compilatore C (gcc, msvc, clang, ecc...)

Una volta installato Python

    pip install -r requirements.txt

installerà tutti i pacchetti prerequisiti.

Per compilare la documentazione su Windows:

    python build.py html

Su Linux

    python3 build.py html

I file intermedi vengono normalmente preparati in `./docs/intermediate/` e la documentazione finale apparirà in `./docs/build/html/`.  Entrambe queste directory possono essere sovrascritte utilizzando variabili d'ambiente.  Per i dettagli, consultare la documentazione nel commento dell'intestazione `build.py`.

Se l'elenco dei file sorgenti del documento (inclusi i file `.h` nella directory `./src/`) è cambiato (nomi o path):

    python build.py clean

Rimuoverà i vecchi file intermedi e di build, eliminando i file orfani che altrimenti si creerebbero.

Per visualizzare un elenco delle opzioni disponibili:

    python build.py

Per una documentazione dettagliata su ciascuna opzione, leggere il commento dell'intestazione in `build.py`.



## Per gli Sviluppatori

Una delle nostre politiche aziendali è ***TUTTO DEVE ESSERE DOCUMENTATO***.

Di seguito sono riportate alcune regole da seguire quando si aggiorna uno qualsiasi dei file `.rst` presenti nella directory `./docs/src/`.



## Contenuto reStructuredText

La documentazione LVGL utilizza **reStructuredText** (reST), trasformato in HTML da Sphinx.  Di seguito si troverà un elenco abbastanza completo di riferimenti su come utilizzare reStructuredText:

| Riferimenti a Docutils (Fondamenti)) | Riferimenti a Sphinx (Cosa aggiunge Sphinx a Docutils) |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [Introduzione](https://docutils.sourceforge.io/docs/ref/rst/introduction.html) | [Configurazione](https://www.sphinx-doc.org/en/master/usage/configuration.html) |
| [Specifiche di Markup](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html) | [Direttive](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html) |
| [Specifiche di markup ∙ Tabelle](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#tables) | [Direttive ∙ Avvertenze](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#admonitions-messages-and-warnings) |
| [Specifiche di Markup ∙ Riferimenti di Sostituzione](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#substitution-references) | [Riferimenti](https://www.sphinx-doc.org/en/master/usage/referencing.html) |
| [Direttive](https://docutils.sourceforge.io/docs/ref/rst/directives.html) | [Ruoli del Testo Interpretato](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html) |
| [Ruoli del Testo Interpretato](https://docutils.sourceforge.io/docs/ref/rst/roles.html) | [Glossario](https://www.sphinx-doc.org/en/master/glossary.html) |
| [Guida Rapida](https://docutils.sourceforge.io/docs/user/rst/quickstart.html) | [Esempi del tema Furo](https://sphinx-themes.org/sample-sites/furo/) |
| [Esempi](https://docutils.sourceforge.io/docs/user/rst/demo.html) | [Pagina Riassuntiva](https://sphinx-themes.org/sample-sites/furo/kitchen-sink/) |
| [Guida Rapida](https://docutils.sourceforge.io/docs/user/rst/quickref.html) | [Galleria dei Temi Sphinx](https://sphinx-themes.org/) |

Se si preferisce imparare tramite esempi, gli[Esempi Furo-theme](https://sphinx-themes.org/sample-sites/furo/) e in particolare la "[Kitchen Sink Page](https://sphinx-themes.org/sample-sites/furo/kitchen-sink/)" [Pagina Riassuntiva] sono ottime risorse.  Visualizzare il file sorgente `.rst` che ha generato quella pagina cliccando sull'icona a forma di "occhio" in cima alla pagina.

Nota: le intestazioni di sezione in queste pagine utilizzano una convenzione diversa da quella presentata di seguito.  Per la documentazione LVGL, utilizzare la [convenzione per le intestazioni di sezione presentata di seguito](https://github.com/lvgl/lvgl/tree/master/docs#section-headings).



### Formato del Testo

Andare a capo intorno alla colonna 86 o meno.  Non è importante che il testo vada *esattamente* a capo alla colonna 86, ma lo sono la leggibilità e la facilità di modifica.

Rientrare utilizzando 4 spazi (non caratteri di tabulazione).  Questo vale anche per i blocchi di codice.



### File index.rst

Se si crea una nuova directory, sarà necessario un file `index.rst` in quella directory e tale file indice deve essere puntato nel file `index.rst` che si trova nella directory padre.

Diamo un'occhiata al file `index.rst` che si trova nella directory `docs/src/common-widget-features/layouts`.

```rst
.. _layouts:
=======
Layouts
=======
.. toctree::
    :maxdepth: 2
    panoramica
    flex
    grid
```


Spiegazione:

```rst
.. _layouts:      <=== Crea un link target esplicito
                  <=== Riga vuota -- importante!
=======
Layouts           <=== Titolo del documento, visibile nella documentazione
=======
                  <=== qualsiasi testo che introduca questo argomento e il Sommario sottostante
.. toctree::      <=== Direttiva del sommario
    :maxdepth: 2  <=== Uso interno e deve essere sempre impostato in questo modo
    panoramica      <=== path relativo ai file .rst situati nella stessa directory
    flex
    grid
```



### Intestazioni di Sezione

Le Intestazioni di sezione vengono create sottolineando il titolo della sezione con un carattere di punteggiatura, lungo almeno quanto il testo.  Esempio:

```
Questo è un Titolo
******************
```

Utilizzare queste convenzioni per le intestazioni delle sezioni nella documentazione LVGL:

```
==============
Document Title
==============
Section
*******
Sub Section
-----------
Sub Sub Section
~~~~~~~~~~~~~~~
```

1.  ``====``, ``****``, ``----`` sono consigliati.
2.  ``~~~~`` solo se realmente necessario.

Essere coerenti in questo aiuta il parser reST a formattare correttamente gli indici.

Per una migliore leggibilità negli editor di testo:

- inserire 3 righe vuote sopra il secondo e i successivi titoli di "Sezione" (vedere sopra),
- 2 righe vuote sopra le intestazioni di "Sottosezione" e
- almeno 1 riga vuota sopra tutte le intestazioni di sezione di livello inferiore.



### Corsivo, Grassetto e Sottolineatura

Enfasi con `*corsivo*`.  Enfasi con `**grassetto**`.

Normalmente, la sottolineatura e la combinazione di questi stili di testo non sono possibili in reStructuredText.  Tuttavia, la documentazione LVGL fornisce una soluzione alternativa utilizzando gli <u>Interpreted Text Roles</u>.  Da ricordare che i nomi degli "Interpreted Text Role" combinano le lettere `i`, `b` e `u` per fornire la combinazione desiderata.  Sono supportate tutte le possibili permutazioni di queste lettere, quindi non si deve ricordare quale sequenza funziona.  Esempi:  ``:u:`underline``` [sottolineato], ``:ub:`underline and bold``` [sottolineato e grassetto], ``:bi:`bold italic```[grassetto corsivo].



### Blocchi di Codice

* Rientrare utilizzando 4 spazi (non caratteri di tabulazione).
* Includere almeno 1 riga vuota dopo un blocco di codice.
* Deve esserci una riga vuota tra la direttiva del blocco di codice e il codice.
* `.. code-block::` è l'unica direttiva da utilizzare.  Non utilizzare solo `::`, `:code:` o `.. code::`.
* Specificare il linguaggio dopo la direttiva per un'evidenziazione sintattica appropriata.  Esempi:

  - `.. code-block:: c`,
  - `.. code-block:: cpp`,
  - `.. code-block:: python`,
  - `.. code-block:: shell`,
  - `.. code-block:: bash`,
  - `.. code-block:: kconfig`,
  - `.. code-block:: json`,
  - `.. code-block:: yaml`,
  - `.. code-block:: dot` (graphviz),
  - `.. code-block:: html`,
  - `.. code-block:: css`,
  - `.. code-block:: xml`,
  - `.. code-block:: make`.

Per maggiori dettagli, vedere [il set completo dei lexer dei codici supportati](https://pygments.org/docs/lexers/).



### Elenchi Puntati

```rst
- Descrizione del primo elemento
- Per estendere l'elenco su più righe, rientrare le
  righe successive per allinearle al testo dell'elemento, in questo modo.
- Per includere più paragrafi e/o blocchi di codice sotto una
  voce di elenco, è necessario allinearli alla voce di elenco in questo modo:
  Secondo paragrafo.
  .. code-block: python
                             <=== la riga vuota qui è importante
      # Qui il codice Python
                             <=== la riga vuota qui è importante
- Per avere elenchi puntati nidificati, rientrare ogni
  nuovo livello per allinearlo alla voce di elenco padre in questo modo:
                             <=== la riga vuota qui è importante
  - livello 2 elemento 1: testo
  - livello 2 elemento 2: testo
                             <=== la riga vuota qui è importante
- Ultimo elemento di elenco.  Si noti che l'elenco nidificato sopra riportato è preceduto
  e seguito da una riga vuota.
```

Tutti gli elenchi (inclusi quelli nidificati) **devono** essere preceduti e seguiti da almeno una riga vuota affinché il parser reST li elabori correttamente.



### Link Esterni

Gli URL vengono convertiti automaticamente in link. Ad esempio `Visitare https://lvgl.io`.

Per aggiungere link con testo personalizzato, utilizzare

```rst
Visitare `Il Mio Sito Web <https://pro.lvgl.io>`__.
```

Se un link esterno verrà utilizzato su più pagine:

- Aggiungerlo a `./docs/src/include/external_links.txt` se non è già presente.  Esempio:

  ```rst
  .. _LVGL Pro:  https://pro.lvgl.io
  ```

- `.. includere:  /include/external_links.txt` una volta all'inizio di ogni file `.rst` che lo utilizza.

- Usarlo per nome nel testo:

  ```rst
  Per ulteriori dettagli, vedere `LVGL Pro`_.
  ```

  Nota: le virgolette inverse non sono necessarie se il nome non contiene spazi.



### Link Interni

Aggiungere un link di destinazione (àncora) prima dell'intestazione o del paragrafo a cui verrà collegato:

```rst
.. _unique_anchor_name:
My Heading
**********
```

`unique_anchor_name` deve essere univoco in tutti i file `.rst` in `./docs/src/`.

Fare riferimento al link (àncora) tramite:

```rst
Cliccare :ref:`qui <unique_anchor_name>` per maggiori dettagli.
```

Risultato:  "Cliccare **_qui_** per maggiori dettagli."

Oppure usare il testo dell'intestazione come testo del link:

```rst
Cliccare :ref:`unique_anchor_name` per maggiori dettagli.
```

Risultato:  "Cliccare **_My Heading_** per maggiori dettagli.."

`unique_anchor_name` può apparire anche in punti diversi da prima di un'intestazione, ma in tal caso è necessario fornire un testo personalizzato per il link (come "qui" nel primo esempio sopra).



### Restringimento di Tabelle

La sintassi di reStructuredText per la creazione di tabelle è disponibile negli [esempi reST](https://sphinx-themes.org/sample-sites/furo/kitchen-sink/tables/) citati sopra.  (Cliccare sull'icona "occhio" per visualizzare il file sorgente).

Tabelle molto lunghe o molto larghe possono essere difficili da leggere e utilizzare.  Per ridurle e renderle più leggibili e utilizzabili, spostare la tabella esistente sotto una direttiva `.. container:: tighter-table-N` (`N` = cifre da 1 a 7, dove 7 è la più stretta) e indentarla per renderla "il contenuto" della direttiva.  Esempio:

```rst
.. container:: tighter-table-3
    +-----------+--------------+--------------+--------+
    | Heading 1 | Heading 2    | Heading 3    | Hdg 4  |
    +===========+==============+==============+========+
    | row 1 c 1 | row 1 col 3  | row 1 col 3  | r1 c4  |
    +-----------+--------------+--------------+--------+
    | row 2 c 1 | row 2 col 3  | row 2 col 3  | r2 c4  |
    +-----------+--------------+--------------+--------+
    | row 3 c 1 | row 3 col 3  | row 3 col 3  | r3 c4  |
    +-----------+--------------+--------------+--------+
```

This works for all types of tables.



### Simboli Speciali

Poiché non tutti dispongono di editor che gestiscono bene i caratteri Unicode, si prega di utilizzare le sostituzioni reST per inserire caratteri speciali nella documentazione.  Un elenco dei simboli speciali più comunemente utilizzati è disponibile in `./docs/src/include/substitutions.txt`.  Per utilizzarne uno, aggiungere questa riga all'inizio del file `.rst`, se non è già presente:

```rst
.. include:: /include/substitutions.txt
```

Poi, , qualsiasi di queste sostituzioni può essere utilizzata nel file `.rst`.  Esempio:

```rst
La temperatura esterna è di 20\ |deg|\ C.
```

Risultato:  "La temperatura esterna è di 20°C."

Gli spazi che circondano le sostituzioni *sono necessari per il parsing*, ma quando è necessario rimuoverli nell'output (come nell'esempio precedente), è possibile farlo utilizzando il carattere di escape `\`.  Eccezione: il file `substitutions.txt` contiene 3 definizioni di sostituzione contrassegnate con l'opzione `:trim:`, poiché il loro utilizzo rimuove *sempre* questi spazi nell'output.  Queste non necessitano di questo escape:

- `|nbsp|` (spazio unificatore),
- `|shy|` (trattino morbido) e
- `|nbhyph|` (trattino unificatore utilizzato nei titoli e nei nomi ufficiali)

Se c'è bisogno di una sostituzione che non è già presente in `substitutions.txt`, aggiungerla.



### Riferimento alla Documentazione API

Utilizzando quanto segue si generano link alla documentazione API su cui il lettore può cliccare direttamente nel testo.

#### Espressioni di Codice In-Line

Utilizzare i seguenti "Interpreted Text Roles" nel testo per includere codice C in-line che rimanda alla documentazione relativa a quel simbolo, quando disponibile:

    :cpp:func:`lv_init`   (notare che non ci sono parentesi dopo il nome della funzione)
    :c:macro:`LV_USE_FLEX`
    :cpp:type:`lv_event_t`
    :cpp:enum:`lv_state_t`
    :cpp:enumerator:`LV_STATE_CHECKED`
    :cpp:struct:`lv_image_dsc_t`
    :cpp:union:`lv_style_value_t`

#### Espressioni Più Complesse

Utilizzare lo "Interpreted Text Role" `:cpp:expr:` per espressioni più complesse, ad esempio quando si visualizzano gli argomenti passati a una funzione.

    :cpp:expr:`lv_obj_set_layout(widget, LV_LAYOUT_FLEX)`
    :cpp:expr:`lv_slider_set_mode(slider, LV_SLIDER_MODE_...)`

Gli argomenti che contengono più di una parola o caratteri non alfanumerici causeranno il fallimento dell'interpreted-text `:cpp:expr:`.  Esempi:

| Espressione | Causa dell'Errore |
| ------------------------------------------------------------ | ---------------------- |
| :cpp:expr:\`lv_obj_set_layout(widget, LV_LAYOUT_FLEX/GRID)\` | argomento con > 1 parola |
| :cpp:expr:\`lv_obj_set_layout(widget, LV_LAYOUT_*)\` | asterisco |
| :cpp:expr:\`lv_obj_set_layout(*widget, LV_LAYOUT_FLEX)\` | asterisco |
| :cpp:expr:\`lv_obj_set_layout((lv_obj_t *)widget, LV_LAYOUT_FLEX)\` | cast |
| :cpp:expr:\`lv_obj_set_layout(&widget, LV_LAYOUT_FLEX);\` | punto e virgola |
| :cpp:expr:\`lv_obj_set_layout(widget, ...)\` | singoli puntini di sospensione |

Per esempi simili, usare semplicemente il markup letterale reStructuredText in questo modo:

```rst
``lv_obj_set_layout(widget, LV_LAYOUT_FLEX/GRID)``
``lv_obj_set_layout(widget, LV_LAYOUT_*)``
``lv_obj_set_layout(*widget, LV_LAYOUT_FLEX)``
``lv_obj_set_layout((lv_obj_t *)widget, LV_LAYOUT_FLEX)``
``lv_obj_set_layout(&widget, LV_LAYOUT_FLEX);``
``lv_obj_set_layout(widget, ...)``
```

#### Fornire Link alle Pagine API

Per creare un link a una o più pagine API, impostare una sezione alla fine del proprio file `.rst` simile a questa e utilizzare uno o entrambi i tipi di pseudo-direttive ``.. API `` seguenti:

```rst
API
***
.. API equals: lv_scale_t, lv_scale_create
.. API startswith: lv_scale, lv_obj_set_style
```

L'elenco dei simboli (o prefissi) può essere separato da virgole o spazi e può essere inserito nelle righe di testo successive, purché siano indentate.  Una riga vuota dopo ogni elenco termina l'elenco stesso.

La logica di generazione delle pagine API aggiungerà al massimo 1 link a ciascuna pagina di documentazione API contenente simboli corrispondenti.  I link sono all'intera pagina API, non ai simboli  Lo scopo è fornire al lettore i link alle pagine API applicabili.  I link diretti al codice (ad esempio la documentazione delle funzioni) vengono realizzati utilizzando le "In-Line Code Expression" documentate sopra.
