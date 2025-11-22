# Argomenti avanzati di GoogleTest

## Introduzione

Dopo aver letto la [Guida di GoogleTest](primer.md) e imparato a scrivere test utilizzando GoogleTest, è il momento di imparare dei nuovi trucchi. Questo documento illustrerà altre asserzioni e come costruire messaggi di errore complessi, propagare errori fatali, riutilizzare e velocizzare fixture e utilizzare vari flag con i test.

## Altre Asserzioni

Questa sezione copre alcune asserzioni usate meno frequentemente, ma comunque significative.

### Successi e Fallimento Espliciti

Vedere [Explicit Success and Failure](reference/assertions.md#success-failure) nei "Riferimenti sulle Asserzioni".

### Asserzioni di Eccezioni

Vedere [Exception Assertions](reference/assertions.md#exceptions) nelle "Asserzioni di Eccezioni".

### Asserzioni di Predicati per del Migliori Messaggi di Errore

Anche se GoogleTest dispone di un ricco insieme di asserzioni, queste non potranno mai essere complete, poiché è impossibile (e non è nemmeno una buona idea) prevedere tutti gli scenari in cui un utente potrebbe imbattersi. Pertanto, a volte un utente deve utilizzare `EXPECT_TRUE()` per verificare un'espressione complessa, in mancanza di una macro migliore. Questo ha il problema di non mostrare i valori delle parti dell'espressione, rendendo difficile capire cosa è andato storto. Come soluzione alternativa, alcuni utenti scelgono di costruirsi da soli il messaggio di errore, accodandolo a `EXPECT_TRUE()`. Tuttavia, ciò risulta problematico, soprattutto quando l'espressione presenta effetti collaterali o è costosa da valutare.

GoogleTest offre tre diverse opzioni per risolvere questo problema:

#### Utilizzo di una Funzione Booleana Esistente

Se c'è già una funzione o un funtore che restituisce `bool` (o un tipo che può essere convertito implicitamente in `bool`), lo si può usare in un'*predicate
assertion* (asserzione di predicato) per ottenere gratuitamente la stampa degli argomenti della funzione. Vedere [`EXPECT_PRED*`](reference/assertions.md#EXPECT_PRED) nei "Riferimenti sulle Asserzioni" per i dettagli.

#### Utilizzo di una Funzione che Restituisce un AssertionResult

Sebbene `EXPECT_PRED*()` e similli siano utili per un lavoro veloce, la sintassi non è soddisfacente: si devono usare macro diverse per caratteristiche diverse, e sembra più Lisp che C++. La classe `::testing::AssertionResult` risolve questo problema.

Un oggetto `AssertionResult` rappresenta il risultato di un'asserzione (sia che si tratti di un successo che di un fallimento, e un messaggio associato). Un `AssertionResult` si può creare utilizzando una di queste funzioni "factory":

```c++
namespace testing {
// Returns an AssertionResult object to indicate that an assertion has
// succeeded.
AssertionResult AssertionSuccess();
// Returns an AssertionResult object to indicate that an assertion has
// failed.
AssertionResult AssertionFailure();
}
```

È poi possibile utilizzare l'operatore `<<` per lo streaming dei messaggi all'oggetto `AssertionResult`.

Per avere messaggi più leggibili nelle asserzioni booleane (ad esempio `EXPECT_TRUE()`), si scrive una funzione predicato che restituisca `AssertionResult` anziché `bool`. Per esempio, se si definisce `IsEven()` come:

```c++
testing::AssertionResult IsEven(int n) {
  if ((n % 2) == 0)
    return testing::AssertionSuccess();
  else
    return testing::AssertionFailure() << n << " is odd";
}

```

invece di:

```c++
bool IsEven(int n) {
  return (n % 2) == 0;
}
```

l'asserzione fallita, `EXPECT_TRUE(IsEven(Fib(4)))`, stamperà:

```none
Value of: IsEven(Fib(4))
  Actual: false (3 is odd)
Expected: true
```

invece di un più opaco

```none
Value of: IsEven(Fib(4))
  Actual: false
Expected: true

```

Per ottenere messaggi informativi anche in `EXPECT_FALSE` e in `ASSERT_FALSE` (un terzo delle asserzioni booleane nel codebase di Google sono negative) e si è d'accordo nel rendere il predicato più lento in il caso di successo, si può fornire un messaggio in caso di successo:

```c++
testing::AssertionResult IsEven(int n) {
  if ((n % 2) == 0)
    return testing::AssertionSuccess() << n << " is even";
  else
    return testing::AssertionFailure() << n << " is odd";
}

```

Quindi verrà stampata l'istruzione `EXPECT_FALSE(IsEven(Fib(6)))`

```none
  Value of: IsEven(Fib(6))
     Actual: true (8 is even)
  Expected: false

```

#### Utilizzo di un Predicato-Formatter

Se si ritiene insoddisfacente il messaggio di default generato da [`EXPECT_PRED*`](reference/assertions.md#EXPECT_PRED) e da [`EXPECT_TRUE`](reference/assertions.md#EXPECT_TRUE) o alcuni argomenti del predicato supportano lo streaming su `ostream`, si possono alternativamente utilizzare *asserzioni predicato-formatter* per personalizzare *completamente* la modalità di formattazione del messaggio. Per i dettagli, vedere [`EXPECT_PRED_FORMAT*`](reference/assertions.md#EXPECT_PRED_FORMAT) nei "Riferimenti sulle Asserzioni".

### Confronto in Virgola Mobile

Vedere [Floating-Point Comparison](reference/assertions.md#floating-point) nei "Riferimenti sulle Asserzioni".

#### Predicato in Virgola Mobile-Funzioni di Formattazione

Alcune operazioni in virgola mobile sono utili, ma non vengono utilizzate tanto spesso. Per evitare un'esplosione di nuove macro, le forniamo come funzioni in formato predicato, utilizzabili nella macro di asserzione del predicato [`EXPECT_PRED_FORMAT2`](reference/assertions.md#EXPECT_PRED_FORMAT), ad esempio:

```c++
using ::testing::FloatLE;
using ::testing::DoubleLE;
...
EXPECT_PRED_FORMAT2(FloatLE, val1, val2);
EXPECT_PRED_FORMAT2(DoubleLE, val1, val2);

```

Il codice precedente controlla che `val1` sia inferiore o approssimativamente uguale a `val2`.

### Asserzioni con l'uso dei Matcher di gMock

Vedere [`EXPECT_THAT`](reference/assertions.md#EXPECT_THAT) nei "Riferimenti sulle Asserzioni".

### Altre Asserzioni di Stringa

(Se non è stato fatto, è opportuno leggere prima la sezione [precedente](#asserting-using-gmock-matchers)).

Si possono usare i [matcher di stringhe](reference/matchers.md#string-matchers) di gMock con [`EXPECT_THAT`](reference/assertions.md#EXPECT_THAT) per fare altri tipi di confronti tra stringhe (sotto-stringa, prefisso, suffisso, espressione regolare, ecc.). Per esempio,

```c++
using ::testing::HasSubstr;
using ::testing::MatchesRegex;
...
  ASSERT_THAT(foo_string, HasSubstr("needle"));
  EXPECT_THAT(bar_string, MatchesRegex("\\w*\\d+"));

```

### Asserzioni HRESULT di Windows

Vedere [Windows HRESULT Assertions](reference/assertions.md#HRESULT) nei "Riferimenti sulle Asserzioni".

### Tipi di Asserzioni

Si può chiamare la funzione

```c++
::testing::StaticAssertTypeEq<T1, T2>();

```

per asserire (affermare) che i tipi `T1` e `T2` sono gli stessi. La funzione non fa nulla se l'asserzione è soddisfatta. Se i tipi sono diversi, la chiamata alla funzione non verrà compilata, il messaggio di errore del compilatore dirà che `T1 e T2 non sono dello stesso tipo` e molto probabilmente (a seconda del compilatore) mostrerà i valori effettivi di `T1` e di `T2`. Ciò è utile principalmente all'interno del codice template.

**Avvertenza**: Se utilizzato all'interno di una funzione membro di una classe template o di una funzione template, `StaticAssertTypeEq<T1, T2>()` è efficace solo se viene istanziata la funzione. Ad esempio, dato:

```c++
template <typename T> class Foo {
 public:
  void Bar() { testing::StaticAssertTypeEq<int, T>(); }
};

```

il codice:

```c++
void Test1() { Foo<bool> foo; }

```

non genererà un errore del compilatore, poiché `Foo<bool>::Bar()` non viene mai effettivamente istanziato. Occorre, invece:

```c++
void Test2() { Foo<bool> foo; foo.Bar(); }

```

per causare un errore del compilatore.

### Posizionamento delle Asserzioni

Le asserzioni si possono usare in qualsiasi funzione C++. In particolare, non deve essere un metodo della classe fixture del test. L'unico vincolo è che le asserzioni che generano un errore irreversibile (`FAIL*` e `ASSERT_*`) sono utilizzabili solo nelle funzioni che restituiscono void. Questa è una conseguenza del fatto che Google non utilizza le eccezioni. Inserendola in una funzione non void si otterrà un errore di compilazione confuso del tipo `"error: void value not ignored as it ought to be"` o `"cannot
initialize return object of type 'bool' with an rvalue of type 'void'"` o `"error: no viable conversion from 'void' to 'string'"`.

Per usare asserzioni fatali in una funzione che restituisce non void, un'opzione è fare in modo che la funzione restituisca il valore in un parametro di output. Per esempio, si può riscrivere `T2 Foo(T1 x)` in `void Foo(T1 x, T2* result)`. `*result` deve contenere un valore sensato anche quando la funzione ritorna prematuramente. Dato che la funzione ora restituisce `void`, si può utilizzare qualsiasi asserzione al suo interno.

Se non è possibile cambiare il tipo della funzione, si devono semplicemente usare asserzioni che generano errori non fatali, come `ADD_FAILURE*` e `EXPECT_*`.

{: .callout .note}
NOTA: Costruttori e distruttori non sono considerati funzioni che restituiscono void, secondo le specifiche del linguaggio C++, e quindi non è possibile utilizzare asserzioni fatali al loro interno; provandoci si riceverà un errore di compilazione. Invece, o si chiama `abort` e si manda in crash tutto l'eseguibile del test, oppure si inserisce l'asserzione fatale in una funzione `SetUp`/`TearDown`; vedere [constructor/destructor vs. `SetUp`/`TearDown`](faq.md#CtorVsSetUp)

{: .callout .warning}
ATTENZIONE: Un'asserzione fatale in una funzione helper (metodo privato che restituisce void) chiamata da un costruttore o da un distruttore non termina il test corrente, come potrebbe suggerire l'intuito: ritorna semplicemente dal costruttore o anticipatamente dal distruttore, forse lasciando l'oggetto in uno stato di parzialmente creato o di parzialmente distrutto! Quasi certamente si vuole, invece, `abort`ire o usare `SetUp`/`TearDown`.

## Saltare l'esecuzione del test

Per quanto riguarda le asserzioni `SUCCEED()` e `FAIL()`, si può evitare l'esecuzione dei test successivi a runtime con la macro `GTEST_SKIP()`. Ciò è utile quando si devono verificare le precondizioni del sistema sotto test durante il runtime e saltare i test in modo significativo.

`GTEST_SKIP()` è utilizzabile nei casi di test individuali o nei metodi `SetUp()` di una classe derivata da `::testing::Environment` o da `::testing::Test`.
Per esempio:

```c++
TEST(SkipTest, DoesSkip) {
  GTEST_SKIP() << "Skipping single test";
  EXPECT_EQ(0, 1);  // Won't fail; it won't be executed
}
class SkipFixture : public ::testing::Test {
 protected:
  void SetUp() override {
    GTEST_SKIP() << "Skipping all tests for this fixture";
  }
};
// Tests for SkipFixture won't be executed.
TEST_F(SkipFixture, SkipsOneTest) {
  EXPECT_EQ(5, 7);  // Won't fail
}

```

Come con le macro delle asserzioni, si può accodare un messaggio personalizzato in `GTEST_SKIP()`.

## Insegnare a GoogleTest Come Stampare i Propri Valori

Quando un'asserzione di test come `EXPECT_EQ` fallisce, GoogleTest stampa i valori degli argomenti per eseguire il debug. Lo fa utilizzando una stampante con valori estensibile dall'utente.

Questa stampante sa come stampare i tipi nativi di C++, gli array, i contenitori STL e qualsiasi tipo che supporti l'operatore `<<`. Per gli altri tipi, stampa i byte grezzi nel valore e spera che l'utente possa capirlo.

Come accennato in precedenza, la stampante è *estensibile*. Ciò significa che le si può insegnare a stampare un proprio tipo particolare piuttosto che eseguirne il dump dei byte. Per farlo, si definisce un overload di `AbslStringify()` come una funzione template `friend` per il proprio tipo:

```cpp
namespace foo {
class Point {  // We want GoogleTest to be able to print instances of this.
  ...
  // Si fornisce un overload friend.
  template <typename Sink>
  friend void AbslStringify(Sink& sink, const Point& point) {
    absl::Format(&sink, "(%d, %d)", point.x, point.y);
  }

  int x;
  int y;
};
// If you can't declare the function in the class it's important that the
// AbslStringify overload is defined in the SAME namespace that defines Point.
// Le regole di ricerca del C++ si basano su questo.
enum class EnumWithStringify { kMany = 0, kChoices = 1 };
template <typename Sink>
void AbslStringify(Sink& sink, EnumWithStringify e) {
  absl::Format(&sink, "%s", e == EnumWithStringify::kMany ? "Many" : "Choices");
}
}  // namespace foo
```

{: .callout .note}
Nota: `AbslStringify()` usa un generico buffer "sink" per costruire la sua stringa. Per ulteriori informazioni sulle operazioni supportate sul sink di `AbslStringify()`, vedere go/abslstringify.

`AbslStringify()` può anche usare, di `absl::StrFormat`, l'identificatore di tipo "tuttofare" `%v` all'interno delle proprie stringhe di formato per eseguire la deduzione del tipo. Il `Point` sopra potrebbe, per esempio, essere formattato come `"(%v, %v)"` e dedurre i valori `int` come `%d`.

A volte, `AbslStringify()` potrebbe non essere un'opzione: il team potrebbe voler stampare tipi con informazioni di debug aggiuntive solo a scopo di test. Se è così, si può definire una funzione `PrintTo()` come questa:

```c++
#include <ostream>
namespace foo {
class Point {
  ...
  friend void PrintTo(const Point& point, std::ostream* os) {
    *os << "(" << point.x << "," << point.y << ")";
  }

  int x;
  int y;
};
// If you can't declare the function in the class it's important that PrintTo()
// is defined in the SAME namespace that defines Point.  Le regole di ricerca del C++
// si basano su questo.
void PrintTo(const Point& point, std::ostream* os) {
    *os << "(" << point.x << "," << point.y << ")";
}
}  // namespace foo
```

Se è stato definito sia `AbslStringify()` che `PrintTo()`, quest'ultimo verrà utilizzato da GoogleTest. Ciò consente di personalizzare il modo in cui il valore appare nell'output di GoogleTest senza influenzare il codice che si basa sul comportamento di `AbslStringify()`.

Se si dispone di un operatore `<<` esistente e si vuol definire un `AbslStringify()`, quest'ultimo verrà utilizzato per la stampa di GoogleTest.

Per stampare in proprio un valore `x` utilizzando la stampante dei valori di GoogleTest, basta chiamare `::testing::PrintToString(x)`, che restituisce una `std::string`:

```c++
vector<pair<Point, int> > point_ints = GetPointIntVector();
EXPECT_TRUE(IsCorrectPointIntVector(point_ints))
    << "point_ints = " << testing::PrintToString(point_ints);

```

Per maggiori dettagli su `AbslStringify()` e la sua integrazione con le altre librerie, vedere go/abslstringify.

## I Death Test

In molte applicazioni sono presenti asserzioni che possono causare errori dell'applicazione se una condizione non viene soddisfatta. Questi controlli di coerenza, per verificare che il programma sia in uno stato sicuramente buono, sono destinati a fallire il prima possibile dopo che uno stato del programma viene corrotto. Se l'asserzione verifica la condizione sbagliata, il programma potrebbe procedere in uno stato errato, che potrebbe portare al danneggiamento della memoria, a buchi di sicurezza o peggio. Pertanto è di vitale importanza verificare che tali affermazioni funzionino come previsto.

Poiché questi controlli sulle precondizioni causano la morte dei processi, questi test si chiamano _death test_. Più in generale, qualsiasi test che controlli se un programma termini (tranne che per un'eccezione) nel modo previsto è un "death test".

Si noti che se un pezzo di codice genera un'eccezione, non la si considera "morte" ai fini dei "death test", poiché il chiamante del codice potrebbe rilevare l'eccezione ed evitare il crash. Per verificare le eccezioni generate dal codice, consultare [Asserzioni di Eccezioni](#ExceptionAssertions).

Per testare gli errori `EXPECT_*()/ASSERT_*()` nel codice, consultare ["Catching" degli Errori](#catching-failures).

### Come Scrivere un Death Test

GoogleTest fornisce macro di asserzioni per supportare i death test. Per i dettagli, vedere [Asserzioni Death](reference/assertions.md#death) nei Riferimenti sulle Asserzioni.

Per scrivere un death test, basta usare una delle macro nella funzione di test.
Per esempio,

```c++
TEST(MyDeathTest, Foo) {
  // Questo death test usa un'istruzione composta.
  ASSERT_DEATH({
    int n = 5;
    Foo(&n);
  }, "Error on line .* of Foo()");
}
TEST(MyDeathTest, NormalExit) {
  EXPECT_EXIT(NormalExit(), testing::ExitedWithCode(0), "Success");
}
TEST(MyDeathTest, KillProcess) {
  EXPECT_EXIT(KillProcess(), testing::KilledBySignal(SIGKILL),
              "Sending myself unblockable signal");
}

```

verifica che:

*   la chiamata a `Foo(5)` provoca la morte del processo con il messaggio di errore indicato,
*   calling `NormalExit()` causes the process to print `"Success"` to stderr and
    exit with exit code 0, and
*   la chiamata a `KillProcess()` termina [kill] il processo con il segnale `SIGKILL`.

Se necessario, il corpo della funzione di test può contenere anche altre asserzioni e dichiarazioni.

Notare che un death test si preoccupa solo di tre cose:

1.  con l'`istruzione` si abortisce o si esce dal processo?
2.  (in the case of `ASSERT_EXIT` and `EXPECT_EXIT`) does the exit status
    satisfy `predicate`? Or (in the case of `ASSERT_DEATH` and `EXPECT_DEATH`)
    is the exit status non-zero? E
3.  l'output su stderr corrisponde al `matcher`?

In particolare, se l'`istruzione` genera un errore `ASSERT_*` o `EXPECT_*`, **non** farà fallire il death test, poiché le asserzioni di GoogleTest non interrompono il processo.

### Nomenclatura del Death Test

{: .callout .important}
IMPORTANTE: Consigliamo vivamente di seguire la convenzione di denominare la **test suite** (not il test) `*DeathTest` quando contiene un death test, come mostrato nell'esempio precedente. La seguente sezione [I Death Test E i Thread](#death-tests-and-threads) spiega il perché.

Se una classe fixture è condivisa tra test normali e death test, si può utilizzare `using` o `typedef` per introdurre un alias per la classe fixture ed evitare di duplicarne il codice:

```c++
class FooTest : public testing::Test { ... };
using FooDeathTest = FooTest;
TEST_F(FooTest, DoesThis) {
  // normal test
}
TEST_F(FooDeathTest, DoesThat) {
  // death test
}

```

### Sintassi delle Espressioni Regolari

Quando si builda con Bazel e utilizzando Abseil, GoogleTest usa la sintassi [RE2](https://github.com/google/re2/wiki/Syntax). Altrimenti, per i sistemi POSIX (Linux, Cygwin, Mac), GoogleTest utilizza la sintassi [POSIX extended regular expression](https://www.opengroup.org/onlinepubs/009695399/basedefs/xbd_chap09.html#tag_09_04). Per conoscere la sintassi POSIX, si potrebbe leggere questa [voce di Wikipedia](https://en.wikipedia.org/wiki/Regular_expression#POSIX_extended).

Su Windows, GoogleTest utilizza la propria semplice implementazione di espressioni regolari. Mancano molte funzionalità. Ad esempio, non supportiamo l'unione (`"x|y"`), il raggruppamento (`"(xy)"`), le parentesi quadre (`"[xy]"`) e il conteggio delle ripetizioni (`"x{5,7}"`), tra le altre cose. Di seguito è riportato ciò che supportiamo (`A` indica un carattere letterale, un punto (`.`), o una singola sequenza di escape `\\ `; `x` e `y` denotano espressioni regolari):

| Espressione | Significato |
---------- | --------------------------------------------------------------
| `c` | corrisponde a qualsiasi carattere letterale `c` |
| `\\d` | corrisponde a qualsiasi cifra decimale |
| `\\D` | corrisponde a qualsiasi carattere che non sia una cifra decimale |
| `\\f` | corrisponde a `\f` |
| `\\n` | corrisponde a `\n` |
| `\\r` | corrisponde a `\r` |
| `\\s` | corrisponde a qualsiasi spazio 'bianco' ASCII, incluso `\n` |
| `\\S` | corrisponde a qualsiasi carattere che non sia uno spazio 'bianco' |
| `\\t` | corrisponde a `\t` |
| `\\v` | corrisponde a `\v` |
| `\\w` | corrisponde a qualsiasi lettera, `_`, o cifra decimale |
| `\\W` | corrisponde a qualsiasi carattere che non corrisponde a `\\w` |
| `\\c` | corrisponde a qualsiasi carattere letterale `c`, che deve essere un segno di punteggiatura |
| `.` | corrisponde a qualsiasi carattere singolo tranne `\n` |
| `A?` | corrisponde a 0 o 1 occorrenze di `A` |
| `A*` | corrisponde a 0 o più occorrenze di `A` |
| `A+` | corrisponde a 1 o più occorrenze di `A` |
| `^` | corrisponde all'inizio di una stringa (non a quello di ogni riga) |
| `$` | corrisponde alla fine di una stringa (non a quella di ogni riga) |
| `xy` | corrisponde a `x` seguito da `y` |

Per aiutare a determinare quale funzionalità è disponibile sul sistema, GoogleTest definisce le macro per governare quale espressione regolare sta utilizzando. Le macro sono: `GTEST_USES_SIMPLE_RE=1` o `GTEST_USES_POSIX_RE=1`. Per far funzionare in ogni caso i death test, si può usare `#if` con queste macro o usare solo la sintassi più limitata.

### Come Funziona

Vedere [Asserzioni Death](reference/assertions.md#death) nei Riferimenti sulle Asserzioni.

### I Death Test E i Thread

Il motivo dei due stili di death test ha a che fare con la "thread safety". A causa dei noti problemi con il forking in presenza dei thread, i death test dovrebbero essere eseguiti in un contesto a thread singolo. A volte, però, non è possibile organizzare questo tipo di ambiente. Ad esempio, i moduli inizializzati staticamente possono avviare i thread prima che venga raggiunto il main. Una volta creati i thread, potrebbe essere difficile o impossibile ripulirli.

GoogleTest ha tre funzionalità destinate ad aumentare la consapevolezza sui problemi di threading.

1.  A warning is emitted if multiple threads are running when a death test is
    encountered.
2.  Test suites with a name ending in "DeathTest" are run before all other
    tests.
3.  It uses `clone()` instead of `fork()` to spawn the child process on Linux
    (`clone()` is not available on Cygwin and Mac), as `fork()` is more likely
    to cause the child to hang when the parent process has multiple threads.

È perfettamente corretto creare thread all'interno di una dichiarazione di death test; vengono eseguiti in un processo separato e non possono influenzare il genitore.

### Stili dei Death Test

Lo stile "threadsafe" del death test è stato introdotto per mitigare i rischi dei test in un ambiente multithread. Scambia un aumento del tempo di esecuzione del test (potenzialmente in modo drammatico) con una migliore sicurezza del thread.

Il framework di test automatizzato non imposta il flag dello stile. Si può scegliere un stile dei death test, impostando il flag a livello di codice:

```c++
GTEST_FLAG_SET(death_test_style, "threadsafe");

```

Lo si può fare nel `main()` per impostare lo stile per tutti i death test nel binario o nei singoli test. Ricordarsi che i flag vengono salvati prima di eseguire ciascun test e ripristinati alla fine, quindi non è necessario farlo esplicitamente. Per esempio:

```c++
int main(int argc, char** argv) {
  testing::InitGoogleTest(&argc, argv);
  GTEST_FLAG_SET(death_test_style, "fast");
  return RUN_ALL_TESTS();
}
TEST(MyDeathTest, TestOne) {
  GTEST_FLAG_SET(death_test_style, "threadsafe");

  // Questo test viene eseguito nello stile "threadsafe":
  ASSERT_DEATH(ThisShouldDie(), "");
}
TEST(MyDeathTest, TestTwo) {
  // Questo test viene eseguito nello stile "fast":
  ASSERT_DEATH(ThisShouldDie(), "");
}

```

### Avvertenze

L'argomento `statement` di `ASSERT_EXIT()` può essere qualsiasi istruzione C++ valida. Se lascia la funzione corrente tramite un'istruzione `return` o per un'eccezione, il death test viene considerato fallito. Alcune macro di GoogleTest potrebbero restituire dalla funzione corrente (ad esempio `ASSERT_TRUE()`), quindi sono da evitarle in `statement`.

Poiché `statement` viene eseguito nel processo figlio, qualsiasi effetto collaterale in memoria (ad esempio la modifica di una variabile, il rilascio di memoria, ecc.) da esso causato *non* sarà osservabile nel processo genitore. In particolare, se si rilascia memoria in un death test, il programma fallirà il controllo dell'heap poiché il processo principale non vedrà mai la memoria recuperata. Per risolvere questo problema, si può

1.  cercare di non liberare la memoria in un death test;
2.  liberare nuovamente la memoria nel processo genitore; o
3.  non utilizzare l'heap checker nel programma.

A causa di un dettaglio implementativo, non è possibile inserire più asserzioni di death test sulla stessa riga; in caso contrario la compilazione fallirà con un messaggio di errore non evidente.

Nonostante la migliorata sicurezza dei thread offerta dallo stile del death test "threadsafe", problemi dei thread come deadlock sono ancora possibili in presenza di gestori registrati con `pthread_atfork(3)`.

## Uso delle Asserzioni nelle Sub-routine

{: .callout .note}
Nota: Per inserire una serie di asserzioni di test in una subroutine per verificare una condizione complessa, considerare invece l'utilizzo di [un matcher GMock personalizzato](gmock_cook_book.md#NewMatchers). Ciò consente di fornire un messaggio di errore più leggibile in caso di errore ed evitare tutti i problemi descritti di seguito.

### Aggiungere Trace alle Asserzioni

Se una sub-routine di test viene chiamata da più posti, quando un'asserzione al suo interno fallisce, può essere difficile dire da quale invocazione della sub-routine provenga il fallimento. È possibile alleviare questo problema utilizzando log aggiuntivi o messaggi di errore personalizzati, ma ciò di solito è ingombrante per i test. Una soluzione migliore è quella di utilizzare la macro `SCOPED_TRACE` o l'utility `ScopedTrace`:

```c++
SCOPED_TRACE(message);

```

```c++
ScopedTrace trace("file_path", line_number, message);

```

dove `message` può essere qualsiasi cosa accodabile a `std::ostream`. La macro `SCOPED_TRACE` farà sì che il nome del file corrente, il numero di riga e il messaggio specificato vengano aggiunti in ogni messaggio di errore. `ScopedTrace` accetta nomi di file e numeri di riga espliciti negli argomenti, il che è utile per scrivere helper di test. L'effetto verrà annullato quando il controllo lascerà lo scope lessicale corrente.

Per esempio,

```c++
10: void Sub1(int n) {
11:   EXPECT_EQ(Bar(n), 1);
12:   EXPECT_EQ(Bar(n + 1), 2);
13: }
14:
15: TEST(FooTest, Bar) {
16:   {
17:     SCOPED_TRACE("A");  // Questo punto di trace verrà incluso in
18:                         // in ogni errore in questo scope.
19:     Sub1(1);
20:   }
21:   // Adesso non lo farà più.
22:   Sub1(9);
23: }

```

potrebbe generare messaggi come questi:

```none
path/to/foo_test.cc:11: Failure
Value of: Bar(n)
Expected: 1
  Actual: 2
Google Test trace:
path/to/foo_test.cc:17: A
path/to/foo_test.cc:12: Failure
Value of: Bar(n + 1)
Expected: 2
  Actual: 3

```


Senza il trace, sarebbe stato difficile sapere da quale invocazione di `Sub1()` provengono rispettivamente i due errori. (Si potrebbe aggiungere un messaggio extra a ciascuna asserzione in `Sub1()` per indicare il valore di `n`, ma è noioso).

Alcuni suggerimenti sull'utilizzo di `SCOPED_TRACE`:

1.  With a suitable message, it's often enough to use `SCOPED_TRACE` at the
    beginning of a sub-routine, instead of at each call site.
2.  When calling sub-routines inside a loop, make the loop iterator part of the
    message in `SCOPED_TRACE` such that you can know which iteration the failure
    is from.
3.  Sometimes the line number of the trace point is enough for identifying the
    particular invocation of a sub-routine. In this case, you don't have to
    choose a unique message for `SCOPED_TRACE`. Basta usare `""`.
4.  You can use `SCOPED_TRACE` in an inner scope when there is one in the outer
    scope. In this case, all active trace points will be included in the failure
    messages, in reverse order they are encountered.
5.  The trace dump is clickable in Emacs - hit `return` on a line number and
    you'll be taken to that line in the source file!

### Propagazione degli Errori Fatali

Un errore comune quando si utilizzano `ASSERT_*` e `FAIL*` è non capire che quando falliscono interrompono solo la _funzione corrente_, non l'intero test. Per esempio, il seguente test genererà un segfault:

```c++
void Subroutine() {
  // Genera un errore fatale e interrompe [abort] la funzione corrente.
  ASSERT_EQ(1, 2);
  // Quanto segue non verrà eseguito.
  ...
}
TEST(FooTest, Bar) {
  Subroutine();  // Il comportamento previsto è che l'errore fatale
                 // in Subroutine() abortisca l'intero test.
  // Il comportamento reale: la funzione continua al ritorno di Subroutine().
  int* p = nullptr;
  *p = 3;  // Segfault!
}

```

Per alleviare questo problema, GoogleTest fornisce tre diverse soluzioni. Potresti utilizzare le eccezioni, le asserzioni `(ASSERT|EXPECT)_NO_FATAL_FAILURE` o la funzione `HasFatalFailure()`. Sono tutte descritte nelle due sottosezioni seguenti.

#### Asserzione sulle Subroutine con un'eccezione

Il seguente codice può trasformare ASSERT-failure in un'eccezione:

```c++
class ThrowListener : public testing::EmptyTestEventListener {
  void OnTestPartResult(const testing::TestPartResult& result) override {
    if (result.type() == testing::TestPartResult::kFatalFailure) {
      throw testing::AssertionException(result);
    }

  }
};
int main(int argc, char** argv) {
  ...
  testing::UnitTest::GetInstance()->listeners().Append(new ThrowListener);
  return RUN_ALL_TESTS();
}

```

Questo listener deve essere aggiunto dopo gli altri listener, se ce ne sono, altrimenti non vedranno `OnTestPartResult` fallire.

#### Asserzione sulle Subroutine

Come mostrato sopra, se il test chiama una subroutine che presenta un errore `ASSERT_*`, il test continuerà dopo il ritorno della subroutine. Questo potrebbe non essere quello che si vuole.

Spesso le persone vogliono che i fallimenti fatali si propaghino come le eccezioni. Per questo GoogleTest offre le seguenti macro:

| Asserzione fatale | Asserzione non-fatale | Verifica |
------------------------------------- | ------------------------------------- | --------
| `ASSERT_NO_FATAL_FAILURE(statement);` | `EXPECT_NO_FATAL_FAILURE(statement);` | `statement` non genera nuovi errori fatali nel thread corrente. |

Vengono controllati solo gli errori nel thread che esegue l'asserzione per determinare il risultato di questo tipo di asserzioni. Se `statement` crea nuovi thread, gli errori in questi thread vengono ignorati.

Esempi:

```c++
ASSERT_NO_FATAL_FAILURE(Foo());
int i;
EXPECT_NO_FATAL_FAILURE({
  i = Bar();
});

```

Le asserzioni provenienti da più thread non sono attualmente supportate in Windows.

#### Verifica degli Errori nel Test Corrente

`HasFatalFailure()` nella classe `::testing::Test` restituisce `true` se un'asserzione nel test corrente ha subito un fallimento fatale. Ciò consente alle funzioni di rilevare errori fatali in una subroutine e di tornare anticipatamente.

```c++
class Test {
 public:
  ...
  static bool HasFatalFailure();
};
```

L'utilizzo tipico, che sostanzialmente simula il comportamento della generazione di un'eccezione, è:

```c++
TEST(FooTest, Bar) {
  Subroutine();
  // Abortisce se Subroutine() ha avuto un errore fatale.
  if (HasFatalFailure()) return;
  // Quanto segue non verrà eseguito.
  ...
}

```

Se `HasFatalFailure()` viene utilizzato al di fuori di `TEST()` , `TEST_F()` , o di una fixture, si deve aggiungere il prefisso `::testing::Test::`, come in:

```c++
if (testing::Test::HasFatalFailure()) return;

```

Allo stesso modo, `HasNonfatalFailure()` restituisce `true` se il test corrente ha almeno un errore non fatale e `HasFailure()` restituisce `true ` se il test corrente presenta almeno un errore di entrambi i tipi.

## Log di Informazioni Aggiuntive

Nel codice del test, si può chiamare `RecordProperty("key", value)` per loggare informazioni aggiuntive, dove `value` può essere una stringa o un `int`. L'*iltimo* valore registrato per una chiave verrà emesso nell'[output XML](#generating-an-xml-report) se se ne specifica uno. Per esempio, il test

```c++
TEST_F(WidgetUsageTest, MinAndMaxWidgets) {
  RecordProperty("MaximumWidgets", ComputeMaxUsage());
  RecordProperty("MinimumWidgets", ComputeMinUsage());
}

```

restituirà XML in questo modo:

```xml
  ...
    <testcase name="MinAndMaxWidgets" file="test.cpp" line="1" status="run" time="0.006" classname="WidgetUsageTest" MaximumWidgets="12" MinimumWidgets="9" />
  ...
```

{: .callout .note}
> NOTA:
>
> *   `RecordProperty()` è un membro statico della classe `Test`. Therefore it
>     needs to be prefixed with `::testing::Test::` if used outside of the
> `TEST` body and the test fixture class.
> *   *`key`* must be a valid XML attribute name, and cannot conflict with the
>     ones already used by GoogleTest (`name`, `status`, `time`, `classname`,
> `type_param`, and `value_param`).
> *   È consentito chiamare `RecordProperty()` al di fuori della durata [lifespan] di un test.
>     If it's called outside of a test but between a test suite's
> `SetUpTestSuite()` and `TearDownTestSuite()` methods, it will be
>     attributed to the XML element for the test suite. If it's called outside
>     of all test suites (e.g. in a test environment), it will be attributed to
>     the top-level XML element.

## Condivisione delle Risorse Tra Test nella Stessa Test Suite

GoogleTest crea un nuovo oggetto fixture per ogni test per rendere i test indipendenti e più facili da debuggare. Tuttavia, a volte i test utilizzano risorse costose da configurare, rendendo il modello "one-copy-per-test" proibitivamente costoso.

Se i test non modificano la risorsa, non c'è alcun danno nel condividere una singola copia della risorsa. Pertanto, oltre alla configurazione/dismissione per ogni test, GoogleTest supporta anche la configurazione/dismissione per ogni test suite. Per usarlo:

1.  In your test fixture class (say `FooTest` ), declare as `static` some member
    variables to hold the shared resources.
2.  Outside your test fixture class (typically just below it), define those
    member variables, optionally giving them initial values.
3.  In the same test fixture class, define a public member function `static void
SetUpTestSuite()` (remember not to spell it as **`SetupTestSuite`** with a
    small `u`!) to set up the shared resources and a `static void
TearDownTestSuite()` function to tear them down.

Questo è tutto! GoogleTest chiama automaticamente `SetUpTestSuite()` prima di eseguire il *primo test* nella test suite `FooTest` (ovvero prima di creare il primo oggetto `FooTest`) e chiama `TearDownTestSuite()` dopo aver eseguito l'*ultimo test* al suo interno (ovvero dopo aver eliminato l'ultimo oggetto `FooTest`). Nel mezzo, i test possono utilizzare le risorse condivise.

Da ricordare che l'ordine dei test non è definito, quindi il codice non può dipendere da un test che ne precede o ne segue un altro. Inoltre, i test non devono modificare lo stato di alcuna risorsa condivisa oppure, se modificano lo stato, devono ripristinarlo al suo valore originale prima di passare il controllo al test successivo.

Notare che `SetUpTestSuite()` può essere chiamato più volte per una classe fixture che ha classi derivate, quindi non ci si deve aspettare che il codice nel corpo della funzione venga eseguito solo una volta. Inoltre, le classi derivate hanno ancora accesso alle risorse condivise definite come membri statici, quindi è necessaria un'attenta considerazione quando si gestiscono le risorse condivise per evitare "memory leak" se le risorse condivise non vengono ripulite correttamente in `TearDownTestSuite()`.

Ecco un esempio di configurazione e dismissione "per-test-suite":

```c++
class FooTest : public testing::Test {
 protected:
  // Configurazione "per-test-suite".
  // Chiamata prima del primo test in questa test suite.
  // Può essere omessa se non necessaria.
  static void SetUpTestSuite() {
    shared_resource_ = new ...;
    // Se `shared_resource_` è **non deleted** in `TearDownTestSuite()`,
    // la riallocazione dovrebbe essere impedita perché potrebbe essere chiamato `SetUpTestSuite()`
    // nelle sottoclassi di FooTest portando a memory leak.
    //
    // if (shared_resource_ == nullptr) {
    //   shared_resource_ = new ...;
    // }
  }

  // Dismissione [tear-down] "per-test-suite".
  // Chiamata dopo l'ultimo test in questa test suite.
  // Può essere omessa se non necessaria.
  static void TearDownTestSuite() {
    delete shared_resource_;
    shared_resource_ = nullptr;
  }

  // È possibile definire la logica di impostazione "per-test" come al solito.
  void SetUp() override { ... }
  // È possibile definire la logica di dismissione "per-test" come al solito.
  void TearDown() override { ... }
  // Alcune risorse costose condivise da tutti i test.
  static T* shared_resource_;
};
T* FooTest::shared_resource_ = nullptr;
TEST_F(FooTest, Test1) {
  ... you can refer to shared_resource_ here ...
}
TEST_F(FooTest, Test2) {
  ... qui si può far riferimento a shared_resource_ ...
}

```

{: .callout .note}
NOTA: Sebbene il codice sopra dichiari `SetUpTestSuite()` protected, a volte potrebbe essere necessario dichiararlo pubblico, come quando lo si utilizza con `TEST_P`.

## Set-Up e Tear-Down Globali

Proprio come è possibile eseguire l'impostazione e la dismissione [tear-down] a livello di test e di test suite, è possibile farlo anche a livello di programma di test. Ecco come.

Per prima cosa, si crea una sottoclasse della classe `::testing::Environment` per definire un ambiente di test, che sappia come impostare e dismettere:

```c++
class Environment : public ::testing::Environment {
 public:
  ~Environment() override {}
  // Override per definire come impostare l'ambiente..
  void SetUp() override {}
  // Override per definire come dismettere [tear down] l'ambiente.
  void TearDown() override {}
};

```

Poi, si registra un'istanza della classe di ambiente con GoogleTest chiamando la funzione `::testing::AddGlobalTestEnvironment()`:

```c++
Environment* AddGlobalTestEnvironment(Environment* env);

```

Ora, quando viene chiamato `RUN_ALL_TESTS()`, prima chiama il metodo `SetUp()` di ciascun oggetto dell'ambiente, poi esegue i test se nessuno degli ambienti ha riportato errori fatali e `GTEST_SKIP()` non è stato chiamato. `RUN_ALL_TESTS()` chiama sempre `TearDown()` con ciascun oggetto dell'ambiente, indipendentemente dal fatto che i test siano stati eseguiti o meno.

È consentito registrare più oggetti dell'ambiente. In questa suite, il loro `SetUp()` verrà chiamato nell'ordine in cui sono registrati, e il loro `TearDown()` verrà chiamato nell'ordine inverso.

Si noti che GoogleTest assume la proprietà degli oggetti dell'ambiente registrati.
Pertanto **non vanno eliminati** manualmente.

Si deve chiamare `AddGlobalTestEnvironment()` prima di chiamare `RUN_ALL_TESTS()`,
probabilmente in `main()`. Se si usa `gtest_main`, lo si deve chiamare pria dell'avvio di `main()` affinché abbia effetto. Un modo per farlo è definire una variabile globale come questa:

```c++
testing::Environment* const foo_env =
    testing::AddGlobalTestEnvironment(new FooEnvironment);

```

Tuttavia, consigliamo vivamente di scrivere il `main()` e di chiamare `AddGlobalTestEnvironment()` lì, poiché fare affidamento sull'inizializzazione delle variabili globali rende il codice più difficile da leggere e potrebbe causare problemi quando si registrano più ambienti da diverse unità di traduzione e gli ambienti hanno dipendenze tra loro (ricordare che il compilatore non garantisce l'ordine in cui vengono inizializzate le variabili globali di diverse unità di traduzione).

## Test con Valori Parametrizzati

I *test con valori parametrizzati* consentono di testare il codice con parametri diversi senza scrivere più copie dello stesso test. Ciò è utile in diverse situazioni, ad esempio:

*   You have a piece of code whose behavior is affected by one or more
    command-line flags. You want to make sure your code performs correctly for
    various values of those flags.
*   Si vogliono testare diverse implementazioni di un'interfaccia OO.
*   Si vuol testare il codice su vari input (ovvero test basati sui dati [data-driven testing]).
    This feature is easy to abuse, so please exercise your good sense when doing
    it!

### Come Scrivere Test con Valori Parametrizzati

Per scrivere test con valori parametrizzati, è necessario innanzitutto definire una classe fixture. Deve essere derivata sia da `testing::Test` che da `testing::WithParamInterface<T>` (quest'ultima è un'interfaccia pura), dove `T` è il tipo dei valori parametrizzati. Per comodità, si può semplicemente derivare la classe fixture da `testing::TestWithParam<T>`, che a sua volta è derivata sia da `testing::Test`
che da `testing::WithParamInterface<T>`. `T` può essere qualsiasi tipo copiabile. Se si tratta di un puntatore semplice [raw], si è responsabili della gestione della durata dei valori puntati.

{: .callout .note}
NOTA: Se la fixture definisce `SetUpTestSuite()` o `TearDownTestSuite()` devono essere dichiarati **public** anziché **protected** per poter utilizzare `TEST_P`.

```c++
class FooTest :
    public testing::TestWithParam<absl::string_view> {
  // Qui si possono implementare tutti i soliti membri della classe fixture.
  // Per accedere al parametro test, chiamare GetParam() dalla classe
  // TestWithParam<T>.
};
// Or, when you want to add parameters to a pre-existing fixture class:
class BaseTest : public testing::Test {
  ...
};
class BarTest : public BaseTest,
                public testing::WithParamInterface<absl::string_view> {
  ...
};

```

Poi, si usa la macro `TEST_P` per definire tutti i pattern di test desiderati utilizzando questa fixture. Il suffisso `_P` sta per "parametrizzato" o "pattern", a seconda di come si preferisce pensare.

```c++
TEST_P(FooTest, DoesBlah) {
  // All'interno di un test, si accede al parametro test con il metodo GetParam()
  // della classe TestWithParam<T>:
  EXPECT_TRUE(foo.Blah(GetParam()));
  ...
}
TEST_P(FooTest, HasBlahBlah) {
  ...
}

```

Infine, si può utilizzare la macro `INSTANTIATE_TEST_SUITE_P` per istanziare la test suite con qualsiasi set di parametri desiderato. GoogleTest definisce una serie di funzioni per la generazione di parametri di test: vedere i dettagli in [`INSTANTIATE_TEST_SUITE_P`](reference/testing.md#INSTANTIATE_TEST_SUITE_P) nel "Riferimento al Testing".

Ad esempio, la seguente istruzione istanzia i test dalla test suite `FooTest` ciascuno con i valori dei parametrzzati `"meeny"`, `"miny"` e `"moe"` utilizzando il generatore di parametri [`Values`](reference/testing.md#param-generators):

```c++
INSTANTIATE_TEST_SUITE_P(MeenyMinyMoe,
                         FooTest,
                         testing::Values("meeny", "miny", "moe"));

```

{: .callout .note}
NOTA: Il codice precedente deve essere inserito nello scope globale o del namespace, non nello scope della funzione.

Il primo argomento di `INSTANTIATE_TEST_SUITE_P` è un nome univoco per l'istanziazione della test suite. L'argomento successivo è il nome del pattern di test e l'ultimo è il [generatore di parametri](reference/testing.md#param-generators) [parameter generator].

L'espressione del generatore di parametri non viene valutata finché GoogleTest non viene inizializzato (tramite `InitGoogleTest()`). Qualsiasi inizializzazione precedente eseguita nella funzione `main` sarà accessibile dal generatore di parametri, ad esempio i risultati del parsing dei flag.

È possibile istanziare un pattern di test più di una volta, quindi per distinguere le diverse istanze del pattern, il nome di istanziazione viene aggiunto come prefisso a quello effettivo della test suite. Ricordarsi di scegliere prefissi univoci per le diverse istanze. I test dell'istanziazione precedente avranno questi nomi:

*   `MeenyMinyMoe/FooTest.DoesBlah/0` per `"meeny"`
*   `MeenyMinyMoe/FooTest.DoesBlah/1` per `"miny"`
*   `MeenyMinyMoe/FooTest.DoesBlah/2` per `"moe"`
*   `MeenyMinyMoe/FooTest.HasBlahBlah/0` per `"meeny"`
*   `MeenyMinyMoe/FooTest.HasBlahBlah/1` per `"miny"`
*   `MeenyMinyMoe/FooTest.HasBlahBlah/2` per `"moe"`

Si possono usare questi nomi in [`--gtest_filter`](#running-a-subset-of-the-tests).

La seguente istruzione istanzia nuovamente tutti i test da `FooTest`, ciascuno con i valori dei parametri `"cat"` e `"dog"` utilizzando il generatore di parametri [`ValuesIn`](reference/testing.md#param-generators):

```c++
constexpr absl::string_view kPets[] = {"cat", "dog"};
INSTANTIATE_TEST_SUITE_P(Pets, FooTest, testing::ValuesIn(kPets));

```

I test dell'istanziazione precedente avranno questi nomi:

*   `Pets/FooTest.DoesBlah/0` per `"cat"`
*   `Pets/FooTest.DoesBlah/1` per `"dog"`
*   `Pets/FooTest.HasBlahBlah/0` per `"cat"`
*   `Pets/FooTest.HasBlahBlah/1` per `"dog"`

Si noti che `INSTANTIATE_TEST_SUITE_P` istanzia *tutti* i test nella test suite, indipendentemente dal fatto che le loro definizioni vengano prima o *dopo* la dichiarazione `INSTANTIATE_TEST_SUITE_P`.

Inoltre, per default, ogni `TEST_P` senza un corrispondente `INSTANTIATE_TEST_SUITE_P` provoca un test non riuscito nella test suite `GoogleTestVerification`. Se si dispone di una test suite in cui tale omissione non è un errore, ad esempio è in una libreria che potrebbe essere linkata per altri motivi o dove l'elenco dei casi di test è dinamico e potrebbe essere vuoto, allora questo controllo può essere soppresso taggando la test suite:

```c++
GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST(FooTest);

```

Esaminare [sample7_unittest.cc] e [sample8_unittest.cc] per altri esempi.

[sample7_unittest.cc]: https://github.com/google/googletest/blob/main/googletest/samples/sample7_unittest.cc "Esempio di Test Parametrizzato"
[sample8_unittest.cc]: https://github.com/google/googletest/blob/main/googletest/samples/sample8_unittest.cc "Esempio di Test Parametrizzato con più parametri"

### Creazione di Test Astratti con Valori Parametrizzati

Abbiamo definito e istanziato `FooTest` nello *stesso* file sorgente.
A volte si vorrebbero definire test con valori parametrizzati in una libreria e consentire ad altre persone di crearne un'istanza successivamente. Questo pattern è chiamato *test astratti*.
Come esempio della sua applicazione, quando si progetta un'interfaccia è possibile scrivere una suite standard di test astratti (magari utilizzando una funzione factory come parametro di test) e ci si aspetta che tutte le implementazioni dell'interfaccia li superino. Quando qualcuno implementa l'interfaccia, può creare un'istanza della suite per ottenere gratuitamente tutti i test di conformità dell'interfaccia.

Per definire test astratti, si deve organizzare il codice in questo modo:

1.  Put the definition of the parameterized test fixture class (e.g. `FooTest`)
    in a header file, say `foo_param_test.h`. Think of this as *declaring* your
    abstract tests.
2.  Si inseriscono le definizioni `TEST_P` in `foo_param_test.cc`, che include `foo_param_test.h`. Lo si consideri come *implementazione* dei test astratti.

Una volta definiti, se ne può creare un'istanza includendo `foo_param_test.h`, richiamando `INSTANTIATE_TEST_SUITE_P()` e in base alla libreria target che contiene `foo_param_test.cc`. È possibile istanziare la stessa test suite astratta più volte, possibilmente in file sorgenti diversi.

### Specificare i Nomi per i Parametri di test con Valori Parametrizzati

L'ultimo argomento facoltativo di `INSTANTIATE_TEST_SUITE_P()` consente all'utente di specificare una funzione o un funtore che genera suffissi personalizzati del nome del test in base ai parametri. La funzione deve accettare un argomento di tipo `testing::TestParamInfo<class ParamType>` e restituire `std::string`.

`testing::PrintToStringParamName` è un generatore di suffissi nativo che restituisce il valore di `testing::PrintToString(GetParam())`. Non funziona con `std::string` né con stringhe C.

{: .callout .note}
NOTA: i nomi dei test devono essere non vuoti, univoci e possono contenere solo caratteri alfanumerici ASCII. In particolare, [non devono contenere gli underscore](faq.md#why-should-test-suite-names-and-test-names-not-contain-underscore)

```c++
class MyTestSuite : public testing::TestWithParam<int> {};
TEST_P(MyTestSuite, MyTest)
{
  std::cout << "Example Test Param: " << GetParam() << std::endl;
}
INSTANTIATE_TEST_SUITE_P(MyGroup, MyTestSuite, testing::Range(0, 10),
                         testing::PrintToStringParamName());

```

Fornire un funtore personalizzato consente un maggiore controllo sulla generazione dei nomi dei parametri dei test, in particolare per i tipi in cui la conversione automatica non genera nomi utili (ad esempio le stringhe come mostrato sopra). L'esempio seguente illustra questo per più parametri, un tipo di enumerazione e una stringa e mostra anche come combinare i generatori. Utilizza un lambda per concisione:

```c++
enum class MyType { MY_FOO = 0, MY_BAR = 1 };
class MyTestSuite : public testing::TestWithParam<std::tuple<MyType, std::string>> {
};
INSTANTIATE_TEST_SUITE_P(
    MyGroup, MyTestSuite,
    testing::Combine(
        testing::Values(MyType::MY_FOO, MyType::MY_BAR),
        testing::Values("A", "B")),
    [](const testing::TestParamInfo<MyTestSuite::ParamType>& info) {
      std::string name = absl::StrCat(
          std::get<0>(info.param) == MyType::MY_FOO ? "Foo" : "Bar",
          std::get<1>(info.param));
      absl::c_replace_if(name, [](char c) { return !std::isalnum(c); }, '_');
      return name;
    });

```

## Test Tipizzati

Supponiamo di avere più implementazioni della stessa interfaccia e di voler assicurarci che tutte soddisfino alcuni requisiti comuni. Oppure si potrebbero aver definito diversi tipi che dovrebbero essere conformi allo stesso "concetto" e si desidera verificarlo. In entrambi i casi, si desidera che la stessa logica di test venga ripetuta per tipi diversi.

Anche se si può scrivere un `TEST` o `TEST_F` per ogni tipo da testare (e si potrebbe anche fattorizzare la logica del test in una funzione template invocata da ` TEST`), è noioso e non scalabile: se si vuole che `m` test su `n` tipi, si finirà per scrivere `m*n` `TEST`.

I *Test tipizzati* consentono di ripetere la stessa logica del test su un elenco di tipi. È necessario scrivere la logica del test solo una volta, anche se è necessario conoscere l'elenco dei tipi quando si scrivono test tipizzati. Ecco come farlo:

Innanzitutto, si definisce una classe fixture template. Dovrebbe essere parametrizzata da un tipo.
Ricordarsi di derivarlo da `::testing::Test`:

```c++
template <typename T>
class FooTest : public testing::Test {
 public:
  ...
  using List = std::list<T>;
  static T shared_;
  T value_;
};

```

Poi, si associa un elenco di tipi alla test suite, che verrà ripetuto per ogni tipo nell'elenco:

```c++
using MyTypes = ::testing::Types<char, int, unsigned int>;
TYPED_TEST_SUITE(FooTest, MyTypes);

```

L'alias del tipo (`using` o `typedef`) è necessario affinché la macro `TYPED_TEST_SUITE` lo possa analizzare correttamente. Altrimenti il compilatore penserà che ogni virgola nell'elenco dei tipi introduca un nuovo argomento della macro.

Poi, si usa `TYPED_TEST()` invece di `TEST_F()` per definire un test tipizzato per questa test suite. Lo si può ripetere più volte:

```c++
TYPED_TEST(FooTest, DoesBlah) {
  // All'interno di un test, fare riferimento al nome speciale TypeParam per ottenere il tipo
  // del parametro.  Poiché ci troviamo all'interno di una classe template derivata, il C++ ci richiede
  // di visitare i membri di FooTest tramite 'this'.
  TypeParam n = this->value_;
  // Per visitare i membri statici della fixture, si antepone 'TestFixture::'
  // come prefisso.
  n += TestFixture::shared_;
  // Per fare riferimento a typedef nella fixture, si antepone 'typename TestFixture::'
  // come prefisso.  Il 'typename' è necessario per soddisfare il compilatore.
  typename TestFixture::List values;
  values.push_back(n);
  ...
}
TYPED_TEST(FooTest, HasPropertyA) { ... }
```

Si può vedere [sample6_unittest.cc] per un esempio completo.

[sample6_unittest.cc]: https://github.com/google/googletest/blob/main/googletest/samples/sample6_unittest.cc "Esempio di Test Tipizzato"

## Test con i Tipi Parametrizzati

I *test type-parameterized* sono come quelli tipizzati, tranne per il fatto che non richiedono che si conosca in anticipo l'elenco dei tipi. È invece possibile definire prima la logica del test e istanziarla successivamente con elenchi di tipi diversi. Si può anche crearne un'istanza più di una volta nello stesso programma.

Se si sta progettando un'interfaccia o un concetto, si può definire una suite di test con i tipi parametrizzati per verificare le proprietà che dovrebbe avere qualsiasi implementazione valida dell'interfaccia/concetto. Quindi, l'autore di ciascuna implementazione può semplicemente istanziare la test suite con il proprio tipo per verificare che sia conforme ai requisiti, senza dover scrivere ripetutamente test simili. Ecco un esempio:

Innanzitutto, definisce una classe fixture template, come abbiamo fatto con i test tipizzati:

```c++
template <typename T>
class FooTest : public testing::Test {
  void DoSomethingInteresting();
  ...
};

```

Successivamente, si dichiara che si definirà una test suite con tipi parametrizzati:

```c++
TYPED_TEST_SUITE_P(FooTest);

```

Poi, si usa `TYPED_TEST_P()` per definire un test con un tipo parametrizzato. Lo si può ripetere più volte:

```c++
TYPED_TEST_P(FooTest, DoesBlah) {
  // All'interno di un test, fare riferimento a TypeParam per ottenere il parametro del tipo.
  TypeParam n = 0;
  // Si deve utilizzare `this` esplicitamente per fare riferimento ai membri della fixture.
  this->DoSomethingInteresting()
  ...
}
TYPED_TEST_P(FooTest, HasPropertyA) { ... }
```

Ora la parte difficile: si devono registrare tutti i pattern dei test utilizzando la macro `REGISTER_TYPED_TEST_SUITE_P` prima di poterli istanziare. Il primo argomento della macro è il nome della test suite; il resto sono i nomi dei test in questa test suite:

```c++
REGISTER_TYPED_TEST_SUITE_P(FooTest,
                            DoesBlah, HasPropertyA);

```

Infine, si può istanziare il pattern con i tipi desiderati. Se si inserisce il codice precedente in un file header, si può `#include`-rlo in pià sorgenti C++e istanziarlo più volte.

```c++
using MyTypes = ::testing::Types<char, int, unsigned int>;
INSTANTIATE_TYPED_TEST_SUITE_P(My, FooTest, MyTypes);

```

Per distinguere le diverse istanze del pattern, il primo argomento della macro `INSTANTIATE_TYPED_TEST_SUITE_P` è un prefisso che verrà anteposto al nome effettivo della test suite. Ricordarsi di scegliere prefissi univoci per istanze diverse.

Nel caso speciale in cui l'elenco dei tipi contiene solo un tipo, lo si può scrivere direttamente senza `::testing::Types<...>`, in questo modo:

```c++
INSTANTIATE_TYPED_TEST_SUITE_P(My, FooTest, int);

```

Si può vedere [sample6_unittest.cc] per un esempio completo.

## Test di Codice Privato

Se si modifica l'implementazione interna del software, i test non dovrebbero smettere di funzionare fin quando la modifica non è osservabile dagli utenti. Pertanto, **secondo il principio del test della black-box, la maggior parte delle volte si deve testare il codice tramite le sue interfacce pubbliche**.

**Se ci si ritrova ancora a dover testare il codice dell'implementazione interna, considerare se esiste un design migliore.** Il desiderio di testare l'implementazione interna è spesso un segno che la classe sta facendo troppo. Si prenda in considerazione l'estrazione di una classe di implementazione e la si testi. Poi si usa quella classe di implementazione nella classe originale.

Se si deve assolutamente testare il codice dell'interfaccia non pubblica, lo si può fare. Ci sono due casi da considerare:

*   Static functions ( *not* the same as static member functions!) or unnamed
    namespaces, and
*   I membri di classe privati o protetti

Per testarli, utilizziamo le seguenti tecniche speciali:

*   Both static functions and definitions/declarations in an unnamed namespace
    are only visible within the same translation unit. Per testarli, si può `#include`-re l'intero file `.cc` da testare nel file `*_test.cc`.
    (#including `.cc` files is not a good way to reuse code - you should not do
    this in production code!)

    However, a better approach is to move the private code into the
    `foo::internal` namespace, where `foo` is the namespace your project
        normally uses, and put the private declarations in a `*-internal.h` file.
        Your production `.cc` files and your tests are allowed to include this
        internal header, but your clients are not. This way, you can fully test your
        internal implementation without leaking it to your clients.

*   Private class members are only accessible from within the class or by
    friends. To access a class' private members, you can declare your test
    fixture as a friend to the class and define accessors in your fixture. Tests
    using the fixture can then access the private members of your production
    class via the accessors in the fixture. Note that even though your fixture
    is a friend to your production class, your tests are not automatically
    friends to it, as they are technically defined in sub-classes of the
    fixture.

    Another way to test private members is to refactor them into an
        implementation class, which is then declared in a `*-internal.h` file. Your
        clients aren't allowed to include this header but your tests can. Such is
        called the
        [Pimpl](https://www.gamedev.net/articles/programming/general-and-gameplay-programming/the-c-pimpl-r1794/)
        (Private Implementation) idiom.

    Or, you can declare an individual test as a friend of your class by adding
        this line in the class body:

    ```c++
        FRIEND_TEST(TestSuiteName, TestName);
    
    ```

    Per esempio,

    ```c++
    // foo.h
    class Foo {
      ...
     private:
      FRIEND_TEST(FooTest, BarReturnsZeroOnNull);
      int Bar(void* x);
    };
    // foo_test.cc
    ...
    TEST(FooTest, BarReturnsZeroOnNull) {
      Foo foo;
      EXPECT_EQ(foo.Bar(NULL), 0);  // Uses Foo's private member Bar().
    }
    
    ```

    Prestare particolare attenzione quando la classe è definita in un namespace. If you want
        your test fixtures and tests to be friends of your class, then they must be
        defined in the exact same namespace (no anonymous or inline namespaces).

    Ad esempio, se il codice da testare è simile a:

    ```c++
    namespace my_namespace {
    class Foo {
      friend class FooTest;
      FRIEND_TEST(FooTest, Bar);
      FRIEND_TEST(FooTest, Baz);
      ... definition of the class Foo ...
    };
    }  // namespace my_namespace
    ```

    Il codice del test dovrebbe essere qualcosa del tipo:

    ```c++
    namespace my_namespace {
    class FooTest : public testing::Test {
     protected:
      ...
    };
    TEST_F(FooTest, Bar) { ... }
    TEST_F(FooTest, Baz) { ... }
    }  // namespace my_namespace
    ```

## "Catching" degli Errori

Se si crea un'utilità di test al di sopra di GoogleTest, la si deve testare. Quale framework si userebbe per testarla? GoogleTest, ovviamente.

La sfida consiste nel verificare che l'utilità di test riporti correttamente gli errori.
Nei framework che riportano un errore lanciando un'eccezione, si potrebbe catturare l'eccezione e metterci un assert. Ma GoogleTest non utilizza eccezioni, quindi come possiamo verificare che una parte di codice generi un errore previsto?

`"gtest/gtest-spi.h"` contiene alcuni costrutti per farlo.
Dopo lo #include di questo header, si può usare

```c++
  EXPECT_FATAL_FAILURE(statement, substring);

```

per asserire che `statement` genera un errore fatale (ad esempio `ASSERT_*`) nel thread corrente il cui messaggio contiene la `substring`, oppure si usa

```c++
  EXPECT_NONFATAL_FAILURE(statement, substring);

```

se ci si aspetta un errore non fatale (per es. `EXPECT_*`).

Vengono controllati solo gli errori nel thread corrente per determinare il risultato di questo tipo di aspettative. Se `statement` crea nuovi thread, anche gli errori in questi thread vengono ignorati. Per rilevare errori anche in altri thread, si utilizza invece una delle seguenti macro:

```c++
  EXPECT_FATAL_FAILURE_ON_ALL_THREADS(statement, substring);
  EXPECT_NONFATAL_FAILURE_ON_ALL_THREADS(statement, substring);

```

{: .callout .note}
NOTA: Le asserzioni provenienti da più thread non sono attualmente supportate su Windows.

Per ragioni tecniche, ci sono alcune avvertenze:

1.  Non è possibile accodare a uno stream un messaggio di errore a nessuna delle macro.

2.  `statement` in `EXPECT_FATAL_FAILURE{_ON_ALL_THREADS}()` cannot reference
    local non-static variables or non-static members of `this` object.

3.  `statement` in `EXPECT_FATAL_FAILURE{_ON_ALL_THREADS}()` cannot return a
    value.

## Registrazione dei test programmaticamente

Le macro `TEST` gestiscono la stragrande maggioranza di tutti i casi d'uso, ma ce ne sono alcuni in cui è richiesta la logica di registrazione a runtime. Per questi casi, il framework fornisce `::testing::RegisterTest` che consente ai chiamanti di registrare test arbitrari in modo dinamico.

Questa è un'API avanzata da utilizzare solo quando le macro `TEST` sono insufficienti.
Le macro dovrebbero essere preferite quando possibile, poiché evitano gran parte della complessità di chiamare questa funzione.

Fornisce la seguente firma [signature]:

```c++
template <typename Factory>
TestInfo* RegisterTest(const char* test_suite_name, const char* test_name,
                       const char* type_param, const char* value_param,
                       const char* file, int line, Factory factory);

```

L'argomento `factory` è un oggetto richiamabile da factory (costruibile tramite spostamento) o un puntatore a funzione che crea una nuova istanza dell'oggetto Test. Gestisce la proprietà del chiamante. La firma del richiamabile è `Fixture*()`, dove `Fixture` è la classe fixture per il test. Tutti i test registrati con lo stesso `test_suite_name` devono restituire lo stesso tipo di fixture. Questo viene controllato in fase di esecuzione.

Il framework dedurrà la classe della fixture dalla factory e per questo chiamerà `SetUpTestSuite` e `TearDownTestSuite`.

Deve essere chiamato prima che venga invocato `RUN_ALL_TESTS()`, altrimenti il comportamento non è definito.

Esempio di caso d'uso:

```c++
class MyFixture : public testing::Test {
 public:
  // Tutto questo è opzionale, proprio come nell'utilizzo delle normali macro.
  static void SetUpTestSuite() { ... }
  static void TearDownTestSuite() { ... }
  void SetUp() override { ... }
  void TearDown() override { ... }
};
class MyTest : public MyFixture {
 public:
  explicit MyTest(int data) : data_(data) {}
  void TestBody() override { ... }
 private:
  int data_;
};
void RegisterMyTests(const std::vector<int>& values) {
  for (int v : values) {
    testing::RegisterTest(
        "MyFixture", ("Test" + std::to_string(v)).c_str(), nullptr,
        std::to_string(v).c_str(),
        __FILE__, __LINE__,
        // È importante utilizzare qui il tipo di fixture come tipo restituito.
        [=]() -> MyFixture* { return new MyTest(v); });
  }
}
...
int main(int argc, char** argv) {
  testing::InitGoogleTest(&argc, argv);
  std::vector<int> values_to_test = LoadValuesFromConfig();
  RegisterMyTests(values_to_test);
  ...
  return RUN_ALL_TESTS();
}

```

## Recuperare il Nome del Test Corrente

A volte una funzione potrebbe aver bisogno di conoscere il nome del test attualmente in esecuzione.
Ad esempio, si potrebbe utilizzare il metodo `SetUp()` della fixture per impostare il nome del "golden file" (ndt: Output campione) in base al test in esecuzione. La classe [`TestInfo`](reference/testing.md#TestInfo) contiene queste informazioni.

Per ottenere un oggetto `TestInfo` per il test attualmente in esecuzione, si chiama `current_test_info()` sull'oggetto singleton [`UnitTest`](reference/testing.md#UnitTest):

```c++
  // Prende le informazioni sul test attualmente in esecuzione.
  // NON eseguire il delete sull'oggetto restituito: è gestito dalla classe UnitTest.
  const testing::TestInfo* const test_info =
      testing::UnitTest::GetInstance()->current_test_info();
  printf("We are in test %s of test suite %s.\n",
         test_info->name(),
         test_info->test_suite_name());

```

`current_test_info()` restituisce un puntatore nullo se non è in esecuzione alcun test. In particolare, non è possibile trovare il nome della test suite in `SetUpTestSuite()`, `TearDownTestSuite()` (dove si conosce implicitamente il nome della test suite) né nelle funzioni chiamate da essi.

## Estendere GoogleTest Gestendo gli Eventi dei Test

GoogleTest fornisce una **event listener API** per ricevere notifiche sull'avanzamento di un programma di test e sugli errori dei test. Gli eventi che si possono rilevare [listen] includono, tra gli altri, l'inizio e la fine del programma di test, di una test suite o di un metodo di test. Questa API è utilizzabile per aumentare o sostituire l'output della console standard, sostituire l'output XML o fornire una forma di output completamente diversa, come una GUI o un database. È inoltre possibile utilizzare gli eventi dei test come checkpoint per implementare, ad esempio, un controllo delle perdite [leak] di risorse.

### Definire i Listener degli Eventi

Per definire un event listener, si crea una sottoclasse di [`testing::TestEventListener`](reference/testing.md#TestEventListener) o di [`testing::EmptyTestEventListener`](reference/testing.md#EmptyTestEventListener).
La prima è un'interfaccia (astratta), in cui *ciascun metodo virtuale puro può essere sovrascritto [overridden] per gestire un evento di test* (Per esempio, quando inizia un test, verrà chiamato il metodo `OnTestStart()`). L'ultimo fornisce un'implementazione vuota di tutti i metodi nell'interfaccia, in modo tale che una sottoclasse debba solo sovrascrivere i metodi che le interessano.

Quando viene generato un evento, il suo contesto viene passato alla funzione del gestore [handler] come argomento. Vengono utilizzati i seguenti tipi di argomento:

*   UnitTest riflette lo stato dell'intero programma di test,
*   TestSuite has information about a test suite, which can contain one or more
    tests,
*   TestInfo contiene lo stato di un test e
*   TestPartResult rappresenta il risultato di un'asserzione di un test.

Una funzione del gestore eventi può esaminare l'argomento che riceve per scoprire informazioni interessanti sull'evento e sullo stato del programma di test.

Ecco un esempio:

```c++
  class MinimalistPrinter : public testing::EmptyTestEventListener {
    // Chiamato prima dell'inizio del test.
    void OnTestStart(const testing::TestInfo& test_info) override {
      printf("*** Test %s.%s starting.\n",
             test_info.test_suite_name(), test_info.name());
    }

    // Chiamato dopo un'asserzione fallita oun SUCCESS().
    void OnTestPartResult(const testing::TestPartResult& test_part_result) override {
      printf("%s in %s:%d\n%s\n",
             test_part_result.failed() ? "*** Failure" : "Success",
             test_part_result.file_name(),
             test_part_result.line_number(),
             test_part_result.summary());
    }

    // Chiamato dopo la fine di un test.
    void OnTestEnd(const testing::TestInfo& test_info) override {
      printf("*** Test %s.%s ending.\n",
             test_info.test_suite_name(), test_info.name());
    }

  };

```

### Utilizzo dei Listener di Eventi

Per usare l'event listener definito, se ne aggiunge un'istanza alla lista degli event listener di GoogleTest (rappresentata dalla classe [`TestEventListeners`](reference/testing.md#TestEventListeners) - notare la "s" alla fine del nome) nella funzione `main()`, prima di chiamare `RUN_ALL_TESTS()`:

```c++
int main(int argc, char** argv) {
  testing::InitGoogleTest(&argc, argv);
  // Preleva l'elenco dei listener di eventi.
  testing::TestEventListeners& listeners =
      testing::UnitTest::GetInstance()->listeners();
  // Aggiunge un listener alla fine.  GoogleTest ne assume la proprietà.
  listeners.Append(new MinimalistPrinter);
  return RUN_ALL_TESTS();
}

```

C'è solo un problema: la stampante di default dei risultati del test è ancora attiva, quindi il suo output si confonderà con quello della propria stampante minimalista. Per sopprimere la stampante di default , basta rilasciarla dall'elenco del listener di eventi ed eseguirne il delete.
Lo si può fare aggiungendo una riga:

```c++
  ...
  delete listeners.Release(listeners.default_result_printer());
  listeners.Append(new MinimalistPrinter);
  return RUN_ALL_TESTS();

```

Ora ci si può rilassare e godersi un risultato completamente diverso dai test. Per ulteriori dettagli, consultare [sample9_unittest.cc].

[sample9_unittest.cc]: https://github.com/google/googletest/blob/main/googletest/samples/sample9_unittest.cc "Esempio di listener di eventi"

Si possono aggiungere più listener alla lista. Quando viene attivato un evento `On*Start()` o un `OnTestPartResult()`, i listener lo riceveranno nell'ordine in cui appaiono nell'elenco (poiché i nuovi listener vengono aggiunti alla finedelle lista, la stampante del testo e il generatore XML di default riceveranno per primi l'evento). Un evento `On*End()` verrà ricevuto dai listener nell'ordine *inverso*. Ciò consente all'output dei listener aggiunti successivamente di essere inquadrati [framed] dall'output dei listener aggiunti in precedenza.

### Generare Errori nei Listener

Si possono utilizzare macro che generano errori (`EXPECT_*()`, `ASSERT_*()`, `FAIL()`, ecc.) durante l'elaborazione di un evento. Ci sono alcune restrizioni:

1.  You cannot generate any failure in `OnTestPartResult()` (otherwise it will
    cause `OnTestPartResult()` to be called recursively).
2.  A listener that handles `OnTestPartResult()` is not allowed to generate any
    failure.

Quando si aggiungono listener alla lista, si devono inserire i listener che gestiscono `OnTestPartResult()` *prima* di quelli che generano errori. Ciò garantisce che i fallimenti generati da questi ultimi vengano attribuiti al test corretto da parte dei primi.

Vedere [sample10_unittest.cc] per un esempio di un listener che genera errori.

[sample10_unittest.cc]: https://github.com/google/googletest/blob/main/googletest/samples/sample10_unittest.cc "Esempio di listener che genera errori"

## Esecuzione dei Programmi di Test: Opzioni Avanzate

I programmi di test di GoogleTest sono normali eseguibili. Una volta creati, si possono eseguire direttamente e influenzarne il comportamento tramite le seguenti variabili di ambiente e/o flag della riga di comando. Affinché i flag funzionino, i programmi devono chiamare `::testing::InitGoogleTest()` prima di chiamare `RUN_ALL_TESTS()`.

Per visualizzare un elenco dei flag supportati e il loro utilizzo, eseguire il programma di test con il flag `--help`. Si può usare anche `-h`, `-?` o `/?` per brevità.

Se un'opzione è specificata sia da una variabile d'ambiente che da un flag, quest'ultimo ha la precedenza.

### Selezione dei Test

#### Elenco dei Nomi dei Test

A volte è necessario elencare i test disponibili in un programma prima di eseguirli in modo da poter applicare un filtro, se necessario. L'inclusione del flag `--gtest_list_tests` sovrascrive tutti gli altri flag ed elenca i test nel seguente formato:

```none
TestSuite1.
  TestName1
  TestName2
TestSuite2.
  TestName

```

Nessuno dei test elencati viene effettivamente eseguito se viene fornito il flag. Non esiste una variabile di ambiente corrispondente per questo flag.

#### Eseguire un Sottoinsieme dei Test

Per default, un programma GoogleTest esegue tutti i test definiti dall'utente. A volte, se ne vogliono eseguire solo un sottoinsieme (ad esempio per eseguire il debug o verificare rapidamente una modifica). Se imposti la variabile di ambiente `GTEST_FILTER` o il flag `--gtest_filter` su una stringa di filtro, GoogleTest eseguirà solo i test i cui nomi completi (nel formato `TestSuiteName.TestName`) corrisponderanno al filtro.

Il formato di un filtro è un elenco di pattern di carattery jolly, separato da '`:`' (detti *pattern positivi*) seguito facoltativamente da un '`-`' e un altro elenco di pattern separato da '`:`' (detti *pattern negativi*). Un test corrisponde al filtro se e solo se corrisponde a uno qualsiasi dei pattern positivi ma non corrisponde a nessuno dei pattern negativi.

Un pattern può contenere `'*'` (corrisponde a qualsiasi stringa) or`'?'` (corrisponde a qualsiasi carattere singolo). Per comodità, il filtro `'*-NegativePatterns'` può anche essere scritto come `'-NegativePatterns'`.

Per esempio:

*   `./foo_test` Non ha flag e quindi esegue tutti i suoi test.
*   `./foo_test --gtest_filter=*` Also runs everything, due to the single
    match-everything `*` value.
*   `./foo_test --gtest_filter=FooTest.*` Esegue tutto nella test suite `FooTest` .
*   `./foo_test --gtest_filter=*Null*:*Constructor*` Runs any test whose full
    name contains either `"Null"` or `"Constructor"` .
*   `./foo_test --gtest_filter=-*DeathTest.*` Esegue tutti i test non-death.
*   `./foo_test --gtest_filter=FooTest.*-FooTest.Bar` Runs everything in test
    suite `FooTest` except `FooTest.Bar`.
*   `./foo_test --gtest_filter=FooTest.*:BarTest.*-FooTest.Bar:BarTest.Foo` Runs
    everything in test suite `FooTest` except `FooTest.Bar` and everything in
    test suite `BarTest` except `BarTest.Foo`.

#### Interrompere l'esecuzione del test al primo errore

Per default, un programma GoogleTest esegue tutti i test definiti dall'utente. In alcuni casi (ad esempio sviluppo ed esecuzione iterativi di test) potrebbe essere auspicabile interrompere l'esecuzione del test al primo fallimento (scambiando la maggiore latenza con la completezza).
Se la variabile di ambiente `GTEST_FAIL_FAST` o il flag `--gtest_fail_fast` sono settati, l'esecutore dei test si interromperà non appena viene rilevato il primo errore.

#### Disattivazione Temporanea dei Test

Se si ha un test non funzionante che non si può correggere subito, si può aggiungere il prefisso `DISABLED_` al nome. Ciò lo escluderà dall'esecuzione. Questo è meglio che commentare il codice o usare `#if 0`, poiché i test disabilitati vengono comunque compilati (e quindi non "marciranno").

Per disabilitare tutti i test in una test suite, si può aggiungere `DISABLED_` all'inizio del nome di ciascun test o in alternativa aggiungerlo all'inizio del nome della test suite.

Ad esempio, i seguenti test non verranno eseguiti da GoogleTest, anche se verranno comunque compilati:

```c++
// Verifica che Foo esegua Abc.
TEST(FooTest, DISABLED_DoesAbc) { ... }
class DISABLED_BarTest : public testing::Test { ... };
// Tests that Bar does Xyz.
TEST_F(DISABLED_BarTest, DoesXyz) { ... }
```

{: .callout .note}
NOTA: Questa funzione deve essere utilizzata solo come soluzione temporanea. Resta ancora correggere i test disabilitati in un secondo momento. Come promemoria, GoogleTest stamperà un banner che avvisa se un programma di test contiene test disabilitati.

{: .callout .tip}
TIP: Si può facilmente contare il numero di test disabilitati con `grep`. Questo numero può essere utilizzato come parametro per migliorare la qualità del test.

#### Abilitazione Temporanea dei Test Disabilitati

Per includere test disabilitati nell'esecuzione del test, è sufficiente richiamare il programma di test con il flag `--gtest_also_run_disabled_tests` o impostare la variabile d'ambiente `GTEST_ALSO_RUN_DISABLED_TESTS` su un valore diverso da `0`.
Lo si può combinare col flag `--gtest_filter` per selezionare ulteriormente quali test disabilitati eseguire.

### Ripetizione dei Test

Di tanto in tanto ci si imbatterà in un test il cui risultato è incostante. Forse fallirà solo l'1% delle volte, rendendo piuttosto difficile riprodurre il bug in un debugger. Questa può essere uno dei principali motivi di frustrazione.

Il flag `--gtest_repeat` consente di ripetere più volte tutti i metodi di test (o quelli selezionati) in un programma. Si spera che un test instabile alla fine fallisca e dia la possibilità di eseguire il debug. Ecco come usarlo:

```none
$ foo_test --gtest_repeat=1000
Ripeti foo_test 1000 volte e non fermarti ai fallimenti.
$ foo_test --gtest_repeat=-1
Un conteggio negativo significa ripetere all'infinito.
$ foo_test --gtest_repeat=1000 --gtest_break_on_failure
Ripete foo_test 1000 volte, fermandosi al primo fallimento.  Ciò è particolarmente utile quando si esegue in un debugger: quando il test fallisce, verrà inserito nel debugger e si potrà poi ispezionare variabili e stack.
$ foo_test --gtest_repeat=1000 --gtest_filter=FooBar.*
Ripeti 1000 volte i test il cui nome corrisponde al filtro.

```

Se il programma di test contiene codice [set-up/tear-down globale](#global-set-up-and-tear-down), verrà ripetuto anche in ogni iterazione, poiché potrebbe esserci qualche instabilità. Per evitare di ripetere il set-up/tear-down globale, si specifica `--gtest_recreate_environments_when_repeating=false`{.nowrap}.

Si può anche specificare il numero di ripetizioni impostando la variabile di ambiente `GTEST_REPEAT`.

### Mischiare i Test

Si può specificare il flag `--gtest_shuffle` (o impostare la variabile di ambiente `GTEST_SHUFFLE` a `1`) per eseguire i test in un programma in ordine casuale .
Questo aiuta a rivelare delle cattive dipendenze tra i test.

Per default, GoogleTest utilizza un seme casuale calcolato dall'ora corrente.
Pertanto si riceverà ogni volta un ordine diverso. L'output della console include il valore di inizializzazione casuale, in modo da poter riprodurre successivamente un errore relativo all'ordine. Per specificare esplicitamente il seed casuale, si usa il flag `--gtest_random_seed=SEED` (o si imposta la variabile di ambiente `GTEST_RANDOM_SEED`), dove `SEED` è un numero intero nell'intervallo [0, 99999]. Il valore seed 0 è speciale: indica a GoogleTest di eseguire il comportamento di default di calcolare il seed dall'ora corrente.

Combinandolo con `--gtest_repeat=N`, GoogleTest selezionerà un seme casuale diverso e rimischierà i test in ogni iterazione.

### Distribuire le Funzioni di Test su Più Macchine

Disponendo di più di macchine su cui eseguire un programma di test, si potrebbero eseguire le funzioni di test in parallelo e ottenere il risultato più velocemente. Chiamiamo questa tecnica *sharding*, dove ogni macchina è chiamata *shard*.

GoogleTest è compatibile con lo sharding dei test. Per sfruttare questa funzione, il test runner (non parte di GoogleTest) deve effettuare le seguenti operazioni:

1.  Allocare un certo numero di macchine (shard) per eseguire i test.
1.  On each shard, set the `GTEST_TOTAL_SHARDS` environment variable to the total
    number of shards. Deve essere lo stesso per tutti gli shard.
1.  On each shard, set the `GTEST_SHARD_INDEX` environment variable to the index
    of the shard. Different shards must be assigned different indices, which
    must be in the range `[0, GTEST_TOTAL_SHARDS - 1]`.
1.  Eseguire lo stesso programma di test su tutti gli shard. When GoogleTest sees the above two
    environment variables, it will select a subset of the test functions to run.
    Across all shards, each test function in the program will be run exactly
    once.
1.  Attendi che tutti gli shard finiscano, quindi raccogliere e riportare i risultati.

Il progetto potrebbe contenere test scritti senza GoogleTest e quindi non capire questo protocollo. Affinché il test runner possa capire quale test supporta lo sharding, può impostare la variabile di ambiente `GTEST_SHARD_STATUS_FILE` su un path di un file inesistente. Se un programma di test supporta lo sharding, creerà questo file per riconoscere questo fatto; altrimenti non lo creerà. Il contenuto effettivo del file non è importante al momento, anche se potremmo inserirvi alcune informazioni utili in futuro.

Ecco un esempio per chiarire. Supponiamo di avere un programma di test `foo_test` che contiene le seguenti 5 funzioni di test:

```
TEST(A, V)
TEST(A, W)
TEST(B, X)
TEST(B, Y)
TEST(B, Z)

```

Supponiamo di avere 3 macchine a nostra disposizione. Per eseguire le funzioni di test in parallelo, si imposta `GTEST_TOTAL_SHARDS` a 3 su tutte le macchine, e si setta `GTEST_SHARD_INDEX` a 0, 1, e 2 sulle macchine rispettivamente. Poi si esegue lo stesso `foo_test` su ciascuna macchina.

GoogleTest si riserva il diritto di modificare la modalità di distribuzione del lavoro tra gli shard, ma ecco uno scenario possibile:

*   La macchina #0 esegue `A.V` e `B.X`.
*   La macchina #1 esegue `A.W` e `B.Y`.
*   La macchina #2 esegue `B.Z`.

### Controllo dell'Output del Test

#### Output Colorato del Terminale

GoogleTest può utilizzare i colori nell'output del terminale per facilitare l'individuazione delle informazioni importanti:

<pre>...
<font color="green">[----------]</font> 1 test from FooTest
<font color="green">[ RUN      ]</font> FooTest.DoesAbc
<font color="green">[       OK ]</font> FooTest.DoesAbc
<font color="green">[----------]</font> 2 tests from BarTest
<font color="green">[ RUN      ]</font> BarTest.HasXyzProperty
<font color="green">[       OK ]</font> BarTest.HasXyzProperty
<font color="green">[ RUN      ]</font> BarTest.ReturnsTrueOnSuccess
... some error messages ...
<font color="red">[   FAILED ]</font> BarTest.ReturnsTrueOnSuccess
...
<font color="green">[==========]</font> 30 tests from 14 test suites ran.
<font color="green">[   PASSED ]</font> 28 tests.
<font color="red">[   FAILED ]</font> 2 tests, listed below:
<font color="red">[   FAILED ]</font> BarTest.ReturnsTrueOnSuccess
<font color="red">[   FAILED ]</font> AnotherTest.DoesXyz

 2 FAILED TESTS
</pre>

Si può impostare la variabile di ambiente `GTEST_COLOR` o il flag della riga di comando `--gtest_color` a `yes`, `no` o `auto` (il default) per abilitare i colori, disabilitarli o lasciare che sia GoogleTest a decidere. Quando il valore è `auto`, GoogleTest utilizzerà i colori se e solo se l'output arriva a un terminale e (su piattaforme non Windows) la variabile di ambiente `TERM` è settata a `xterm` o a `xterm-color`.

#### Sopprimere i test superati

Per default, GoogleTest stampa 1 riga di output per ogni test, indicando se è stato superato o meno. Per mostrare solo i test falliti, eseguire il programma di test con `--gtest_brief=1`, o impostare la variabile di ambiente GTEST_BRIEF a `1`.

#### Sopprimere il Tempo Trascorso

Per default, GoogleTest stampa il tempo necessario per eseguire ciascun test. Per disabilitarlo, si esegue il programma di test con il flag della riga di comando `--gtest_print_time=0` o si setta la variabile di ambiente GTEST_PRINT_TIME a `0`.

#### Sopprimere l'Output di Testo UTF-8

In caso di errori di asserzione, GoogleTest stampa i valori previsti ed effettivi di tipo `string` sia come stringhe con codifica esadecimale sia come testo UTF-8 leggibile se contengono caratteri UTF-8 non ASCII validi. Per sopprimere il testo UTF-8 perché, ad esempio, non si dispone di un supporto di output compatibile con UTF-8, si esegue il programma di test con `--gtest_print_utf8=0` o si setta la variabile di ambiente `GTEST_PRINT_UTF8` con `0`.

#### Generare un Report XML

GoogleTest può emettere un report XML dettagliato in un file, oltre al normale output testuale. Il report contiene la durata di ciascun test e quindi può aiutare a identificare i test lenti.

Per generare il report XML, si imposta la variabile di ambiente `GTEST_OUTPUT` o il flag `--gtest_output` con la stringa `"xml:path_to_output_file"`, che creerà il file nella posizione specificata. Si può anche utilizzare semplicemente la stringa `"xml"`, nel qual caso l'output si trova nel file `test_detail.xml` nella directory corrente.

Specificando una directory (per esempio, `"xml:output/directory/"` su Linux o `"xml:output\directory\"` su Windows), GoogleTest creerà il file XML in tale directory, che prende il nome dall'eseguibile del test (ad esempio `foo_test.xml` per il programma di test `foo_test` o `foo_test.exe`). Se il file esiste già (magari rimasto da un'esecuzione precedente), GoogleTest sceglierà un nome diverso (ad esempio `foo_test_1.xml`) per evitare di sovrascriverlo.

Il report si basa sul task Ant `junitreport`. Poiché tale formato era originariamente previsto per Java, è necessaria una piccola interpretazione per applicarlo ai test di GoogleTest, come mostrato qui:

```xml
<testsuites name="AllTests" ...>
  <testsuite name="test_case_name" ...>
    <testcase    name="test_name" ...>
      <failure message="..."/>
      <failure message="..."/>
      <failure message="..."/>
    </testcase>
  </testsuite>
</testsuites>

```

*   L'elemento root `<testsuites>` corrisponde all'intero programma di test.
*   Gli elementi `<testsuite>` corrispondono alle test suite di GoogleTest.
*   Gli elementi `<testcase>` corrispondono alle funzioni di test di GoogleTest.

Ad esempio, il seguente programma

```c++
TEST(MathTest, Addition) { ... }
TEST(MathTest, Subtraction) { ... }
TEST(LogicTest, NonContradiction) { ... }

```

potrebbe generare questo report:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites tests="3" failures="1" errors="0" time="0.035" timestamp="2011-10-31T18:52:42" name="AllTests">
  <testsuite name="MathTest" tests="2" failures="1" errors="0" time="0.015">
    <testcase name="Addition" file="test.cpp" line="1" status="run" time="0.007" classname="">
      <failure message="Value of: add(1, 1)&#x0A;  Actual: 3&#x0A;Expected: 2" type="">...</failure>
      <failure message="Value of: add(1, -1)&#x0A;  Actual: 1&#x0A;Expected: 0" type="">...</failure>
    </testcase>
    <testcase name="Subtraction" file="test.cpp" line="2" status="run" time="0.005" classname="">
    </testcase>
  </testsuite>
  <testsuite name="LogicTest" tests="1" failures="0" errors="0" time="0.005">
    <testcase name="NonContradiction" file="test.cpp" line="3" status="run" time="0.005" classname="">
    </testcase>
  </testsuite>
</testsuites>

```

Cose da notare:

*   The `tests` attribute of a `<testsuites>` or `<testsuite>` element tells how
    many test functions the GoogleTest program or test suite contains, while the
`failures` attribute tells how many of them failed.

*   The `time` attribute expresses the duration of the test, test suite, or
    entire test program in seconds.

*   The `timestamp` attribute records the local date and time of the test
    execution.

*   The `file` and `line` attributes record the source file location, where the
    test was defined.

*   Each `<failure>` element corresponds to a single failed GoogleTest
    assertion.

#### Generare un Report JSON

GoogleTest può anche emettere un report JSON come formato alternativo a XML. Per generare il report JSON, si imposta la variabile di ambiente `GTEST_OUTPUT` o il flag `--gtest_output` con la stringa `"json:path_to_output_file"`, che creerà il file nella posizione specificata. Si può anche utilizzare semplicemente la stringa `"json"`, nel qual caso l'output si trova nel file `test_detail.json` nella directory corrente.

Il formato del report è conforme al seguente schema JSON:

```json
{
  "$schema": "https://json-schema.org/schema#",
  "type": "object",
  "definitions": {
    "TestCase": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "tests": { "type": "integer" },
        "failures": { "type": "integer" },
        "disabled": { "type": "integer" },
        "time": { "type": "string" },
        "testsuite": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/TestInfo"
          }

        }

      }

    },
    "TestInfo": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "file": { "type": "string" },
        "line": { "type": "integer" },
        "status": {
          "type": "string",
          "enum": ["RUN", "NOTRUN"]
        },
        "time": { "type": "string" },
        "classname": { "type": "string" },
        "failures": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Failure"
          }

        }

      }

    },
    "Failure": {
      "type": "object",
      "properties": {
        "failures": { "type": "string" },
        "type": { "type": "string" }
      }

    }

  },
  "properties": {
    "tests": { "type": "integer" },
    "failures": { "type": "integer" },
    "disabled": { "type": "integer" },
    "errors": { "type": "integer" },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "time": { "type": "string" },
    "name": { "type": "string" },
    "testsuites": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/TestCase"
      }

    }

  }
}

```

Il report utilizza il formato conforme al seguente Proto3 utilizzando la [codifica JSON](https://developers.google.com/protocol-buffers/docs/proto3#json):

```proto
syntax = "proto3";
package googletest;
import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";
message UnitTest {
  int32 tests = 1;
  int32 failures = 2;
  int32 disabled = 3;
  int32 errors = 4;
  google.protobuf.Timestamp timestamp = 5;
  google.protobuf.Duration time = 6;
  string name = 7;
  repeated TestCase testsuites = 8;
}
message TestCase {
  string name = 1;
  int32 tests = 2;
  int32 failures = 3;
  int32 disabled = 4;
  int32 errors = 5;
  google.protobuf.Duration time = 6;
  repeated TestInfo testsuite = 7;
}
message TestInfo {
  string name = 1;
  string file = 6;
  int32 line = 7;
  enum Status {
    RUN = 0;
    NOTRUN = 1;
  }

  Status status = 2;
  google.protobuf.Duration time = 3;
  string classname = 4;
  message Failure {
    string failures = 1;
    string type = 2;
  }

  repeated Failure failures = 5;
}

```

Ad esempio, il seguente programma

```c++
TEST(MathTest, Addition) { ... }
TEST(MathTest, Subtraction) { ... }
TEST(LogicTest, NonContradiction) { ... }

```

potrebbe generare questo report:

```json
{
  "tests": 3,
  "failures": 1,
  "errors": 0,
  "time": "0.035s",
  "timestamp": "2011-10-31T18:52:42Z",
  "name": "AllTests",
  "testsuites": [
    {
      "name": "MathTest",
      "tests": 2,
      "failures": 1,
      "errors": 0,
      "time": "0.015s",
      "testsuite": [
        {
          "name": "Addition",
          "file": "test.cpp",
          "line": 1,
          "status": "RUN",
          "time": "0.007s",
          "classname": "",
          "failures": [
            {
              "message": "Value of: add(1, 1)\n  Actual: 3\nExpected: 2",
              "type": ""
            },
            {
              "message": "Value of: add(1, -1)\n  Actual: 1\nExpected: 0",
              "type": ""
            }

          ]
        },
        {
          "name": "Subtraction",
          "file": "test.cpp",
          "line": 2,
          "status": "RUN",
          "time": "0.005s",
          "classname": ""
        }

      ]
    },
    {
      "name": "LogicTest",
      "tests": 1,
      "failures": 0,
      "errors": 0,
      "time": "0.005s",
      "testsuite": [
        {
          "name": "NonContradiction",
          "file": "test.cpp",
          "line": 3,
          "status": "RUN",
          "time": "0.005s",
          "classname": ""
        }

      ]
    }

  ]
}

```

{: .callout .important}
IMPORTANTE: Il formato esatto del documento JSON è soggetto a modifiche.

### Controllare Come Vengono Riportati gli Errori

#### Rilevare le Uscite Premature dei Test

Google Test implementa il protocollo _premature-exit-file_ per consentire ai test runner di rilevare qualsiasi tipo di uscita imprevista dei programmi di test. All'avvio, Google Test crea il file che verrà automaticamente eliminato al termine di tutto il lavoro. Poi, il test runner può verificare se questo file esiste. Nel caso in cui il file rimanga non eliminato, il test ispezionato è terminato prematuramente.

Questa funzione è abilitata solo se è stata impostata la variabile di ambiente `TEST_PREMATURE_EXIT_FILE`.

#### Trasformare gli Errori delle Asserzioni in Break-Point

Quando si eseguono programmi di test in un debugger, è molto conveniente che il debugger possa rilevare un errore di asserzione e passare automaticamente alla modalità interattiva. La modalità *break-on-failure* di GoogleTest supporta questo comportamento.

Per abilitarlo, si imposta la variabile di ambiente `GTEST_BREAK_ON_FAILURE` su un valore diverso da `0`. In alternativa, puoi utilizzare il flag della riga di comando `--gtest_break_on_failure`.

#### Disabilitare la Cattura di Eccezioni Test-Thrown

GoogleTest può essere utilizzato con o senza eccezioni abilitate. Se un test genera un'eccezione C++ o (su Windows) un'eccezione strutturata (SEH), per default GoogleTest la rileva, la segnala come un errore del test e continua con il metodo di test successivo. Ciò massimizza la copertura di un'esecuzione di test. Inoltre, su Windows un'eccezione non rilevata genererà una finestra popup, quindi catturare le eccezioni consente di eseguire i test automaticamente.

Durante il debug degli errori di test, tuttavia, si potrebbe invece volere che le eccezioni vengano gestite dal debugger, in modo da poter esaminare lo stack delle chiamate quando viene generata un'eccezione. Per raggiungere questo obiettivo, si imposta la variabile di ambiente `GTEST_CATCH_EXCEPTIONS` su `0` o si usa il flag `--gtest_catch_exceptions=0` durante l'esecuzione dei test.

### Integrazione del Sanitizer

[Undefined Behavior Sanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html), [Address Sanitizer](https://github.com/google/sanitizers/wiki/AddressSanitizer) e [Thread Sanitizer](https://github.com/google/sanitizers/wiki/ThreadSanitizerCppManual) forniscono tutti funzioni deboli che si possono sovrascrivere [override] per sollevare errori espliciti quando rilevano errori di sanitizer, come la creazione di un riferimento da `nullptr`.
Per sovrascrivere queste funzioni, si inseriscono le relative definizioni in un file sorgente che si compila come parte del binario principale:

```
extern "C" {
void __ubsan_on_report() {
  FAIL() << "Encountered an undefined behavior sanitizer error";
}
void __asan_on_error() {
  FAIL() << "Encountered an address sanitizer error";
}
void __tsan_on_report() {
  FAIL() << "Encountered a thread sanitizer error";
}
}  // extern "C"

```

Dopo aver compilato il progetto con uno dei sanitizer abilitati, se un particolare test attiva un errore del sanitizer, GoogleTest segnalerà che non è riuscito.
