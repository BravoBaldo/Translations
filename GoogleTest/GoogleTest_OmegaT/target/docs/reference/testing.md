# Riferimento al Testing

<!--* toc_depth: 3 *-->

Questa pagina elenca le funzionalità fornite da GoogleTest per scrivere programmi di test.
Per usarle, si aggiunge `#include <gtest/gtest.h>`.

## Le Macro

GoogleTest definisce le seguenti macro per scrivere i test.

### TEST {#TEST}

<pre>
TEST(<em>TestSuiteName</em>, <em>TestName</em>) {
  ... <em>statements</em> ...
}
</pre>

Definisce un singolo test denominato *`TestName`* nella test suite *`TestSuiteName`*, costituito dalle determinate istruzioni.

Entrambi gli argomenti *`TestSuiteName`* e *`TestName`* devono essere identificatori C++ validi e non devono contenere underscore (`_`). I test in diverse test suite possono avere lo stesso nome individuale.

Le istruzioni all'interno del corpo del test possono essere qualsiasi codice da testare.
Le [asserzioni](assertions.md) utilizzate all'interno del corpo del test determinano l'esito del test.

### TEST_F {#TEST_F}

<pre>
TEST_F(<em>TestFixtureName</em>, <em>TestName</em>) {
  ... <em>statements</em> ...
}
</pre>

Definisce un singolo test denominato *`TestName`* che usa la classe fixture *`TestFixtureName`*. Il nome della test suite è *`TestFixtureName`*.

Entrambi gli argomenti *`TestFixtureName`* e *`TestName`* devono essere identificatori C++ validi e non devono contenere underscore (`_`). *`TestFixtureName`* deve essere il nome di una classe fixture di test; vedere [Test Fixtures](../primer.md#same-data-multiple-tests).

Le istruzioni all'interno del corpo del test possono essere qualsiasi codice da testare.
Le [asserzioni](assertions.md) utilizzate all'interno del corpo del test determinano l'esito del test.

### TEST_P {#TEST_P}

<pre>
TEST_P(<em>TestFixtureName</em>, <em>TestName</em>) {
  ... <em>statements</em> ...
}
</pre>

Definisce un singolo test con valori parametrizzati denominato *`TestName`* che usa la classe fixture *`TestFixtureName`*. Il nome della test suite è *`TestFixtureName`*.

Entrambi gli argomenti *`TestFixtureName`* e *`TestName`* devono essere identificatori C++ validi e non devono contenere underscore (`_`). *`TestFixtureName`* deve essere il nome di una classe fixture con valori parametrizzati; vedere [Test con Valori Parametrizzati](../advanced.md#value-parameterized-tests).

Le istruzioni all'interno del corpo del test possono essere qualsiasi codice da testare. Le istruzioni all'interno del corpo del test, è possibile accedere al parametro del test con la funzione `GetParam()` (vedere [`WithParamInterface`](#WithParamInterface)). Per esempio:

```cpp
TEST_P(MyTestSuite, DoesSomething) {
  ...
  EXPECT_TRUE(DoSomething(GetParam()));
  ...
}

```

Le [asserzioni](assertions.md) utilizzate all'interno del corpo del test determinano l'esito del test.

Vedere anche [`INSTANTIATE_TEST_SUITE_P`](#INSTANTIATE_TEST_SUITE_P).

### INSTANTIATE_TEST_SUITE_P {#INSTANTIATE_TEST_SUITE_P}

`INSTANTIATE_TEST_SUITE_P(`*`InstantiationName`*`,`*`TestSuiteName`*`,`*`param_generator`*`)`
\
`INSTANTIATE_TEST_SUITE_P(`*`InstantiationName`*`,`*`TestSuiteName`*`,`*`param_generator`*`,`*`name_generator`*`)`

Crea un'istanza della test suite *`TestSuiteName`* con valori parametrizzati (definita con [`TEST_P`](#TEST_P)).

L'argomento *`InstantiationName`* è un nome univoco per l'istanziazione della test suite, per distinguere tra più istanze. Nell'output del test, il nome dell'istanza viene aggiunto come prefisso al nome della test suite *`TestSuiteName`*.

L'argomento *`param_generator`* è una delle seguenti funzioni fornite da GoogleTest che generano i parametri di test, tutti definiti nel namespace `::testing`:

<span id="param-generators"></span>

| Generatore di Parametri | Comportamento |
| ------------------- | ---------------------------------------------------- |
| `Range(begin, end [, step])` | Restituisce i valori `{begin, begin+step, begin+step+step, ...}`. I valori non includono `end`. Il default di `step` è 1. |
| `Values(v1, v2, ..., vN)` | Restituisce i valori `{v1, v2, ..., vN}`. |
| `ValuesIn(container)` o `ValuesIn(begin,end)` | Restituisce valori da un array in stile C, un contenitore in stile STL o un iteratore range `[begin, end)`. |
| `Bool()` | Restituisce la sequenza `{false, true}`. |
| `Combine(g1, g2, ..., gN)` | Restituisce come `std::tuple` *n* tutte le combinazioni (prodotto cartesiano) dei valori generati dagli *n* generatori `g1`, `g2`, ..., `gN`. |
| `ConvertGenerator<T>(g)` | Restituisce i valori generati dal generatore `g`, `static_cast` a `T`. |

L'ultimo argomento facoltativo *`name_generator`* è una funzione o un funtore che genera suffissi personalizzati del nome del test in base ai parametri del test. La funzione deve accettare un argomento di tipo [`TestParamInfo<class ParamType>`](#TestParamInfo) e restituire una `std::string`.
Il suffisso del nome del test può contenere solo caratteri alfanumerici e underscore.
GoogleTest fornisce [`PrintToStringParamName`](#PrintToStringParamName), oppure è possibile utilizzare una funzione personalizzata per un maggiore controllo:

```cpp
INSTANTIATE_TEST_SUITE_P(
    MyInstantiation, MyTestSuite,
    testing::Values(...),
    [](const testing::TestParamInfo<MyTestSuite::ParamType>& info) {
      // Può utilizzare info.param per generare il suffisso del test
      std::string name = ...
      return name;
    });

```

Per ulteriori informazioni, consultare [Test con Valori Parametrizzati](../advanced.md#value-parameterized-tests).

Vedere anche [`GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST`](#GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST).

### TYPED_TEST_SUITE {#TYPED_TEST_SUITE}

`TYPED_TEST_SUITE(`*`TestFixtureName`*`,`*`Types`*`)`

Definisce una test suite tipizzata in base alla fixture *`TestFixtureName`*. Il nome della test suite è *`TestFixtureName`*.

L'argomento *`TestFixtureName`* è una classe fixture template, parametrizzata da un tipo, per esempio:

```cpp
template <typename T>
class MyFixture : public testing::Test {
 public:
  ...
  using List = std::list<T>;
  static T shared_;
  T value_;
};

```

L'argomento *`Types`* è un oggetto [`Types`](#Types) che rappresenta l'elenco dei tipi su cui eseguire i test, ad esempio:

```cpp
using MyTypes = ::testing::Types<char, int, unsigned int>;
TYPED_TEST_SUITE(MyFixture, MyTypes);

```

L'alias del tipo (`using` o `typedef`) è necessario affinché la macro `TYPED_TEST_SUITE` lo possa analizzare correttamente.

Vedere anche [`TYPED_TEST`](#TYPED_TEST) e [Test Tipizzati](../advanced.md#typed-tests) per ulteriori informazioni.

### TYPED_TEST {#TYPED_TEST}

<pre>
TYPED_TEST(<em>TestSuiteName</em>, <em>TestName</em>) {
  ... <em>statements</em> ...
}
</pre>

Definisce un singolo test tipizzato denominato *`TestName`* nella test suite tipizzata *`TestSuiteName`*. La test suite dev'essere definita con [`TYPED_TEST_SUITE`](#TYPED_TEST_SUITE).

All'interno del corpo del test, il nome speciale `TypeParam` si riferisce al parametro del tipo e `TestFixture` si riferisce alla classe fixture. Vedere l'esempio seguente:

```cpp
TYPED_TEST(MyFixture, Example) {
  // All'interno di un test, fare riferimento al nome speciale TypeParam per ottenere il tipo
  // del parametro.  Poiché ci troviamo all'interno di una classe template derivata, il C++ ci richiede
  // di visitare i membri di MyFixture tramite 'this'.
  TypeParam n = this->value_;
  // Per visitare i membri statici della fixture, si antepone 'TestFixture::'
  // come prefisso.
  n += TestFixture::shared_;
  // Per fare riferimento a typedef nella fixture, si antepone 'typename TestFixture::'
  // come prefisso. Il 'typename' è necessario per soddisfare il compilatore.
  typename TestFixture::List values;
  values.push_back(n);
  ...
}

```

Per ulteriori informazioni, consultare [Test Tipizzati](../advanced.md#typed-tests).

### TYPED_TEST_SUITE_P {#TYPED_TEST_SUITE_P}

`TYPED_TEST_SUITE_P(`*`TestFixtureName`*`)`

Definisce test suite con tipi parametrizzati basata sulla fixture *`TestFixtureName`*. Il nome della test suite è *`TestFixtureName`*.

L'argomento *`TestFixtureName`* è una classe fixture template, parametrizzata da un tipo. Vedere [`TYPED_TEST_SUITE`](#TYPED_TEST_SUITE) per un esempio.

Vedere anche [`TYPED_TEST_P`](#TYPED_TEST_P) e [Test con i Tipi Parametrizzati](../advanced.md#type-parameterized-tests) per ulteriori informazioni.

### TYPED_TEST_P {#TYPED_TEST_P}

<pre>
TYPED_TEST_P(<em>TestSuiteName</em>, <em>TestName</em>) {
  ... <em>statements</em> ...
}
</pre>

Definisce un singolo test con tipi parametrizzati *`TestName`* nella test suite con tipi parametrizzati *`TestSuiteName`*. La test suite dev'essere definita con [`TYPED_TEST_SUITE_P`](#TYPED_TEST_SUITE_P).

All'interno del corpo del test, il nome speciale `TypeParam` si riferisce al parametro del tipo e `TestFixture` si riferisce alla classe fixture. Vedere [`TYPED_TEST`](#TYPED_TEST) per un esempio.

Consultare anche [`REGISTER_TYPED_TEST_SUITE_P`](#REGISTER_TYPED_TEST_SUITE_P) e [Test con i Tipi Parametrizzati](../advanced.md#type-parameterized-tests) per ulteriori informazioni.

### REGISTER_TYPED_TEST_SUITE_P {#REGISTER_TYPED_TEST_SUITE_P}

`REGISTER_TYPED_TEST_SUITE_P(`*`TestSuiteName`*`,`*`TestNames...`*`)`

Registra i test con tipi parametrizzati *`TestNames...`* della test suite *`TestSuiteName`*. La test suite e i test devono essere definiti con [`TYPED_TEST_SUITE_P`](#TYPED_TEST_SUITE_P) e [`TYPED_TEST_P`](#TYPED_TEST_P).

Per esempio:

```cpp
// Definisce la test suite e i test.
TYPED_TEST_SUITE_P(MyFixture);
TYPED_TEST_P(MyFixture, HasPropertyA) { ... }
TYPED_TEST_P(MyFixture, HasPropertyB) { ... }
// Register the tests in the test suite.
REGISTER_TYPED_TEST_SUITE_P(MyFixture, HasPropertyA, HasPropertyB);

```

Consultare anche [`INSTANTIATE_TYPED_TEST_SUITE_P`](#INSTANTIATE_TYPED_TEST_SUITE_P) e [Test con i Tipi Parametrizzati](../advanced.md#type-parameterized-tests) per ulteriori informazioni.

### INSTANTIATE_TYPED_TEST_SUITE_P {#INSTANTIATE_TYPED_TEST_SUITE_P}

`INSTANTIATE_TYPED_TEST_SUITE_P(`*`InstantiationName`*`,`*`TestSuiteName`*`,`*`Types`*`)`

Crea un'istanza della test suite con tipi parametrizzati *`TestSuiteName`*. La test suite deve essere registrata con [`REGISTER_TYPED_TEST_SUITE_P`](#REGISTER_TYPED_TEST_SUITE_P).

L'argomento *`InstantiationName`* è un nome univoco per l'istanziazione della test suite, per distinguere tra più istanze. Nell'output del test, il nome dell'istanza viene aggiunto come prefisso al nome della test suite *`TestSuiteName`*.

L'argomento *`Types`* è un oggetto [`Types`](#Types) che rappresenta l'elenco dei tipi su cui eseguire i test, ad esempio:

```cpp
using MyTypes = ::testing::Types<char, int, unsigned int>;
INSTANTIATE_TYPED_TEST_SUITE_P(MyInstantiation, MyFixture, MyTypes);

```

L'alias del tipo (`using` o `typedef`) è necessario affinché la macro `INSTANTIATE_TYPED_TEST_SUITE_P` lo possa analizzare correttamente.

Per ulteriori informazioni, consultare [Test con i Tipi Parametrizzati](../advanced.md#type-parameterized-tests).

### FRIEND_TEST {#FRIEND_TEST}

`FRIEND_TEST(`*`TestSuiteName`*`,`*`TestName`*`)`

All'interno del corpo di una classe, dichiara un singolo test come 'friend' della classe, consentendo al test di accedere ai membri privati della classe.

Se la classe è definita in un namespace, allora per essere 'friend' della classe, le fixture e i test devono essere definiti esattamente nello stesso namespace, non inline né namespace anonimi.

Ad esempio, se la definizione della classe è simile alla seguente:

```cpp
namespace my_namespace {
class MyClass {
  friend class MyClassTest;
  FRIEND_TEST(MyClassTest, HasPropertyA);
  FRIEND_TEST(MyClassTest, HasPropertyB);
  ... definition of class MyClass ...
};
}  // namespace my_namespace
```

Allora il codice del test dovrebbe essere simile a:

```cpp
namespace my_namespace {
class MyClassTest : public testing::Test {
  ...
};
TEST_F(MyClassTest, HasPropertyA) { ... }
TEST_F(MyClassTest, HasPropertyB) { ... }
}  // namespace my_namespace
```

Vedere [Testing Private Code](../advanced.md#testing-private-code) per ulteriori informazioni.

### SCOPED_TRACE {#SCOPED_TRACE}

`SCOPED_TRACE(`*`message`*`)`

Fa sì che il nome file corrente, il numero di riga e il messaggio *`message`* specificato vengano aggiunti al messaggio di errore per ogni errore di asserzione che si verifica nello scope.

Per ulteriori informazioni, consultare [Adding Traces to Assertions](../advanced.md#adding-traces-to-assertions).

Vedere anche la [classe `ScopedTrace`](#ScopedTrace).

### GTEST_SKIP {#GTEST_SKIP}

`GTEST_SKIP()`

Impedisce l'esecuzione di ulteriori test a runtime.

Utilizzabile nei singoli casi di test o nei metodi `SetUp()` di ambienti di test o di fixture (classi derivate dalle classi [`Environment`](#Environment) o [`Test`](#Test)). Se utilizzato in un metodo `SetUp()` dell'ambiente di test globale, salta tutti i test nel programma di test. Se utilizzato in un metodo `SetUp()` di fixture, salta tutti i test nella test suite corrispondente.

Similmente alle asserzioni, `GTEST_SKIP` consente al suo interno lo streaming di un messaggio personalizzato.

Vedere [Skipping Test Execution](../advanced.md#skipping-test-execution) per ulteriori informazioni.

### GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST {#GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST}

`GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST(`*`TestSuiteName`*`)`

Consente di annullare l'istanza della test suite con valori parametrizzati *`TestSuiteName`*.

Per default, ogni chiamata a [`TEST_P`](#TEST_P) senza una corrispondente chiamata a [`INSTANTIATE_TEST_SUITE_P`](#INSTANTIATE_TEST_SUITE_P) provoca un test non riuscito nella test suite `GoogleTestVerification`.
`GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST` sopprime questo errore per la test suite specificata.

## Classi e tipi

GoogleTest definisce le seguenti classi e tipi per facilitare la scrittura dei test.

### AssertionResult {#AssertionResult}

`testing::AssertionResult`

Una classe per indicare se un'asserzione ha avuto successo.

Quando l'asserzione non ha avuto successo, l'oggetto `AssertionResult` memorizza un messaggio di errore non vuoto recuperabile col metodo `message()` dell'oggetto.

Per creare un'istanza di questa classe, utilizzare una delle funzioni factory [`AssertionSuccess()`](#AssertionSuccess) o [`AssertionFailure()`](#AssertionFailure).

### AssertionException {#AssertionException}

`testing::AssertionException`

Eccezione che può essere generata da [`TestEventListener::OnTestPartResult`](#TestEventListener::OnTestPartResult).

### EmptyTestEventListener {#EmptyTestEventListener}

`testing::EmptyTestEventListener`

Fornisce un'implementazione vuota di tutti i metodi nell'interfaccia [`TestEventListener`](#TestEventListener), in modo tale che una sottoclasse debba solo sovrascrivere [override] i metodi che le interessano.

### Environment {#Environment}

`testing::Environment`

Rappresenta un ambiente di test globale. Consultare [Set-Up e Tear-Down Globali](../advanced.md#global-set-up-and-tear-down).

#### Metodi Protetti {#Environment-protected}

##### SetUp {#Environment::SetUp}

`virtual void Environment::SetUp()`

Si crea l'override di questo per definire come configurare l'ambiente.

##### TearDown {#Environment::TearDown}

`virtual void Environment::TearDown()`

Si crea l'override di questo per definire come eseguire il [tear down] dell'environment.

### ScopedTrace {#ScopedTrace}

`testing::ScopedTrace`

Un'istanza di questa classe fa sì che venga inclusa un trace in ogni messaggio di fallimento del test generato dal codice nello scope della durata dell'istanza di `ScopedTrace`. L'effetto viene annullato con la distruzione dell'istanza.

Il costruttore di `ScopedTrace` ha la seguente forma:

```cpp
template <typename T>
ScopedTrace(const char* file, int line, const T& message)

```

Esempio d'uso:

```cpp
testing::ScopedTrace trace("file.cc", 123, "message");

```

Il trace risultante include il path del file sorgente e il numero di riga specificati, nonché il messaggio specificato. L'argomento `message` può essere qualsiasi cosa accodabile a `std::ostream`.

Vedere anche [`SCOPED_TRACE`](#SCOPED_TRACE).

### Test {#Test}

`testing::Test`

La classe astratta da cui ereditano tutti i test. `Test` non è copiabile.

#### Public Methods {#Test-public}

##### SetUpTestSuite {#Test::SetUpTestSuite}

`static void Test::SetUpTestSuite()`

Esegue la configurazione condivisa [shared] per tutti i test nella test suite. GoogleTest chiama `SetUpTestSuite()` prima di eseguire il primo test nella test suite.

##### TearDownTestSuite {#Test::TearDownTestSuite}

`static void Test::TearDownTestSuite()`

Esegue il teardown condiviso [shared] per tutti i test della test suite. GoogleTest chiama `TearDownTestSuite()` dopo aver eseguito l'ultimo test nella test suite.

##### HasFatalFailure {#Test::HasFatalFailure}

`static bool Test::HasFatalFailure()`

Restituisce true se e solo se il test corrente ha un fallimento fatale.

##### HasNonfatalFailure {#Test::HasNonfatalFailure}

`static bool Test::HasNonfatalFailure()`

Restituisce true se e solo se il test corrente ha un fallimento non fatale.

##### HasFailure {#Test::HasFailure}

`static bool Test::HasFailure()`

restituisce true se e solo se il test corrente ha un qualsiasi fallimento, fatale o meno.

##### IsSkipped {#Test::IsSkipped}

`static bool Test::IsSkipped()`

Restituisce true se e solo se il test corrente è stato saltato [skip].

##### RecordProperty {#Test::RecordProperty}

`static void Test::RecordProperty(const std::string& key, const std::string&
value)` \
`static void Test::RecordProperty(const std::string& key, int value)`

Logga una proprietà per il test corrente, la test suite o l'intera invocazione del programma di test. Viene loggato solo l'ultimo valore per una determinata chiave.

La chiave deve essere un nome di attributo XML valido e non può entrare in conflitto con quelli già utilizzati da GoogleTest (`name`, `file`, `line`, `status`, `time`, `classname`, `type_param` e `value_param`).

`RecordProperty` è `public static` quindi può essere chiamato da funzioni di utilità che non sono membri della fixture.

Le chiamate a `RecordProperty` effettuate durante la durata del test (dal momento in cui inizia il suo costruttore al momento in cui termina il suo distruttore) vengono restituite in XML come attributi dell'elemento `<testcase>`. Le proprietà registrate dai metodi `SetUpTestSuite` o `TearDownTestSuite` della fixture vengono loggate come attributi del corrispondente elemento `<testsuite>`. Le chiamate a `RecordProperty` effettuate nel contesto globale (prima o dopo l'invocazione di `RUN_ALL_TESTS` o dai metodi `SetUp`/`TearDown` degli oggetti `Environment` registrati) vengono emessi come attributi dell'elemento `<testsuites>`.

#### Metodi Protected {#Test-protected}

##### SetUp {#Test::SetUp}

`virtual void Test::SetUp()`

Si crea l'override di questo per eseguire il setup della fixture. GoogleTest chiama `SetUp()` prima di eseguire ciascun test.

##### TearDown {#Test::TearDown}

`virtual void Test::TearDown()`

Si crea l'override di questo per eseguire il teardown della fixture. GoogleTest chiama `TearDown()` dopo l'esecuzione di ciascun singolo test.

### TestWithParam {#TestWithParam}

`testing::TestWithParam<T>`

Una classe di convenienza che eredita sia da [`Test`](#Test) che da [`WithParamInterface<T>`](#WithParamInterface).

### TestSuite {#TestSuite}

Rappresenta una test suite. `TestSuite` non è copiabile.

#### Metodi Pubblici {#TestSuite-public}

##### name {#TestSuite::name}

`const char* TestSuite::name() const`

Prende il nome della test suite.

##### type_param {#TestSuite::type_param}

`const char* TestSuite::type_param() const`

Restituisce il nome del tipo di parametro o `NULL` se non si tratta di una test suite tipizzata o con tipi parametrizzati. Vedere [Test Tipizzati](../advanced.md#typed-tests) e [Test con i Tipi Parametrizzati](../advanced.md#type-parameterized-tests).

##### should_run {#TestSuite::should_run}

`bool TestSuite::should_run() const`

Restituisce true se qualsiasi test in questa test suite dev'essere eseguito.

##### successful_test_count {#TestSuite::successful_test_count}

`int TestSuite::successful_test_count() const`

Ottiene il numero di test riusciti in questa test suite.

##### skipped_test_count {#TestSuite::skipped_test_count}

`int TestSuite::skipped_test_count() const`

Ottiene il numero di test saltati [skip] in questa test suite.

##### failed_test_count {#TestSuite::failed_test_count}

`int TestSuite::failed_test_count() const`

Ottiene il numero di test non riusciti in questa test suite.

##### reportable_disabled_test_count {#TestSuite::reportable_disabled_test_count}

`int TestSuite::reportable_disabled_test_count() const`

Ottiene il numero di test disabilitati che verranno riportati nel report XML.

##### disabled_test_count {#TestSuite::disabled_test_count}

`int TestSuite::disabled_test_count() const`

Ottiene il numero di test disabilitati in questa test suite.

##### reportable_test_count {#TestSuite::reportable_test_count}

`int TestSuite::reportable_test_count() const`

Ottiene il numero di test da stampare nel report XML.

##### test_to_run_count {#TestSuite::test_to_run_count}

`int TestSuite::test_to_run_count() const`

Ottiene il numero di test in questa test suite che dovrebbero essere eseguiti.

##### total_test_count {#TestSuite::total_test_count}

`int TestSuite::total_test_count() const`

Ottiene il numero di tutti i test in questa test suite.

##### Passed {#TestSuite::Passed}

`bool TestSuite::Passed() const`

Restituisce true se e solo se la test suite è stata superata.

##### Failed {#TestSuite::Failed}

`bool TestSuite::Failed() const`

Restituisce true se e solo se la test suite ha fallito.

##### elapsed_time {#TestSuite::elapsed_time}

`TimeInMillis TestSuite::elapsed_time() const`

Restituisce il tempo trascorso, in millisecondi.

##### start_timestamp {#TestSuite::start_timestamp}

`TimeInMillis TestSuite::start_timestamp() const`

Ottiene l'ora di inizio della test suite, in ms dall'inizio della epoch UNIX.

##### GetTestInfo {#TestSuite::GetTestInfo}

`const TestInfo* TestSuite::GetTestInfo(int i) const`

Restituisce la [`TestInfo`](#TestInfo) per l'`i`-esimo test tra tutti i test. `i` può variare da 0 a `total_test_count() - 1`. Se `i` non è compreso in quell'intervallo, restituisce `NULL`.

##### ad_hoc_test_result {#TestSuite::ad_hoc_test_result}

`const TestResult& TestSuite::ad_hoc_test_result() const`

Restituisce il [`TestResult`](#TestResult) che contiene le proprietà di test registrate durante l'esecuzione di `SetUpTestSuite` e `TearDownTestSuite`.

### TestInfo {#TestInfo}

`testing::TestInfo`

Memorizza le informazioni su un test.

#### Public Methods {#TestInfo-public}

##### test_suite_name {#TestInfo::test_suite_name}

`const char* TestInfo::test_suite_name() const`

Restituisce il nome della test suite.

##### name {#TestInfo::name}

`const char* TestInfo::name() const`

Restituisce il nome del test.

##### type_param {#TestInfo::type_param}

`const char* TestInfo::type_param() const`

Restituisce il nome del tipo di parametro o `NULL` se non si tratta di un test tipizzato o con tipi parametrizzati. Vedere [Test Tipizzati](../advanced.md#typed-tests) e [Test con i Tipi Parametrizzati](../advanced.md#type-parameterized-tests).

##### value_param {#TestInfo::value_param}

`const char* TestInfo::value_param() const`

Restituisce la rappresentazione testuale del parametro valore o `NULL` se non si tratta di un test con valori parametrizzati. Vedere [Test con Valori Parametrizzati](../advanced.md#value-parameterized-tests).

##### file {#TestInfo::file}

`const char* TestInfo::file() const`

Restituisce il nome del file in cui è definito questo test.

##### line {#TestInfo::line}

`int TestInfo::line() const`

Restituisce la riga in cui è definito questo test.

##### is_in_another_shard {#TestInfo::is_in_another_shard}

`bool TestInfo::is_in_another_shard() const`

Restituisce true se questo test non deve essere eseguito perché si trova in un altra macchina di test [shard].

##### should_run {#TestInfo::should_run}

`bool TestInfo::should_run() const`

Restituisce true se questo test deve essere eseguito, cioè se il test non è disabilitato (o è disabilitato ma è stato specificato il flag `also_run_disabled_tests`) e il suo nome completo corrisponde [match] al filtro specificato dall'utente.

GoogleTest consente all'utente di filtrare i test in base al nome completo. Verranno eseguiti solo i test che corrispondono al filtro. Per ulteriori informazioni, consultare [Eseguire un Sottoinsieme dei Test](../advanced.md#running-a-subset-of-the-tests).

##### is_reportable {#TestInfo::is_reportable}

`bool TestInfo::is_reportable() const`

Restituisce true se e solo se questo test apparirà nel report XML.

##### result {#TestInfo::result}

`const TestResult* TestInfo::result() const`

Restituisce il risultato del test. Vedere [`TestResult`](#TestResult).

### TestParamInfo {#TestParamInfo}

`testing::TestParamInfo<T>`

Descrive un parametro per un test con valori parametrizzati. Il tipo `T` è il tipo del parametro.

Contiene i campi `param` e `index` che contengono rispettivamente il valore del parametro e il suo indice intero.

### UnitTest {#UnitTest}

`testing::UnitTest`

Questa classe contiene informazioni sul programma di test.

`UnitTest` è una classe singleton. L'unica istanza viene creata quando `UnitTest::GetInstance()` viene chiamato per la prima volta. Questa istanza non viene mai eliminata.

`UnitTest` non è copiabile.

#### Metodi Pubblici {#UnitTest-public}

##### GetInstance {#UnitTest::GetInstance}

`static UnitTest* UnitTest::GetInstance()`

Ottiene l'oggetto singleton `UnitTest`. La prima volta che viene chiamato questo metodo, viene costruito e restituito un oggetto `UnitTest`. Le chiamate consecutive restituiranno lo stesso oggetto.

##### original_working_dir {#UnitTest::original_working_dir}

`const char* UnitTest::original_working_dir() const`

Restituisce la directory di lavoro quando è stato eseguito il primo [`TEST()`](#TEST) o [`TEST_F()`](#TEST_F). L'oggetto `UnitTest` possiede la stringa.

##### current_test_suite {#UnitTest::current_test_suite}

`const TestSuite* UnitTest::current_test_suite() const`

Restituisce l'oggetto [`TestSuite`](#TestSuite) per il test attualmente in esecuzione o `NULL` se non è in esecuzione alcun test.

##### current_test_info {#UnitTest::current_test_info}

`const TestInfo* UnitTest::current_test_info() const`

Restituisce l'oggetto [`TestInfo`](#TestInfo) per il test attualmente in esecuzione o `NULL` se non è in esecuzione alcun test.

##### random_seed {#UnitTest::random_seed}

`int UnitTest::random_seed() const`

Restituisce il seme random utilizzato all'inizio dell'esecuzione del test corrente.

##### successful_test_suite_count {#UnitTest::successful_test_suite_count}

`int UnitTest::successful_test_suite_count() const`

Ottiene il numero di test suite riuscite.

##### failed_test_suite_count {#UnitTest::failed_test_suite_count}

`int UnitTest::failed_test_suite_count() const`

Ottiene il numero di test suite fallite.

##### total_test_suite_count {#UnitTest::total_test_suite_count}

`int UnitTest::total_test_suite_count() const`

Ottiene il numero di tutte le test suite.

##### test_suite_to_run_count {#UnitTest::test_suite_to_run_count}

`int UnitTest::test_suite_to_run_count() const`

Ottiene il numero di tutte le test suite che contengono almeno un test da eseguire.

##### successful_test_count {#UnitTest::successful_test_count}

`int UnitTest::successful_test_count() const`

Ottiene il numero di test riusciti.

##### skipped_test_count {#UnitTest::skipped_test_count}

`int UnitTest::skipped_test_count() const`

Ottiene il numero di test saltati [skip].

##### failed_test_count {#UnitTest::failed_test_count}

`int UnitTest::failed_test_count() const`

Ottiene il numero di test falliti.

##### reportable_disabled_test_count {#UnitTest::reportable_disabled_test_count}

`int UnitTest::reportable_disabled_test_count() const`

Ottiene il numero di test disabilitati che verranno riportati nel report XML.

##### disabled_test_count {#UnitTest::disabled_test_count}

`int UnitTest::disabled_test_count() const`

Ottiene il numero di test disabilitati.

##### reportable_test_count {#UnitTest::reportable_test_count}

`int UnitTest::reportable_test_count() const`

Ottiene il numero di test da stampare nel report XML.

##### total_test_count {#UnitTest::total_test_count}

`int UnitTest::total_test_count() const`

Ottiene il numero di tutti i test.

##### test_to_run_count {#UnitTest::test_to_run_count}

`int UnitTest::test_to_run_count() const`

Ottiene il numero di test da eseguire.

##### start_timestamp {#UnitTest::start_timestamp}

`TimeInMillis UnitTest::start_timestamp() const`

Ottiene l'ora di inizio del programma di test, in ms dall'inizio della epoch UNIX.

##### elapsed_time {#UnitTest::elapsed_time}

`TimeInMillis UnitTest::elapsed_time() const`

Ottiene il tempo trascorso, in millisecondi.

##### Passed {#UnitTest::Passed}

`bool UnitTest::Passed() const`

Restituisce true se e solo se la unit test è stata superata (ovvero tutte le test suite sono state superate).

##### Failed {#UnitTest::Failed}

`bool UnitTest::Failed() const`

Restituisce true se e solo se la unit test è fallita (cioè qualche test suite ha fallito o qualcosa al di fuori di tutti i test è fallito).

##### GetTestSuite {#UnitTest::GetTestSuite}

`const TestSuite* UnitTest::GetTestSuite(int i) const`

Ottiene l'oggetto [`TestSuite`](#TestSuite) per la `i`-esima test suite tra tutte le test suite. `i` può variare da 0 a `total_test_suite_count() - 1`. Se `i` non è compreso in quell'intervallo, restituisce `NULL`.

##### ad_hoc_test_result {#UnitTest::ad_hoc_test_result}

`const TestResult& UnitTest::ad_hoc_test_result() const`

Restituisce il [`TestResult`](#TestResult) contenente informazioni sugli errori dei test e sulle proprietà loggate all'esterno delle singole test suite.

##### listeners {#UnitTest::listeners}

`TestEventListeners& UnitTest::listeners()`

Restituisce l'elenco dei listener degli eventi utilizzabili per tenere traccia degli eventi all'interno di GoogleTest. Vedere [`TestEventListeners`](#TestEventListeners).

### TestEventListener {#TestEventListener}

`testing::TestEventListener`

L'interfaccia per tracciare [tracing] l'esecuzione dei test. I metodi seguenti sono elencati nell'ordine in cui vengono attivati gli eventi corrispondenti.

#### Metodi Pubblici {#TestEventListener-public}

##### OnTestProgramStart {#TestEventListener::OnTestProgramStart}

`virtual void TestEventListener::OnTestProgramStart(const UnitTest& unit_test)`

Attivato prima dell'inizio di qualsiasi attività di test.

##### OnTestIterationStart {#TestEventListener::OnTestIterationStart}

`virtual void TestEventListener::OnTestIterationStart(const UnitTest& unit_test,
int iteration)`

Attivato prima dell'inizio di ogni iterazione dei test. Potrebbero esserci più iterazioni se è impostato `GTEST_FLAG(repeat)`. `iteration` è l'indice di iterazione, a partire da 0.

##### OnEnvironmentsSetUpStart {#TestEventListener::OnEnvironmentsSetUpStart}

`virtual void TestEventListener::OnEnvironmentsSetUpStart(const UnitTest&
unit_test)`

Attivato prima dell'avvio della configurazione dell'ambiente per ogni iterazione dei test.

##### OnEnvironmentsSetUpEnd {#TestEventListener::OnEnvironmentsSetUpEnd}

`virtual void TestEventListener::OnEnvironmentsSetUpEnd(const UnitTest&
unit_test)`

Attivato al termine della configurazione dell'ambiente per ogni iterazione dei test.

##### OnTestSuiteStart {#TestEventListener::OnTestSuiteStart}

`virtual void TestEventListener::OnTestSuiteStart(const TestSuite& test_suite)`

Attivato prima dell'avvio della test suite.

##### OnTestStart {#TestEventListener::OnTestStart}

`virtual void TestEventListener::OnTestStart(const TestInfo& test_info)`

Attivato prima dell'inizio del test.

##### OnTestPartResult {#TestEventListener::OnTestPartResult}

`virtual void TestEventListener::OnTestPartResult(const TestPartResult&
test_part_result)`

Attivato dopo un'asserzione non riuscita o un'invocazione `SUCCEED()`. Per lanciare un'eccezione da questa funzione per passare al test successivo, deve essere una [`AssertionException`](#AssertionException) o ereditata da essa.

##### OnTestEnd {#TestEventListener::OnTestEnd}

`virtual void TestEventListener::OnTestEnd(const TestInfo& test_info)`

Attivato al termine del test.

##### OnTestSuiteEnd {#TestEventListener::OnTestSuiteEnd}

`virtual void TestEventListener::OnTestSuiteEnd(const TestSuite& test_suite)`

Attivato al termine della test suite.

##### OnEnvironmentsTearDownStart {#TestEventListener::OnEnvironmentsTearDownStart}

`virtual void TestEventListener::OnEnvironmentsTearDownStart(const UnitTest&
unit_test)`

Attivato prima dell'avvio del tear-down dell'ambiente per ogni iterazione dei test.

##### OnEnvironmentsTearDownEnd {#TestEventListener::OnEnvironmentsTearDownEnd}

`virtual void TestEventListener::OnEnvironmentsTearDownEnd(const UnitTest&
unit_test)`

Attivato al termine del tear-down dell'ambiente per ogni iterazione dei test.

##### OnTestIterationEnd {#TestEventListener::OnTestIterationEnd}

`virtual void TestEventListener::OnTestIterationEnd(const UnitTest& unit_test,
int iteration)`

Attivato al termine di ogni iterazione dei test.

##### OnTestProgramEnd {#TestEventListener::OnTestProgramEnd}

`virtual void TestEventListener::OnTestProgramEnd(const UnitTest& unit_test)`

Attivato al termine di tutte le attività di test.

### TestEventListeners {#TestEventListeners}

`testing::TestEventListeners`

Consente agli utenti di aggiungere listener per tenere traccia degli eventi in GoogleTest.

#### Metodi Pubblici {#TestEventListeners-public}

##### Append {#TestEventListeners::Append}

`void TestEventListeners::Append(TestEventListener* listener)`

Aggiunge un listener di eventi alla fine dell'elenco. GoogleTest assume la proprietà [owner] del listener (ovvero eliminerà il listener al termine del programma di test).

##### Release {#TestEventListeners::Release}

`TestEventListener* TestEventListeners::Release(TestEventListener* listener)`

Rimuove il listener di eventi specificato dall'elenco e lo restituisce. Diventa quindi responsabilità del chiamante eliminarlo. Restituisce `NULL` se il listener non viene trovato nell'elenco.

##### default_result_printer {#TestEventListeners::default_result_printer}

`TestEventListener* TestEventListeners::default_result_printer() const`

Restituisce il listener standard responsabile dell'output della console di default. Può essere rimosso dall'elenco dei listener per disattivare l'output della console di default. Notare che rimuovendo questo oggetto dall'elenco dei listener con [`Release()`](#TestEventListeners::Release) ne trasferisce la proprietà al chiamante e fa sì che questa funzione restituisca `NULL` la volta successiva.

##### default_xml_generator {#TestEventListeners::default_xml_generator}

`TestEventListener* TestEventListeners::default_xml_generator() const`

Restituisce il listener standard responsabile dell'output XML di default controllato dal flag `--gtest_output=xml`. Può essere rimosso dall'elenco dei listener dagli utenti che desiderano arrestare l'output XML di default controllato da questo flag e sostituirlo con uno personalizzato. Notare che rimuovendo questo oggetto dall'elenco dei listener con [`Release()`](#TestEventListeners::Release) ne trasferisce la proprietà al chiamante e fa sì che questa funzione restituisca `NULL` la volta successiva.

### TestPartResult {#TestPartResult}

`testing::TestPartResult`

Un oggetto copiabile che rappresenta il risultato di una parte di test (ovvero un'asserzione o un `FAIL()`, `ADD_FAILURE()` o `SUCCESS()` esplicito).

#### Metodi Pubblici {#TestPartResult-public}

##### type {#TestPartResult::type}

`Type TestPartResult::type() const`

Ottiene il risultato della parte di test.

Il tipo restituito `Type` è un enum definito come segue:

```cpp
enum Type {
  kSuccess,          // Operazione riuscita.
  kNonFatalFailure,  // Fallito ma il test può continuare.
  kFatalFailure,     // Fallito e il test deve essere terminato.
  kSkip              // Saltato [skip].
};

```

##### file_name {#TestPartResult::file_name}

`const char* TestPartResult::file_name() const`

Ottiene il nome del file sorgente in cui ha avuto luogo la parte di test o `NULL` se è sconosciuto.

##### line_number {#TestPartResult::line_number}

`int TestPartResult::line_number() const`

Ottiene la riga nel file sorgente in cui ha avuto luogo la parte di test o `-1` se è sconosciuta.

##### summary {#TestPartResult::summary}

`const char* TestPartResult::summary() const`

Ottiene il riepilogo del messaggio di errore.

##### message {#TestPartResult::message}

`const char* TestPartResult::message() const`

Ottiene il messaggio associato alla parte di test.

##### skipped {#TestPartResult::skipped}

`bool TestPartResult::skipped() const`

Restituisce true se e solo se la parte del test è stata saltata [skip].

##### passed {#TestPartResult::passed}

`bool TestPartResult::passed() const`

Restituisce true se e solo se la parte del test è stata superata.

##### nonfatally_failed {#TestPartResult::nonfatally_failed}

`bool TestPartResult::nonfatally_failed() const`

Restituisce true se e solo se la parte del test ha fallito in modo non fatale.

##### fatally_failed {#TestPartResult::fatally_failed}

`bool TestPartResult::fatally_failed() const`

Restituisce true se e solo se la parte del test ha fallito fatalmente.

##### failed {#TestPartResult::failed}

`bool TestPartResult::failed() const`

Restituisce true se e solo se la parte del test ha fallito.

### TestProperty {#TestProperty}

`testing::TestProperty`

Un oggetto copiabile che rappresenta una proprietà di test specificata dall'utente che può essere restituita come coppia di stringhe chiave/valore.

#### Metodi Pubblici {#TestProperty-public}

##### key {#key}

`const char* key() const`

Ottiene la chiave fornita dall'utente.

##### value {#value}

`const char* value() const`

Ottiene il valore fornito dall'utente.

##### SetValue {#SetValue}

`void SetValue(const std::string& new_value)`

Imposta un nuovo valore, sovrascrivendo quello precedente.

### TestResult {#TestResult}

`testing::TestResult`

Contiene informazioni sul risultato di un singolo test.

`TestResult` non è copiabile.

#### Metodi Pubblici {#TestResult-public}

##### total_part_count {#TestResult::total_part_count}

`int TestResult::total_part_count() const`

Ottiene il numero di tutte le parti di test. Questa è la somma del numero di parti di test riuscite e di quelle fallite.

##### test_property_count {#TestResult::test_property_count}

`int TestResult::test_property_count() const`

Restituisce il numero di proprietà dei test.

##### Passed {#TestResult::Passed}

`bool TestResult::Passed() const`

Restituisce true se e solo se il test è stato superato (ovvero nessuna parte del test ha fallito).

##### Skipped {#TestResult::Skipped}

`bool TestResult::Skipped() const`

Restituisce true se e solo se il test è stato saltato [skip].

##### Failed {#TestResult::Failed}

`bool TestResult::Failed() const`

Restituisce true se e solo se il test è è fallito.

##### HasFatalFailure {#TestResult::HasFatalFailure}

`bool TestResult::HasFatalFailure() const`

Restituisce true se e solo se il test è fallito fatalmente.

##### HasNonfatalFailure {#TestResult::HasNonfatalFailure}

`bool TestResult::HasNonfatalFailure() const`

Restituisce true se e solo se il test è fallito non fatalmente.

##### elapsed_time {#TestResult::elapsed_time}

`TimeInMillis TestResult::elapsed_time() const`

Restituisce il tempo trascorso, in millisecondi.

##### start_timestamp {#TestResult::start_timestamp}

`TimeInMillis TestResult::start_timestamp() const`

Ottiene l'ora di inizio del test case, in ms dall'inizio della epoch UNIX.

##### GetTestPartResult {#TestResult::GetTestPartResult}

`const TestPartResult& TestResult::GetTestPartResult(int i) const`

Restituisce la [`TestPartResult`](#TestPartResult) per l'`i`-esimo risultato della parte di test tra tutti i risultati. `i` può variare da 0 a `total_part_count() - 1`. Se `i` non è compreso in quell'intervallo, interrompe [abort] il programma.

##### GetTestProperty {#TestResult::GetTestProperty}

`const TestProperty& TestResult::GetTestProperty(int i) const`

Restituisce l'oggetto [`TestProperty`](#TestProperty) per l'`i`-esima proprietà del test.
`i` può variare da 0 a `test_property_count() - 1`. Se `i` non è compreso in quell'intervallo, interrompe [abort] il programma.

### TimeInMillis {#TimeInMillis}

`testing::TimeInMillis`

Un tipo intero che rappresenta il tempo in millisecondi.

### Tipi {#Types}

`testing::Types<T...>`

Rappresenta un elenco di tipi da utilizzare nei test tipizzati e nei test con tipi parametrizzati.

L'argomento template `T...` può essere di qualsiasi tipo, ad esempio:

```
testing::Types<char, int, unsigned int>

```

Vedere [Test Tipizzati](../advanced.md#typed-tests) e [Test con i Tipi Parametrizzati](../advanced.md#type-parameterized-tests) per ulteriori informazioni.

### WithParamInterface {#WithParamInterface}

`testing::WithParamInterface<T>`

La classe di interfaccia pura da cui ereditano tutti i test valori parametrizzati.

Una classe fixture con valori parametrizzati deve ereditare sia da [`Test`](#Test) che da `WithParamInterface`. Nella maggior parte dei casi ciò significa semplicemente ereditare da [`TestWithParam`](#TestWithParam), ma per gerarchie di test più complicate potrebbe essere necessario ereditare da `Test` e da `WithParamInterface` a diversi livelli.

Questa interfaccia definisce l'alias del tipo `ParamType` per il tipo di parametro `T` e supporta l'accesso al valore del parametro di test tramite il metodo `GetParam()`:

```
static const ParamType& GetParam()

```

Per ulteriori informazioni, consultare [Test con Valori Parametrizzati](../advanced.md#value-parameterized-tests).

## Funzioni

GoogleTest definisce le seguenti funzioni per facilitare la scrittura e l'esecuzione dei test.

### InitGoogleTest {#InitGoogleTest}

`void testing::InitGoogleTest(int* argc, char** argv)` \
`void testing::InitGoogleTest(int* argc, wchar_t** argv)` \
`void testing::InitGoogleTest()`

Inizializza GoogleTest. Deve essere chiamato prima di chiamare [`RUN_ALL_TESTS()`](#RUN_ALL_TESTS). In particolare, analizza la riga di comando per i flag riconosciuti da GoogleTest. Ogni volta che viene visualizzato un flag di GoogleTest, viene rimosso da `argv` e `*argc` viene decrementato. Da tenere presente che `argv` deve terminare con un puntatore `NULL` (cioè `argv[argc]` è `NULL`), che è
è già il caso con il valore di default di `argv` passato a `main`.

Non viene restituito alcun valore. Vengono invece aggiornate le variabili flag di GoogleTest.

L'overload `InitGoogleTest(int* argc, wchar_t** argv)` è utilizzabile nei programmi Windows compilati in modalità `UNICODE`.

L'overload senza argomenti, `InitGoogleTest()` è utilizzabile su piattaforme Arduino/embedded dove non è presente `argc`/`argv`.

### AddGlobalTestEnvironment {#AddGlobalTestEnvironment}

`Environment* testing::AddGlobalTestEnvironment(Environment* env)`

Aggiunge un ambiente di test al programma di test. Deve essere chiamato prima di [`RUN_ALL_TESTS()`](#RUN_ALL_TESTS). Vedere [Set-Up e Tear-Down Globali](../advanced.md#global-set-up-and-tear-down) per ulteriori informazioni.

Consultare anche [`Environment`](#Environment).

### RegisterTest {#RegisterTest}

```cpp
template <typename Factory>
TestInfo* testing::RegisterTest(const char* test_suite_name, const char* test_name,
                                  const char* type_param, const char* value_param,
                                  const char* file, int line, Factory factory)

```

Registra dinamicamente un test con il framework.

L'argomento `factory` è un oggetto richiamabile factory (costruibile tramite spostamento) o un puntatore a funzione che crea una nuova istanza dell'oggetto`Test`. Gestisce la proprietà del chiamante. La firma del richiamabile è `Fixture*()`, dove `Fixture` è la classe fixture per il test. Tutti i test registrati con lo stesso `test_suite_name` devono restituire lo stesso tipo di fixture. Questo viene controllato in fase di esecuzione.

Il framework dedurrà la classe fixture dalla factory e vi chiamerà i metodi `SetUpTestSuite` e `TearDownTestSuite`.

Deve essere chiamato prima che venga invocato [`RUN_ALL_TESTS()`](#RUN_ALL_TESTS), altrimenti il comportamento non è definito.

Vedere [Registrazione dei test programmaticamente](../advanced.md#registering-tests-programmatically) per ulteriori informazioni.

### RUN_ALL_TESTS {#RUN_ALL_TESTS}

`int RUN_ALL_TESTS()`

Utilizzare questa funzione in `main()` per eseguire tutti i test. Restituisce `0`se tutti i test hanno esito positivo, altrimenti `1`.

`RUN_ALL_TESTS()` deve essere richiamato dopo che la riga di comando è stata analizzata da [`InitGoogleTest()`](#InitGoogleTest).

Questa funzione in precedenza era una macro; quindi, si trova nel namespace globale e ha un nome tutto in maiuscolo.

### AssertionSuccess {#AssertionSuccess}

`AssertionResult testing::AssertionSuccess()`

Crea un risultato di asserzione corretta. Vedere [`AssertionResult`](#AssertionResult).

### AssertionFailure {#AssertionFailure}

`AssertionResult testing::AssertionFailure()`

Crea un risultato di asserzione non riuscita Utilizzare l'operatore `<<` per memorizzare un messaggio di errore:

```cpp
testing::AssertionFailure() << "My failure message";

```

Vedere [`AssertionResult`](#AssertionResult).

### StaticAssertTypeEq {#StaticAssertTypeEq}

`testing::StaticAssertTypeEq<T1, T2>()`

Asserzione in fase di compilazione per l'uguaglianza dei tipi. Compila se e solo se `T1` e `T2` sono dello stesso tipo. Il valore restituito è irrilevante.

Consultare [Type Assertions](../advanced.md#type-assertions) per ulteriori informazioni.

### PrintToString {#PrintToString}

`std::string testing::PrintToString(x)`

Stampa qualsiasi valore `x` utilizzando la stampante di valori di GoogleTest.

Vedere [Insegnare a GoogleTest Come Stampare i Propri Valori](../advanced.md#teaching-googletest-how-to-print-your-values) per ulteriori informazioni.

### PrintToStringParamName {#PrintToStringParamName}

`std::string testing::PrintToStringParamName(TestParamInfo<T>& info)`

Un generatore nativo di nomi di test con parametri che restituisce il risultato di [`PrintToString`](#PrintToString) chiamato su `info.param`. Non funziona quando il parametro di test è una `std::string` o una stringa C. Consultare [Specificare i Nomi per i Parametri di test con Valori Parametrizzati](../advanced.md#specifying-names-for-value-parameterized-test-parameters) per ulteriori informazioni.

Vedere anche [`TestParamInfo`](#TestParamInfo) e [`INSTANTIATE_TEST_SUITE_P`](#INSTANTIATE_TEST_SUITE_P).
