# Domande frequenti su gMock Legacy

### Quando chiamo un metodo sul mio oggetto mock, viene invece richiamato il metodo per l'oggetto reale. Qual è il problema?

Affinché un metodo possa essere mock-ato, deve essere *virtual*, a meno che non si utilizzi la [high-perf dependency injection technique](gmock_cook_book.md#MockingNonVirtualMethods).

### Posso mock-are una funzione variadica?

Non è possibile mock -are una funzione variadica (ovvero una funzione che accetta argomenti con puntini di sospensione (`...`)) direttamente in gMock.

Il problema è che, in generale, non c'è *nessun modo* per un oggetto mock di sapere quanti argomenti vengono passati al metodo variadico e quali sono i tipi degli argomenti. Solo l'*autore della classe base* conosce il protocollo e non possiamo guardargli nella testa.

Pertanto, per simulare una funzione del genere, l'*utente* deve insegnare all'oggetto mock-ato come calcolare il numero di argomenti e i loro tipi. Un modo per farlo è fornire versioni sovraccaricate [overloaded] della funzione.

Gli argomenti con i puntini di sospensione sono ereditati dal C e non sono realmente una funzionalità del C++. Non sono sicuri da usare e non funzionano con argomenti che hanno costruttori o distruttori. Pertanto consigliamo di evitarli il più possibile in C++.

### MSVC mi dà un warning C4301 o C4373 quando definisco un metodo mock con un parametro const. Perché?

Se lo compili utilizzando Microsoft Visual C++ 2005 SP1:

```cpp
class Foo {
  ...
  virtual void Bar(const int i) = 0;
};
class MockFoo : public Foo {
  ...
  MOCK_METHOD(void, Bar, (const int i), (override));
};

```

Si potrebbe ricevere il seguente warning:

```shell
warning C4301: 'MockFoo::Bar': overriding virtual function only differs from 'Foo::Bar' by const/volatile qualifier

```

Questo è un bug di MSVC. Lo stesso codice viene compilato bene con gcc, ad esempio. Se si usa Visual C++ 2008 SP1, si riceverà il warning:

```shell
warning C4373: 'MockFoo::Bar': virtual function overrides 'Foo::Bar', previous versions of the compiler did not override when parameters only differed by const/volatile qualifiers

```

In C++, se si *dichiara* una funzione con un parametro `const`, il modificatore `const` viene ignorato. Pertanto, la classe base `Foo` sopra è equivalente a:

```cpp
class Foo {
  ...
  virtual void Bar(int i) = 0;  // int o const int?  Non fa differenza.
};

```

Infatti, si può *dichiarare* `Bar()` con un parametro `int` e definirlo con un parametro `const int`. Il compilatore li abbinerà comunque.

Poiché la creazione di un parametro `const` non ha significato nella dichiarazione del metodo, consigliamo di rimuoverlo sia in `Foo` che in `MockFoo`. Ciò dovrebbe risolvere il bug VC.

Si noti che qui stiamo parlando del modificatore *top-level* `const`. Se il parametro della funzione viene passato tramite puntatore o riferimento, dichiarare il puntato o il riferito come `const` ha ancora senso. Ad esempio, le due dichiarazioni seguenti *non* sono equivalenti:

```cpp
void Bar(int* p);         // Neither p nor *p is const.
void Bar(const int* p);  // p is not const, but *p is.

```

### Non riesco a capire perché gMock pensi che le mie aspettative non siano soddisfatte. Cosa dovrei fare?

Potresti voler eseguire il test con `--gmock_verbose=info`. Questo flag consente a gMock di stampare un trace per ogni chiamata di funzione mock che riceve. Studiando il trace, si otterranno informazioni sul motivo per cui le aspettative [expectation] impostate non vengono soddisfatte.

Se si vede il messaggio "The mock function has no default action set, and its return type has no default value set.", provare ad [aggiungere un'azione di default](gmock_cheat_sheet.md#OnCall). A causa di un problema noto, le chiamate impreviste ai mock senza azioni di default non stampano un confronto dettagliato tra gli argomenti effettivi e quelli previsti.

### Il mio programma è crashato e `ScopedMockLog` ha inviato tonnellate di messaggi. È un bug di gMock?

gMock e `ScopedMockLog` probabilmente stanno facendo la cosa giusta in questo caso.

Quando un test va in crash, l'handler del segnale di errore tenterà di loggare molte informazioni (il trace dello stack e la mappa degli indirizzi, ad esempio). I messaggi sono complessi se sono presenti molti thread con stack profondi. Quando `ScopedMockLog` intercetta questi messaggi e rileva che non corrispondono ad alcuna aspettativa, stampa un errore per ciascuno di essi.

Si può imparare a ignorare gli errori oppure si possono riscrivere le aspettative per rendere il test più robusto, ad esempio aggiungendo qualcosa come:

```cpp
using ::testing::AnyNumber;
using ::testing::Not;
...
  // Ignora qualsiasi log non generato da noi.
  EXPECT_CALL(log, Log(_, Not(EndsWith("/my_file.cc")), _))
      .Times(AnyNumber());

```

### Come posso asserire che una funzione non viene MAI chiamata?

```cpp
using ::testing::_;
...
  EXPECT_CALL(foo, Bar(_))
      .Times(0);

```

### Ho un test fallito in cui gMock mi dice DUE VOLTE che una particolare expectation non è soddisfatta. Non è ridondante?

Quando gMock rileva un errore, stampa le informazioni rilevanti (gli argomenti della funzione mock, lo stato delle expectation rilevanti, ecc.) per aiutare l'utente a eseguire il debug.
Se viene rilevato un altro errore, gMock farà lo stesso, inclusa la stampa dello stato delle expectation rilevanti.

A volte lo stato di una expectation non cambia tra due fallimenti e si vedrà la stessa descrizione dello stato due volte. Tuttavia *non* sono ridondanti, poiché si riferiscono a *diversi momenti nel tempo*. Il fatto che siano la stessa cosa *è* un'informazione interessante.

### Ho un errore sul check dell'heap quando utilizzo un oggetto mock, ma usando un oggetto reale va bene. Cosa può esserci di sbagliato?

La classe (si spera un'interfaccia pura) che si sta mock-ando ha un distruttore virtuale?

Ogni volta che si deriva da una classe base, assicurarsi che il suo distruttore sia virtuale.
Altrimenti Accadranno Cose Brutte. Si consideri il seguente codice:

```cpp
class Base {
 public:
  // Non virtual, ma dovrebbe esserlo.
  ~Base() { ... }
  ...
};
class Derived : public Base {
 public:
  ...
 private:
  std::string value_;
};
...
  Base* p = new Derived;
  ...
  delete p;  // Sorpresa! verrà chiamato ~Base(), ma non ~Derived()
                 // - value_ viene perso [leak].

```

Cambiando `~Base()` in virtual, `~Derived()` verrà chiamato correttamente quando viene eseguito `delete p` e il checker dell'heap sarà contento.

### La regola "Le expectation più nuove sovrascrivono quelle più vecchie" complica la scrittura delle expectation. Perché gMock lo fa?

Quando le persone si lamentano di questo, spesso si riferiscono a codici come:

```cpp
using ::testing::Return;
...
  // foo.Bar() dovrebbe essere chiamato due volte, restituire 1 la prima volta e restituire
  // 2 la seconda volta.  Devo però scrivere le expectation
  // nell'ordine inverso.  Questo fa davvero schifo!!!
  EXPECT_CALL(foo, Bar())
      .WillOnce(Return(2))
      .RetiresOnSaturation();

  EXPECT_CALL(foo, Bar())
      .WillOnce(Return(1))
      .RetiresOnSaturation();

```

Il problema è che non hanno scelto il modo **migliore** per esprimere l'intento del test.

Per default, non è necessario che le expectation corrispondano in *ogni* particolare ordine. Se si vuole che corrispondano in un certo ordine, si deve essere espliciti. Questa è la filosofia fondamentale di gMock (e di jMock): è facile sovra-specificare accidentalmente i test e noi vogliamo rendere più difficile farlo.

Esistono due modi migliori per scrivere le specifiche del test. Si potrebbero mettere le expectation in sequenza:

```cpp
using ::testing::Return;
...
  // foo.Bar() dovrebbe essere chiamato due volte, restituire 1 la prima volta e restituire
  // 2 la seconda volta.  Usando una sequenza, possiamo scrivere le expectation
  // nel loro ordine naturale.
  {
    InSequence s;
    EXPECT_CALL(foo, Bar())
        .WillOnce(Return(1))
        .RetiresOnSaturation();

    EXPECT_CALL(foo, Bar())
        .WillOnce(Return(2))
        .RetiresOnSaturation();

  }

```

oppure si può mettere la sequenza di azioni nella stessa expectation:

```cpp
using ::testing::Return;
...
  // foo.Bar() dovrebbe essere chiamato due volte, restituire 1 la prima volta e restituire
  // 2 la seconda volta.
  EXPECT_CALL(foo, Bar())
      .WillOnce(Return(1))
      .WillOnce(Return(2))
      .RetiresOnSaturation();

```

Torniamo alle domande originali: perché gMock cerca le expectation (e le `ON_CALL`) da dietro in avanti? Perché ciò consente all'utente di impostare in anticipo il comportamento di un mock per il caso comune (ad esempio nel costruttore del mock o nella fase di impostazione della fixture) e di personalizzarlo con regole più specifiche in seguito. Se gMock effettua la ricerca dalla parte anteriore a quella posteriore, questo modello molto utile non sarà possibile.

### gMock stampa un warning quando viene chiamata una funzione senza EXPECT_CALL, anche se ho impostato il suo comportamento utilizzando ON_CALL. Sarebbe ragionevole non mostrare il warning in questo caso?

Quando scegliamo tra l’essere puliti e l’essere al sicuro, tendiamo verso quest’ultimo. Quindi la risposta è che pensiamo sia meglio mostrare il warning.

Spesso le persone scrivono `ON_CALL` nel costruttore dell'oggetto mock o in `SetUp()`, poiché il comportamento di default raramente cambia da test a test. Poi nel corpo del test si stabiliscono le expectation, che spesso sono diverse per ogni test. Avere un `ON_CALL` nella parte del set-up di un test non significa che le chiamate siano previste [expected].
Se non c'è `EXPECT_CALL` e il metodo viene chiamato, probabilmente si tratta di un errore. Se lasciamo passare la chiamata senza notificare all'utente, i bug potrebbero insinuarsi inosservati.

Se invece si è sicuri che le chiamate siano andate bene si può scrivere

```cpp
using ::testing::_;
...
  EXPECT_CALL(foo, Bar(_))
      .WillRepeatedly(...);

```

invece di

```cpp
using ::testing::_;
...
  ON_CALL(foo, Bar(_))
      .WillByDefault(...);

```

Questo dice a gMock che ci si aspettano le chiamate e non dovrebbe essere stampato alcun warning.

Inoltre, si può controllare la verbosità specificando `--gmock_verbose=error`. Altri valori sono `info` e `warning`. Se si ritiene che l'output sia troppo prolisso durante il debug, si sceglie semplicemente un livello meno dettagliato di verbosità.

### Come si può eliminare l'argomento della funzione mock in un'azione?

<N>If your mock function takes a pointer argument and you want to delete that
argument, you can use testing::DeleteArg() to delete the N'th (zero-indexed)
argument:

```cpp
using ::testing::_;
  ...
  MOCK_METHOD(void, Bar, (X* x, const Y& y));
  ...
  EXPECT_CALL(mock_foo_, Bar(_, _))
      .WillOnce(testing::DeleteArg<0>()));

```

### Come posso eseguire un'azione arbitraria sull'argomento di una funzione mock?

Se si deve eseguire qualche azione non supportata direttamente da gMock, ci si ricordi che si possono definire le proprie azioni utilizzando [`MakeAction()`](#NewMonoActions) o [`MakePolymorphicAction()`](#NewPolyActions), oppure si può scrivere una funzione stub e invocarla utilizzando [`Invoke()`](#FunctionsAsActions).

```cpp
using ::testing::_;
using ::testing::Invoke;
  ...
  MOCK_METHOD(void, Bar, (X* p));
  ...
  EXPECT_CALL(mock_foo_, Bar(_))
      .WillOnce(Invoke(MyAction(...)));

```

### Il mio codice chiama una funzione statica/globale. Posso renderla mock?

Si può, ma si devono apportare alcune modifiche.

In generale, se si deve rendere mock una funzione statica, è segno che i moduli sono accoppiati troppo strettamente (e meno flessibili, meno riutilizzabili, meno testabili, ecc.). Probabilmente sarebbe meglio definire una piccola interfaccia e chiamare la funzione attraverso quell'interfaccia, che quindi può essere facilmente resa mock. Inizialmente C'è un po' di lavoro, ma di solito si ripaga rapidamente.

Questo [post](https://testing.googleblog.com/2008/06/defeat-static-cling.html) del Google Testing Blog lo dice in modo eccellente. Consultarlo.

### Il mio oggetto mock deve fare cose complesse. È molto faticoso specificare le azioni. gMock fa schifo!

So che non è una domanda, ma riceverai comunque una risposta gratuitamente. :-)

Con gMock puoi creare facilmente mock in C++. E le persone potrebbero essere tentate di usarli ovunque. A volte funzionano alla grande, a volte potresti trovarli, beh, difficili da usare. Quindi, cosa c'è che non va in quest'ultimo caso?

Quando si scrive un test senza utilizzare mock, si sollecita il codice e si afferma che restituisce il valore corretto o che il sistema è in uno stato previsto. Questo è talvolta chiamato "test basato sullo stato".

I mock sono ottimi per quello che alcuni chiamano test "basati sull'interazione": invece di controllare lo stato del sistema alla fine, gli oggetti mock verificano che siano invocati nel modo giusto e segnalano un errore non appena si verifica, dando un controllo preciso sul contesto in cui si è verificato l'errore. Questo è spesso più efficace ed economico rispetto ai test state-based.

Se si eseguono test basati sullo stato e si utilizza un test doppione solo per simulare l'oggetto reale, probabilmente è meglio utilizzare un falso. Usare un mock in questo caso è faticoso, poiché non è un punto di forza per i mock eseguire azioni complesse. Se ci si trova in questo caso e si pensa che i mock facciano schifo, semplicemente non si sta usando lo strumento giusto per il problema. Oppure si sta cercando di risolvere il problema sbagliato. :-)

### Ho ricevuto un warning "Uninteresting function call encountered - default action taken.." Devo andare nel panico?

Certamente NO! E' solo per tua informazione. :-)

Ciò che si intende è che si ha una funzione mock, non è stata impostata alcuna expectation su di essa (secondo la regola di gMock ciò significa che non si è interessati alle chiamate a questa funzione e quindi può essere chiamata un numero qualsiasi di volte), e viene chiamata.
Va bene: non è stato detto che non è OK chiamare la funzione!

Cosa succederebbe se in realtà si intendesse impedire la chiamata di questa funzione, ma ci si dimenticasse di scrivere `EXPECT_CALL(foo, Bar()).Times(0)`? Anche se si può sostenere che è colpa dell'utente, gMock cerca di essere gentile e stampa una nota.

Quindi, quando si vede il messaggio e si crede che non dovrebbero esserci chiamate poco interessanti, si dovrebbe indagare su cosa sta succedendo. Per semplificarci la vita, gMock scarica l'analisi dello stack quando viene incontrata una chiamata poco interessante.
Da ciò si può capire quale funzione mock è e come viene chiamata.

### Voglio definire un'azione personalizzata. Dovrei usare Invoke() o implementare l'interfaccia ActionInterface?

Va bene in ogni caso: si scelga quello più conveniente per le proprie circostanze.

Di solito, se l'azione riguarda un particolare tipo di funzione, definirla utilizzando `Invoke()` dovrebbe essere più semplice; se l'azione può essere utilizzata in funzioni di diverso tipo (ad esempio si sta definendo `Return(*value*)`), `MakePolymorphicAction()` è più semplice. A volte si vuole un controllo preciso sui tipi delle funzioni in cui può essere utilizzata l'azione e implementare `ActionInterface` è la strada da percorrere in questo caso. Vedere l'implementazione di `Return()` in `gmock-actions.h` per un esempio.

### Io uso SetArgPointee() in WillOnce(), ma gcc si lamenta di "conflicting return type specified". Cosa significa?

Hai ricevuto questo errore poiché gMock non ha idea di quale valore dovrebbe restituire quando viene chiamato il metodo mock. `SetArgPointee()` dice qual è l'effetto collaterale, ma non dice quale dovrebbe essere il valore restituito. È necessario che `DoAll()` concateni un `SetArgPointee()` con un `Return()` che fornisca un valore appropriato all'API mock-ata.

Vedere questa [ricetta](gmock_cook_book.md#mocking-side-effects) per maggiori dettagli e un esempio.

### Ho un'enorme classe mock e Microsoft Visual C++ va in "out of memory" durante la compilazione. Cosa posso fare?

Abbiamo notato che quando viene utilizzato il flag del compilatore `/clr` , Visual C++ usa 5~6 volte più memoria durante la compilazione di una classe mock. Suggeriamo di evitare `/clr` durante la compilazione di mock C++ nativi.
