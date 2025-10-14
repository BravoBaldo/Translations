# Documentazione


## Building

Il "building" [creazione] della documentazione è semplice.  Compilare la documentazione è semplice.

* Doxygen
* Python >= 3.10
* Compilatore C (gcc, msvc, clang, ecc...)

Una volta installato Python

    pip install -r requirements.txt

installerà tutti i pacchetti prerequisiti:

* Sphinx
* breathe
* imagesize
* importlib-metadata
* sphinx-rtd-theme
* sphinx-sitemap
* sphinxcontrib-applehelp
* sphinxcontrib-devhelp
* sphinxcontrib-htmlhelp
* sphinxcontrib-jsmath
* sphinxcontrib-qthelp
* sphinxcontrib-serializinghtml
* sphinxcontrib-mermaid==0.9.2
* sphinx-copybutton
* sphinx-design
* typing-extensions
* sphinx-reredirects
* dirsync
* furo
* accessible-pygments

Ora si è pronti per compilare la documentazione:

    python build.py html

oppure se si usa un sistema operativo simile a Unix:

    python3 build.py html

I file intermedi vengono normalmente preparati in `./docs/intermediate/` e la documentazione finale apparirà in `./docs/build/html/`.  (Entrambe queste directory possono essere sovrascritte utilizzando variabili d'ambiente.  Consultare la documentazione nel commento dell'intestazione in `build.py` per i dettagli).

Se l'elenco dei file sorgente del documento è cambiato (nomi o percorsi):

    python build.py clean html

Rimuoverà i vecchi file intermedi e di build e ne rigenererà di nuovi che corrispondono alla nuova struttura, eliminando i file orfani che altrimenti si creerebbero.

Per visualizzare un elenco delle opzioni disponibili:

    python build.py

Leggere il commento dell'intestazione in `build.py` per la documentazione dettagliata di ciascuna opzione.


## Per gli Sviluppatori

Una delle nostre politiche aziendali è ***TUTTO DEVE ESSERE DOCUMENTATO***.

Di seguito sono riportate alcune regole da seguire quando si aggiorna uno qualsiasi dei file `.rst` presenti nella directory `./docs/src/`.


### Come Nominare il File `.rst`

La struttura nella directory `./docs/src/` e i nomi dei file `.rst` determinano gli URL generati nell'output HTML.  Queste directory sono organizzate in modo da riflettere la natura del contenuto.  Esempio: i file `.rst` in `./docs/src/intro` contengono materiale introduttivo; il materiale di riferimento dettagliato non andrebbe inserito lì, bensì in una sottodirectory appropriata di `./docs/src/details/`.  Ci si aspetta che il contenuto e la posizione di tutti i nuovi documenti aggiunti siano in linea con questa struttura di directory e che siano posizionati e denominati in base al loro contenuto.  Inoltre, per essere collegato alla documentazione generata, la radice del nuovo nome file deve apparire in almeno una (normalmente *una sola*) direttiva `.. toctree::`, solitamente in un file `index.rst` nella directory in cui apparirà nell'indice (TOC) di quella pagina.

A parte questo, non ci sono restrizioni sui nomi file.  Il precedente collegamento dei nomi file ai link API generati è stato rimosso e sostituito da uno schema migliore.  A titolo esemplificativo, supponiamo che si stia creando (o migliorando) la documentazione relativa al tipo di dati `lv_scale_t` (uno dei widget LVGL): se si desidera che la logica di doc-build generi link appropriati alle pagine API LVGL, inserire una sezione API alla fine del documento (deve essere alla fine) in questo modo:

```rst
API
***
```

e poi, se si desidera che la logica di generazione dei link API generi collegamenti ipertestuali alle pagine API in base a una ***corrispondenza esatta di stringhe, con distinzione tra maiuscole e minuscole***, con simboli C specifici, è necessario aggiungere un commento reStructuredText utilizzando questa sintassi:

```rst
.. API equals: lv_scale_t, lv_scale_create
```

Ciò che segue i due punti è un elenco separato da virgole o spazi di simboli C esatti, documentati da qualche parte nella directory `lvgl/src/`.  Se l'elenco è lungo, può essere suddiviso in righe successive, sebbene le righe di continuazione debbano essere tutte rientrate allo stesso livello.  L'elenco termina con la prima riga vuota dopo questa pseudo-direttiva.

Se invece si desidera che la logica di generazione dei link API includa semplicemente link a codice che ***inizia con una stringa specifica***, utilizzare questa sintassi.  Il formato dell'elenco è lo stesso di `.. API equals:`:

```rst
.. API startswith: lv_scale, lv_obj_set_style
```

È anche possibile creare manualmente un collegamento alle pagine API, nel qual caso la logica di generazione dei collegamenti API rileverà che sono già stati aggiunti collegamenti e non li ripeterà.

```rst
:ref:`lv_scale_h`
```

Si noti che il punto prima di `h` viene sostituito con un trattino basso (`_`).  La denominazione di questo riferimento (`lv_scale_h`) genererà un collegamento ipertestuale alla documentazione estratta da Doxygen dal file `lvgl/src/widgets/scale/lv_scale.h`.


### Formato del Testo

Con i file `.md`, è importante consentire ai paragrafi di scorrere verso destra con un'unica riga lunga, in modo che, quando vengono formattati come file `.html`, i paragrafi vengano visualizzati a capo in base alla larghezza del browser.  Fortunatamente, questa limitazione non si verifica con i file reStructuredText (`.rst`).  [Sphinx](https://www.sphinx-doc.org/en/master/) e il suo [motore di analisi docutils](https://docutils.sourceforge.io/docs/) sottostante combinano opportunamente il testo raggruppato in un paragrafo appropriato con questo comportamento di ritorno a capo automatico.  Questo consente ai documenti di testo sorgente di essere ordinatamente mandati a capo, rendendoli più leggibili negli editor di testo e di codice che non dispongono di ampie finestre di modifica.  Quindi, si consiglia di mandare il testo a capo automatico entro la colonna 86 o più stretta.  Andare a capo *esattamente* alla colonna 86 non è importante, ma la leggibilità e la facilità di modifica lo sono.


### File index.rst

Se si crea una nuova directory, sarà necessario un file `index.rst` in quella directory e tale file indice deve essere puntato nel file `index.rst` che si trova nella directory padre.

Diamo un'occhiata al file `index.rst` che si trova nella directory `docs/src/details/common-widget-features/layouts`.

```
.. _layouts:
=======
Layouts
=======
.. toctree::
    :maxdepth: 2
    flex
    grid
```


Di seguito vengono spiegate le parti di questo file.

```
.. _layouts:      <=== Crea un link target esplicito
                  <=== Riga vuota -- importante!
=======
Layouts           <=== Titolo del documento, visibile nella documentazione
=======
                  <=== qualsiasi testo che introduca questo argomento e il Sommario sottostante
.. toctree::      <=== Direttiva del sommario
    :maxdepth: 2  <=== Uso interno e deve essere sempre impostato in questo modo
    flex          <=== percorso relativo ai file .rst che si trovano nella stessa directory
    grid
```

La prima riga serve a fornire un **link target** con un nome univoco a cui è possibile fare riferimento altrove nella documentazione.

    .. _{LINK NAME}:

Notare che `{LINK NAME}`:

- **deve** essere preceduto da un singolo carattere di sottolineatura,
- **deve** essere seguito da due punti e
- **deve** essere seguito da almeno una riga vuota affinché la logica di generazione dei documenti lo elabori correttamente.

Sostituire `{LINK NAME}` con un nome di link univoco tra tutti i documenti nella directory `./docs/src/`.  Può contenere più parole, se necessario per renderlo univoco o quando altrimenti appropriato per chiarezza.  Se vengono utilizzate più parole, possono essere separate da spazi singoli, trattini o caratteri di sottolineatura.  Qualunque cosa si usi, la stringa `{LINK NAME}` utilizzata per fare riferimento deve essere identica.  Le stringhe `{LINK NAME}` non distinguono tra maiuscole e minuscole.

Quel nome univoco viene quindi utilizzato per fornire un riferimento al collegamento in un'altra parte della documentazione utilizzando uno dei due formati seguenti.



##### Quando il "testo del link" deve essere un titolo o un'intestazione di sezione del documento di destinazione:

```reStructuredText
:ref:`{LINK NAME}`
```

Questo markup in linea (testo interpretato utilizzando il ruolo personalizzato `:ref:` definito da Sphinx) viene poi sostituito con un collegamento ipertestuale il cui "testo del link" è il nome dell'intestazione di sezione o del titolo del documento appena sotto il **link target**.  Per questo motivo, quando si utilizza questa sintassi, `{LINK NAME}` deve fare riferimento ai **link target** che si trovano appena sopra un titolo o un'intestazione di sezione.



##### Quando il "testo del link" deve essere qualcos'altro:

```reStructuredText
:ref:`altro testo del link <{LINK NAME}>`
```

Quest'ultima sintassi consente di inserire un **link target** in qualsiasi punto di un file .RST (non solo sopra un'intestazione) e di collegarsi ad esso utilizzando questa sintassi.

Nota: Quest'ultima sintassi è stata aggiunta o corretta di recente in Sphinx.  Non funzionava in Sphinx 7.3.7.




### Intestazioni di Sezione

Le [Intestazioni di Sezione](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#sections) vengono create sottolineando il titolo della sezione con un carattere di punteggiatura, lungo almeno quanto il testo.  Esempio:

```
Questo è un Titolo
******************
```

reStructuredText non impone alcun livello di titolo specifico assegnato a determinati caratteri, poiché la struttura è determinata dalla successione dei titoli.  Tuttavia, la politica della documentazione LVGL prevede l'utilizzo della seguente convenzione sui titoli:

```
======
Titolo
======
Capitolo
********
Sezione
-------
Sub Sezione
~~~~~~~~~~~
Sub Sub Sezione
^^^^^^^^^^^^^^^
Sub Sub Sub Sezione
'''''''''''''''''''
```

Essere coerenti in questo aiuta il parser Sphinx/docutils a formattare correttamente gli indici.

Si noti che la "sottolineatura" può essere più lunga del titolo, ma se è più corta, la logica di generazione della documentazione fallirà con un errore.

Per migliorare la leggibilità del file .RST:

- inserire 3 righe vuote sopra il titolo del secondo capitolo e dei successivi (vedi sopra) e
- inserire 2 righe vuote sopra i titoli delle sezioni sotto i capitoli.


### Blocchi di Codice

* Non utilizzare caratteri di tabulazione nei blocchi di codice.
* Ogni livello di rientro utilizza 4 spazi.
* Includere almeno 1 riga vuota dopo un blocco di codice.
* Deve esserci una riga vuota tra la direttiva del blocco di codice e il codice.
* `.. code-block::` è l'unica direttiva da utilizzare.  Si noti attentamente che, a differenza della direttiva **link target** sopra, questa direttiva ha 2 punti.  (Le uniche direttive reST e Sphinx valide con un solo punto sono le **link target**, come mostrato sopra). Non utilizzare le sole direttive `::`, `:code:` o `.. code:`.
* Per separare il codice in sezioni più facili da comprendere, è possibile farlo con una singola riga vuota.
* Per un'evidenziazione della sintassi appropriata al linguaggio nel blocco di codice, specificare il linguaggio dopo la direttiva.  Alcuni esempi sono:

  - `.. code-block:: c`,
  - `.. code-block:: cpp`,
  - `.. code-block:: python`,
  - `.. code-block:: shell`,
  - `.. code-block:: bash`,
  - `.. code-block:: kconfig`,
  - `.. code-block:: json`,
  - `.. code-block:: yaml`,
  - `.. code-block:: csharp` (o "cs"),
  - `.. code-block:: vb.net`,
  - `.. code-block:: dot` (graphviz),
  - `.. code-block:: html`,
  - `.. code-block:: css`,
  - `.. code-block:: xml`,
  - `.. code-block:: make`.

L'elenco completo dei lexer supportati è elencato nella [documentazione della Libreria Pygments](https://pygments.org/docs/lexers/).


### Elenchi Puntati

Per creare un elenco puntato, procedere come segue:

    - Descrizione del primo elemento
    - Per estendere l'elenco su più righe, rientrare le
      righe successive per allinearle al testo dell'elemento, in questo modo.
    - Per includere un blocco di codice sotto una voce di elenco,
      deve essere allineato con la voce di elenco in questo modo:
    
      .. code-block: python
                                 <=== la riga vuota qui è importante
          # questo è del codice
                                 <=== la riga vuota qui è importante
    - Per avere elenchi puntati nidificati, rientrare ogni
      nuovo livello per allinearlo alla voce di elenco padre in questo modo:
                                 <=== la riga vuota qui è importante
      - livello 2 elemento 1: testo
      - livello 2 elemento 2: testo
                                 <=== la riga vuota qui è importante
    - Ultimo elemento di elenco.  Si noti che l'elenco nidificato sopra riportato è preceduto
      e seguito da una riga vuota.

Tutti gli elenchi (inclusi quelli nidificati) **devono** essere preceduti e seguiti da almeno una riga vuota.  Questo è obbligatorio affinché la logica di generazione della documentazione possa elaborarla correttamente.


### Riferimento alla Documentazione API

Per fare riferimento a parti del codice LVGL dalla documentazione (in file .RST), sono disponibili direttive speciali per farlo:

    :cpp:func:`lv_init`
    :c:macro:`LV_USE_FLEX`
    :cpp:type:`lv_event_t`
    :cpp:enum:`lv_state_t`
    :cpp:enumerator:`LV_STATE_CHECKED`
    :cpp:struct:`lv_image_dsc_t`
    :cpp:union:`lv_style_value_t`

Esiste una direttiva speciale quando si desidera utilizzare un'espressione più complessa.  Ad esempio, quando si mostrano gli argomenti passati a una funzione.

    :cpp:expr:`lv_obj_set_layout(widget, LV_LAYOUT_FLEX)`
    :cpp:expr:`lv_slider_set_mode(slider, LV_SLIDER_MODE_...)`

Gli argomenti che sono espressioni (più di una parola) o contengono caratteri non alfanumerici causeranno il fallimento dello "interpreted-text" `:cpp:expr:`.  Esempi:

    :cpp:expr:`lv_obj_set_layout(widget, LV_LAYOUT_FLEX/GRID)`         <== argomento con > 1 parola
    :cpp:expr:`lv_obj_set_layout(widget, LV_LAYOUT_*)`                 <== asterisco
    :cpp:expr:`lv_obj_set_layout(*widget, LV_LAYOUT_FLEX)`             <== asterisco
    :cpp:expr:`lv_obj_set_layout((lv_obj_t *)widget, LV_LAYOUT_FLEX)`  <== cast
    :cpp:expr:`lv_obj_set_layout(&widget, LV_LAYOUT_FLEX);`            <== ampersand & "punto e virgola"
    :cpp:expr:`lv_obj_set_layout(widget, ...)`                         <== Puntini di sospensione solitari

Per esempi simili, usare semplicemente il markup letterale reStructuredText in questo modo:

    ``lv_obj_set_layout(widget, LV_LAYOUT_FLEX/GRID)``
    ``lv_obj_set_layout(widget, LV_LAYOUT_*)``
    ``lv_obj_set_layout(*widget, LV_LAYOUT_FLEX)``
    ``lv_obj_set_layout((lv_obj_t *)widget, LV_LAYOUT_FLEX)``
    ``lv_obj_set_layout(&widget, LV_LAYOUT_FLEX);``
    ``lv_obj_set_layout(widget, ...)``

