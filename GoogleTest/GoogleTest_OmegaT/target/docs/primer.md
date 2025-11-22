# Guida di GoogleTest

## Introduzione: Perché GoogleTest?

*GoogleTest* aiuta a scrivere meglio i test di C++.

GoogleTest è un framework per i test sviluppato dal team "Testing Technology" tenendo presenti i requisiti e i vincoli specifici di Google. Sia se si lavora su Linux, su Windows, o su Mac, se si scrive codice C++, GoogleTest può essere utile. Supporta *qualsiasi* tipo di test, non solo le "unit test".

Quindi cosa rende buon un test e come si inserisce GoogleTest? Noi crediamo che:

1.  I test dovrebbero essere *independeni* e *ripetibili*. It's a pain to debug a test
    that succeeds or fails as a result of other tests. GoogleTest isolates the
    tests by running each of them on a different object. When a test fails,
    GoogleTest allows you to run it in isolation for quick debugging.
2.  Tests should be well *organized* and reflect the structure of the tested
    code. GoogleTest groups related tests into test suites that can share data
    and subroutines. This common pattern is easy to recognize and makes tests
    easy to maintain. Such consistency is especially helpful when people switch
    projects and start to work on a new code base.
3.  I test dovrebbero essere *portabili* e *riutilizzabili*. Google has a lot of code that is
    platform-neutral; its tests should also be platform-neutral. GoogleTest
    works on different OSes, with different compilers, with or without
    exceptions, so GoogleTest tests can work with a variety of configurations.
4.  When tests fail, they should provide as much *information* about the problem
    as possible. GoogleTest non si ferma al primo fallimento del test. Instead, it
    only stops the current test and continues with the next. You can also set up
    tests that report non-fatal failures after which the current test continues.
    Thus, you can detect and fix multiple bugs in a single run-edit-compile
    cycle.
5.  The testing framework should liberate test writers from housekeeping chores
    and let them focus on the test *content*. GoogleTest automatically keeps
    track of all tests defined, and doesn't require the user to enumerate them
    in order to run them.
6.  I test dovrebbero essere *veloci*. With GoogleTest, you can reuse shared resources
    across tests and pay for the set-up/tear-down only once, without making
    tests depend on each other.

Dat che GoogleTest è basato sulla popolare architettura xUnit, ci si sentirà come a casa se si è già utenti di JUnit o di PyUnit. In caso contrario, ci vorranno circa 10 minuti per apprendere le nozioni di base e cominciare. Quindi andiamo!

## Attenzione alla Nomenclatura

{: .callout .note}
*Nota:* Potrebbe verificarsi un po' di confusione derivante dalle diverse definizioni dei termini *Test*, *Test Case* e *Test Suite*, quindi attenzione a non confonderli.

Storicamente, GoogleTest ha iniziato a utilizzare il termine *Test Case* per raggruppare test correlati, mentre le pubblicazioni attuali, inclusi i materiali dell'International Software Testing Qualifications Board ([ISTQB](https://www.istqb.org/)) e vari libri di testo sulla qualità del software, utilizzano il termine *[Test Suite][istqb test suite]* per questo.*

Il termine correlato *Test*, così come viene utilizzato in GoogleTest, corrisponde al termine *[Test Case][istqb test case]* di ISTQB e di altri.*

Il termine *Test* ha comunemente un senso sufficientemente ampio, inclusa la definizione di *Test Case*, di ISTQB, quindi non è un grosso problema. Ma il termine *Test Case* così come è stato utilizzato in Google Test ha un senso contraddittorio e quindi crea confusione.

GoogleTest ha recentemente iniziato a sostituire il termine *Test Case* con *Test Suite*.
L'API preferita è *TestSuite*. La vecchia API TestCase viene lentamente deprecata e sottoposta a refactoring.

Si prega quindi di prestare attenzione alle diverse definizioni dei termini:


| Significato | Termine GoogleTest | Termine [ISTQB](https://www.istqb.org/) |
:----------------------------------------------------------------------------------- | :---------------------- | :----------------------------------
| Testare un particolare path del programma con valori di input specifici e verificare i risultati | [TEST()](#simple-tests) | [Test Case][istqb test case] |


[istqb test case]: https://glossary.istqb.org/en_US/term/test-case-2
[istqb test suite]: https://glossary.istqb.org/en_US/term/test-suite-1-3

## Concetti Base

Quando si usa GoogleTest, si comincia scrivendo *asserzioni*, ovvero affermazioni che verificano se una condizione è vera. Il risultato di un'asserzione può essere *success*, *nonfatal failure* o *fatal failure*. Se avviane una "fatal failure", interrompe la funzione corrente; altrimenti il programma continua normalmente.

I *test* utilizzano le asserzioni per verificare il comportamento del codice in esame. Se un test va in crash o ha fallisce un'asserzione, allora *fail*; altrimenti *succeed*.

Una *test suite* contiene uno o più test. I test si dovrebbero raggruppare in test suite che riflettono la struttura del codice in esame. Quando più test, in una test suite, devono condividere oggetti e subroutine comuni, si possono inserire in una classe *test fixture*.

Un *test program* può contenere più test suite.

Spiegheremo ora come scrivere un "test program", partendo dal livello della singola asserzione e costruendo poi "test" e "test suite".

## Le Asserzioni

Le asserzioni di GoogleTest sono macro che assomigliano alle chiamate alle funzioni. Una classe o una funzione si può testare facendo asserzioni sul suo comportamento. Quando un'asserzione fallisce, GoogleTest stampa il file sorgente dell'asserzione e la posizione del numero di riga, insieme a un messaggio di errore. Si può anche avere un messaggio di errore personalizzato che verrà aggiunto al messaggio di GoogleTest.

Le asserzioni si presentano in coppie che mettono alla prova la stessa cosa ma hanno effetti diversi sulla funzione corrente. Le versioni `ASSERT_*` generano errori fatali quando falliscono e **interrompono la funzione corrente**. Le versioni `EXPECT_*` generano errori non fatali, che non interrompono la funzione corrente. Solitamente si preferiscono le `EXPECT_*`, poiché consentono di segnalare più di un errore in un test.
Tuttavia, si usa `ASSERT_*` se non ha senso continuare quando l'asserzione in questione fallisce.

Poiché un `ASSERT_*` non riuscito ritorna immediatamente dalla funzione corrente, probabilmente saltando il codice di pulizia successivo, potrebbe causare dei "memory leak".
A seconda della natura del leak, potrebbe valere o meno la pena risolverlo, quindi lo si tenga a mente se si riceve un errore sul controllo dell'heap oltre agli errori dell'asserzione.

Per avere un messaggio di errore personalizzato, è sufficiente inserirlo nella macro utilizzando l'operatore `<<` o una sequenza di tali operatori. Esaminare l'esempio seguente, utilizzando le macro [`ASSERT_EQ` e `EXPECT_EQ`](reference/assertions.md#EXPECT_EQ) per verificare l'uguaglianza dei valori:

```c++
ASSERT_EQ(x.size(), y.size()) << "Vectors x and y are of unequal length";
for (int i = 0; i < x.size(); ++i) {
  EXPECT_EQ(x[i], y[i]) << "Vectors x and y differ at index " << i;
}
```

Tutto ciò che può essere inviato a un `ostream` e può essere inviato ad una macro di asserzione--in particolare, stringhe C e oggetti `string`. Se una stringa estesa [wide] (`wchar_t*`, `TCHAR*` in modalità `UNICODE` su Windows, o `std::wstring`) viene inviata ad un'asserzione, verrà tradotta in UTF-8 per la stampa.

GoogleTest fornisce una raccolta di asserzioni per verificare il comportamento del codice in vari modi. Si possono controllare le condizioni booleane, confrontare valori in base a operatori relazionali, verificare valori stringa, valori in virgola mobile e molto altro. Esistono anche asserzioni che consentono di verificare stati più complessi fornendo predicati personalizzati. Per l'elenco completo delle asserzioni fornite da GoogleTest, consultare i [Riferimenti sulle Asserzioni](reference/assertions.md).

## Test Semplici

Per creare un test:

1.  Si usa la macro `TEST()` per definire e dare un nome a una funzione di test. These are
    ordinary C++ functions that don't return a value.
2.  In this function, along with any valid C++ statements you want to include,
    use the various GoogleTest assertions to check values.
3.  The test's result is determined by the assertions; if any assertion in the
    test fails (either fatally or non-fatally), or if the test crashes, the
    entire test fails. Altrimenti, è riuscito.

```c++
TEST(TestSuiteName, TestName) {
  ... test body ...
}
```

Gli argomenti di `TEST()` vanno dal generale allo specifico. Il *primo* argomento è il nome della "test suite" e il *secondo* argomento è il nome del test nella "test suite". Entrambi i nomi devono essere identificatori C++ validi e non devono contenere underscore (`_`). Il *nome completo* di un test è costituito dalla test suite che lo contiene e dal suo nome individuale. I test di diverse test suite possono avere lo stesso nome individuale.

Ad esempio, prendiamo una semplice funzione intera:

```c++
int Factorial(int n);  // Restituisce il fattoriale di n
```

Una test suite per questa funzione potrebbe essere simile a:

```c++
// Testa il fattoriale di 0.
TEST(FactorialTest, HandlesZeroInput) {
  EXPECT_EQ(Factorial(0), 1);
}
// Tests factorial of positive numbers.
TEST(FactorialTest, HandlesPositiveInput) {
  EXPECT_EQ(Factorial(1), 1);
  EXPECT_EQ(Factorial(2), 2);
  EXPECT_EQ(Factorial(3), 6);
  EXPECT_EQ(Factorial(8), 40320);
}
```

GoogleTest raggruppa i risultati dei test per "test suite", quindi i test logicamente correlati dovrebbero trovarsi nella stessa test suite; in altre parole, il primo argomento del loro `TEST()` dovrebbe essere lo stesso. Nell'esempio precedente, abbiamo due test, `HandlesZeroInput` e `HandlesPositiveInput`, che appartengono alla test suite `FactorialTest`.

Quando si dà un nome alle test suite e ai test, si deve seguire la stessa convenzione usata per [denominare funzioni e classi](https://google.github.io/styleguide/cppguide.html#Function_Names).

**Disponibilità**: Linux, Windows, Mac.

## Test Fixture: Uso della Stessa Configurazione dei Dati per Più Test {#same-data-multiple-tests}

Se ci si ritrova a scrivere due o più test che operano su dati simili, si può usare una *test fixture*. Questa consente di riutilizzare la stessa configurazione di oggetti per più test.

Per creare una fixture:

1.  Si deriva una classe da `testing::Test` . Start its body with `protected:`, as
    we'll want to access fixture members from sub-classes.
2.  All'interno della classe, si dichiarano tutti gli oggetti che si intendono usare.
3.  If necessary, write a default constructor or `SetUp()` function to prepare
    the objects for each test. A common mistake is to spell `SetUp()` as
**`Setup()`** with a small `u` - Use `override` in C++11 to make sure you
    spelled it correctly.
4.  If necessary, write a destructor or `TearDown()` function to release any
    resources you allocated in `SetUp()` . To learn when you should use the
    constructor/destructor and when you should use `SetUp()/TearDown()`, read
    the [FAQ](faq.md#CtorVsSetUp).
5.  Se necessario, definire delle subroutine da condividere tra i test.

Quando si usa una fixture, si usa `TEST_F()` anziché `TEST()` in quanto consente di accedere a oggetti e subroutine nella fixture di test:

```c++
TEST_F(TestFixtureClassName, TestName) {
  ... test body ...
}
```

A differenza di `TEST()`, in `TEST_F()` il primo argomento deve essere il nome della classe della fixture di test. (`_F` sta per "Fixture"). Per questa macro non è specificato alcun nome di test suite.

Sfortunatamente, il sistema delle macro di C++ non ci consente di creare un'unica macro per gestire entrambi i tipi di test. L'utilizzo della macro errata provoca un errore del compilatore.

Inoltre, si deve definire una classe per la fixture di test prima di usarla in una `TEST_F()`, altrimenti si riceve l'errore del compilatore "`virtual outside class declaration`".

Per ogni test definito con `TEST_F()`, GoogleTest creerà una *nuova* fixture a runtime, lo inizializzerà immediatamente tramite `SetUp()`, esegue il test, ripulisce chiamando `TearDown()` ed esegue il delete della fixture di test. Si tenga presente che test diversi nella stessa suite di test hanno oggetti fixture di test diversi e GoogleTest elimina sempre una fixture di test prima di creare quella successiva.
GoogleTest **non** riutilizza la stessa fixture per più test. Qualsiasi modifica apportata da un test alla fixture non influisce sugli altri test.

Ad esempio, scriviamo i test per una classe di una coda FIFO chiamata `Queue`, che ha la seguente interfaccia:

```c++
template <typename E>  // E è il tipo dell'elemento.
class Queue {
 public:
  Queue();
  void Enqueue(const E& element);
  E* Dequeue();  // Restituisce NULL se la coda è vuota.
  size_t size() const;
  ...
};

```

Innanzitutto, si definisce una classe fixture. Per convenzione, si da il nome `FooTest` dove `Foo` è la classe da testare.

```c++
class QueueTest : public testing::Test {
 protected:
  void SetUp() override {
     // q0_ resta vuoto
     q1_.Enqueue(1);
     q2_.Enqueue(2);
     q2_.Enqueue(3);
  }

  // void TearDown() override {}
  Queue<int> q0_;
  Queue<int> q1_;
  Queue<int> q2_;
};
```

In questo caso, `TearDown()` non è necessario poiché non dobbiamo ripulire dopo ogni test, oltre a ciò che è già stato fatto dal distruttore.

Ora scriveremo i test utilizzando `TEST_F()` e questa fixture.

```c++
TEST_F(QueueTest, IsEmptyInitially) {
  EXPECT_EQ(q0_.size(), 0);
}
TEST_F(QueueTest, DequeueWorks) {
  int* n = q0_.Dequeue();
  EXPECT_EQ(n, nullptr);
  n = q1_.Dequeue();
  ASSERT_NE(n, nullptr);
  EXPECT_EQ(*n, 1);
  EXPECT_EQ(q1_.size(), 0);
  delete n;
  n = q2_.Dequeue();
  ASSERT_NE(n, nullptr);
  EXPECT_EQ(*n, 2);
  EXPECT_EQ(q2_.size(), 1);
  delete n;
}
```

Quanto sopra utilizza entrambe le asserzioni `ASSERT_*` e `EXPECT_*`. La regola pratica è quella di utilizzare `EXPECT_*` quando si desidera che il test continui a scoprire altri errori dopo il fallimento dell'asserzione e utilizzare `ASSERT_*` quando continuare dopo il fallimento non ha senso. Ad esempio, la seconda asserzione nel test `Dequeue` è `ASSERT_NE(n, nullptr)`, poiché in seguito dobbiamo dereferenziare il puntatore `n`, che porterebbe a un segfault quando `n` è `NULL`.

Quando vengono eseguiti questi test, accade quanto segue:

1.  GoogleTest costruisce un oggetto `QueueTest` (chiamiamolo `t1`).
2.  `t1.SetUp()` inizializza`t1`.
3.  Il primo test (`IsEmptyInitially`) viene eseguito su `t1`.
4.  `t1.TearDown()` esegue la pulizia al termine del test.
5.  `t1` viene distrutto.
6.  The above steps are repeated on another `QueueTest` object, this time
    running the `DequeueWorks` test.

**Disponibilità**: Linux, Windows, Mac.

## Invocare i Test

`TEST()` e `TEST_F()` registrano implicitamente i loro test con GoogleTest. Pertanto, a differenza di molti altri framework di test C++, non è necessario elencare nuovamente tutti i test definiti per eseguirli.

Dopo aver definito tuoi test, si possono eseguire con `RUN_ALL_TESTS()`, che restituisce `0` se tutti i test hanno esito positivo, o `1` in caso contrario. Notare che `RUN_ALL_TESTS()` esegue *tutti i test* nella [link unit]--possono appartenere a diverse test suite, o anche a diversi file sorgenti.

Quando viene richiamata, la macro `RUN_ALL_TESTS()`:

*   Salva lo stato di tutti i flag di GoogleTest.

*   Crea un oggetto fixture per il primo test.

*   Lo inizializza tramite `SetUp()`.

*   Esegue il test sull'oggetto fixture.

*   Ripulisce la fixture tramite `TearDown()`.

*   Cancella la fixture.

*   Ripristina lo stato di tutti i flag di GoogleTest.

*   Ripete i passaggi precedenti per il test successivo, fino all'esecuzione di tutti i test.

Se si verifica un errore irreversibile, i passaggi successivi verranno saltati.

{: .callout .important}
> IMPORTANTE: **Non** si deve ignorare il valore di ritorno di `RUN_ALL_TESTS()` altrimenti si riceve un errore del compilatore. La logica di questa progettazione è che il servizio di test automatizzato determina se un test è stato superato in base al suo codice di uscita, non all'output stdout/stderr; quindi la funzione `main()` deve restituire il valore di `RUN_ALL_TESTS()`.
>
> Inoltre, si deve chiamare `RUN_ALL_TESTS()` solo **una volta**. Chiamandola più volte, si entra in conflitto con delle funzionalità avanzate di GoogleTest (ad esempio, i [death test](advanced.md#death-tests) thread-safe) e quindi non è supportato.

**Disponibilità**: Linux, Windows, Mac.

## Scrivere la Funzione main()

La maggior parte degli utenti *non* dovrebbe aver bisogno di scrivere la propria funzione `main` e linkare invece `gtest_main` (al contrario di `gtest`), che definisce un punto di ingresso adeguato. Per i dettagli vedere la fine di questa sezione. Il resto di questa sezione dovrebbe applicarsi solo quando è necessario fare qualcosa di personalizzato prima dell'esecuzione dei test che non possa essere espresso nell'ambito delle fixture e delle test suite.

Se si scrive la propria funzione `main`, essa deve restituire il valore di `RUN_ALL_TESTS()`.

Si può iniziare da questo prototipo:

```c++
#include "this/package/foo.h"
#include <gtest/gtest.h>
namespace my {
namespace project {
namespace {
// The fixture for testing class Foo.
class FooTest : public testing::Test {
 protected:
  // Si possono rimuovere alcune o tutte le funzioni seguenti se il loro contenuto
  // è vuoto.
  FooTest() {
     // Quì si può eseguire il lavoro di set-up per ciascun test.
  }

  ~FooTest() override {
     // Quì si può fare un lavoro di pulizia che non generi eccezioni.
  }

  // Se il costruttore e il distruttore non sono sufficienti per impostare
  // e ripulire ciascun test, è possibile definire i seguenti metodi:
  void SetUp() override {
     // Il codice qui verrà chiamato immediatamente dopo il costruttore (subito
     // prima di ogni test).
  }

  void TearDown() override {
     // Il codice qui verrà chiamato immediatamente dopo ogni test (subito
     // prima del distruttore).
  }

  // I membri della classe dichiarati qui possono essere utilizzati da tutti i test nella test suite
  // per Foo.
};
// Tests that the Foo::Bar() method does Abc.
TEST_F(FooTest, MethodBarDoesAbc) {
  const std::string input_filepath = "this/package/testdata/myinputfile.dat";
  const std::string output_filepath = "this/package/testdata/myoutputfile.dat";
  Foo f;
  EXPECT_EQ(f.Bar(input_filepath, output_filepath), 0);
}
// Tests that Foo does Xyz.
TEST_F(FooTest, DoesXyz) {
  // Esegue la funzionalità Xyz di Foo.
}
}  // namespace
}  // namespace project
}  // namespace my
int main(int argc, char **argv) {
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}

```

La funzione `testing::InitGoogleTest()` analizza la riga di comando per i flag di GoogleTest e rimuove tutti i flag riconosciuti. Ciò consente all'utente di controllare il comportamento di un programma di test tramite vari flag, di cui parleremo nella [AdvancedGuide](advanced.md). Si **deve** chiamare questa funzione prima di chiamare `RUN_ALL_TESTS()`, altrimenti i flag non verranno inizializzati correttamente.

Su Windows, `InitGoogleTest()` funziona anche con stringhe estese [wide], quindi può essere utilizzato anche in programmi compilati in modalità `UNICODE`.

Ma forse si sta pensando che scrivere tutte queste funzioni di `main` sia troppo? Siamo completamente d'accordo ed è per questo che Google Test fornisce un'implementazione di base di main(). Se soddisfa le esigenze, basta linkare il test alla libreria `gtest_main` e si è a posto.

{: .callout .note}
NOTA: `ParseGUnitFlags()` è deprecato a favore di `InitGoogleTest()`.

## Limitazioni Note

*   Google Test è progettato per essere thread-safe. The implementation is thread-safe
    on systems where the `pthreads` library is available. It is currently
*unsafe* to use Google Test assertions from two threads concurrently on
    other systems (e.g. Windows). In most tests this is not an issue as usually
    the assertions are done in the main thread. If you want to help, you can
    volunteer to implement the necessary synchronization primitives in
`gtest-port.h` for your platform.
