# Cheat Sheet di gMock

## Definizione di una Classe Mock

### Mock di una Classe Normale {#MockClass}

Dato

```cpp
class Foo {
 public:
  virtual ~Foo();
  virtual int GetSize() const = 0;
  virtual string Describe(const char* name) = 0;
  virtual string Describe(int type) = 0;
  virtual bool Process(Bar elem, int count) = 0;
};

```

(notare che `~Foo()` **deve** essere virtual) possiamo definirne il mock come

```cpp
#include <gmock/gmock.h>
class MockFoo : public Foo {
 public:
  MOCK_METHOD(int, GetSize, (), (const, override));
  MOCK_METHOD(string, Describe, (const char* name), (override));
  MOCK_METHOD(string, Describe, (int type), (override));
  MOCK_METHOD(bool, Process, (Bar elem, int count), (override));
};

```

Per creare un "nice" mock, che ignora tutte le chiamate [uninteresting], un mock "naggy", che emette warning su tutte le chiamate [uninteresting], o un mock "strict", che li tratta come fallimenti:

```cpp
using ::testing::NiceMock;
using ::testing::NaggyMock;
using ::testing::StrictMock;
NiceMock<MockFoo> nice_foo;      // The type is a subclass of MockFoo.
NaggyMock<MockFoo> naggy_foo;    // Il tipo è una sottoclasse di MockFoo.
StrictMock<MockFoo> strict_foo;  // Il tipo è una sottoclasse di MockFoo.

```

{: .callout .note}
**Nota:** Un oggetto mock è attualmente naggy per default. Potremmo renderlo nice per default in futuro.

### Mock di una Classe Template {#MockTemplate}

Le classi templates si possono rendere mocked proprio come qualsiasi classe.

Per il mock di

```cpp
template <typename Elem>
class StackInterface {
 public:
  virtual ~StackInterface();
  virtual int GetSize() const = 0;
  virtual void Push(const Elem& x) = 0;
};

```

(notare che il mock di tutte le funzioni membro, compreso `~StackInterface()` **devono** essere virtual).

```cpp
template <typename Elem>
class MockStack : public StackInterface<Elem> {
 public:
  MOCK_METHOD(int, GetSize, (), (const, override));
  MOCK_METHOD(void, Push, (const Elem& x), (override));
};

```

### Specificare le Convenzioni di Chiamata per le Funzioni Mock

Se la funzione mock non utilizza la convenzione di chiamata di default, la si può specificare aggiungendo `Calltype(convention)` al quarto parametro di `MOCK_METHOD`.
Per esempio,

```cpp
  MOCK_METHOD(bool, Foo, (int n), (Calltype(STDMETHODCALLTYPE)));
  MOCK_METHOD(int, Bar, (double x, double y),
              (const, Calltype(STDMETHODCALLTYPE)));

```

dove `STDMETHODCALLTYPE` è definito da `<objbase.h>` su Windows.

## Uso dei Mock nei Test {#UsingMocks}

Il flusso di lavoro tipico è:

1.  Si importano i nomi gMock da utilizzare. Tutti i simboli gMock si trovano nel namespace `testing` a meno che non siano macro o diversamente indicati.
2.  Si creano gli oggetti mock.
3.  Facoltativamente, imposta le azioni di default degli oggetti mock.
4.  Si settano le expectation sugli oggetti mock (Come verranno chiamati? What
    will they do?).
5.  Exercise code that uses the mock objects; if necessary, check the result
    using googletest assertions.
6.  When a mock object is destructed, gMock automatically verifies that all
    expectations on it have been satisfied.

Ecco un esempio:

```cpp
using ::testing::Return;                          // #1
TEST(BarTest, DoesThis) {
  MockFoo foo;                                    // #2
  ON_CALL(foo, GetSize())                         // #3
      .WillByDefault(Return(1));
  // ... altre azioni di default ...
  EXPECT_CALL(foo, Describe(5))                   // #4
      .Times(3)
      .WillRepeatedly(Return("Category 5"));
  // ... altre expectation ...
  EXPECT_EQ(MyProductionFunction(&foo), "good");  // #5
}                                                 // #6

```

## Impostazione delle Azioni di Default {#OnCall}

gMock ha un'**azione di default nativa** per qualsiasi funzione che restituisce `void`, `bool`, un valore numerico o un puntatore. In C++11, restituirà inoltre il valore costruito di default, se ne esiste uno per il tipo specificato.

Per personalizzare l'azione di default per le funzioni con tipo restituito `T`, si usa [`DefaultValue<T>`](reference/mocking.md#DefaultValue). Per esempio:

```cpp
  // Setta l'azione di default per il tipo restituito std::unique_ptr<Buzz>
  // per creare ogni volta un nuovo Buzz.
  DefaultValue<std::unique_ptr<Buzz>>::SetFactory(
      [] { return std::make_unique<Buzz>(AccessLevel::kInternal); });
  // Quando viene attivato, verrà eseguita l'azione di default di MakeBuzz(),
  // che restituirà un nuovo oggetto Buzz.
  EXPECT_CALL(mock_buzzer_, MakeBuzz("hello")).Times(AnyNumber());
  auto buzz1 = mock_buzzer_.MakeBuzz("hello");
  auto buzz2 = mock_buzzer_.MakeBuzz("hello");
  EXPECT_NE(buzz1, nullptr);
  EXPECT_NE(buzz2, nullptr);
  EXPECT_NE(buzz1, buzz2);
  // Resetta l'azione di default per il tipo restituito std::unique_ptr<Buzz>,
  // per evitare interferenze con altri test.
  DefaultValue<std::unique_ptr<Buzz>>::Clear();

```

Per personalizzare l'azione di default per un metodo particolare di uno specifico oggetto mock, si usa [`ON_CALL`](reference/mocking.md#ON_CALL). `ON_CALL` ha una sintassi simile a `EXPECT_CALL`, ma viene utilizzato per impostare comportamenti di default quando non è necessario che venga chiamato il metodo mock. Vedere [Quando usare Expect](gmock_cook_book.md#UseOnCall) per una discussione più dettagliata.

## Impostare le Expectation {#ExpectCall}

Vedere [`EXPECT_CALL`](reference/mocking.md#EXPECT_CALL) nella "Guida al Mocking".

## I Matcher {#MatcherList}

Vedere i [Riferimenti ai Matcher](reference/matchers.md).

## Le Action {#ActionList}

Vedere i [Riferimenti alle Action](reference/actions.md).

## Cardinalità {#CardinalityList}

Vedere le [clausole `Times`](reference/mocking.md#EXPECT_CALL.Times) di `EXPECT_CALL` nela "Guida al Mocking".

## Ordine delle Expectation

Per default, le expectation possono essere soddisfatte in *qualsiasi* ordine. Se alcune o tutte le expectation devono essere soddisfatte in un determinato ordine, si può utilizzare la [clausola `After`](reference/mocking.md#EXPECT_CALL.After) o la [clausola `InSequence`](reference/mocking.md#EXPECT_CALL.InSequence) di `EXPECT_CALL`, oppure usare un [oggetto `InSequence`](reference/mocking.md#InSequence).

## Verificare e Resettare un Mock

gMock verificherà le expectation su un oggetto mock quando viene distrutto, oppure lo si può fare prima:

```cpp
using ::testing::Mock;
...
// Verifica e rimuove le expectation su mock_obj;
// restituisce true se e solo se ha successo.
Mock::VerifyAndClearExpectations(&mock_obj);
...
// Verifica e rimuove le expectation su mock_obj;
// rimuove anche le azioni di default impostate da ON_CALL();
// restituisce true se e solo se ha successo.
Mock::VerifyAndClear(&mock_obj);

```

Non stabilire nuove expectation dopo aver verificato e ripulito un mock dopo il suo utilizzo.
L'impostazione delle expectation dopo il codice che esercita il mock ha un comportamento indefinito.
Vedere [Uso dei Mock nei Test](gmock_for_dummies.md#using-mocks-in-tests) per ulteriori informazioni.

Si può anche dire a gMock che un oggetto mock può essere perso [leaked] e non è necessario verificarlo:

```cpp
Mock::AllowLeak(&mock_obj);

```

## Classi Mock

gMock definisce un comodo template di classe mock

```cpp
class MockFunction<R(A1, ..., An)> {
 public:
  MOCK_METHOD(R, Call, (A1, ..., An));
};

```

Consultare questa [ricetta](gmock_cook_book.md#UsingCheckPoints) per una sua applicazione.

## I Flag

| Flag | Descrizione |
| :----------------------------- | :---------------------------------------- |
| `--gmock_catch_leaked_mocks=0` | Non segnalare gli oggetti mock [leaked] come fallimenti. |
| `--gmock_verbose=LEVEL` | Imposta il livello di verbosità di default (`info`, `warning`, o `error`) dei messaggi di Google Mock. |
