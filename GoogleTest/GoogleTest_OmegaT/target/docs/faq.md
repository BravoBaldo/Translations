# FAQ di GoogleTest

## Perché i nomi delle test suite e dei test non devono contenere un underscore?

{: .callout .note}
Nota: GoogleTest si riserva l'underscore (`_`) per parole chiave con scopi speciali, come [il prefisso `DISABLED_`](advanced.md#temporarily-disabling-tests), in aggiunta alla motivazione seguente.

Underscore (`_`) è speciale, poiché il C++ riserva quanto segue per essere utilizzato dal compilatore e dalla libreria standard:

1.  qualsiasi identificatore che inizia con un `_` seguito da una lettera maiuscola e
2.  qualsiasi identificatore che contiene due underscore consecutivi (cioè `__`) *ovunque* nel suo nome.

Al codice utente è *vietato* utilizzare tali identificatori.

Ora vediamo cosa significa per `TEST` e `TEST_F`.

Attualmente `TEST(TestSuiteName, TestName)` genera una classe denominata `TestSuiteName_TestName_Test`. Cosa succede se `TestSuiteName` o `TestName` contengono `_`?

1.  If `TestSuiteName` starts with an `_` followed by an upper-case letter (say,
`_Foo`), we end up with `_Foo_TestName_Test`, which is reserved and thus
    invalid.
2.  Se `TestSuiteName` termina con un `_` (ad esempio `Foo_`), otteniamo `Foo__TestName_Test`, che non è valido.
3.  Se `TestName` inizia con un `_` (ad esempio `_Bar`), otteniamo `TestSuiteName__Bar_Test`, che non è valido.
4.  Se `TestName` termina con un `_` (ad esempio `Bar_`), otteniamo `TestSuiteName_Bar__Test`, che non è valido.

Quindi chiaramente `TestSuiteName` e `TestName` non possono iniziare o finire con `_` (In realtà, `TestSuiteName` può iniziare con `_`—purché il `_` non sia seguito da una lettera maiuscola. Ma la cosa sta diventando complicata. Quindi per semplicità diciamo semplicemente che non può iniziare con `_`.).

Potrebbe sembrare corretto che `TestSuiteName` e `TestName` contengano `_` nel mezzo. Tuttavia, c'è questo da considerare:

```c++
TEST(Time, Flies_Like_An_Arrow) { ... }
TEST(Time_Flies, Like_An_Arrow) { ... }

```

Ora, i due `TEST` genereranno entrambi la stessa classe `Time_Flies_Like_An_Arrow_Test`). Questo non è buono.

Quindi, per semplicità, chiediamo agli utenti di evitare `_` in `TestSuiteName` e in `TestName`. La regola è più vincolante del necessario, ma è semplice e facile da ricordare. Offre inoltre a GoogleTest un po' di margine di manovra nel caso in cui la sua implementazione debba cambiare in futuro.

Violando la regola, potrebbero non esserci conseguenze immediate, ma il test potrebbe (solo potrebbe) "rompersi" con un nuovo compilatore (o una nuova versione del compilatore utilizzato) o con una nuova versione di GoogleTest. Quindi è meglio seguire la regola.

## Perché GoogleTest supporta `EXPECT_EQ(NULL, ptr)` e `ASSERT_EQ(NULL, ptr)` ma non `EXPECT_NE(NULL, ptr)` e `ASSERT_NE(NULL, ptr)`?

Prima di tutto, si può usare `nullptr` con ciascuna di queste macro, ad es. `EXPECT_EQ(ptr, nullptr)`, `EXPECT_NE(ptr, nullptr)`, `ASSERT_EQ(ptr, nullptr)`, `ASSERT_NE(ptr, nullptr)`. Questa è la sintassi preferita nella guida stilistica perché `nullptr` non presenta i problemi sul tipo che presenta `NULL`.

A causa di alcune peculiarità del C++, sono necessari alcuni trucchi di metaprogrammazione non banali per supportare l'uso di `NULL` come argomento delle macro `EXPECT_XX()` e `ASSERT_XX()`. Pertanto lo facciamo solo dove è più necessario (altrimenti rendiamo l'implementazione di GoogleTest più difficile da mantenere e più soggetta a errori del necessario).

Storicamente, la macro `EXPECT_EQ()` prendeva il valore *expected* come primo argomento e il valore *actual* come secondo, sebbene l'ordine degli argomenti ora sia scoraggiato. Era ragionevole che qualcuno volesse scrivere `EXPECT_EQ(NULL, some_expression)`, e in effetti questo è stato richiesto più volte. Pertanto lo abbiamo implementato.

La necessità di `EXPECT_NE(NULL, ptr)` non era così pressante. Quando l'asserzione fallisce, si sa già che `ptr` deve essere `NULL`, quindi non aggiunge alcuna informazione per stampare `ptr` in questo caso. Ciò significa che `EXPECT_TRUE(ptr != NULL)` funziona altrettanto bene.

Se dovessimo supportare `EXPECT_NE(NULL, ptr)`, per coerenza dovremmo supportare anche `EXPECT_NE(ptr, NULL)`. Ciò significa utilizzare i trucchi della metaprogrammazione del template due volte nell'implementazione, rendendolo ancora più difficile da comprendere e mantenere. Riteniamo che il vantaggio non giustifichi il costo.

Infine, con la crescita della libreria di matcher gMock, stiamo incoraggiando le persone a utilizzare la sintassi unificata `EXPECT_THAT(value, matcher)` più spesso nei test. Un vantaggio significativo dell'approccio con i matcher è che questi possono essere facilmente combinati per formare nuovi matcher, mentre le macro `EXPECT_NE`, ecc, non possono essere facilmente combinate. Pertanto vogliamo investire di più nei matcher che nelle macro `EXPECT_XX()`.

## Devo verificare che diverse implementazioni di un'interfaccia soddisfino alcuni requisiti comuni. Dovrei utilizzare test tipizzati o test con valori parametrizzati?

Per testare varie implementazioni della stessa interfaccia, è possibile eseguire test tipizzati o test con valori parametrizzati. È davvero personale decidere quale sia più conveniente, a seconda del caso particolare. Alcune linee guida approssimative:

*   Typed tests can be easier to write if instances of the different
    implementations can be created the same way, modulo the type. Per esempio,
    if all these implementations have a public default constructor (such that
    you can write `new TypeParam`), or if their factory functions have the same
    form (e.g. `CreateInstance<TypeParam>()`).
*   Value-parameterized tests can be easier to write if you need different code
    patterns to create different implementations' instances, e.g. `new Foo` vs
`new Bar(5)`. To accommodate for the differences, you can write factory
    function wrappers and pass these function pointers to the tests as their
    parameters.
*   When a typed test fails, the default output includes the name of the type,
    which can help you quickly identify which implementation is wrong.
    Value-parameterized tests only show the number of the failed iteration by
    default. You will need to define a function that returns the iteration name
    and pass it as the third parameter to INSTANTIATE_TEST_SUITE_P to have more
    useful output.
*   When using typed tests, you need to make sure you are testing against the
    interface type, not the concrete types (in other words, you want to make
    sure `implicit_cast<MyInterface*>(my_concrete_impl)` works, not just that
`my_concrete_impl` works). It's less likely to make mistakes in this area
    when using value-parameterized tests.

Speriamo di non aver aumentato la confusione. :-) Se possibile, suggeriamo di provare entrambi gli approcci. La pratica è un modo molto migliore per cogliere le sottili differenze tra i due strumenti. Una volta acquisita un'esperienza concreta, si potrà decidere molto più facilmente quale utilizzare.

## Il mio "death test" modifica alcuni stati, ma il cambiamento sembra perso al termine del test. Perché?

I death test (`EXPECT_DEATH`, ecc.) vengono eseguiti in un sottoprocesso s.t. il crash previsto non kill-erà il programma di test (ovvero il processo principale). Di conseguenza, eventuali effetti collaterali in memoria che avvengono sono osservabili nei rispettivi sottoprocessi, ma non nel processo principale. Si possono pensare come se venissero eseguiti in un universo parallelo, più o meno.

In particolare, se si utilizza il mocking e l'enunciato del death test invoca alcuni metodi mock, il processo genitore penserà che le chiamate non siano mai avvenute. Pertanto, si potrebbero spostare le istruzioni `EXPECT_CALL` nella macro `EXPECT_DEATH`.

## EXPECT_EQ(htonl(blah), blah_blah) genera strani errori del compilatore in modalità opt. È un bug di GoogleTest?

In realtà il bug è in `htonl()`.

Secondo `'man htonl'`, `htonl()` è una *funzione*, il che significa che è corretto utilizzare `htonl` come puntatore a funzione. Tuttavia, in modalità opt `htonl()` è definito come una *macro*, il che interrompe questo utilizzo.

Peggio ancora, la definizione della macro di `htonl()` utilizza un'estensione di `gcc` che *non* è C++ standard. Questa implementazione complicata presenta alcune limitazioni ad hoc. In particolare, impedisce di scrivere `Foo<sizeof(htonl(x))>()`, dove `Foo` è un template che ha un argomento intero.

L'implementazione di `EXPECT_EQ(a, b)` usa `sizeof(... a ...)` all'interno di un argomento template e quindi non viene compilato in modalità opt quando `a` contiene una chiamata a `htonl()`. È difficile fare in modo che `EXPECT_EQ` bypassi il bug `htonl()`, poiché la soluzione deve funzionare con diversi compilatori su varie piattaforme.

## Il compilatore si lamenta di "riferimenti non definiti" ad alcune variabili membro const statiche, ma sono state definite nel corpo della classe. Cosa c'è che non va?

Se la classe ha un membro dati static:

```c++
// foo.h
class Foo {
  ...
  static const int kBar = 100;
};

```

lo si deve definire anche *al di fuori* del corpo della classe in `foo.cc`:

```c++
const int Foo::kBar;  // Nessun inizializzatore qui.

```

Altrimenti il codice sarà **C++ invalido**, e potrebbe 'rompersi' in modi imprevisti. In particolare, utilizzarlo nelle asserzioni di confronto di GoogleTest (`EXPECT_EQ`, ecc.) genererà un errore del linker "undefined reference". Il fatto che "funzionava" non significa che sia valido. Significa solo che si è stati fortunati. :-)

Se la dichiarazione del membro dati statico è `constexpr` allora è implicitamente una definizione `inline` e non è necessaria una definizione separata in `foo.cc`:

```c++
// foo.h
class Foo {
  ...
  static constexpr int kBar = 100;  // Defines kBar, no need to do it in foo.cc.
};

```

## Posso derivare una fixture da un'altra?

Sì.

Ogni fixture ha una test suite corrispondente e con lo stesso nome. Ciò significa che solo una test suite può utilizzare una particolare fixture. A volte, tuttavia, più casi di test potrebbero voler utilizzare le stesse fixture o leggermente diverse. Ad esempio, si potrebbe vole essere sicuri che tutte le test suite di una libreria GUI non abbiano importanti "leak" di risorse di sistema come font e brush.

In GoogleTest, si condivide una fixture tra le test suite inserendo la logica condivisa in una fixture di base, poi derivando da quella base una fixture separata per ciascuna test suite che voglia utilizzare questa logica comune. Poi si usa `TEST_F()` per scrivere i test utilizzando ciascuna fixture derivata.

In genere, il codice è simile al seguente:

```c++
// Definisce una fixture base.
class BaseTest : public ::testing::Test {
 protected:
  ...
};
// Derives a fixture FooTest from BaseTest.
class FooTest : public BaseTest {
 protected:
  void SetUp() override {
    BaseTest::SetUp();  // Configura prima la fixture base.
    ... ulteriori impostazioni ...
  }

  void TearDown() override {
    ... ripulitura di FooTest ...
    BaseTest::TearDown();  // Ricordarsi di dismettere la fixture base
                           // dopo aver ripulito FooTest!
  }

  ... functions and variables for FooTest ...
};
// Tests that use the fixture FooTest.
TEST_F(FooTest, Bar) { ... }
TEST_F(FooTest, Baz) { ... }
... additional fixtures derived from BaseTest ...
```

Se necessario, è possibile continuare a derivare fixture da una fixture derivata.
GoogleTest non ha limiti sulla profondità della gerarchia.

Per un esempio completo sull'uso delle fixture derivate, vedere [sample5_unittest.cc](https://github.com/google/googletest/blob/main/googletest/samples/sample5_unittest.cc).

## Il mio compilatore dice "void value not ignored as it ought to be". Cosa significa?

Probabilmente si sta utilizzando un `ASSERT_*()` in una funzione che non restituisce `void`.
`ASSERT_*()` può essere utilizzato solo nelle funzioni `void`, poiché le eccezioni sono disabilitate dal nostro sistema di build. Consultare ulteriori dettagli [qui](advanced.md#assertion-placement).

## Il mio death test si blocca (o ci sono errori seg-fault). Come lo si ripara?

In GoogleTest, i death test vengono eseguiti in un processo figlio e il modo in cui funzionano è delicato. Per scrivere dei death test si devono veramente capire come funzionano: vederei i dettagli nelle [Asserzioni Death](reference/assertions.md#death) nei Riferimenti sulle Asserzioni.

In particolare, ai death test non piace avere più thread nel processo principale. Quindi la prima cosa che si può provare è eliminare la creazione di thread al di fuori di `EXPECT_DEATH()`. Ad esempio, si potrebbero utilizzare oggetti mock o fake invece di quelli reali nei test.

A volte questo è impossibile poiché alcune librerie da utilizzare potrebbero creare thread prima ancora che venga raggiunto il `main()`. In questo caso, si può provare a ridurre al minimo la possibilità di conflitti spostando quante più attività possibili all'interno di `EXPECT_DEATH()` (nel caso estremo, si può spostare tutto all'interno), o lasciandone poche cose. Inoltre, si può provare a impostare lo stile del death test su `"threadsafe"`, che è più sicuro ma più lento, e vedere se aiuta.

Se si usano i death test thread-safe, ricordarsi che eseguono nuovamente il programma di test dall'inizio nel processo figlio. Il programma deve poter funzionare fianco a fianco con se stesso e che sia deterministico.

Alla fine, questo si riduce a una buona programmazione concorrente. Non ci devono essere condizioni di race o deadlock nel programma. Spiacenti: nessuna soluzione miracolosa!

## Si usa il costruttore/distruttore della fixture o SetUp()/TearDown()? {#CtorVsSetUp}

La prima cosa da ricordare è che that GoogleTest **non** riutilizza lo stesso oggetto fixture in più test. Per ciascun `TEST_F`, GoogleTest creerà un **nuovo** oggetto fixture, chiamerà immediatamente `SetUp()`, eseguirà il corpo del test, chiamerà `TearDown()` per poi eseguire il delete dell'oggetto fixture.

Quando è necessario scrivere la logica di configurazione e ripulitura per ciascun test, è possibile scegliere tra utilizzare il costruttore/distruttore della fixture o `SetUp()`/`TearDown()`.
Il primo è solitamente preferito perché presenta i seguenti vantaggi:

*   By initializing a member variable in the constructor, we have the option to
    make it `const`, which helps prevent accidental changes to its value and
    makes the tests more obviously correct.
*   In case we need to subclass the test fixture class, the subclass'
    constructor is guaranteed to call the base class' constructor *first*, and
    the subclass' destructor is guaranteed to call the base class' destructor
*afterward*. With `SetUp()/TearDown()`, a subclass may make the mistake of
    forgetting to call the base class' `SetUp()/TearDown()` or call them at the
    wrong time.

Si potrebbe comunque usare `SetUp()/TearDown()` nei seguenti casi:

*   Il C++ non consente chiamate di funzioni virtuali nei costruttori e nei distruttori.
    You can call a method declared as virtual, but it will not use dynamic
    dispatch. It will use the definition from the class the constructor of which
    is currently executing. This is because calling a virtual method before the
    derived class constructor has a chance to run is very dangerous - the
    virtual method might operate on uninitialized data. Therefore, if you need
    to call a method that will be overridden in a derived class, you have to use
`SetUp()/TearDown()`.
*   Nel corpo di un costruttore (o di un distruttore), non è possibile utilizzare le macro `ASSERT_xx`. Therefore, if the set-up operation could cause a fatal
    test failure that should prevent the test from running, it's necessary to
    use `abort` and abort the whole test
    executable, or to use `SetUp()` instead of a constructor.
*   If the tear-down operation could throw an exception, you must use
`TearDown()` as opposed to the destructor, as throwing in a destructor leads
    to undefined behavior and usually will kill your program right away. Note
    that many standard libraries (like STL) may throw when exceptions are
    enabled in the compiler. Therefore you should prefer `TearDown()` if you
    want to write portable tests that work with or without exceptions.
*   The GoogleTest team is considering making the assertion macros throw on
    platforms where exceptions are enabled (e.g. Windows, Mac OS, and Linux
    client-side), which will eliminate the need for the user to propagate
    failures from a subroutine to its caller. Therefore, you shouldn't use
    GoogleTest assertions in a destructor if your code could run on such a
    platform.

## Il compilatore dice "no matching function to call" quando si usa `ASSERT_PRED*`. Come lo si ripara?

Vedere i dettagli per [`EXPECT_PRED*`](reference/assertions.md#EXPECT_PRED) nei "Riferimenti sulle Asserzioni"

## Il compilatore dice "ignoring return value" quando si chiama RUN_ALL_TESTS(). Perché?

Qualcuno ha ignorato il valore restituito da `RUN_ALL_TESTS()`. Cioè, invece di

```c++
  return RUN_ALL_TESTS();

```

scrivono

```c++
  RUN_ALL_TESTS();

```

Questo è **sbagliato e pericoloso**. I servizi di test devono vedere il valore restituito di `RUN_ALL_TESTS()` per determinare se un test è stato superato. Se la funzione `main()` lo ignora, il test verrà considerato riuscito anche se presenta un errore nell'asserzione di GoogleTest. Molto brutto.

Abbiamo deciso di risolvere questo problema (grazie a Michael Chastain per l'idea). Ora il codice non sarà più in grado di ignorare `RUN_ALL_TESTS()` quando verrà compilato con `gcc`. Facendolo, si riceverà un errore del compilatore.

Se il compilatore si lamenta del fatto che viene ignorato il valore restituito di `RUN_ALL_TESTS()`, la soluzione è semplice: si deve utilizzare il valore come valore restituito da `main()`.

Ma come potremmo introdurre un cambiamento che renda non funzionanti i test esistenti? Bene, in questo caso il codice era già bacato, quindi non è stato guastato adesso. :-)

## Il compilatore dice che un costruttore (o un distruttore) non può restituire un valore. Cosa sta succedendo?

A causa di una peculiarità del C++, per supportare la sintassi per lo streaming dei messaggi su un `ASSERT_*`, ad es.

```c++
  ASSERT_EQ(1, Foo()) << "blah blah" << foo;

```

abbiamo dovuto rinunciare a utilizzare `ASSERT*` e `FAIL*` (ma non `EXPECT*` e `ADD_FAILURE*`) nei costruttori e nei distruttori. La soluzione alternativa è quella di spostare il contenuto del costruttore/distruttore in una funzione membro void privata o passare a `EXPECT_*()` se funziona. Questa [sezione](advanced.md#assertion-placement) nella guida utente lo spiega.

## La funzione SetUp() non viene chiamata. Perché?

Il C++ fa distinzione tra maiuscole e minuscole. È stato scritto `Setup()`?

Allo stesso modo, a volte le persone scrivono `SetUpTestSuite()` come `SetupTestSuite()` e si chiedono perché non venga mai chiamato.

## Abbiamo diverse test suite che condividono la stessa logica della fixture; si deve definire una nuova classe fixture per ognuna di esse? Sembra piuttosto noioso.

Non è necessario. Invece di

```c++
class FooTest : public BaseTest {};
TEST_F(FooTest, Abc) { ... }
TEST_F(FooTest, Def) { ... }
class BarTest : public BaseTest {};
TEST_F(BarTest, Abc) { ... }
TEST_F(BarTest, Def) { ... }
```

si può semplicemente avere un `typedef` delle fixture:

```c++
typedef BaseTest FooTest;
TEST_F(FooTest, Abc) { ... }
TEST_F(FooTest, Def) { ... }
typedef BaseTest BarTest;
TEST_F(BarTest, Abc) { ... }
TEST_F(BarTest, Def) { ... }
```

## L'output di GoogleTest è sepolto in un sacco di messaggi di LOG. Cosa si deve fare?

L'output di GoogleTest vuole essere un rapporto conciso e di facile comprensione. Se il test genera esso stesso un output testuale, si mescolerà con l'output di GoogleTest, rendendolo difficile da leggere. Tuttavia, esiste una soluzione semplice a questo problema.

Poiché i messaggi di `LOG` vanno a stderr, abbiamo deciso di lasciare che l'output di GoogleTest vada a stdout. In questo modo, si possono facilmente separare i due utilizzando il reindirizzamento. Per esempio:

```shell
$ ./my_test > gtest_output.txt

```

## Perché dovrei preferire le fixture alle variabili globali?

Ci sono diversi buoni motivi:

1.  È probabile che il test debba modificare gli stati delle sue variabili globali.
    This makes it difficult to keep side effects from escaping one test and
    contaminating others, making debugging difficult. By using fixtures, each
    test has a fresh set of variables that's different (but with the same
    names). Pertanto, i test vengono mantenuti indipendenti l'uno dall'altro.
2.  Le variabili globali inquinano il namespace globale.
3.  Test fixtures can be reused via subclassing, which cannot be done easily
    with global variables. This is useful if many test suites have something in
    common.

## Quale può essere l'argomento dell'istruzione in ASSERT_DEATH()?

`ASSERT_DEATH(statement, matcher)` (o qualsiasi macro di asserzione death) può essere utilizzato ovunque sia valido *`statement`*. Quindi, in pratica *`statement`* può essere qualsiasi istruzione C++ che abbia senso nel contesto corrente. In particolare può fare riferimento a variabili globali e/o locali e può essere:

*   una semplice chiamata di funzione (spesso accade),
*   un'espressione complessa, o
*   un'istruzione composta.

Alcuni esempi sono mostrati qui:

```c++
// Un death test può essere una semplice chiamata di funzione.
TEST(MyDeathTest, FunctionCall) {
  ASSERT_DEATH(Xyz(5), "Xyz failed");
}
// Or a complex expression that references variables and functions.
TEST(MyDeathTest, ComplexExpression) {
  const bool c = Condition();
  ASSERT_DEATH((c ? Func1(0) : object2.Method("test")),
               "(Func1|Method) failed");
}
// Death assertions can be used anywhere in a function.  In
// particolare, possono trovarsi all'interno di un loop.
TEST(MyDeathTest, InsideLoop) {
  // Verifica che Foo(0), Foo(1), ..., e Foo(4) 'muoiano' tutte.
  for (int i = 0; i < 5; i++) {
    EXPECT_DEATH_M(Foo(i), "Foo has \\d+ errors",
                   ::testing::Message() << "where i is " << i);
  }
}
// A death assertion can contain a compound statement.
TEST(MyDeathTest, CompoundStatement) {
  // Verifica che almeno uno tra Bar(0), Bar(1), ..., e
  // Bar(4) 'muoia'.
  ASSERT_DEATH({
    for (int i = 0; i < 5; i++) {
      Bar(i);
    }

  },
  "Bar has \\d+ errors");
}

```

## Ho una classe fixture `FooTest`, ma `TEST_F(FooTest, Bar)` mi dà l'errore ``"no matching function for call to `FooTest::FooTest()'"``. Perché?

GoogleTest deve essere in grado di creare oggetti della classe fixture, quindi deve avere un costruttore di default. Normalmente il compilatore ne definisce uno.
Tuttavia, ci sono casi in cui è necessario definirne uno manualmente:

*   If you explicitly declare a non-default constructor for class `FooTest`
    (`DISALLOW_EVIL_CONSTRUCTORS()` does this), then you need to define a
    default constructor, even if it would be empty.
*   If `FooTest` has a const non-static data member, then you have to define the
    default constructor *and* initialize the const member in the initializer
    list of the constructor. (Early versions of `gcc` doesn't force you to
    initialize the const member. È un bug corretto in `gcc 4`.)

## Perché ASSERT_DEATH dice che era già [joined] ai thread precedenti?

Con la libreria pthread di Linux, non è possibile tornare indietro una volta oltrepassata la linea da un singolo thread a più thread. La prima volta che si crea un thread, viene creato in aggiunta un thread di gestione, quindi si hanno 3 thread, non 2. Successivamente, quando il thread creato va in join al thread principale, il conteggio dei thread diminuisce di 1, ma il thread di gestione non verrà mai killato, quindi si avranno ancora 2 thread, il che significa che non si può eseguire in sicurezza un death test.

La nuova libreria di thread NPTL non soffre di questo problema, poiché non crea un thread di gestione. Tuttavia, se non si controlla su quale macchina viene eseguito il test, non si dovrebbe dipendere da questo.

## Perché GoogleTest richiede che l'intera test suite, anziché i singoli test, venga denominata `*DeathTest` quando usa `ASSERT_DEATH`?

GoogleTest non intercala test di diverse test suite. Cioè, esegue prima tutti i test in una test suite, poi esegue tutti i test nella test suite successiva e così via. GoogleTest fa questo perché deve impostare una test suite prima che venga eseguito il primo test al suo interno ed eseguirne il "tear down" successivamente. La suddivisione del test case richiederebbe più processi di set-up e tear-down, il che è inefficiente e rende la semantica impura.

Se dovessimo determinare l'ordine dei test in base al nome del test invece che al nome del test case, avremmo un problema con la seguente situazione:

```c++
TEST_F(FooTest, AbcDeathTest) { ... }
TEST_F(FooTest, Uvw) { ... }
TEST_F(BarTest, DefDeathTest) { ... }
TEST_F(BarTest, Xyz) { ... }
```

Poiché `FooTest.AbcDeathTest` deve essere eseguito prima di `BarTest.Xyz`, e non interlacciamo test di diverse test suite, dobbiamo eseguire tutti i test nel caso `FooTest` prima di eseguire qualsiasi test nel caso `BarTest`. Ciò è in contraddizione con l'obbligo di eseguire `BarTest.DefDeathTest` prima di `FooTest.Uvw`.

## Ma non mi piace chiamare tutta la mia test suite `*DeathTest` quando contiene sia death test che non. Cosa si deve fare?

Non è necessario, ma volendo, si può suddividere la test suite in `FooTest` e `FooDeathTest`, dove i nomi chiariscono che sono correlati:

```c++
class FooTest : public ::testing::Test { ... };
TEST_F(FooTest, Abc) { ... }
TEST_F(FooTest, Def) { ... }
using FooDeathTest = FooTest;
TEST_F(FooDeathTest, Uvw) { ... EXPECT_DEATH(...) ... }
TEST_F(FooDeathTest, Xyz) { ... ASSERT_DEATH(...) ... }

```

## GoogleTest stampa i messaggi di LOG nel processo figlio di un death test solo quando il test fallisce. Come posso vedere i messaggi di LOG quando il death test ha successo?

Stampare i messaggi di LOG generati dall'istruzione all'interno di `EXPECT_DEATH()` rende più difficile la ricerca di problemi reali nel log del genitore. Pertanto GoogleTest li stampa solo quando il death test è fallito.

Se c'è davvero bisogno di vedere tali messaggi di LOG, una soluzione alternativa è quella di interrompere temporaneamente il death test (ad esempio modificando il pattern regex che dovrebbe corrispondere). Certo, questo è un trucco. Prenderemo in considerazione una soluzione più permanente dopo l'implementazione dei death test in stile fork-and-exec.

## Il compilatore dice `no match for 'operator<<'` quando si usa un'asserzione. Cosa dà?

Se si usa un tipo definito dall'utente `FooType` in un'asserzione, ci dev'essere una funzione `std::ostream& operator<<(std::ostream&, const FooType&)` definita in modo tale da poter stampare un valore di `FooType`.

Inoltre, se `FooType` è dichiarato in un namespace, anche l'operatore `<<` deve essere definito nello *stesso* namespace. Per i dettagli vedere [Tip of the Week #49](https://abseil.io/tips/49).

## Come sopprimere i messaggi riguardo ai memory leak su Windows?

Poiché il singleton GoogleTest inizializzato staticamente richiede allocazioni nell'heap, il rilevatore di memory leak di Visual C++ segnalerà le perdite di memoria alla fine dell'esecuzione del programma. Il modo più semplice per evitare ciò è utilizzare le chiamate `_CrtMemCheckpoint` e `_CrtMemDumpAllObjectsSince` per non riportare alcun oggetto heap inizializzato staticamente. Consultare MSDN per ulteriori dettagli e routine aggiuntive di check/debug.

## Come può il mio codice rilevare se è in esecuzione in un test?

Se si scrive codice che "annusa" se è in esecuzione in un test e fa cose diverse di conseguenza, si sta perdendo la logica "test-only" nel codice di produzione e non esiste un modo semplice per garantire che i percorsi del codice test-only non vengano eseguiti per errore in produzione. Tale intelligenza porta anche agli [Heisenbugs](https://en.wikipedia.org/wiki/Heisenbug). Pertanto sconsigliamo vivamente questa pratica e GoogleTest non fornisce un modo per farlo.

In generale, il modo consigliato per far sì che il codice si comporti diversamente durante il test è la [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection). È possibile iniettare funzionalità diverse dal codice di test e quello di produzione. Poiché il codice di produzione non si collega affatto alla logica for-test (l'attributo [`testonly`](https://docs.bazel.build/versions/master/be/common-definitions.html#common.testonly) per i target BUILD aiuta a garantirlo), non c'è pericolo di eseguirlo accidentalmente.

Tuttavia, se *davvero*, *davvero*, *davvero* non si ha scelta e se si segue la regola di terminare i nomi dei programmi di test con `_test`, si può usare il trucco *orribile* di sniffare il nome dell'eseguibile (`argv[0]` in `main()`) per sapere se il codice è in fase di test.

## Come disattivare temporaneamente un test?

Se si ha un test non funzionante che non si può correggere subito, si può aggiungere il prefisso `DISABLED_` al nome. Ciò lo escluderà dall'esecuzione. Questo è meglio che commentare il codice o usare `#if 0`, poiché i test disabilitati vengono comunque compilati (e quindi non "marciranno").

Per includere i test disabilitati nell'esecuzione del test, basta richiamare il programma di test con il flag `--gtest_also_run_disabled_tests`.

## Va bene se ho due metodi di test `TEST(Foo, Bar)` separati definiti in namespace diversi?

Sì.

La regola è che **tutti i metodi dei test nella stessa test suite devono utilizzare la stessa classe fixture**. Ciò significa che quanto segue è **consentito** poiché entrambi i test utilizzano la stessa classe fixture (`::testing::Test`).

```c++
namespace foo {
TEST(CoolTest, DoSomething) {
  SUCCEED();
}
}  // namespace foo
namespace bar {
TEST(CoolTest, DoSomething) {
  SUCCEED();
}
}  // namespace bar

```

Tuttavia, il codice seguente **non è consentito** e genererà un errore a runtime da GoogleTest poiché i metodi di test utilizzano classi di fixture diverse con lo stesso nome della test suite.

```c++
namespace foo {
class CoolTest : public ::testing::Test {};  // Fixture foo::CoolTest
TEST_F(CoolTest, DoSomething) {
  SUCCEED();
}
}  // namespace foo
namespace bar {
class CoolTest : public ::testing::Test {};  // Fixture: bar::CoolTest
TEST_F(CoolTest, DoSomething) {
  SUCCEED();
}
}  // namespace bar

```
