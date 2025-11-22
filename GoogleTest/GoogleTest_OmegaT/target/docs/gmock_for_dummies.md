# gMock per Principianti

## Cos'è gMock?

Quando si scrive un prototipo o un test, spesso non è fattibile o saggio affidarsi interamente a oggetti reali. Un **oggetto mock** implementa la stessa interfaccia di un oggetto reale (quindi può essere utilizzato in sua vece), ma consente di specificare in fase di esecuzione come verrà utilizzato e cosa dovrebbe fare (quali metodi saranno chiamati? In quale ordine? Quante volte? Con quali argomenti? Cosa restituiranno? ecc.).

È facile confondere il termine *oggetti fake* (falsi) con oggetto mock (simulati). I fake e i mock in realtà significano cose molto diverse nella comunità del Test-Driven Development (TDD):

*   **Fake** objects have working implementations, but usually take some
    shortcut (perhaps to make the operations less expensive), which makes them
    not suitable for production. An in-memory file system would be an example of
    a fake.
*   **Mocks** are objects pre-programmed with *expectations*, which form a
    specification of the calls they are expected to receive.

Se tutto questo appare troppo astratto, non c'è da preoccuparsi: la cosa più importante da ricordare è che un mock consente di verificare l'*interazione* tra se stesso e il codice che lo utilizza. La differenza tra i fake e i mock diventerà molto più chiara una volta che si inizia ad usare utilizzare i mock.

**gMock** è una libreria (a volte la chiamiamo anche "framework" per farlo sembrare interessante) per creare classi mock e utilizzarle. Fa a C++ quello che jMock/EasyMock fa a Java (beh, più o meno).

Quando si usa gMock,

1.  first, you use some simple macros to describe the interface you want to
    mock, and they will expand to the implementation of your mock class;
2.  next, you create some mock objects and specify its expectations and behavior
    using an intuitive syntax;
3.  quindi si usa il codice che utilizza gli oggetti mock. gMock will catch any
    violation to the expectations as soon as it arises.

## Perché gMock?

Sebbene gli oggetti mock aiutino a rimuovere le dipendenze non necessarie nei test e a renderli veloci e affidabili, usare i mock manualmente in C++ è *difficile*:

*   Qualcuno deve implementare i mock. The job is usually tedious and
    error-prone. Non c'è da stupirsi che si facciano lunghi giri per evitarlo.
*   La qualità di questi mock scritti manualmente è un po', ehm, imprevedibile. You
    may see some really polished ones, but you may also see some that were
    hacked up in a hurry and have all sorts of ad hoc restrictions.
*   The knowledge you gained from using one mock doesn't transfer to the next
    one.

Al contrario, i programmatori Java e Python dispongono di alcuni ottimi framework di simulazione (jMock, EasyMock, ecc.), che automatizzano la creazione di mock. Di conseguenza, il mocking è una tecnica comprovata ed efficace e una pratica ampiamente adottata in quelle comunità.
Avere lo strumento giusto fa assolutamente la differenza.

gMock è stato creato per aiutare i programmatori C++. È stato ispirato da jMock e EasyMock, ma progettato pensando alle specifiche del C++. Risulta amichevole se uno qualsiasi dei seguenti problemi è un disturbo:

*   You are stuck with a sub-optimal design and wish you had done more
    prototyping before it was too late, but prototyping in C++ is by no means
    "rapid".
*   Your tests are slow as they depend on too many libraries or use expensive
    resources (e.g. a database).
*   Your tests are brittle as some resources they use are unreliable (e.g. the
    network).
*   You want to test how your code handles a failure (e.g. a file checksum
    error), but it's not easy to cause one.
*   You need to make sure that your module interacts with other modules in the
    right way, but it's hard to observe the interaction; therefore you resort to
    observing the side effects at the end of the action, but it's awkward at
    best.
*   You want to "mock out" your dependencies, except that they don't have mock
    implementations yet; and, frankly, you aren't thrilled by some of those
    hand-written mocks.

Invitiamo a utilizzare gMock come

*   a *design* tool, for it lets you experiment with your interface design early
    and often. Più iterazioni portano a progetti migliori!
*   a *testing* tool to cut your tests' outbound dependencies and probe the
    interaction between your module and its collaborators.

## Iniziamo

gMock è allegato a googletest.

## Un Caso per Tartarughe Mock

Diamo un'occhiata a un esempio. Supponiamo che si stia sviluppando un programma di grafica che si basa su un'API simile a [LOGO](https://en.wikipedia.org/wiki/Logo_programming_language) per il disegno. Come provare che faccia la cosa giusta? Bene, lo si può eseguire e confrontare lo schermo con una schermata campione, ma ammettiamolo: test come questo sono costosi da eseguire e fragili (e se si passasse a una nuova brillante scheda grafica con un anti-aliasing migliore? All'improvviso si devono aggiornare tutte le immagini campione). Sarebbe troppo laborioso se tutti i test fossero così. Fortunatamente, è nota la [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection) e si conosce la cosa giusta da fare: anziché far dialogare l'applicazione direttamente con l'API di sistema, si avvolgono le API in un'interfaccia (ad esempio, `Turtle`) e il codice di tale interfaccia:

```cpp
class Turtle {
  ...
  virtual ~Turtle() {}
  virtual void PenUp() = 0;
  virtual void PenDown() = 0;
  virtual void Forward(int distance) = 0;
  virtual void Turn(int degrees) = 0;
  virtual void GoTo(int x, int y) = 0;
  virtual int GetX() const = 0;
  virtual int GetY() const = 0;
};
```

(Notare che il distruttore di `Turtle` **deve** essere virtual, come nel caso di **tutte** le classi da cui si intende ereditare - altrimenti il distruttore della classe derivata non verrà chiamata quando si elimina un oggetto tramite un puntatore base e si otterranno stati del programma danneggiati come i memory leak).

Si può controllare se il movimento della tartaruga lascerà una traccia usando `PenUp()` e `PenDown()` e controllarne il movimento con `Forward()`, `Turn()` e `GoTo()`. Infine, `GetX()` e `GetY()` dicono la posizione attuale della tartaruga.

Il programma normalmente utilizzerà un'implementazione reale di questa interfaccia. Nei test è invece possibile utilizzare un'implementazione mock. Ciò consente di controllare facilmente quali primitive di disegno sta chiamando il programma, con quali argomenti e in quale ordine. I test scritti in questo modo sono molto più robusti (non si romperanno perché la nuova macchina esegue l'anti-aliasing in modo diverso), sono più facili da leggere e mantenere (l'intento di un test è espresso nel codice, non in alcune immagini binarie) e si gira *molto, molto più velocemente*.

## Scrittura della Classe Mock

Se si è fortunati, i mock da utilizzare sono già stati implementati da alcune persone simpatiche. Se, tuttavia, ci si trova nella posizione di scrivere una classe mock, si può stare tranquilli: gMock trasforma questo compito in un gioco divertente! (Be' quasi).

### Come la si Definisce

Utilizzando l'interfaccia di `Turtle` come esempio, ecco i semplici passaggi da seguire:

*   Derivare una classe `MockTurtle` da `Turtle`.
*   Take a *virtual* function of `Turtle` (while it's possible to
    [mock non-virtual methods using templates](gmock_cook_book.md#MockingNonVirtualMethods),
    it's much more involved).
*   Nella sezione `public:` della classe figlia, si scrive `MOCK_METHOD();`
*   Now comes the fun part: you take the function signature, cut-and-paste it
    into the macro, and add two commas - one between the return type and the
    name, another between the name and the argument list.
*   If you're mocking a const method, add a 4th parameter containing `(const)`
    (the parentheses are required).
*   Since you're overriding a virtual method, we suggest adding the `override`
    keyword. For const methods the 4th parameter becomes `(const, override)`,
    for non-const methods just `(override)`. Questo non è obbligatorio.
*   Si ripete per tutte le funzioni virtuali da simulare (mock-are). (It goes
    without saying that *all* pure virtual methods in your abstract class must
    be either mocked or overridden.)

Alla fine del processo, si dovrebbe avere qualcosa del genere:

```cpp
#include <gmock/gmock.h>  // Brings in gMock.
class MockTurtle : public Turtle {
 public:
  ...
  MOCK_METHOD(void, PenUp, (), (override));
  MOCK_METHOD(void, PenDown, (), (override));
  MOCK_METHOD(void, Forward, (int distance), (override));
  MOCK_METHOD(void, Turn, (int degrees), (override));
  MOCK_METHOD(void, GoTo, (int x, int y), (override));
  MOCK_METHOD(int, GetX, (), (const, override));
  MOCK_METHOD(int, GetY, (), (const, override));
};
```

Non è necessario definire questi metodi mock da qualche altra parte: la macro `MOCK_METHOD` genererà le definizioni automaticamente. È così semplice!

### Dove Metterlo

Quando si definisce una classe mock, si deve decidere dove inserire la sua definizione.
Qualcuno le mette in un `_test.cc`. Questo va bene quando l'interfaccia mock-ata (ad esempio, `Foo`) è di proprietà della stessa persona o team. Altrimenti, quando il proprietario di `Foo` la modifica, il test potrebbe non funzionare. (Non ci si può certo aspettare che il manutentore di `Foo` corregga ogni test che usa `Foo`, vero?)

In generale, non si dovrebbero mock-are le classi altrui. Per mock-are una classe simile di altri, si definisce la classe mock nel pacchetto Bazel di `Foo` (di solito la stessa directory o una sottodirectory di `testing`) e la si inserisce in un `.h` e un `cc_library` con `testonly=True`. Dopodiché tutti possono farvi riferimento dai loro test. Se `Foo` cambia, c'è solo una copia di `MockFoo` da modificare e solo i test che dipendono dai metodi modificati devono essere corretti.

C'è un altro modo per farlo: si può introdurre un sottile layer `FooAdaptor` al di sopra di `Foo` e inserire il codice per questa nuova interfaccia. Poiché si è proprietari di `FooAdaptor`, si possono assorbire più facilmente le modifiche in `Foo`. Anche se inizialmente questo richiede più lavoro, scegliere attentamente l'interfaccia dell'adattatore [adaptor] può rendere il codice più facile da scrivere e più leggibile (un vantaggio netto a lungo termine), poiché si può scegliere `FooAdaptor` per adattarlo maggiormente al dominio specifico meglio di `Foo`.

## Uso dei Mock nei Test

Una volta che si ha una classe mock, usarla è facile. Il flusso di lavoro tipico è:

1.  Import the gMock names from the `testing` namespace such that you can use
    them unqualified (You only have to do it once per file). Remember that
    namespaces are a good idea.
2.  Si creano degli oggetti mock.
3.  Si specificano le [expectation] aspettative su di essi (quante volte verrà chiamato un metodo?
    Con quali argomenti? Cosa dovrebbe fare? ecc.).
4.  Exercise some code that uses the mocks; optionally, check the result using
    googletest assertions. If a mock method is called more than expected or with
    wrong arguments, you'll get an error immediately.
5.  When a mock is destructed, gMock will automatically check whether all
    expectations on it have been satisfied.

Ecco un esempio:

```cpp
#include "path/to/mock-turtle.h"
#include <gmock/gmock.h>
#include <gtest/gtest.h>
using ::testing::AtLeast;                         // #1
TEST(PainterTest, CanDrawSomething) {
  MockTurtle turtle;                              // #2
  EXPECT_CALL(turtle, PenDown())                  // #3
      .Times(AtLeast(1));
  Painter painter(&turtle);                       // #4
  EXPECT_TRUE(painter.DrawCircle(0, 0, 10));      // #5
}
```

Come intuito, questo test verifica che `PenDown()` venga chiamato almeno una volta. Se l'oggetto `painter` non ha chiamato questo metodo, il test fallirà con un messaggio come questo:

```text
path/to/my_test.cc:119: Failure
Actual function call count doesn't match this expectation:
Actually: never called;
Expected: called at least once.
Stack trace:
...
```

**Tip 1:** Se si esegue il test da un buffer Emacs, si può premere `<Invio>` sul numero di riga per passare direttamente alla expectation non riuscita.

**Tip 2:** Se gli oggetti mock non vengono mai eliminati, la verifica finale non avrà luogo. Pertanto è una buona idea attivare il controllo dell'heap nei test quando si allocano i mock sull'heap. Lo si ottiene automaticamente se si usa già la libreria `gtest_main`.

**Nota importante:** gMock richiede che le expectation siano impostate **prima** di chiamare le funzioni mock, altrimenti il comportamento è **indefinito**. Non alternare le chiamate a `EXPECT_CALL()` e le chiamate alle funzioni mock e non impostare alcuna expectation su un mock dopo averlo passato a un'API.

Ciò significa che `EXPECT_CALL()` dovrebbe essere letto come se si aspettasse che una chiamata avverrà *in futuro*, non che una chiamata sia avvenuta. Perché gMock funziona così?
Ebbene, specificare in anticipo la expectation consente a gMock di riportare una violazione non appena si verifica, quando il contesto (stack trace, ecc.) è ancora disponibile.
Ciò semplifica molto il debug.

Certo, questo test è artificioso e non fa molto. Si può facilmente ottenere lo stesso effetto senza utilizzare gMock. Tuttavia, come vedremo presto, gMock permette di fare *molto di più* con i mock.

## Impostare le Expectation

La chiave per utilizzare con successo un oggetto mock è quella di impostarvi le *expectation giuste*. Con delle expectation troppo rigide, il test fallirà per modifiche non correlate. Se sono troppo blande, qualche bug potrebbe sfuggire. Lo si vuole fare nel modo giusto in modo che il test possa rilevare esattamente il tipo di bug che si intende rilevare. gMock fornisce i mezzi necessari per farlo "nel modo giusto".

### Sintassi Generale

In gMock usiamo la macro `EXPECT_CALL()` per impostare una expectation su un metodo mock. La sintassi generale è:

```cpp
EXPECT_CALL(mock_object, method(matchers))
    .Times(cardinality)
    .WillOnce(action)
    .WillRepeatedly(action);
```

La macro ha due argomenti: prima l'oggetto mock, poi il metodo e i suoi argomenti. Si noti che i due sono separati da una virgola (`,`), non da un punto (`.`).
(Perché si usa una virgola? La risposta è che era necessario per motivi tecnici).
Se il metodo non è overloaded, la macro può essere richiamata anche senza i matcher:

```cpp
EXPECT_CALL(mock_object, non-overloaded-method)
    .Times(cardinality)
    .WillOnce(action)
    .WillRepeatedly(action);
```

Questa sintassi consente a chi scrive il test di specificare che è "chiamato con qualsiasi argomento" senza specificare esplicitamente il numero o il tipo di argomenti. Per evitare ambiguità indesiderate, questa sintassi può essere utilizzata solo per metodi che non sono sovraccaricati [overloaded].

Entrambe le forme della macro possono essere seguite da alcune *clausole* [clause] facoltative che forniscono ulteriori informazioni sulla expectation. Illustreremo come funziona ciascuna clausola nelle prossime sezioni.

Questa sintassi è progettata per far sì che una expectation venga letta come l'inglese. Ad esempio, probabilmente si intuirà che

```cpp
using ::testing::Return;
...
EXPECT_CALL(turtle, GetX())
    .Times(5)
    .WillOnce(Return(100))
    .WillOnce(Return(150))
    .WillRepeatedly(Return(200));
```

dice che il metodo `turtle` dell'oggetto `GetX()` verrà chiamato cinque volte, restituirà 100 la prima volta, 150 la seconda volta e poi 200 ogni volta.
A qualcuno piace chiamare questo stile di sintassi un Domain-Specific Language (DSL).

{: .callout .note}
**Nota:** Perché utilizziamo una macro per fare questo? Beh, ha due scopi: in primo luogo rende le expectation facilmente identificabili (sia da `grep` che da un lettore umano), e in secondo luogo consente a gMock di includere la posizione del file sorgente di una expectation non riuscita nei messaggi, facilitando il debugging.

### I Matcher: Quali Argomenti Ci Aspettiamo?

Quando una funzione mock accetta argomenti, possiamo specificare quali ci aspettiamo, ad esempio:

```cpp
// Si aspetta che la tartaruga si muova in avanti di 100 unità.
EXPECT_CALL(turtle, Forward(100));
```

Spesso non si vuol essere troppo specifici. Ricordate quando si parlava di test troppo rigidi? Una specifica eccessiva porta a test fragili e oscura l'intento dei test. Pertanto invitiamo a specificare solo ciò che è necessario, né più né meno. Se non interessa il valore di un argomento, si scrive `_` come argomento, che significa "va bene qualsiasi cosa":

```cpp
using ::testing::_;
...
// Si aspetta che la tartaruga salti da qualche parte sulla linea x=50.
EXPECT_CALL(turtle, GoTo(50, _));
```

`_` è un'istanza di quelle che chiamiamo **matcher**. Un matcher è come un predicato e può verificare se un argomento è quello che ci aspetteremmo. Si può utilizzare un matcher all'interno di `EXPECT_CALL()` ovunque sia previsto un argomento di funzione. `_` è un modo conveniente per dire "qualsiasi valore".

Negli esempi precedenti, anche `100` e `50` sono matcher; implicitamente, sono lo stesso di `Eq(100)` e `Eq(50)`, che specificano che l'argomento deve essere uguale (usando `operator==`) all'argomento matcher. Esistono molti [matcher nativi [built-in]](reference/matchers.md) per i tipi comuni (così come [matcher personalizzati](gmock_cook_book.md#NewMatchers)); per esempio:

```cpp
using ::testing::Ge;
...
// Si aspetta che la tartaruga si muova in avanti di almeno 100.
EXPECT_CALL(turtle, Forward(Ge(100)));
```

Se non interessa *qualsiasi* argomento, anziché specificare `_` per ciascuno di essi si può omettere l'elenco dei parametri:

```cpp
// Si aspetta che la tartaruga vada avanti.
EXPECT_CALL(turtle, Forward);
// Si aspetta che la tartaruga salti da qualche parte.
EXPECT_CALL(turtle, GoTo);
```

Funziona con tutti i metodi non-overloaded; se un metodo lo è, è necessario aiutare gMock a risolvere quale overload ci si aspetta specificando il numero di argomenti ed eventualmente anche i [tipi degli argomenti](gmock_cook_book.md#SelectOverload).

### Le Cardinalità: Quante Volte Verrà Chiamata?

La prima clausola che possiamo specificare dopo una `EXPECT_CALL()` è `Times()`. Chiamiamo il suo argomento una **cardinalità** per dire *quante volte* dovrebbe verificarsi la chiamata. Consente di ripetere una expectation molte volte senza in realtà scriverla tante volte. Ancora più importante, una cardinalità può essere "fuzzy" (vago), proprio come può esserlo un matcher. Ciò consente all'utente di esprimere esattamente l'intento di un test.

Un caso speciale interessante è quando diciamo `Times(0)`. Come si intuisce - significa che la funzione non dovrebbe essere chiamata con gli argomenti forniti e gMock segnalerà un errore di googletest ogni volta che la funzione viene chiamata (erroneamente).

Abbiamo visto `AtLeast(n)` come esempio di cardinalità fuzzy in precedenza. Per l'elenco delle cardinalità native utilizzabili, vedere [qui](gmock_cheat_sheet.md#CardinalityList).

La clausola `Times()` può essere omessa. **Se si omette `Times()`, gMock dedurrà autonomamente la cardinalità.** Le regole sono facili da ricordare:

*   Se non c'è **né** `WillOnce()` **né** `WillRepeatedly()` nella `EXPECT_CALL()`, la cardinalità dedotta è `Times(1)`.
*   If there are *n* `WillOnce()`'s but **no** `WillRepeatedly()`, where *n* >=
    1, the cardinality is `Times(n)`.
*   If there are *n* `WillOnce()`'s and **one** `WillRepeatedly()`, where *n* >=
    0, the cardinality is `Times(AtLeast(n))`.

**Quiz veloce:** cosa accadrà se si prevede che una funzione venga chiamata due volte ma in realtà viene chiamata quattro volte?

### Azioni: Cosa Dovrebbe Fare?

Ci si ricorda che un oggetto mock non ha in realtà un'implementazione funzionante? Noi come utenti dobbiamo dirgli cosa fare quando viene invocato un metodo. Questo è facile in gMock.

Innanzitutto, se il tipo restituito di una funzione mock è un tipo nativo o un puntatore, la funzione ha un'**azione di default** (una funzione `void` tornerà e basta, una funzione `bool` restituirà `false` e le altre funzioni restituiranno 0). Inoltre, in C++ 11 e nelle versioni successive, una funzione mock il cui tipo restituito è default-constructible (ovvero ha un costruttore di default) ha un'azione di default che restituisce un valore costruito dal default. Se non si dice nulla, verrà utilizzato questo comportamento.

In secondo luogo, se una funzione mock non ha un'azione di default, o questa non è adatta alle proprie esigenze, si può specificare l'azione da intraprendere ogni volta che la expectation corrisponde utilizzando una serie di clausole `WillOnce()` seguite da un facoltativo `WillRepeatedly()`. Per esempio,

```cpp
using ::testing::Return;
...
EXPECT_CALL(turtle, GetX())
     .WillOnce(Return(100))
     .WillOnce(Return(200))
     .WillOnce(Return(300));
```

dice che `turtle.GetX()` verrà chiamata *esattamente tre volte* (gMock lo ha dedotto da quante clausole `WillOnce()` abbiamo scritto, poiché non abbiamo scritto esplicitamente `Times()`), e restituirà rispettivamente 100, 200 e 300.

```cpp
using ::testing::Return;
...
EXPECT_CALL(turtle, GetY())
     .WillOnce(Return(100))
     .WillOnce(Return(200))
     .WillRepeatedly(Return(300));
```

dice che `turtle.GetY()` sarà chiamata *almeno due volte* (gMock lo sa perché abbiamo scritto due clausole `WillOnce()` e una `WillRepeatedly()` pur non avendo esplicitato `Times()`), restituirà 100 e 200 rispettivamente le prime due volte e 300 dalla terza volta in poi.

Naturalmente, se si scrive esplicitamente un `Times()`, gMock non tenterà di dedurre la cardinalità. Cosa succede se il numero specificato è maggiore delle clausole `WillOnce()`? Bene, dopo che tutti i `WillOnce()` sono esauriti, gMock eseguirà ogni volta l'azione di *default* per la funzione (a meno che, ovviamente, non si abbia un `WillRepeatedly ()`).

Cosa possiamo fare all'interno di `WillOnce()` oltre a `Return()`? Si può restituire un riferimento utilizzando `ReturnRef(`*`variable`*`)`, o richiamare una funzione pre-definita, tra [[others] (altre)](gmock_cook_book.md#using-actions).

**Nota importante:** L'istruzione `EXPECT_CALL()` valuta la clausola dell'azione una sola volta, anche se l'azione può essere eseguita più volte. Pertanto è necessario fare attenzione agli effetti collaterali. Quanto segue potrebbe non fare quello che si desidera:

```cpp
using ::testing::Return;
...
int n = 100;
EXPECT_CALL(turtle, GetX())
    .Times(4)
    .WillRepeatedly(Return(n++));
```

Invece di restituire 100, 101, 102, ..., consecutivamente, questa funzione mock restituirà sempre 100 in quanto `n++` viene valutato solo una volta. Allo stesso modo, `Return(new Foo)` creerà un nuovo oggetto `Foo` quando viene eseguito `EXPECT_CALL()` e restituirà ogni volta lo stesso puntatore. Se si vuole che l'effetto collaterale si verifichi ogni volta, si deve definire un'azione personalizzata, che illustreremo nel [cook book](gmock_cook_book.md).

È ora di un altro quiz! Cosa significa quanto segue?

```cpp
using ::testing::Return;
...
EXPECT_CALL(turtle, GetY())
    .Times(4)
    .WillOnce(Return(100));
```

Ovviamente `turtle.GetY()` ci si aspetta che venga chiamato quattro volte. Ma se si crede che restituirà 100 ogni volta, è meglio pensarci due volte! Ricordarsi che una clausola `WillOnce()` verrà utilizzata ogni volta che la funzione viene invocata e successivamente verrà eseguita l'azione di default. Quindi la risposta giusta è che `turtle.GetY()` restituirà 100 la prima volta, ma **restituirà 0 dalla seconda volta in poi**, poiché restituire 0 è l'azione predefinita per le funzioni `int`.

### Uso di Expectation Multiple {#MultiExpectations}

Finora abbiamo mostrato solo esempi con una sola expectation. Più realisticamente, si specificheranno le expectation su più metodi mock che potrebbero provenire da più oggetti mock.

Per default, quando viene richiamato un metodo mock, gMock cercherà le expectation nell'**ordine inverso** in cui sono definite e si fermerà quando viene trovata una expectation attiva che corrisponde agli argomenti (si possono considerare come "le regole più recenti scavalcano quelle più vecchie"). Se la corrispondente expectation non può accettare più chiamate, si verificherà un errore con violazione del limite superiore [upper-bound-violated]. Ecco un esempio:

```cpp
using ::testing::_;
...
EXPECT_CALL(turtle, Forward(_));  // #1
EXPECT_CALL(turtle, Forward(10))  // #2
    .Times(2);
```

Se `Forward(10)` viene chiamato tre volte di seguito, la terza volta si verificherà un errore, poiché l'ultima expectation corrispondente (#2) è stata saturata. Se, tuttavia, la terza chiamata `Forward(10)` viene sostituita da `Forward(20)`, allora andrebbe bene, poiché ora #1 sarà la expectation corrispondente.

{: .callout .note}
**Nota:** Perché gMock cerca una corrispondenza nell'ordine *inverso* delle expectation? Il motivo è che ciò consente all'utente di impostare le expectation di default nel costruttore di un oggetto mock o nella fase di impostazione del [test fixture] e quindi personalizzare il mock expectation più specifiche nel corpo del test. Quindi, se si hanno due expectation sullo stesso metodo, si vuol mettere quella con matcher più specifici **dopo** l'altra, altrimenti la regola più specifica verrebbe oscurata da quella più generale che viene dopo.

{: .callout .tip}
**Tip:** È molto comune iniziare con una expectation generale per un metodo e con `Times(AnyNumber())` (omettendo gli argomenti, o con `_` per tutti gli argomenti, se [overloaded] sovraccaricati). Ciò rende expected tutte le chiamate al metodo. Ciò non è necessario per i metodi non menzionati (questi sono "poco interessanti"), ma è utile per i metodi che hanno alcune expectation, ma per i quali vanno bene altre chiamate. Vedere [Le Chiamate Poco Interessanti e Quelle Unexpected](gmock_cook_book.md#uninteresting-vs-unexpected).

### Chiamate ordinate e Non {#OrderedCalls}

Per default, una expectation può corrispondere a una chiamata anche se una expectation precedente non è stata soddisfatta. In altre parole, le chiamate non devono avvenire nell'ordine in cui sono specificate le expectation.

A volte, si vuole che tutte le chiamate previste avvengano in un ordine rigoroso. Dirlo in gMock è semplice:

```cpp
using ::testing::InSequence;
...
TEST(FooTest, DrawsLineSegment) {
  ...
  {
    InSequence seq;
    EXPECT_CALL(turtle, PenDown());
    EXPECT_CALL(turtle, Forward(100));
    EXPECT_CALL(turtle, PenUp());
  }

  Foo();
}
```

Creando un oggetto di tipo `InSequence`, tutte le expectation nel suo scope vengono inserite in una *sequenza* e devono verificarsi *sequenzialmente*. Dato che facciamo affidamento solo sul costruttore e sul distruttore di questo oggetto per svolgere il lavoro vero e proprio, il suo nome è davvero irrilevante.

In questo esempio, testiamo che `Foo()` chiami le tre funzioni expected nell'ordine in cui sono scritte. Se una chiamata viene effettuata fuori ordine, sarà un errore.

(E se interessa l'ordine relativo di alcune chiamate, ma non di tutte? È possibile specificare un arbitrario ordine parziale? La risposta è ... sì! I dettagli si trovano [qui](gmock_cook_book.md#OrderedCalls).)

### Tutte le expectation sono fisse (a meno che non venga detto diversamente) {#StickyExpectations}

Ora facciamo un breve quiz per vedere quanto bene si possano già usare queste cose di mock.
Come verificare che alla tartaruga venga chiesto di andare all'origine *esattamente due volte* (ignorare qualsiasi altra istruzione ricevuta)?

Dopo aver trovato la risposta, date un'occhiata alla nostra e confrontate le note (da risolvere in autonomia - non imbrogliare!):

```cpp
using ::testing::_;
using ::testing::AnyNumber;
...
EXPECT_CALL(turtle, GoTo(_, _))  // #1
     .Times(AnyNumber());
EXPECT_CALL(turtle, GoTo(0, 0))  // #2
     .Times(2);
```

Supponiamo che `turtle.GoTo(0, 0)` sia chiamata tre volte. Nella terza volta, gMock vedrà che gli argomenti corrispondono alla expectation #2 (ricordate che scegliamo sempre l'ultima expectation corrispondente). Ora, poiché abbiamo detto che dovrebbero esserci solo due chiamate di questo tipo, gMock segnalerà immediatamente un errore. Questo è fondamentalmente ciò che abbiamo detto nella sezione [Uso di Expectation Multiple](#MultiExpectations) sopra.

Questo esempio mostra che **le expectation in gMock sono per default "appiccicose"**, nel senso che rimangono attive anche dopo aver raggiunto i limiti superiori della loro invocazione. Questa è una regola importante da ricordare, poiché influenza il significato delle specifiche ed è **diversa** da come viene eseguita in molti altri framework di simulazione (Perché dovremmo farlo? Perché pensiamo che la nostra regola renda i casi comuni più facili da esprimere e comprendere).

Semplice? Vediamo se è stato ben compreso: cosa dice il seguente codice?

```cpp
using ::testing::Return;
...
for (int i = n; i > 0; i--) {
  EXPECT_CALL(turtle, GetX())
      .WillOnce(Return(10*i));
}
```

Se si pensa che dica che `turtle.GetX()` verrà chiamato `n` volte e restituirà 10, 20, 30, ..., consecutivamente, ripensateci! Il problema è che, come abbiamo detto, le expectation sono appiccicose. Pertanto, la seconda volta che viene chiamato `turtle.GetX()`, l'ultima (più recente) istruzione `EXPECT_CALL()` corrisponderà e porterà immediatamente a un errore di "upper bound violated": questo pezzo di codice non è molto utile!

Un modo corretto per dire che `turtle.GetX()` restituirà 10, 20, 30, ..., è dire esplicitamente che le expectation *non* sono appiccicose. In altre parole, dovrebbero *ritirarsi* appena saturate:

```cpp
using ::testing::Return;
...
for (int i = n; i > 0; i--) {
  EXPECT_CALL(turtle, GetX())
      .WillOnce(Return(10*i))
      .RetiresOnSaturation();
}
```

E c'è un modo migliore per farlo: in questo caso, ci aspettiamo che le chiamate avvengano in un ordine specifico e allineiamo le azioni in modo che corrispondano all'ordine. Poiché in questo caso l'ordine è importante, dovremmo renderlo esplicito utilizzando una sequenza:

```cpp
using ::testing::InSequence;
using ::testing::Return;
...
{
  InSequence s;
  for (int i = 1; i <= n; i++) {
    EXPECT_CALL(turtle, GetX())
        .WillOnce(Return(10*i))
        .RetiresOnSaturation();

  }
}

```

A proposito, l'altra situazione in cui una expectation può *non* essere appiccicosa è quando è in una sequenza: non appena viene utilizzata un'altra expectation che viene dopo di essa nella sequenza, viene automaticamente 'ritirata' (e non verrà mai più usata per abbinare alcuna chiamata).

### Chiamate Non Interessanti

Un oggetto mock può avere molti metodi e non tutti sono così interessanti.
Ad esempio, in alcuni test potremmo non interessarci a quante volte `GetX()` e `GetY()` vengono chiamate.

In gMock, se non si è interessati a un metodo, non si dice nulla a riguardo. Se c'è una chiamata a questo metodo, verrà visualizzato un warning nell'output del test, ma non si tratterà di un errore. Questo comportamento è detto "naggy" (fastidioso); per modificarlo, vedere [Nice, Strict e Naggy](gmock_cook_book.md#NiceStrictNaggy).
