# Guida al Mocking

Questa pagina elenca le funzionalità fornite da GoogleTest per creare e lavorare con oggetti mock. Per usarli, si aggiunge `#include <gmock/gmock.h>`.

## Le Macro {#macros}

GoogleTest definisce le seguenti macro per lavorare con i mock.

### MOCK_METHOD {#MOCK_METHOD}

`MOCK_METHOD(`*`return_type`*`,`*`method_name`*`, (`*`args...`*`));` \
`MOCK_METHOD(`*`return_type`*`,`*`method_name`*`, (`*`args...`*`),
(`*`specs...`*`));`

Definisce un metodo mock *`method_name`* con argomenti `(`*`args...`*`)` e tipo restituito *`return_type`* all'interno di una classe mock.

I parametri di `MOCK_METHOD` riflettono la dichiarazione del metodo. Il quarto parametro facoltativo *`specs...`* è un elenco di qualificatori separati da virgole. Sono accettati i seguenti qualificatori:

| Qualificatore | Significato |
| -------------------------- | -------------------------------------------- |
| `const` | Rende il metodo mock-ato un metodo `const`. Obbligatorio se si "override" un metodo `const`. |
| `override` | Contrassegna il metodo con `override`. Consigliato se si sovrascrive un metodo `virtual`. |
| `noexcept` | Contrassegna il metodo con `noexcept`. Obbligatorio se si sovrascrive un metodo `noexcept`. |
| `Calltype(`*`calltype`*`)` | Imposta il tipo di chiamata per il metodo, ad esempio `Calltype(STDMETHODCALLTYPE)`. Utile su Windows. |
| `ref(`*`qualifier`*`)` | Contrassegna il metodo con il qualificatore di riferimento specificato, ad esempio `ref(&)` o `ref(&&)`. Obbligatorio se si esegue l'override di un metodo che dispone di un qualificatore di riferimento. |

Notare che le virgole negli argomenti impediscono a `MOCK_METHOD` di analizzare correttamente gli argomenti se non sono adeguatamente racchiusi tra parentesi. Vedere l'esempio seguente:

```cpp
class MyMock {
 public:
  // Le seguenti 2 righe non verranno compilate a causa delle virgole negli argomenti:
  MOCK_METHOD(std::pair<bool, int>, GetPair, ());              // Errore!
  MOCK_METHOD(bool, CheckMap, (std::map<int, double>, bool));  // Errore!
  // Una soluzione: racchiudere gli argomenti che contengono virgole tra parentesi:
  MOCK_METHOD((std::pair<bool, int>), GetPair, ());
  MOCK_METHOD(bool, CheckMap, ((std::map<int, double>), bool));
  // Un'altra soluzione: utilizzare gli alias dei tipi:
  using BoolAndInt = std::pair<bool, int>;
  MOCK_METHOD(BoolAndInt, GetPair, ());
  using MapIntDouble = std::map<int, double>;
  MOCK_METHOD(bool, CheckMap, (MapIntDouble, bool));
};

```

`MOCK_METHOD` deve essere utilizzata nella sezione `public:` di una definizione di classe mock, indipendentemente dal fatto che il metodo mock-ato sia `public`, `protected` o `private` nella classe base.

### EXPECT_CALL {#EXPECT_CALL}

`EXPECT_CALL(`*`mock_object`*`,`*`method_name`*`(`*`matchers...`*`))`

Crea una [expectation](../gmock_for_dummies.md#setting-expectations) (aspettativa) che il metodo *`method_name`* dell'oggetto *`mock_object`* venga chiamato con argomenti che coincidano con i corrispondenti *`matchers...`*. `EXPECT_CALL` deve precedere qualsiasi codice che eserciti l'oggetto mock.

Il parametro *`matchers...`* è un elenco separato da virgole di [matchers](../gmock_for_dummies.md#matchers-what-arguments-do-we-expect) che corrispondono a ciascun argomento del metodo *`method_name`*. La expectation si applicherà solo alle chiamate di *`method_name`* i cui argomenti corrispondono a tutti i matcher. Se `(`*`matchers...`*`)` viene omesso, la expectation si comporta come se il matcher di ogni argomento fosse un [matcher-jolly (`_`)](matchers.md#wildcard).
Consultare i [Riferimenti ai Matcher](matchers.md) per un elenco di tutti i matcher nativi.

Le seguenti clausole concatenabili possono essere utilizzate per modificare la expectation e devono essere utilizzate nel seguente ordine:

```cpp
EXPECT_CALL(mock_object, method_name(matchers...))
    .With(multi_argument_matcher)  // Può essere utilizzato al massimo una volta
    .Times(cardinality)            // Può essere utilizzato al massimo una volta
    .InSequence(sequences...)      // Può essere utilizzato un numero qualsiasi di volte
    .After(expectations...)        // Può essere utilizzato un numero qualsiasi di volte
    .WillRepeatedly(action)        // Può essere utilizzato un numero qualsiasi di volte
    .WillOnce(action)              // Può essere utilizzato al massimo una volta
    .RetiresOnSaturation();        // Può essere utilizzato al massimo una volta
```

Vedere in seguito i dettagli per ciascuna clausola modificatrice.

#### With {#EXPECT_CALL.With}

`.With(`*`multi_argument_matcher`*`)`

Limita expectation ad applicarsi solo alle chiamate di funzione mock i cui argomenti nel complesso corrispondono al matcher multi-argomento *`multi_argument_matcher`*.

GoogleTest passa tutti gli argomenti come una tupla al matcher. Il parametro *`multi_argument_matcher`* deve quindi essere un matcher di tipo `Matcher<std::tuple<A1, ..., An>>`, dove `A1, ..., An` sono i tipi degli argomenti della funzione.

Ad esempio, il codice seguente imposta la expectation che `my_mock.SetPosition()` venga chiamata con due argomenti qualsiasi, col primo argomento minore del secondo:

```cpp
using ::testing::_;
using ::testing::Lt;
...
EXPECT_CALL(my_mock, SetPosition(_, _))
    .With(Lt());

```

GoogleTest fornisce alcuni matcher nativi per 2-tuple (doppie), incluso il matcher `Lt()` sopra. Consultare [Matcher Multi-argomento](matchers.md#MultiArgMatchers).

La clausola `With` può essere utilizzata al massimo una volta su una expectation e deve essere la prima clausola.

#### Times {#EXPECT_CALL.Times}

`.Times(`*`cardinality`*`)`

Specifica quante volte è prevista la chiamata alla funzione mock.

Il parametro *`cardinality`* rappresenta il numero di chiamate previste e può essere uno dei seguenti, tutti definiti nel namespace `::testing`:

| Cardinalità | Significato |
| ------------------- | --------------------------------------------------- |
| `AnyNumber()` | La funzione può essere chiamata un numero qualsiasi di volte. |
| `AtLeast(n)` | La chiamata alla funzione è prevista almeno per *n* volte. |
| `AtMost(n)` | La chiamata alla funzione è prevista al massimo per *n* volte. |
| `Between(m, n)` | La chiamata alla funzione è prevista tra *m* e *n* volte, estremi inclusi. |
| `Exactly(n)` o `n` | La chiamata alla funzione è prevista esattamente *n* volte. Se *n* è 0, la chiamata non dovrebbe mai avvenire. |

Se la clausola `Times` viene omessa, GoogleTest deduce la cardinalità come segue:

*   If neither [`WillOnce`](#EXPECT_CALL.WillOnce) nor
    [`WillRepeatedly`](#EXPECT_CALL.WillRepeatedly) are specified, the inferred
    cardinality is `Times(1)`.
*   Se sono presenti *n* clausole `WillOnce` e nessuna clausola `WillRepeatedly`, dove *n* >= 1, la cardinalità dedotta è `Times(n)`.
*   Se sono presenti *n* clausole `WillOnce` e una clausola `WillRepeatedly`, dove *n* >= 0, la cardinalità dedotta è `Times(AtLeast(n))`.

La clausola `Times` può essere utilizzata al massimo una volta su una expectation.

#### InSequence {#EXPECT_CALL.InSequence}

`.InSequence(`*`sequences...`*`)`

Specifica che la chiamata alla funzione mock è prevista in una determinata sequenza.

Il parametro *`sequences...`* è un numero qualsiasi di oggetti [`Sequence`](#Sequence).
Le chiamate previste assegnate alla stessa sequenza ci si aspetta che avvengano nell'ordine in cui vengono dichiarate le expectation.

Ad esempio, il codice seguente imposta la expectation che il metodo `Reset()` di `my_mock` venga chiamato prima sia di `GetSize()` che di `Describe()` e `GetSize()` e `Describe()` possono verificarsi in qualsiasi ordine relativo l'uno rispetto all'altro:

```cpp
using ::testing::Sequence;
Sequence s1, s2;
...
EXPECT_CALL(my_mock, Reset())
    .InSequence(s1, s2);
EXPECT_CALL(my_mock, GetSize())
    .InSequence(s1);
EXPECT_CALL(my_mock, Describe())
    .InSequence(s2);

```

La clausola `InSequence` è utilizzabile un numero qualsiasi di volte in per ogni expectation.

Vedere anche la [classe `InSequence`](#InSequence).

#### After {#EXPECT_CALL.After}

`.After(`*`expectations...`*`)`

Specifica che ci si aspetta che la chiamata alla funzione mock avvenga dopo una o più altre chiamate.

Il parametro *`expectations...`* può contenere fino a cinque oggetti [`Expectation`](#Expectation) o [`ExpectationSet`](#ExpectationSet).
Ci si aspetta che la chiamata di funzione mock avvenga dopo tutte le expectation indicate.

Ad esempio, il codice seguente imposta la expectation che il metodo `Describe()` di `my_mock` venga chiamato dopo che sia `InitX()` che `InitY()` siano stati chiamati.

```cpp
using ::testing::Expectation;
...
Expectation init_x = EXPECT_CALL(my_mock, InitX());
Expectation init_y = EXPECT_CALL(my_mock, InitY());
EXPECT_CALL(my_mock, Describe())
    .After(init_x, init_y);

```

L'oggetto `ExpectationSet` è utile quando il numero di prerequisiti per una expectation è elevato o variabile, ad esempio:

```cpp
using ::testing::ExpectationSet;
...
ExpectationSet all_inits;
// Racchiude tutte le expectation delle chiamate a InitElement()
for (int i = 0; i < element_count; i++) {
  all_inits += EXPECT_CALL(my_mock, InitElement(i));
}
EXPECT_CALL(my_mock, Describe())
    .After(all_inits);  // Ci si aspetta la chiamata a Describe() dopo tutte le chiamate di InitElement()

```

La clausola `After` è utilizzabile un numero qualsiasi di volte per ogni expectation.

#### WillOnce {#EXPECT_CALL.WillOnce}

`.WillOnce(`*`action`*`)`

Specifica il comportamento effettivo della funzione mock quando richiamata, per una singola chiamata di funzione corrispondente [matching].

Il parametro *`action`* rappresenta la [action](../gmock_for_dummies.md#actions-what-should-it-do) che la chiamata alla funzione eseguirà. Consultare i [Riferimenti alle Action](actions.md) per un elenco delle action native.

L'uso di `WillOnce` imposta implicitamente una cardinalità sulla expectation quando `Times` non è specificato. Vedere [`Times`](#EXPECT_CALL.Times).

Ogni chiamata di funzione corrispondente [match] eseguirà la action successiva nell'ordine dichiarato.
Ad esempio, il codice seguente specifica che `my_mock.GetNumber()` ci si aspetta che venga chiamata esattamente 3 volte e restituirà `1`, `2` e `3` rispettivamente alla prima, seconda e terza chiamata:

```cpp
using ::testing::Return;
...
EXPECT_CALL(my_mock, GetNumber())
    .WillOnce(Return(1))
    .WillOnce(Return(2))
    .WillOnce(Return(3));

```

La clausola `WillOnce` è utilizzabile un numero qualsiasi di volte per ogni expectation. Diversamente da `WillRepeatedly`, la action fornita a ciascuna chiamata `WillOnce` verrà chiamata al massimo una volta, quindi potrebbe essere di tipo move-only e/o avere un operatore di chiamata qualificato con `&&`.

#### WillRepeatedly {#EXPECT_CALL.WillRepeatedly}

`.WillRepeatedly(`*`action`*`)`

Specifica il comportamento effettivo della funzione mock quando richiamata, per tutte le successive chiamate di funzione corrispondenti [match]. Ha effetto dopo l'esecuzione delle action specificate nelle clausole [`WillOnce`](#EXPECT_CALL.WillOnce), se presenti.

Il parametro *`action`* rappresenta la [action](../gmock_for_dummies.md#actions-what-should-it-do) che la chiamata alla funzione eseguirà. Consultare i [Riferimenti alle Action](actions.md) per un elenco delle action native.

L'uso di `WillRepeatedly` imposta implicitamente una cardinalità sulla expectation quando `Times` non è specificato. Vedere [`Times`](#EXPECT_CALL.Times).

Se sono state specificate clausole `WillOnce`, le chiamate di funzione corrispondenti [match] eseguiranno tali actions prima di quella specificata da `WillRepeatedly`. Vedere l'esempio seguente:

```cpp
using ::testing::Return;
...
EXPECT_CALL(my_mock, GetName())
    .WillRepeatedly(Return("John Doe"));  // Return "John Doe" on all calls
EXPECT_CALL(my_mock, GetNumber())
    .WillOnce(Return(42))        // Restituisce 42 alla prima chiamata
    .WillRepeatedly(Return(7));  // Restituisce 7 a tutte le chiamate successive

```

La clausola `WillRepeatedly` può essere utilizzata al massimo una volta su una expectation.

#### RetiresOnSaturation {#EXPECT_CALL.RetiresOnSaturation}

`.RetiresOnSaturation()`

Indica che la expectation non sarà più attiva una volta raggiunto il numero previsto di chiamate di funzione corrispondenti.

La clausola `RetiresOnSaturation` è significativa solo per le expectation con una cardinalità con un limite superiore. La expectation verrà *retire* (ritirata) (non corrisponderà più ad alcuna chiamata di funzione) dopo essere stata *saturata* (il limite superiore è stato raggiunto). Vedere l'esempio seguente:

```cpp
using ::testing::_;
using ::testing::AnyNumber;
...
EXPECT_CALL(my_mock, SetNumber(_))  // Expectation 1
    .Times(AnyNumber());
EXPECT_CALL(my_mock, SetNumber(7))  // Expectation 2
    .Times(2)
    .RetiresOnSaturation();

```

Nell'esempio precedente, le prime due chiamate a `my_mock.SetNumber(7)` corrispondono [match] alla expectation 2, che quindi diventa inattiva e non corrisponde [match] più ad alcuna chiamata. Una terza chiamata a `my_mock.SetNumber(7)` corrisponderebbe [match] quindi alla expectation 1. Senza `RetiresOnSaturation()` sulla expectation 2, una terza chiamata a `my_mock.SetNumber(7)` corrisponderebbe [match] nuovamente alla expectation 2, producendo un errore poiché è stato superato il limite di 2 chiamate.

La clausola `RetiresOnSaturation` può essere utilizzata al massimo una volta su una expectation e deve essere l'ultima clausola.

### ON_CALL {#ON_CALL}

`ON_CALL(`*`mock_object`*`,`*`method_name`*`(`*`matchers...`*`))`

Definisce cosa succede quando il metodo *`method_name`* dell'oggetto *`mock_object`* viene chiamato con argomenti che corrispondono ai *`matchers...`* specificati. Richiede un modificatore di clausola per specificare il comportamento del metodo.
*Non* imposta alcuna expectation che il metodo verrà chiamato.

Il parametro *`matchers...`* è un elenco separato da virgole di [matchers](../gmock_for_dummies.md#matchers-what-arguments-do-we-expect) che corrispondono a ciascun argomento del metodo *`method_name`*. La specifica `ON_CALL` si applicherà solo alle chiamate di *`method_name`* i cui argomenti corrispondono a tutti i matcher. Se `(`*`matchers...`*`)` viene omesso, il comportamento è come se il matcher di ogni argomento fosse un [matcher-jolly (`_`)](matchers.md#wildcard).
Consultare i [Riferimenti ai Matcher](matchers.md) per un elenco di tutti i matcher nativi.

Le seguenti clausole concatenabili possono essere utilizzate per impostare il comportamento del metodo e devono essere utilizzate nel seguente ordine:

```cpp
ON_CALL(mock_object, method_name(matchers...))
    .With(multi_argument_matcher)  // Può essere utilizzato al massimo una volta
    .WillByDefault(action);        // Necessario

```

Vedere in seguito i dettagli per ciascuna clausola modificatrice.

#### With {#ON_CALL.With}

`.With(`*`multi_argument_matcher`*`)`

Limita la specifica solo alle chiamate di funzione mock i cui argomenti nel complesso corrispondono al matcher multi-argomento *`multi_argument_matcher`*.

GoogleTest passa tutti gli argomenti come una tupla al matcher. Il parametro *`multi_argument_matcher`* deve quindi essere un matcher di tipo `Matcher<std::tuple<A1, ..., An>>`, dove `A1, ..., An` sono i tipi degli argomenti della funzione.

Ad esempio, il codice seguente imposta il comportamento di default quando `my_mock.SetPosition()` venga chiamata con due argomenti qualsiasi, col primo argomento minore del secondo:

```cpp
using ::testing::_;
using ::testing::Lt;
using ::testing::Return;
...
ON_CALL(my_mock, SetPosition(_, _))
    .With(Lt())
    .WillByDefault(Return(true));

```

GoogleTest fornisce alcuni matcher nativi per 2-tuple (doppie), incluso il matcher `Lt()` sopra. Consultare [Matcher Multi-argomento](matchers.md#MultiArgMatchers).

La clausola `With` può essere utilizzata al massimo una volta su ogni istruzione `ON_CALL`.

#### WillByDefault {#ON_CALL.WillByDefault}

`.WillByDefault(`*`action`*`)`

Specifica il comportamento di default di una chiamata di funzione mock corrispondente [match].

Il parametro *`action`* rappresenta la [action](../gmock_for_dummies.md#actions-what-should-it-do) che la chiamata alla funzione eseguirà. Consultare i [Riferimenti alle Action](actions.md) per un elenco delle action native.

Ad esempio, il codice seguente specifica che, per default, una chiamata a `my_mock.Greet()` restituirà `"hello"`:

```cpp
using ::testing::Return;
...
ON_CALL(my_mock, Greet())
    .WillByDefault(Return("hello"));

```

La action specificata da `WillByDefault` viene sostituita dalle action specificate in un'istruzione `EXPECT_CALL` corrispondente, se presente. Vedere le clausole [`WillOnce`](#EXPECT_CALL.WillOnce) e [`WillRepeatedly`](#EXPECT_CALL.WillRepeatedly) di `EXPECT_CALL`.

La clausola `WillByDefault` deve essere utilizzata esattamente una volta con ciascuna istruzione `ON_CALL`.

## Le Classi {#classes}

GoogleTest definisce le seguenti classi per lavorare con i mock.

### DefaultValue {#DefaultValue}

`::testing::DefaultValue<T>`

Consente all'utente di specificare il valore di default per un tipo `T` che è sia copiabile che pubblicamente distruttibile (ovvero qualsiasi cosa che possa essere utilizzata come tipo restituito da una funzione). Per le funzioni mock con un tipo di ritorno `T`, questo valore di default viene restituito dalle chiamate di funzione che non specificano una action.

Fornisce i metodi statici `Set()`, `SetFactory()` e `Clear()` per gestire il valore di default:

```cpp
// Setta il valore di default da restituire. T deve avere un costruttore copia.
DefaultValue<T>::Set(value);
// Sets a factory. Verrà richiamato su richiesta. deve avere un costruttore di spostamento [move].
T MakeT();
DefaultValue<T>::SetFactory(&MakeT);
// Unsets the default value.
DefaultValue<T>::Clear();
```

### NiceMock {#NiceMock}

`::testing::NiceMock<T>`

Rappresenta un oggetto mock che sopprime i warning sulle [chiamate uninteresting](../gmock_cook_book.md#uninteresting-vs-unexpected). Il parametro template `T` è qualsiasi classe mock, ad eccezione di un altra `NiceMock`, `NaggyMock` o `StrictMock`.

L'utilizzo di `NiceMock<T>` è analogo a quello di `T`. `NiceMock<T>` è una sottoclasse di `T`, quindi può essere utilizzata ovunque sia accettato un oggetto di tipo `T`. Inoltre, `NiceMock<T>` può essere costruito con qualsiasi argomento accettato dal costruttore di `T`.

Ad esempio, il codice seguente sopprime i warning sul mock `my_mock` di tipo `MockClass` se viene chiamato un metodo diverso da `DoSomething()`:

```cpp
using ::testing::NiceMock;
...
NiceMock<MockClass> my_mock("some", "args");
EXPECT_CALL(my_mock, DoSomething());
... codice che usa my_mock ...

```

`NiceMock<T>` funziona solo con metodi mock definiti utilizzando la macro `MOCK_METHOD` direttamente nella definizione della classe `T`. Se un metodo mock è definito in una classe base di `T`, potrebbe comunque essere generato un warning.

`NiceMock<T>` potrebbe non funzionare correttamente se il distruttore di `T` non è virtuale.

### NaggyMock {#NaggyMock}

`::testing::NaggyMock<T>`

Rappresenta un mock fittizio che genera warning su [chiamate uninteresting](../gmock_cook_book.md#uninteresting-vs-unexpected). Il parametro template `T` è qualsiasi classe mock, ad eccezione di un altra `NiceMock`, `NaggyMock` o `StrictMock`.

L'utilizzo di `NaggyMock<T>` è analogo a quello di `T`. `NaggyMock<T>` è una sottoclasse di `T`, quindi può essere utilizzata ovunque sia accettato un oggetto di tipo `T`.
Inoltre, `NaggyMock<T>` può essere costruito con qualsiasi argomento accettato dal costruttore di `T`.

Ad esempio, il codice seguente genera i warning sul mock `my_mock` di tipo `MockClass` se viene chiamato un metodo diverso da `DoSomething()`:

```cpp
using ::testing::NaggyMock;
...
NaggyMock<MockClass> my_mock("some", "args");
EXPECT_CALL(my_mock, DoSomething());
... codice che usa my_mock ...

```

Gli oggetti mock di tipo `T` per default si comportano allo stesso modo di `NaggyMock<T>`.

### StrictMock {#StrictMock}

`::testing::StrictMock<T>`

Rappresenta un oggetto mock che genera fallimenti dei test sulle [chiamate uninteresting](../gmock_cook_book.md#uninteresting-vs-unexpected). Il parametro template `T` è qualsiasi classe mock, ad eccezione di un altra `NiceMock`, `NaggyMock` o `StrictMock`.

L'utilizzo di `StrictMock<T>` è analogo a quello di `T`. `StrictMock<T>` è una sottoclasse di `T`, quindi può essere utilizzata ovunque sia accettato un oggetto di tipo `T`.
Inoltre, `StrictMock<T>` può essere costruito con qualsiasi argomento accettato dal costruttore di `T`.

Ad esempio, il codice seguente genera il fallimento del test sul mock `my_mock` di tipo `MockClass` se viene chiamato un metodo diverso da `DoSomething()`:

```cpp
using ::testing::StrictMock;
...
StrictMock<MockClass> my_mock("some", "args");
EXPECT_CALL(my_mock, DoSomething());
... codice che usa uses my_mock ...

```

`StrictMock<T>` funziona solo con metodi mock definiti utilizzando la macro `MOCK_METHOD` direttamente nella definizione della classe `T`. Se un metodo mock è definito in una classe base di `T`, potrebbe non essere generato un errore.

`StrictMock<T>` potrebbe non funzionare correttamente se il distruttore di `T` non è virtuale.

### Sequence {#Sequence}

`::testing::Sequence`

Rappresenta una sequenza cronologica di expectation. Vedere la clausola [`InSequence`](#EXPECT_CALL.InSequence) di `EXPECT_CALL` per l'utilizzo.

### InSequence {#InSequence}

`::testing::InSequence`

Un oggetto di questo tipo fa sì che tutte le expectation incontrate nel suo scope vengano messe in una sequenza anonima.

Ciò consente un'espressione più conveniente di molteplici expectation in un'unica sequenza:

```cpp
using ::testing::InSequence;
{
  InSequence seq;
  // Ci si aspetta che quanto segue avvenga nell'ordine dichiarato.
  EXPECT_CALL(...);
  EXPECT_CALL(...);
  ...
  EXPECT_CALL(...);
}

```

Il nome dell'oggetto `InSequence` non ha importanza.

### Expectation {#Expectation}

`::testing::Expectation`

Rappresenta una expectation di chiamata a mock creata da [`EXPECT_CALL`](#EXPECT_CALL):

```cpp
using ::testing::Expectation;
Expectation my_expectation = EXPECT_CALL(...);

```

Utile per specificare sequenze di expectation; vedere la clausola [`After`](#EXPECT_CALL.After) di `EXPECT_CALL`.

### ExpectationSet {#ExpectationSet}

`::testing::ExpectationSet`

Rappresenta un insieme di expectation di chiamate a funzione mock.

Usare l'operatore `+=` per aggiungere oggetti [`Expectation`](#Expectation) all'insieme:

```cpp
using ::testing::ExpectationSet;
ExpectationSet my_expectations;
my_expectations += EXPECT_CALL(...);

```

Utile per specificare sequenze di expectation; vedere la clausola [`After`](#EXPECT_CALL.After) di `EXPECT_CALL`.
