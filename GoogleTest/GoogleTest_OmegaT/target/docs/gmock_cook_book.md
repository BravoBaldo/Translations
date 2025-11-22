# Ricettario di gMock

Qui si trovano delle ricette per utilizzare gMock. Se non è stato ancora fatto, leggere prima la guida [gMock per Principianti](gmock_for_dummies.md) per capire le basi.

{: .callout .note}
**Nota:** gMock risiede nel namespace `testing`. Per maggiore leggibilità, si consiglia di scrivere `using ::testing::Foo;` una volta nel file prima di utilizzare il nome `Foo` definito da gMock. In questa sezione, per brevità, omettiamo le istruzioni `using`, ma nel codice lo si dovrebbe fare.

## Creare Classi Mock

Le classi mock vengono definite come le normali classi, utilizzando la macro `MOCK_METHOD` per generare metodi mock-ati. La macro prende 3 o 4 parametri:

```cpp
class MyMock {
 public:
  MOCK_METHOD(ReturnType, MethodName, (Args...));
  MOCK_METHOD(ReturnType, MethodName, (Args...), (Specs...));
};

```

I primi 3 parametri sono semplicemente la dichiarazione del metodo, divisa in 3 parti.
Il 4° parametro accetta un elenco chiuso di qualificatori, che riguardano il metodo generato:

*   **`const`** - Rende il metodo mock-ato un metodo `const`. Required if
    overriding a `const` method.
*   **`override`** - Contrassegna il metodo con `override`. Recommended if overriding
    a `virtual` method.
*   **`noexcept`** - Contrassegna il metodo con `noexcept`. Obbligatorio se si sovrascrive un metodo `noexcept`.
*   **`Calltype(...)`** - Imposta il tipo di chiamata per il metodo (ad esempio su `STDMETHODCALLTYPE`), utile in Windows.
*   **`ref(...)`** - Marks the method with the reference qualification
    specified. Required if overriding a method that has reference
    qualifications. Ad esempio `ref(&)` o `ref(&&)`.

### Trattare le virgole non protette

Le virgole non-protette, ovvero le virgole non racchiuse tra parentesi, impediscono a `MOCK_METHOD` di analizzare correttamente i suoi argomenti:

{: .bad}
```cpp
class MockFoo {
 public:
  MOCK_METHOD(std::pair<bool, int>, GetPair, ());  // Non verrà compilato!
  MOCK_METHOD(bool, CheckMap, (std::map<int, double>, bool));  // Non verrà compilato!
};

```

Soluzione 1 - racchiudere tra le parentesi:

{: .good}
```cpp
class MockFoo {
 public:
  MOCK_METHOD((std::pair<bool, int>), GetPair, ());
  MOCK_METHOD(bool, CheckMap, ((std::map<int, double>), bool));
};

```

Si noti che racchiudere un tipo di ritorno o un tipo di un argomento tra le parentesi non è, in generale, sbagliato in C++. `MOCK_METHOD` rimuove le parentesi.

Soluzione 2 - definire un alias:

{: .good}
```cpp
class MockFoo {
 public:
  using BoolAndInt = std::pair<bool, int>;
  MOCK_METHOD(BoolAndInt, GetPair, ());
  using MapIntDouble = std::map<int, double>;
  MOCK_METHOD(bool, CheckMap, (MapIntDouble, bool));
};

```

### Il Mock di Metodi Privati or Protetti

Si deve sempre inserire una definizione del metodo mock (`MOCK_METHOD`) in una sezione `public:` della classe mock, indipendentemente dal fatto che il metodo mocked sia `public`, `protected`, o `private` nella classe base. Ciò consente a `ON_CALL` e a `EXPECT_CALL` di fare riferimento alla funzione mock dall'esterno della classe mock.
(Sì, il C++ consente a una sottoclasse di modificare il livello di accesso di una funzione virtuale nella classe base). Esempio:

```cpp
class Foo {
 public:
  ...
  virtual bool Transform(Gadget* g) = 0;
 protected:
  virtual void Resume();
 private:
  virtual int GetTimeOut();
};
class MockFoo : public Foo {
 public:
  ...
  MOCK_METHOD(bool, Transform, (Gadget* g), (override));
  // Quanto segue deve stare nella sezione public, anche se i
  // metodi sono protected o private nella classe base.
  MOCK_METHOD(void, Resume, (), (override));
  MOCK_METHOD(int, GetTimeOut, (), (override));
};

```

### Mock di Metodi Overloaded

Si possono avere funzioni overloaded mock-ate come al solito. Non è richiesta alcuna attenzione particolare:

```cpp
class Foo {
  ...
  // Deve essere virtuale poiché erediteremo da Foo.
  virtual ~Foo();
  // Overloaded sui tipi e/o numeri di argomenti.
  virtual int Add(Element x);
  virtual int Add(int times, Element x);
  // Overloaded sul const di questo oggetto.
  virtual Bar& GetBar();
  virtual const Bar& GetBar() const;
};
class MockFoo : public Foo {
  ...
  MOCK_METHOD(int, Add, (Element x), (override));
  MOCK_METHOD(int, Add, (int times, Element x), (override));
  MOCK_METHOD(Bar&, GetBar, (), (override));
  MOCK_METHOD(const Bar&, GetBar, (), (const, override));
};

```

{: .callout .note}
**Nota:** se non si mock-ano tutte le versioni del metodo sovraccaricato, il compilatore darà un warning sul fatto che che alcuni metodi nella classe base sono nascosti. Per risolvere questo problema, usare `using` per inserirli nello scope:

```cpp
class MockFoo : public Foo {
  ...
  using Foo::Add;
  MOCK_METHOD(int, Add, (Element x), (override));
  // Non vogliamo versione mock di Add(int times, Element x);
  ...
};

```

### Mock di Classi Template

Si può avere la versione mock di classi template come con qualsiasi classe.

```cpp
template <typename Elem>
class StackInterface {
  ...
  // Deve essere virtual poiché erediteremo da StackInterface.
  virtual ~StackInterface();
  virtual int GetSize() const = 0;
  virtual void Push(const Elem& x) = 0;
};
template <typename Elem>
class MockStack : public StackInterface<Elem> {
  ...
  MOCK_METHOD(int, GetSize, (), (override));
  MOCK_METHOD(void, Push, (const Elem& x), (override));
};

```

### Mock di Metodi Non-virtual {#MockingNonVirtualMethods}

gMock può produrre versioni mock di funzioni non-virtual da utilizzare nell'inserimento [injection] delle dipendenze Hi-perf.

In questo caso, invece di condividere una classe base comune con la classe reale, la classe mock sarà *non correlata* alla classe reale, ma conterrà metodi con le stesse firme. La sintassi per il mock dei metodi non-virtual è la *stessa* dei mock dei metodi virtual (basta non aggiungere `override`):

```cpp
// Una semplice classe per lo stream di pacchetti [packet].  Nessuno dei suoi membri è virtual.
class ConcretePacketStream {
 public:
  void AppendPacket(Packet* new_packet);
  const Packet* GetPacket(size_t packet_number) const;
  size_t NumberOfPackets() const;
  ...
};
// A mock packet stream class.  Non eredita da nessun altro, ma definisce
// GetPacket() e NumberOfPackets().
class MockPacketStream {
 public:
  MOCK_METHOD(const Packet*, GetPacket, (size_t packet_number), (const));
  MOCK_METHOD(size_t, NumberOfPackets, (), (const));
  ...
};

```

Notare che la classe mock non definisce `AppendPacket()`, come la classe reale.
Va bene fin quando non è necessario che il test lo chiami.

Successivamente, c'è bisogno di un modo per dire che si vuole utilizzare `ConcretePacketStream` nel codice di produzione mentre `MockPacketStream` nei test. Dato che le funzioni non sono virtuali e le due classi non sono correlate, si deve specificare la scelta in *fase di compilazione* (invece che in fase di esecuzione [run time]).

Un modo per farlo è creare un template del codice che deve utilizzare lo stream di packet.
Più specificamente, si fornirà al codice un argomento di tipo template per il tipo di stream di packet. In produzione, si creerà un'istanza del template con `ConcretePacketStream` come argomento del tipo. Nei test, si istanzierà lo stesso template con `MockPacketStream`. Per esempio, si può scrivere:

```cpp
template <class PacketStream>
void CreateConnection(PacketStream* stream) { ... }
template <class PacketStream>
class PacketReader {
 public:
  void ReadPackets(PacketStream* stream, size_t packet_num);
};

```

Poi si possono usare `CreateConnection<ConcretePacketStream>()` e `PacketReader<ConcretePacketStream>` nel codice di produzione, e nei test `CreateConnection<MockPacketStream>()` e `PacketReader<MockPacketStream>`.

```cpp
  MockPacketStream mock_stream;
  EXPECT_CALL(mock_stream, ...)...;
  .. set more expectations on mock_stream ...
  PacketReader<MockPacketStream> reader(&mock_stream);
  ... exercise reader ...

```

### Mock di Funzioni Libere [Free]

Non è possibile avere direttamente mock di una funzione libera (ad esempio una funzione in stile C o un metodo statico). Se necessario, si può riscrivere il codice per utilizzare un'interfaccia (classe astratta).

Invece di chiamare direttamente una funzione libera (ad esempio, `OpenFile`), se ne introduce un'interfaccia e si dispone una sottoclasse concreta che chiama la funzione libera:

```cpp
class FileInterface {
 public:
  ...
  virtual bool Open(const char* path, const char* mode) = 0;
};
class File : public FileInterface {
 public:
  ...
  bool Open(const char* path, const char* mode) override {
     return OpenFile(path, mode);
  }
};

```

Il codice dovrebbe comunicare con `FileInterface` per aprire un file. Ora è facile mock-are la funzione.

Potrebbe sembrare una seccatura, ma in pratica spesso ci sono più funzioni correlate inseribili nella stessa interfaccia, quindi la complicazione sintattica per ogni funzione sarà molto inferiore.

Se si è preoccupati per la resa prestazionale sostenuta dalle funzioni virtuali e la profilazione conferma tale preoccupazione, lo si può combinare con la ricetta per i [mock di metodi non-virtual](#MockingNonVirtualMethods).

In alternativa, invece di introdurre una nuova interfaccia, si può riscrivere il codice per accettare una std::function invece della funzione libera per poi utilizzare [MockFunction](#MockFunction) per simulare la std::function.

### Macro `MOCK_METHODn` Old-Style

Prima che la macro generica `MOCK_METHOD` [venisse introdotta nel 2018](https://github.com/google/googletest/commit/c5f08bf91944ce1b19bcf414fa1760e69d20afc2), i mock venivano creati utilizzando una famiglia di macro chiamate `MOCK_METHODn`.
Queste macro sono ancora supportate, sebbene sia consigliata la migrazione al nuovo `MOCK_METHOD`.

Le macro nella famiglia `MOCK_METHODn` differiscono da `MOCK_METHOD`:

*   The general structure is `MOCK_METHODn(MethodName, ReturnType(Args))`,
    instead of `MOCK_METHOD(ReturnType, MethodName, (Args))`.
*   Il numero `n` deve essere uguale al numero di argomenti.
*   Quando si crea il mock di un metodo const, è necessario utilizzare `MOCK_CONST_METHODn`.
*   Quando si crea il mock di una classe template, il nome della macro deve avere il suffisso `_T`.
*   Per specificare il tipo di chiamata, il nome della macro deve avere il suffisso `_WITH_CALLTYPE` e il tipo di chiamata è il primo argomento della macro.

Le vecchie macro e i loro nuovi equivalenti:

<table>
  <tr><th colspan=2>Semplice</th></tr>
  <tr>
    <td>Vecchia</td>
    <td><code>MOCK_METHOD1(Foo, bool(int))</code></td>
  </tr>
  <tr>
    <td>Nuova</td>
    <td><code>MOCK_METHOD(bool, Foo, (int))</code></td>
  </tr>

  <tr><th colspan=2>Metodo Const</th></tr>
  <tr>
    <td>Vecchia</td>
    <td><code>MOCK_CONST_METHOD1(Foo, bool(int))</code></td>
  </tr>
  <tr>
    <td>Nuova</td>
    <td><code>MOCK_METHOD(bool, Foo, (int), (const))</code></td>
  </tr>

  <tr><th colspan=2>Metodo in una Classe Template</th></tr>
  <tr>
    <td>Vecchia</td>
    <td><code>MOCK_METHOD1_T(Foo, bool(int))</code></td>
  </tr>
  <tr>
    <td>Nuova</td>
    <td><code>MOCK_METHOD(bool, Foo, (int))</code></td>
  </tr>

  <tr><th colspan=2>Metodo Const in una Classe Template</th></tr>
  <tr>
    <td>Vecchia</td>
    <td><code>MOCK_CONST_METHOD1_T(Foo, bool(int))</code></td>
  </tr>
  <tr>
    <td>Nuova</td>
    <td><code>MOCK_METHOD(bool, Foo, (int), (const))</code></td>
  </tr>

  <tr><th colspan=2>Metodo con un Tipo di Chiamata [Call Type]</th></tr>
  <tr>
    <td>Vecchia</td>
    <td><code>MOCK_METHOD1_WITH_CALLTYPE(STDMETHODCALLTYPE, Foo, bool(int))</code></td>
  </tr>
  <tr>
    <td>Nuova</td>
    <td><code>MOCK_METHOD(bool, Foo, (int), (Calltype(STDMETHODCALLTYPE)))</code></td>
  </tr>

  <tr><th colspan=2>Metodo Const con una [Call Type]</th></tr>
  <tr>
    <td>Vecchia</td>
    <td><code>MOCK_CONST_METHOD1_WITH_CALLTYPE(STDMETHODCALLTYPE, Foo, bool(int))</code></td>
  </tr>
  <tr>
    <td>Nuova</td>
    <td><code>MOCK_METHOD(bool, Foo, (int), (const, Calltype(STDMETHODCALLTYPE)))</code></td>
  </tr>

  <tr><th colspan=2>Metodo con una [Call Type] in una Classe Template</th></tr>
  <tr>
    <td>Vecchia</td>
    <td><code>MOCK_METHOD1_T_WITH_CALLTYPE(STDMETHODCALLTYPE, Foo, bool(int))</code></td>
  </tr>
  <tr>
    <td>Nuova</td>
    <td><code>MOCK_METHOD(bool, Foo, (int), (Calltype(STDMETHODCALLTYPE)))</code></td>
  </tr>

  <tr><th colspan=2>Metodo Const con una [Call Type] in una Classe Template</th></tr>
  <tr>
    <td>Vecchia</td>
    <td><code>MOCK_CONST_METHOD1_T_WITH_CALLTYPE(STDMETHODCALLTYPE, Foo, bool(int))</code></td>
  </tr>
  <tr>
    <td>Nuova</td>
    <td><code>MOCK_METHOD(bool, Foo, (int), (const, Calltype(STDMETHODCALLTYPE)))</code></td>
  </tr>
</table>

### Nice, Strict e Naggy {#NiceStrictNaggy}

Se un metodo mock non ha specifiche `EXPECT_CALL` ma viene chiamato, si dice che è una "non interessante" e verrà eseguita l'azione di default (specificabile con `ON_CALL()`). Attualmente, una chiamata non interessante farà sì che gMock stampi un warning per default.

Tuttavia, a volte si vorrebbero ignorare queste chiamate poco interessanti, altre volte le si vorrebbe trattare come errori. gMock consente di decidere per ciascun oggetto mock.

Supponiamo che il test utilizzi una classe mock `MockFoo`:

```cpp
TEST(...) {
  MockFoo mock_foo;
  EXPECT_CALL(mock_foo, DoThis());
  ... codice che usa mock_foo ...
}

```

Se viene chiamato un metodo di `mock_foo` diverso da `DoThis()`, si otterrà un warning. Tuttavia, se si riscrive il test per utilizzare invece `NiceMock<MockFoo>`, si può sopprimere il warning:

```cpp
using ::testing::NiceMock;
TEST(...) {
  NiceMock<MockFoo> mock_foo;
  EXPECT_CALL(mock_foo, DoThis());
  ... codice che usa mock_foo ...
}

```

`NiceMock<MockFoo>` è una sottoclasse di `MockFoo`, quindi può essere utilizzata ovunque sia accettata `MockFoo`.

Funziona anche se il costruttore di `MockFoo` accetta alcuni argomenti, poiché `NiceMock<MockFoo>` "eredita" i costruttori di `MockFoo`:

```cpp
using ::testing::NiceMock;
TEST(...) {
  NiceMock<MockFoo> mock_foo(5, "hi");  // Calls MockFoo(5, "hi").
  EXPECT_CALL(mock_foo, DoThis());
  ... codice che usa mock_foo ...
}

```

L'utilizzo di `StrictMock` è simile, tranne per il fatto che trasforma tutte le chiamate "non interessanti" in errori:

```cpp
using ::testing::StrictMock;
TEST(...) {
  StrictMock<MockFoo> mock_foo;
  EXPECT_CALL(mock_foo, DoThis());
  ... codice che usa mock_foo ...
  // Il test fallisce se si usa un metodo di mock_foo anziché DoThis()
  //.
}

```

{: .callout .note}
NOTA: `NiceMock` e `StrictMock` influenzano solo le chiamate *non interessanti* (chiamate di *metodi* senza [expectation]); non influenzano le chiamate *unexpected* (chiamate di metodi con expectation, ma che non corrispondono). Vedere [Le Chiamate Poco Interessanti e Quelle Unexpected](#uninteresting-vs-unexpected).

Ci sono però alcuni avvertimenti (purtroppo sono effetti collaterali delle limitazioni del C++):

1.  `NiceMock<MockFoo>` and `StrictMock<MockFoo>` only work for mock methods
    defined using the `MOCK_METHOD` macro **directly** in the `MockFoo` class.
    If a mock method is defined in a **base class** of `MockFoo`, the "nice" or
    "strict" modifier may not affect it, depending on the compiler. In
    particular, nesting `NiceMock` and `StrictMock` (e.g.
`NiceMock<StrictMock<MockFoo> >`) is **not** supported.
2.  `NiceMock<MockFoo>` and `StrictMock<MockFoo>` may not work correctly if the
    destructor of `MockFoo` is not virtual. We would like to fix this, but it
    requires cleaning up existing tests.

Infine, si deve porre **molta attenzione** su quando utilizzare mock "naggy" o "strict", poiché tendono a rendere i test più fragili e più difficili da mantenere. Quando si esegue il refactoring del codice senza modificarne il comportamento visibile dall'esterno, idealmente si dovrebbe aver bisogno di aggiornare alcun test. Se il codice interagisce con un mock "naggy", però, si potrebbe iniziare a ricevere notevoli warning come risultato della modifica. Peggio ancora, se il codice interagisce con un mock "strict", i test potrebbero iniziare a fallire e si sarà costretti a correggerli. La nostra raccomandazione generale è quella di utilizzare mock "nice" (non ancora il default) per la maggior parte del tempo, usare mock "naggy" (l'attuale default) durante lo sviluppo o il debug dei test e usare mock "strict" solo come ultima risorsa.

### Semplificare l'Interfaccia senza Compromettere il Codice Esistente {#SimplerInterfaces}

A volte un metodo ha un lungo elenco di argomenti che nella maggior parte dei casi non sono interessanti.
Per esempio:

```cpp
class LogSink {
 public:
  ...
  virtual void send(LogSeverity severity, const char* full_filename,
                    const char* base_filename, int line,
                    const struct tm* tm_time,
                    const char* message, size_t message_len) = 0;
};

```

L'elenco degli argomenti di questo metodo è lungo e difficile da gestire (l'argomento `message` non è nemmeno "0-terminated"). Se si crea il mock così com'è, il suo uso risulterà problematico. Se, tuttavia, proviamo a semplificare questa interfaccia, dovremo sistemare tutti i client che dipendono da essa, il che spesso è irrealizzabile.

Il trucco sta nel redistribuire il metodo nella classe mock:

```cpp
class ScopedMockLog : public LogSink {
 public:
  ...
  void send(LogSeverity severity, const char* full_filename,
                    const char* base_filename, int line, const tm* tm_time,
                    const char* message, size_t message_len) override {
    // Siamo interessati solo alla gravità nel log, il nome completo del file e
    // al messaggio del log.
    Log(severity, full_filename, std::string(message, message_len));
  }

  // Implementa il metodo mock:
  //
  //   void Log(LogSeverity severity,
  //            const string& file_path,
  //            const string& message);
  MOCK_METHOD(void, Log,
              (LogSeverity severity, const string& file_path,
               const string& message));
};

```

Definendo un nuovo metodo mock con un elenco di argomenti ridotto, rendiamo la classe mock più user-friendly.

Questa tecnica può essere applicata anche per facilitare la creazione di mock dei metodi [overloaded]. Ad esempio, quando sono stati utilizzati gli overload per implementare argomenti di default:

```cpp
class MockTurtleFactory : public TurtleFactory {
 public:
  Turtle* MakeTurtle(int length, int weight) override { ... }
  Turtle* MakeTurtle(int length, int weight, int speed) override { ... }
  // i metodi precedenti delegano questo:
  MOCK_METHOD(Turtle*, DoMakeTurtle, ());
};

```

Ciò consente di avere test a cui non interessa quale overload sia stato invocato per evitare di specificare i matcher degli argomenti:

```cpp
ON_CALL(factory, DoMakeTurtle)
    .WillByDefault(Return(MakeMockTurtle()));

```

### Alternativa ai Mock delle Classi Concrete

Spesso ci si ritrova a utilizzare classi che non implementano interfacce. Per testare il codice che utilizza una classe di questo tipo (chiamiamola `Concrete`), si potrebbe essere tentati di rendere virtuali i metodi di `Concrete` e crearne il mock.

Cercare di non farlo.

Rendere virtuale una funzione non virtuale è una decisione importante. Si crea un punto di estensione in cui le sottoclassi possono modificare il comportamento della classe. Ciò indebolisce il controllo sulla classe perché ora è più difficile mantenere le invarianti della classe. Si deve rendere virtuale una funzione solo quando esiste un motivo valido per cui una sottoclasse la debba sovrascrivere [override].

Creare direttamente mock di classi concrete è problematico in quanto crea uno stretto accoppiamento tra la classe e i test: qualsiasi piccolo cambiamento nella classe può invalidare i test e rendere difficile la manutenzione dei test.

Per evitare tali problemi, molti programmatori praticano la "codificazione delle interfacce": invece di parlare con la classe `Concrete`, il codice dovrebbe definire un'interfaccia e comunicare tramite essa. Quindi si implementa l'interfaccia come un adattatore al di sopra di `Concrete`. Nei test, si puoi facilmente creare il mock dell'interfaccia per osservare come sta andando il codice.

Questa tecnica comporta un po' di lavoro:

*   Si paga il costo delle chiamate di funzioni virtuali (di solito non è un problema).
*   C'è più astrazione da imparare per i programmatori.

Tuttavia, si possono anche apportare benefici significativi oltre a una migliore testabilità:

*   `Concrete`'s API may not fit your problem domain very well, as you may not
    be the only client it tries to serve. By designing your own interface, you
    have a chance to tailor it to your need - you may add higher-level
    functionalities, rename stuff, etc instead of just trimming the class. This
    allows you to write your code (user of the interface) in a more natural way,
    which means it will be more readable, more maintainable, and you'll be more
    productive.
*   If `Concrete`'s implementation ever has to change, you don't have to rewrite
    everywhere it is used. Instead, you can absorb the change in your
    implementation of the interface, and your other code and tests will be
    insulated from this change.

Qualcuno teme che se tutti praticassero questa tecnica, si finirebbe per scrivere molto codice ridondante. Questa preoccupazione è del tutto comprensibile.
Tuttavia, ci sono due ragioni per cui potrebbe non essere così:

*   Different projects may need to use `Concrete` in different ways, so the best
    interfaces for them will be different. Therefore, each of them will have its
    own domain-specific interface on top of `Concrete`, and they will not be the
    same code.
*   If enough projects want to use the same interface, they can always share it,
    just like they have been sharing `Concrete`. You can check in the interface
    and the adaptor somewhere near `Concrete` (perhaps in a `contrib`
    sub-directory) and let many projects use it.

Si devono valutare attentamente i pro e i contro per il problema particolare, ma certamente la comunità Java lo pratica da molto tempo ed è una tecnica comprovata ed efficace applicabile in un'ampia varietà di situazioni. :-)

### Delegare le Chiamate ad una Fake {#DelegatingToFake}

Talvolta si hanno implementazioni [fake] non banali di un'interfaccia. Per esempio:

```cpp
class Foo {
 public:
  virtual ~Foo() {}
  virtual char DoThis(int n) = 0;
  virtual void DoThat(const char* s, int* p) = 0;
};
class FakeFoo : public Foo {
 public:
  char DoThis(int n) override {
    return (n > 0) ? '+' :
           (n < 0) ? '-' : '0';
  }

  void DoThat(const char* s, int* p) override {
    *p = strlen(s);
  }
};

```

Ora si vuole creare la mock di questa interfaccia in modo da potervi impostare delle expectation.
Tuttavia, si vuole usare anche `FakeFoo` per il comportamento di default, poiché duplicarlo nell'oggetto mock richiede molto lavoro.

Quando si definisce la classe mock utilizzando gMock, si può far sì che deleghi la sua azione di default a una classe fake che già si possiede, utilizzando questo pattern:

```cpp
class MockFoo : public Foo {
 public:
  // Definizioni di metodi mock normali utilizzando gMock.
  MOCK_METHOD(char, DoThis, (int n), (override));
  MOCK_METHOD(void, DoThat, (const char* s, int* p), (override));
  // Delegates le azioni di default dei metodi a un oggetto di FakeFoo.
  // Deve essere chiamato *prima* delle istruzioni custom di ON_CALL().
  void DelegateToFake() {
    ON_CALL(*this, DoThis).WillByDefault([this](int n) {
      return fake_.DoThis(n);
    });

    ON_CALL(*this, DoThat).WillByDefault([this](const char* s, int* p) {
      fake_.DoThat(s, p);
    });

  }

 private:
  FakeFoo fake_;  // Mantiene un'istanza del fake nel mock.
};

```

Con questo si può usare `MockFoo` nei test come al solito. Ricordarsi solo che se non si imposta esplicitamente un'azione in una `ON_CALL()` o in una `EXPECT_CALL()`, la fake verrà chiamato a farlo.:

```cpp
using ::testing::_;
TEST(AbcTest, Xyz) {
  MockFoo foo;
  foo.DelegateToFake();  // Enables the fake for delegation.
  // Se ce ne sono, mettere qui le ON_CALL(foo, ...).
  // Nessuna azione specificata, ovvero utilizzare l'azione di default.
  EXPECT_CALL(foo, DoThis(5));
  EXPECT_CALL(foo, DoThat(_, _));
  int n = 0;
  EXPECT_EQ(foo.DoThis(5), '+');  // FakeFoo::DoThis() is invoked.
  foo.DoThat("Hi", &n);  // FakeFoo::DoThat() is invoked.
  EXPECT_EQ(n, 2);
}

```

**Alcuni suggerimenti:**

*   Volendo, si può comunque sovrascrivere l'azione di default fornendo la propria `ON_CALL()` o utilizzando `.WillOnce()` / `.WillRepeatedly()` in `EXPECT_CALL()`.
*   In `DelegateToFake()`, you only need to delegate the methods whose fake
    implementation you intend to use.

*   The general technique discussed here works for overloaded methods, but
    you'll need to tell the compiler which version you mean. To disambiguate a
    mock function (the one you specify inside the parentheses of `ON_CALL()`),
    use [this technique](#SelectOverload); to disambiguate a fake function (the
    one you place inside `Invoke()`), use a `static_cast` to specify the
    function's type. For instance, if class `Foo` has methods `char DoThis(int
n)` and `bool DoThis(double x) const`, and you want to invoke the latter,
    you need to write `Invoke(&fake_, static_cast<bool (FakeFoo::*)(double)
const>(&FakeFoo::DoThis))` instead of `Invoke(&fake_, &FakeFoo::DoThis)`
    (The strange-looking thing inside the angled brackets of `static_cast` is
    the type of a function pointer to the second `DoThis()` method.).

*   Dover mischiare una mock con una fake è spesso un segno che qualcosa è andato storto.
    Forse non si è ancora abituati al metodo di test basato sull'interazione [interaction-based]. Or
    perhaps your interface is taking on too many roles and should be split up.
    Pertanto, **non abusare**. We would only recommend to do it as an
    intermediate step when you are refactoring your code.

Per quanto riguarda il suggerimento su come mescolare un mock e un fake, ecco un esempio del perché potrebbe essere un brutto segno: supponiamo di avere una classe `System` per operazioni di sistema di basso livello. In particolare, vengono eseguite operazioni su file e I/O. E supponiamo che si voglia testare come il codice utilizza `System` per eseguire I/O e si voglia semplicemente che le operazioni sui file funzionino normalmente. Se si crea la mock di tutta la classe `System`, si dovrà fornire un'implementazione fake per la parte relativa alle operazioni sui file, il che suggerisce che `System` sta assumendo troppi ruoli.

Si può invece definire un'interfaccia `FileOps` e un'interfaccia `IOOps` dividendo le funzionalità di `System` in due. Poi si può creare la mock di `IOOps` senza avere un mock di `FileOps`.

### Delegare le Chiamate all'Oggetto Reale

Quando si utilizzano copie di test (mock, fake, stub e così via), a volte i loro comportamenti differiranno da quelli degli oggetti reali. Questa differenza potrebbe essere intenzionale (come nella simulazione di un errore in modo da poter testare il codice di gestione degli errori) o involontaria. Se per errore i mock hanno comportamenti diversi rispetto agli oggetti reali, ci si potrebbe ritrovare con un codice che supera i test ma fallisce in produzione.

Si può utilizzare la tecnica *delegating-to-real* per fare in modo che il mock abbia lo stesso comportamento dell'oggetto reale pur mantenendo la capacità di convalidare le chiamate.
Questa tecnica è molto simile alla [delegating-to-fake](#DelegatingToFake), con la differenza che utilizziamo un oggetto reale invece di un fake.
Ecco un esempio:

```cpp
using ::testing::AtLeast;
class MockFoo : public Foo {
 public:
  MockFoo() {
    // Per default, tutte le chiamate sono delegate all'oggetto reale.
    ON_CALL(*this, DoThis).WillByDefault([this](int n) {
      return real_.DoThis(n);
    });

    ON_CALL(*this, DoThat).WillByDefault([this](const char* s, int* p) {
      real_.DoThat(s, p);
    });

    ...
  }

  MOCK_METHOD(char, DoThis, ...);
  MOCK_METHOD(void, DoThat, ...);
  ...
 private:
  Foo real_;
};
...
  MockFoo mock;
  EXPECT_CALL(mock, DoThis())
      .Times(3);
  EXPECT_CALL(mock, DoThat("Hi"))
      .Times(AtLeast(1));
  ... use mock in test ...

```

Con questo, gMock verificherà che il codice abbia effettuato le chiamate giuste (con gli argomenti giusti, nell'ordine giusto, chiamato il numero giusto di volte, ecc.) e un oggetto reale risponderà alle chiamate (quindi il comportamento sarà lo stesso come in produzione). Questo fornisce il meglio di entrambi i mondi.

### Delegare le Chiamate a una Classe Genitore

Idealmente, si dovrebbero codificare le interfacce, i cui metodi sono tutti puramente virtuali. In realtà, a volte è necessario creare la mock di un metodo virtuale che non è puro (ovvero ha già un'implementazione). Per esempio:

```cpp
class Foo {
 public:
  virtual ~Foo();
  virtual void Pure(int n) = 0;
  virtual int Concrete(const char* str) { ... }
};
class MockFoo : public Foo {
 public:
  // Il mock di un metodo puro.
  MOCK_METHOD(void, Pure, (int n), (override));
  // Il mock di un metodo concreto.  Foo::Concrete() is shadowed.
  MOCK_METHOD(int, Concrete, (const char* str), (override));
};

```

A volte si vorrebbe chiamare `Foo::Concrete()` invece di `MockFoo::Concrete()`. Probabilmente come parte di un'azione stub, o forse il test non ha bisogno del mock di `Concrete()` (ma sarebbe davvero tedioso dover definire una nuova classe mock ogni volta che non è necessario il mock di uno dei suoi metodi).

Si può chiamare `Foo::Concrete()` all'interno di un'azione:

```cpp
...
  EXPECT_CALL(foo, Concrete).WillOnce([&foo](const char* str) {
    return foo.Foo::Concrete(str);
  });

```

oppure dire al mock dell'oggetto che non si vuole il mock di `Concrete()`:

```cpp
...
  ON_CALL(foo, Concrete).WillByDefault([&foo](const char* str) {
    return foo.Foo::Concrete(str);
  });

```

(Perché non scrivere semplicemente `{ return foo.Concrete(str); }`? Se lo si fa, verrà chiamato `MockFoo::Concrete()` (provocando una ricorsione infinita) in quanto `Foo::Concrete()` è virtuale. È così che funziona il C++).

## Uso dei Matcher

### Matching Esatto dei Valori degli Argomenti

Si può specificare esattamente quali argomenti si aspetta un metodo mock:

```cpp
using ::testing::Return;
...
  EXPECT_CALL(foo, DoThis(5))
      .WillOnce(Return('a'));
  EXPECT_CALL(foo, DoThat("Hello", bar));

```

### Uso di Semplici Matcher

I matcher si possono usare per abbinare [match] argomenti che hanno una certa proprietà:

```cpp
using ::testing::NotNull;
using ::testing::Return;
...
  EXPECT_CALL(foo, DoThis(Ge(5)))  // The argument must be >= 5.
      .WillOnce(Return('a'));
  EXPECT_CALL(foo, DoThat("Hello", NotNull()));
      // Il secondo argomento non deve essere NULL.

```

Un matcher usato spesso è `_`, che corrisponde a qualsiasi cosa:

```cpp
  EXPECT_CALL(foo, DoThat(_, NotNull()));

```

### Combinazione di Matcher {#CombiningMatchers}

Si possono creare abbinamenti complessi da quelli esistenti utilizzando `AllOf()`, `AllOfArray()`, `AnyOf()`, `AnyOfArray()` e `Not()`:

```cpp
using ::testing::AllOf;
using ::testing::Gt;
using ::testing::HasSubstr;
using ::testing::Ne;
using ::testing::Not;
...
  // L'argomento dev'essere > 5 e != 10.
  EXPECT_CALL(foo, DoThis(AllOf(Gt(5),
                                Ne(10))));
  // Il primo argomento non deve contenere la sotto-stringa "blah".
  EXPECT_CALL(foo, DoThat(Not(HasSubstr("blah")),
                          NULL));

```

I matcher sono oggetti funzione e quelli parametrizzati possono essere composti proprio come qualsiasi altra funzione. Tuttavia, poiché i tipi possono essere lunghi e raramente forniscono informazioni significative, può essere più semplice esprimerli con le generiche lambda di C++14 per evitare di specificare i tipi. Per esempio,

```cpp
using ::testing::Contains;
using ::testing::Property;
inline constexpr auto HasFoo = [](const auto& f) {
  return Property("foo", &MyClass::foo, Contains(f));
};
...
  EXPECT_THAT(x, HasFoo("blah"));

```

### Casting dei Matcher {#SafeMatcherCast}

I matcher di gMock sono tipizzati staticamente, il che significa che il compilatore può individuare l'errore se si usa un matcher del tipo sbagliato (ad esempio, se si usa `Eq(5)` per trovare una corrispondenza con un argomento `string`). Una cosa buona!

A volte, però, sapendo cosa si fa, si vuole che il compilatore dia un po' di tregua. Un esempio è che si abbia un matcher per `long` e l'argomento che si vuol trovare è `int`. Sebbene i due tipi non siano esattamente gli stessi, non c'è niente di veramente sbagliato nell'usare un `Matcher<long>` per abbinare un `int` - dopo tutto, possiamo convertire prima l'argomento `int` in un `long` senza perdere informazioni prima di passarlo al matcher.

Per supportare questa esigenza, gMock offre la funzione `SafeMatcherCast<T>(m)`. Si effettua il cast di un matcher `m` nel tipo `Matcher<T>`. Per garantire la sicurezza, gMock verifica che sia `U` il tipo accettato da `m`:

1.  Il tipo `T` può essere convertito [cast] *implicitamente* nel tipo `U`;
2.  When both `T` and `U` are built-in arithmetic types (`bool`, integers, and
    floating-point numbers), the conversion from `T` to `U` is not lossy (in
    other words, any value representable by `T` can also be represented by `U`);
    e
3.  When `U` is a reference, `T` must also be a reference (as the underlying
    matcher may be interested in the address of the `U` value).

Il codice non verrà compilato se una di queste condizioni non viene soddisfatta.

Ecco un esempio:

```cpp
using ::testing::SafeMatcherCast;
// A base class and a child class.
class Base { ... };
class Derived : public Base { ... };
class MockFoo : public Foo {
 public:
  MOCK_METHOD(void, DoThis, (Derived* derived), (override));
};
...
  MockFoo foo;
  // m è un Matcher<Base*> che abbiamo ottenuto da qualche parte.
  EXPECT_CALL(foo, DoThis(SafeMatcherCast<Derived*>(m)));

```

Se si ritiene la `SafeMatcherCast<T>(m)` troppo limitante, si può usare una funzione simile `MatcherCast<T>(m)`. La differenza è che `MatcherCast` funziona finquando si può eseguire lo `static_cast` del tipo `T` nel tipo `U`.

`MatcherCast` consente essenzialmente di aggirare il sistema di tipi di C++ (`static_cast` non è sempre sicuro in quanto potrebbe eliminare informazioni, ad esempio), si faccia quindi attenzione a non abusarne.

### Scegliere le Funzioni Overloaded {#SelectOverload}

Se ci si aspetta che venga chiamata una funzione overloaded, il compilatore potrebbe aver bisogno di aiuto sulla scelta della versione.

Per chiarire le ambiguità delle funzioni overloaded tramite l'essere const di questo oggetto, si usa l'argomento wrapper di `Const()`.

```cpp
using ::testing::ReturnRef;
class MockFoo : public Foo {
  ...
  MOCK_METHOD(Bar&, GetBar, (), (override));
  MOCK_METHOD(const Bar&, GetBar, (), (const, override));
};
...
  MockFoo foo;
  Bar bar1, bar2;
  EXPECT_CALL(foo, GetBar())         // Il GetBar() non-const.
      .WillOnce(ReturnRef(bar1));
  EXPECT_CALL(Const(foo), GetBar())  // Il GetBar() const.
      .WillOnce(ReturnRef(bar2));

```

(`Const()` è definito da gMock e restituisce un riferimento `const` al suo argomento).

Per chiarire le ambiguità delle funzioni overloaded con lo stesso numero di argomenti ma tipi di argomento diversi, potrebbe essere necessario specificare il tipo esatto di un matcher, racchiudendolo in `Matcher<type>()` o utilizzando un matcher il cui tipo è fisso (`TypedEq<type>`, `An<type>()`, ecc.):

```cpp
using ::testing::An;
using ::testing::Matcher;
using ::testing::TypedEq;
class MockPrinter : public Printer {
 public:
  MOCK_METHOD(void, Print, (int n), (override));
  MOCK_METHOD(void, Print, (char c), (override));
};
TEST(PrinterTest, Print) {
  MockPrinter printer;
  EXPECT_CALL(printer, Print(An<int>()));            // void Print(int);
  EXPECT_CALL(printer, Print(Matcher<int>(Lt(5))));  // void Print(int);
  EXPECT_CALL(printer, Print(TypedEq<char>('a')));   // void Print(char);
  printer.Print(3);
  printer.Print(6);
  printer.Print('a');
}

```

### Eseguire Azioni Diverse in Base agli Argomenti

Quando viene chiamato un metodo mock, verrà selezionato l'*ultimo* matching expectation ancora attiva (si pensi che "il più recente sovrascrive il più vecchio"). Quindi, si può fare in modo che un metodo faccia cose diverse a seconda dei valori dei suoi argomenti in questo modo:

```cpp
using ::testing::_;
using ::testing::Lt;
using ::testing::Return;
...
  // Il caso di default.
  EXPECT_CALL(foo, DoThis(_))
      .WillRepeatedly(Return('b'));
  // Il caso più specifico.
  EXPECT_CALL(foo, DoThis(Lt(5)))
      .WillRepeatedly(Return('a'));

```

Ora, se `foo.DoThis()` viene chiamato con un valore inferiore a 5, verrà restituito `'a'`; altrimenti verrà restituito `'b'`.

### Corrispondenza di Più Argomenti come un Tutt'uno

A volte non è sufficiente abbinare [match] gli argomenti individualmente. Ad esempio, potremmo voler dire che il primo argomento deve essere minore del secondo argomento.
La clausola `With()` ci consente di abbinare tutti gli argomenti di una funzione mock nel suo insieme. Per esempio,

```cpp
using ::testing::_;
using ::testing::Ne;
using ::testing::Lt;
...
  EXPECT_CALL(foo, InRange(Ne(0), _))
      .With(Lt());

```

dice che il primo argomento di `InRange()` non deve essere 0 e deve essere minore del secondo argomento.

L'espressione in `With()` dev'essere un matcher del tipo `Matcher<std::tuple<A1, ..., An>>`, dove `A1`, ..., `An` sono i tipi degli argomenti della funzione.

Si può anche scrivere `AllArgs(m)` invece di `m` in `.With()`. Le due forme sono equivalenti, ma `.With(AllArgs(Lt()))` è più leggibile di `.With(Lt())`.

Si può usare `Args<k1, ..., kn>(m)` per far corrispondere gli `n` argomenti selezionati (come una tupla) con `m`. Per esempio,

```cpp
using ::testing::_;
using ::testing::AllOf;
using ::testing::Args;
using ::testing::Lt;
...
  EXPECT_CALL(foo, Blah)
      .With(AllOf(Args<0, 1>(Lt()), Args<1, 2>(Lt())));

```

dice che `Blah` verrà chiamato con gli argomenti `x`, `y` e `z` dove `x < y < z`. Si noti che in questo esempio, non è stato necessario specificare i matcher posizionali.

Per comodità ed esempio, gMock fornisce alcuni matcher per 2-tuple, incluso il matcher `Lt()` precedente. Consultare [Matcher Multi-argomento](reference/matchers.md#MultiArgMatchers) per la lista completa.

Si noti che per passare gli argomenti a un proprio predicato (p.es. `.With(Args<0, 1>(Truly(&MyPredicate)))`), quel predicato DEVE essere scritto per accettare un `std::tuple` come argomento; gMock passerà gli `n` argomenti selezionati come *una* singola tupla al predicato.

### Usare i Matcher come Predicati

Si è notato che un matcher è solo un fantasioso predicato che sa anche come descrivere se stesso? Molti algoritmi esistenti accettano predicati come argomenti (ad esempio quelli definiti nell'header `<algorithm>` di STL) e sarebbe un peccato se ai matcher gMock non fosse consentito partecipare.

Fortunatamente, si può utilizzare un matcher in cui è previsto un funtore del predicato unario racchiudendolo nella funzione `Matches()`. Per esempio,

```cpp
#include <algorithm>
#include <vector>
using ::testing::Matches;
using ::testing::Ge;
vector<int> v;
...
// How many elements in v are >= 10?
const int count = count_if(v.begin(), v.end(), Matches(Ge(10)));

```

Dal momento che si possono creare facilmente matcher complessi da quelli più semplici utilizzando gMock, questo fornisce un modo per costruire comodamente predicati compositi (fare lo stesso usando l'header `<functional>` di STL è semplicemente complicato). Per esempio, ecco un predicato soddisfatto da qualsiasi numero >= 0, <= 100 e != 50:

```cpp
using ::testing::AllOf;
using ::testing::Ge;
using ::testing::Le;
using ::testing::Matches;
using ::testing::Ne;
...
Matches(AllOf(Ge(0), Le(100), Ne(50)))

```

### Uso dei Matcher nelle Asserzioni di googletest

Vedere [`EXPECT_THAT`](reference/assertions.md#EXPECT_THAT) nei "Riferimenti sulle Asserzioni".

### Uso dei Predicati come Matcher

gMock fornisce un insieme di matcher nativi per far corrispondere gli argomenti con i valori attesi: per ulteriori informazioni consultare i [Riferimenti ai Matcher](reference/matchers.md).
Nel caso in cui si trovi carente il set nativo, si può utilizzare una funzione di predicato unario arbitrario o un funtore come matcher, purché il predicato accetti un valore del tipo desiderato. Lo si può fare racchiudendo il predicato all'interno della funzione `Truly()`, per esempio:

```cpp
using ::testing::Truly;
int IsEven(int n) { return (n % 2) == 0 ? 1 : 0; }
...
  // Bar() deve essere chiamato con un numero pari.
  EXPECT_CALL(foo, Bar(Truly(IsEven)));

```

Notare che la funzione/funtore del predicato non deve restituire `bool`. Funziona fin quando il valore restituito può essere utilizzato come condizione nell'istruzione `if (condizione) ...`.

### Match di Argomenti che Non Sono Copiabili

Quando si esegue un `EXPECT_CALL(mock_obj, Foo(bar))`, gMock salva una copia di `bar`. Quando `Foo()` viene chiamato in seguito, gMock confronta l'argomento di `Foo()` con la copia salvata di `bar`. In questo modo, non ci si deve preoccupare che la `bar` venga modificata o distrutta dopo l'esecuzione di `EXPECT_CALL()`. Lo stesso vale quando si usano matcher come `Eq(bar)`, `Le(bar)` e così via.

Ma cosa succede se `bar` non può essere copiato (cioè non ha un costruttore di copia)? Si potrebbe definire la propria funzione matcher o callback e usarla con `Truly()`, come mostrato nelle due ricette precedenti. Oppure si potrebbe riuscire a evitarlo se se si garantisce che la `bar` non verrà modificata dopo l'esecuzione di `EXPECT_CALL()`. Basta dire a gMock che dovrebbe salvare un riferimento a `bar`, invece di una sua copia. Ecco come:

```cpp
using ::testing::Eq;
using ::testing::Lt;
...
  // Si aspetta che l'argomento di Foo() == bar.
  EXPECT_CALL(mock_obj, Foo(Eq(std::ref(bar))));
  // Si aspetta che l'argomento di Foo() < bar.
  EXPECT_CALL(mock_obj, Foo(Lt(std::ref(bar))));

```

Da ricordare: se lo si fa, non modificare `bar` dopo la `EXPECT_CALL()`, altrimenti il risultato non sarà definito.

### Validare un Membro di un Oggetto

Spesso una funzione mock accetta un riferimento all'oggetto come argomento. Quando si esegue il matching di argomenti, si potrebbe non voler confrontare l'intero oggetto con un oggetto fisso, poiché ciò potrebbe essere eccessivo. Potrebbe invece essere necessario validare una determinata variabile membro o il risultato di un determinato metodo getter dell'oggetto.
Lo si può fare con `Field()` e con `Property()`. Più specificamente,

```cpp
Field(&Foo::bar, m)

```

è un matcher che corrisponde a un oggetto `Foo` la cui variabile membro `bar` soddisfa il matcher `m`.

```cpp
Property(&Foo::baz, m)

```

è un matcher che corrisponde a un oggetto `Foo` il cui metodo `baz()` restituisce un valore che soddisfa il matcher `m`.

Per esempio:

| Espressione | Descrizione |
| :--------------------------- | :--------------------------------------- |
| `Field(&Foo::number, Ge(3))` | Corrisponde a `x` dove `x.number >= 3`. |
| `Property(&Foo::name,  StartsWith("John "))` | Corrisponde a `x` dove `x.name()` inizia con `"John "`. |

Notare che in `Property(&Foo::baz, ...)`, il metodo `baz()` non deve accettare argomenti ed essere dichiarato come `const`. Non usare `Property()` contro funzioni membro che non si possiedono, perché prendere gli indirizzi delle funzioni è "fragile" e generalmente non fa parte del contratto della funzione.

`Field()` e `Property()` possono anche eseguire il match di semplici puntatori a oggetti. Per esempio,

```cpp
using ::testing::Field;
using ::testing::Ge;
...
Field(&Foo::number, Ge(3))

```

corrisponde a un semplice puntatore `p` dove `p->number >= 3`. Se `p` è `NULL`, il match fallirà sempre indipendentemente dal matcher interno.

Cosa succede se si validano più di un membro contemporaneamente? Si ricorda che ci sono [`AllOf()` e `AllOfArray()`](#CombiningMatchers).

Infine `Field()` e `Property()` forniscono gli overload che accettano i nomi del campo o della proprietà come primo argomento per includerlo nel messaggio di errore. Questo può essere utile quando si creano matcher combinati.

```cpp
using ::testing::AllOf;
using ::testing::Field;
using ::testing::Matcher;
using ::testing::SafeMatcherCast;
Matcher<Foo> IsFoo(const Foo& foo) {
  return AllOf(Field("some_field", &Foo::some_field, foo.some_field),
               Field("other_field", &Foo::other_field, foo.other_field),
               Field("last_field", &Foo::last_field, foo.last_field));
}

```

### Validare il Valore Puntato da un Argomento Puntatore

Le funzioni C++ spesso accettano puntatori come argomenti. Si possono usare matcher come `IsNull()`, `NotNull()` e altri per avere una corrispondenza con un puntatore, ma cosa succede se ci si vuol accertare che il valore *puntato* dal puntatore, anziché il puntatore stesso, ha una certa proprietà? Ebbene, si può usare il matcher `Pointee(m)`.

`Pointee(m)` esegue il matching di un puntatore se e solo se `m` corrisponde al valore a cui punta il puntatore. Per esempio:

```cpp
using ::testing::Ge;
using ::testing::Pointee;
...
  EXPECT_CALL(foo, Bar(Pointee(Ge(3))));

```

si aspetta che `foo.Bar()` venga chiamato con un puntatore che punta a un valore maggiore o uguale a 3.

Una cosa bella di `Pointee()` è che tratta un puntatore `NULL` come una corrispondenza fallita, quindi si può scrivere `Pointee(m)` anziché

```cpp
using ::testing::AllOf;
using ::testing::NotNull;
using ::testing::Pointee;
...
  AllOf(NotNull(), Pointee(m))

```

senza preoccuparsi che un puntatore `NULL` mandi in crash il test.

Inoltre, abbiamo detto che `Pointee()` funziona sia con puntatori [raw] **sia con**
puntatori smart (`std::unique_ptr`, `std::shared_ptr`, ecc.)?

Cosa succede se si ha un puntatore a puntatore? Indovinato - si può usare `Pointee()` nidificato 'scavare' più a fondo il valore. Per esempio, `Pointee(Pointee(Lt(3)))` è il match di un puntatore che punta a un puntatore che punta a un numero inferiore a 3 (che salti...).

### Definizione di una Classe Matcher Custom {#CustomMatcherClass}

La maggior parte dei matcher può essere definita semplicemente utilizzando [le macro MATCHER*](#NewMatchers), che sono concise e flessibili e producono buoni messaggi di errore. Tuttavia, queste macro non sono molto esplicite riguardo alle interfacce che creano e non sono sempre adatte, soprattutto per i matcher che verranno ampiamente riutilizzati.

Per i casi più avanzati, potrebbe essere necessario definire la propria classe matcher. Un matcher custom consente di testare una proprietà invariante specifica di quell'oggetto. Vediamo come farlo.

Immaginiamo di avere una funzione mock che accetta un oggetto di tipo `Foo`, che ha un metodo `int bar()` e un metodo `int baz()`. Si vuol vincolare il fatto che il valore dell'argomento di `bar()` più il valore del suo `baz()` sia un certo numero. (Questo è un invariante). Ecco come possiamo scrivere e utilizzare una classe matcher per farlo:

```cpp
class BarPlusBazEqMatcher {
 public:
  using is_gtest_matcher = void;

  explicit BarPlusBazEqMatcher(int expected_sum)
      : expected_sum_(expected_sum) {}
  bool MatchAndExplain(const Foo& foo,
                       std::ostream* /* listener */) const {
    return (foo.bar() + foo.baz()) == expected_sum_;
  }

  void DescribeTo(std::ostream* os) const {
    *os << "bar() + baz() equals " << expected_sum_;
  }

  void DescribeNegationTo(std::ostream* os) const {
    *os << "bar() + baz() does not equal " << expected_sum_;
  }

 private:
  const int expected_sum_;
};
::testing::Matcher<const Foo&> BarPlusBazEq(int expected_sum) {
  return BarPlusBazEqMatcher(expected_sum);
}
...
  Foo foo;
  EXPECT_THAT(foo, BarPlusBazEq(5))...;

```

### Il Matching dei Contenitori

A volte un container STL (ad esempio lista, vettore, mappa, ...) viene passato a una funzione mock e lo si vorrebbe convalidare. Poiché la maggior parte dei container STL supportano l'operatore `==`, si può scrivere `Eq(expected_container)` o semplicemente `expected_container` per verificare esattamente un container.

A volte, però, si necessita di una maggiore flessibilità (ad esempio, il primo elemento deve corrispondere esattamente, ma il secondo elemento può essere qualsiasi numero positivo e così via). Inoltre, i container utilizzati nei test hanno spesso un numero limitato di elementi e doverli definire [out-of-line] è un po' complicato.

In questi casi si può utilizzare il matcher `ElementsAre()` o `UnorderedElementsAre()`:

```cpp
using ::testing::_;
using ::testing::ElementsAre;
using ::testing::Gt;
...
  MOCK_METHOD(void, Foo, (const vector<int>& numbers), (override));
...
  EXPECT_CALL(mock, Foo(ElementsAre(1, Gt(0), _, 5)));

```

Il matcher sopra dice che il container deve avere 4 elementi, che devono essere rispettivamente 1, maggiore di 0, qualsiasi cosa e 5.

Se invece si scrive:

```cpp
using ::testing::_;
using ::testing::Gt;
using ::testing::UnorderedElementsAre;
...
  MOCK_METHOD(void, Foo, (const vector<int>& numbers), (override));
...
  EXPECT_CALL(mock, Foo(UnorderedElementsAre(1, Gt(0), _, 5)));

```

Significa che il container deve avere 4 elementi, che (con qualche permutazione) devono essere rispettivamente 1, maggiore di 0, qualsiasi cosa e 5.

In alternativa si possono inserire gli argomenti in un array in stile C e utilizzare invece `ElementsAreArray()` o `UnorderedElementsAreArray()`:

```cpp
using ::testing::ElementsAreArray;
...
  // ElementsAreArray accetta un array di elementi valori.
  const int expected_vector1[] = {1, 5, 2, 4, ...};
  EXPECT_CALL(mock, Foo(ElementsAreArray(expected_vector1)));
  // Oppure un array di elementi di matcher.
  Matcher<int> expected_vector2[] = {1, Gt(2), _, 3, ...};
  EXPECT_CALL(mock, Foo(ElementsAreArray(expected_vector2)));

```

Nel caso in cui l'array debba essere creato dinamicamente (e quindi la dimensione dell'array non possa essere dedotta dal compilatore), si può fornire a `ElementsAreArray()` un argomento aggiuntivo per specificare la dimensione dell'array:

```cpp
using ::testing::ElementsAreArray;
...
  int* const expected_vector3 = new int[count];
  ... fill expected_vector3 with values ...
  EXPECT_CALL(mock, Foo(ElementsAreArray(expected_vector3, count)));

```

Si usa `Pair` quando si confrontano mappe o altri container associativi.

{% raw %}

```cpp
using ::testing::UnorderedElementsAre;
using ::testing::Pair;
...
  absl::flat_hash_map<string, int> m = {{"a", 1}, {"b", 2}, {"c", 3}};
  EXPECT_THAT(m, UnorderedElementsAre(
      Pair("a", 1), Pair("b", 2), Pair("c", 3)));

```

{% endraw %}


**Suggerimenti:**

*   `ElementsAre*()` can be used to match *any* container that implements the
    STL iterator pattern (i.e. it has a `const_iterator` type and supports
`begin()/end()`), not just the ones defined in STL. It will even work with
    container types yet to be written - as long as they follows the above
    pattern.
*   You can use nested `ElementsAre*()` to match nested (multi-dimensional)
    containers.
*   Se il container viene passato tramite puntatore anziché per riferimento, si scrive semplicemente `Pointee(ElementsAre*(...))`.
*   L'ordine degli elementi *è importante* per `ElementsAre*()`. If you are using it
    with containers whose element order are undefined (such as a
`std::unordered_map`) you should use `UnorderedElementsAre`.

### Matcher Condivisi

Internamente, un oggetto matcher gMock è costituito da un puntatore a un oggetto di implementazione con conteggio dei riferimenti. La copia dei matcher è consentita ed è molto efficiente, poiché viene copiato solo il puntatore. Quando l'ultimo matcher che fa riferimento all'oggetto di implementazione muore, l'oggetto di implementazione verrà eliminato.

Pertanto, se si ha un matcher complesso che si vuole utilizzare più e più volte, non è necessario crearlo ogni volta. Basta assegnarlo a una variabile matcher e utilizzare quella variabile ripetutamente! Per esempio,

```cpp
using ::testing::AllOf;
using ::testing::Gt;
using ::testing::Le;
using ::testing::Matcher;
...
  Matcher<int> in_range = AllOf(Gt(5), Le(10));
  ... usare in_range come matcher nelle EXPECT_CALL multiple...

```

### I matcher non devono avere effetti collaterali {#PureMatchers}

{: .callout .warning}
ATTENZIONE: gMock non garantisce quando o quante volte un matcher verrà invocato. Pertanto, tutti i matcher devono essere *puramente funzionali*: non possono avere effetti collaterali e il risultato della corrispondenza non deve dipendere da nient'altro che dai parametri del matcher e dal valore da abbinare.

Questo requisito deve essere soddisfatto indipendentemente da come viene definito un matcher (ad esempio, se è uno dei matcher standard o un matcher personalizzato). In particolare, un matcher non può mai chiamare una funzione mock, poiché ciò influenzerà lo stato dell'oggetto mock e di gMock.

## Impostare le Expectation

### Quando usare Expect {#UseOnCall}

**`ON_CALL`** è probabilmente il *costrutto singolo più sotto-utilizzato* in gMock.

Esistono fondamentalmente due costrutti per definire il comportamento di un oggetto mock: `ON_CALL` e `EXPECT_CALL`. La differenza? `ON_CALL` defines what happens when
a mock method is called, but <em>doesn't imply any expectation on the method
being called</em>. `EXPECT_CALL` not only defines the behavior, but also sets an
expectation that <em>the method will be called with the given arguments, for the
given number of times</em> (and *in the given order* when you specify the order
too).

Dato che `EXPECT_CALL` fa di più, non è meglio di `ON_CALL`? Non proprio. Ogni `EXPECT_CALL` aggiunge un vincolo sul comportamento del codice sotto test. Avere più vincoli del necessario è *una pessima idea* - anche peggio che non avere abbastanza vincoli.

Questo potrebbe essere controintuitivo. Come potrebbero i test che verificano di più essere peggiori dei test che verificano di meno? La verifica non è il punto centrale dei test?

La risposta sta in *cosa* dovrebbe verificare un test. **Un buon test verifica il contratto del codice.** Se un test specifica eccessivamente, non lascia abbastanza libertà all'implementazione. Di conseguenza, modificare l'implementazione senza infrangere il contratto (ad esempio refactoring e ottimizzazione), cosa che dovrebbe essere perfettamente consentita, può "rompere" tali test. Quindi si deve dedicare del tempo a risolverli, solo per vederli rotti nuovamente la prossima volta che l'implementazione viene modificata.

Si tenga presente che non è necessario verificare più di una proprietà in un test.
In effetti, **è buona norma stilistica verificare solo una cosa in un test.** Se lo si fa, un bug probabilmente romperà solo uno o due test invece di dozzine (nel qual caso si vorrebbe eseguire il debug?). Se si ha anche l'abitudine di dare ai test nomi descrittivi che indichino ciò che verificano, spesso si può facilmente indovinare cosa c'è che non va solo dal log.

Quindi usare `ON_CALL` per default e usare `EXPECT_CALL` solo quando si intende effettivamente verificare che la chiamata sia stata effettuata. Ad esempio, si potrebbero avere un sacco di `ON_CALL` nella fixture di test per impostare il comportamento comune del mock condiviso da tutti i test nello stesso gruppo e scrivere (appena) diversi `EXPECT_CALL` in diversi `TEST_F` per verificare diversi aspetti del comportamento del codice. Rispetto allo stile in cui ogni `TEST` ha molte `EXPECT_CALL`, questo porta a test più resilienti alle modifiche implementative (e quindi con meno probabilità di richiedere manutenzione) e rende l'intento dei test più ovvi (quindi sono più facili da manutenere).

Se infastidisce dal messaggio "Uninteresting mock function call" stampato quando viene chiamato un metodo mock senza una `EXPECT_CALL`, si può usare invece un `NiceMock` per sopprimere tutti questi messaggi per l'oggetto mock, o per sopprimere il messaggio per metodi specifici aggiungendo `EXPECT_CALL(...).Times(AnyNumber())`. NON sopprimerlo aggiungendo ciecamente un `EXPECT_CALL(...)`altrimenti il test sarà difficile da manutenere.

### Ignorare le Chiamate [Uninteresting]

Se non si è interessati a come viene chiamato un metodo mock, basta non dire nulla al riguardo. In questo caso, se il metodo viene chiamato, gMock eseguirà la sua azione di default per consentire al programma di test di continuare. Se non si è soddisfatti dell'azione di default intrapresa da gMock, la si può sovrascrivere utilizzando `DefaultValue<T>::Set()` (descritto [qui](#DefaultValue)) o `ON_CALL()`.

Si tenga presente che una volta espresso interesse per un particolare metodo mock (tramite `EXPECT_CALL()`), tutte le invocazioni ad esso devono corrispondere a qualche expectation. Se questa funzione viene chiamata ma gli argomenti non corrispondono ad alcuna istruzione `EXPECT_CALL()`, sarà un errore.

### Evitare Chiamate [Unexpected]

Se un metodo mock non deve essere affatto chiamato, lo si dica esplicitamente:

```cpp
using ::testing::_;
...
  EXPECT_CALL(foo, Bar(_))
      .Times(0);

```

Se alcune chiamate al metodo sono consentite, ma le altre no, elencare semplicemente tutte le chiamate previste:

```cpp
using ::testing::AnyNumber;
using ::testing::Gt;
...
  EXPECT_CALL(foo, Bar(5));
  EXPECT_CALL(foo, Bar(Gt(10)))
      .Times(AnyNumber());

```

Una chiamata a `foo.Bar()` che non corrisponde a nessuna delle istruzioni `EXPECT_CALL()` sarà un errore.

### Le Chiamate Poco Interessanti e Quelle Unexpected {#uninteresting-vs-unexpected}

Le chiamate *uninteresting* e quelle *unexpected* sono concetti diversi in gMock.
*Molto* diversi.

Una chiamata `x.Y(...)` è **uninteresting** se non è impostata *nemmeno una singola* `EXPECT_CALL(x, Y(...))`. In altre parole, il test non è affatto interessato al metodo `x.Y()`, come è evidente dal fatto che al test non interessa dire nulla al riguardo.

Una chiamata `x.Y(...)` è **unexpected** se è impostata *qualche* `EXPECT_CALL(x, Y(...))`, ma nessuna di esse corrisponde [match] alla chiamata. In altre parole, il test è interessato al metodo `x.Y()` (quindi imposta esplicitamente alcune `EXPECT_CALL` per verificare come viene chiamato); tuttavia, la verifica fallisce poiché il test non prevede [expect] che si verifichi questa particolare chiamata.

**Una chiamata unexpected è sempre un errore**, poiché il codice sottoposto a test non si comporta come il test si aspetta che si comporti.

**Per default, una chiamata uninteresting non è un errore**, poiché non viola alcun vincolo specificato dal test. (La filosofia di gMock è che non dire nulla significa che non ci sono vincoli). Tuttavia, porta a un warning, poiché *potrebbe* indicare un problema (ad esempio l'autore del test potrebbe aver dimenticato di specificare un vincolo).

In gMock, `NiceMock` e `StrictMock` possono essere utilizzati per rendere una classe mock "acondiscendente" [nice] o "rigorosa" [strict]. In che modo ciò influisce sulle chiamate uninteresting e le unexpected?

Un **nice mock** sopprime i *warning* sulle chiamate uninteresting. È meno loquace del mock di default, ma per il resto è lo stesso. Se un test fallisce con un mock di default, fallirà anche utilizzando un mock "nice". E viceversa. Non ci si aspetti che rendere un mock "nice" possa cambiare il risultato del test.

Un **mock strict** trasforma i warning sulle chiamate uninteresting in errori. Quindi rendere un mock strict può cambiare il risultato del test.

Diamo un'occhiata ad un esempio:

```cpp
TEST(...) {
  NiceMock<MockDomainRegistry> mock_registry;
  EXPECT_CALL(mock_registry, GetDomainOwner("google.com"))
          .WillRepeatedly(Return("Larry Page"));

  // Usare mock_registry nel codice da testare.
  ... &mock_registry ...
}

```

L'unico `EXPECT_CALL` qui dice che tutte le chiamate a `GetDomainOwner()` devono avere `"google.com"` come argomento. Se viene chiamata `GetDomainOwner("yahoo.com")`, si tratterà di una chiamata inaspettata [unexpected] e quindi di un errore. *Avere un mock nice non cambia la gravità di una chiamata unexpected.*

Allora come diciamo a gMock che `GetDomainOwner()` può essere chiamato anche con altri argomenti? La tecnica standard consiste nell'aggiungere un "acchiappa-tutto" `EXPECT_CALL`:

```cpp
  EXPECT_CALL(mock_registry, GetDomainOwner(_))
        .Times(AnyNumber());  // catches all other calls to this method.
  EXPECT_CALL(mock_registry, GetDomainOwner("google.com"))
        .WillRepeatedly(Return("Larry Page"));

```

Da tener presente che `_` è il carattere jolly che corrisponde a "qualsiasi cosa". Con questo, se viene chiamato `GetDomainOwner("google.com")`, farà ciò che dice il secondo `EXPECT_CALL`; se viene chiamato con un argomento diverso, farà quello che dice il primo `EXPECT_CALL`.

Notare che l'ordine dei due `EXPECT_CALL` è importante, poiché un `EXPECT_CALL` più recente ha la precedenza su quello precedente.

Per ulteriori informazioni su chiamate uninteresting, mock nice e mock strict, leggere ["Nice, Strict e Naggy"](#NiceStrictNaggy).

### Ignorare gli Argomenti Non Interessanti {#ParameterlessExpectations}

Se il test non si preoccupa dei parametri (si preoccupa solo del numero o dell'ordine delle chiamate), spesso si può semplicemente omettere l'elenco dei parametri:

```cpp
  // Si aspetta foo.Bar( ... ) due volte con qualsiasi argomento.
  EXPECT_CALL(foo, Bar).Times(2);
  // Delega al metodo specificato ogni volta che viene invocata la factory.
  ON_CALL(foo_factory, MakeFoo)
      .WillByDefault(&BuildFooForTest);

```

Questa funzionalità è disponibile solo quando un metodo non è overloaded; per evitare comportamenti imprevisti, tentare di impostare un'aspettativa [expectation] su un metodo in cui l'overload specifico è ambiguo costituisce un errore di compilazione. Il problema si può aggirare fornendo una [interfaccia più semplice del mock](#SimplerInterfaces) rispetto a quella fornita dalla classe mock-ata.

Questo pattern è utile anche quando gli argomenti sono interessanti, ma la logica della corrispondenza [match] è sostanzialmente complessa. Si può lasciare l'elenco degli argomenti non specificato e utilizzare le azioni SaveArg per [salvare i valori per una successiva verifica](#SaveArgVerify). Facendolo, si può facilmente distinguere la chiamata al metodo per il numero sbagliato di volte dalla chiamata con gli argomenti sbagliati.

### Expect di Chiamate Ordinate {#OrderedCalls}

Sebbene un'istruzione `EXPECT_CALL()` definita successivamente abbia la precedenza quando gMock tenta di far corrispondere [to match] una chiamata di funzione con una expectation, per default le chiamate non devono avvenire nell'ordine con cui sono scritte le istruzioni `EXPECT_CALL()`. Ad esempio, se gli argomenti corrispondono ai matcher nella seconda `EXPECT_CALL()`, ma non a quelli nella prima o nella terza, allora verrà utilizzata la seconda expectation.

Se si preferisce che tutte le chiamate avvengano nell'ordine previsto, inserire le istruzioni `EXPECT_CALL()` in un blocco in cui si definisce una variabile di tipo `InSequence`:

```cpp
using ::testing::_;
using ::testing::InSequence;
  {
    InSequence s;
    EXPECT_CALL(foo, DoThis(5));
    EXPECT_CALL(bar, DoThat(_))
        .Times(2);
    EXPECT_CALL(foo, DoThis(6));
  }

```

In questo esempio, ci aspettiamo una chiamata a `foo.DoThis(5)`, seguita da due chiamate a `bar.DoThat()` dove l'argomento può essere qualsiasi cosa, che sono a turno seguito da una chiamata a `foo.DoThis(6)`. Se una chiamata è avvenuta fuori ordine, gMock segnalerà un errore.

### Expecting Chiamate Parzialmente Ordinate {#PartialOrder}

A volte richiedere che tutto avvenga in un ordine predeterminato può portare a test fragili. Ad esempio, potremmo preoccuparci che `A` si presenti prima sia di `B` e `C`, ma non siamo interessati all'ordine relativo di `B` e `C`. In questo caso, il test dovrebbe riflettere il nostro reale intento, invece di essere eccessivamente vincolante.

gMock consente di imporre un DAG (directed acyclic graph) arbitrario sulle chiamate. Un modo per esprimere il DAG è utilizzare la [clausola  `After`](reference/mocking.md#EXPECT_CALL.After) di `EXPECT_CALL`.

Un altro modo è tramite la clausola `InSequence()` (diversa dalla classe `InSequence`), che abbiamo preso in prestito da jMock 2. È meno flessibile di `After()`, ma più conveniente quando si hanno lunghe catene di chiamate sequenziali, poiché non richiede di trovare nomi diversi per le expectation nelle catene.
Ecco come funziona:

Se consideriamo le istruzioni `EXPECT_CALL()` come nodi in un grafo e aggiungiamo un arco dal nodo A al nodo B ovunque A debba trovarsi prima di B, possiamo ottenere un DAG. Usiamo il termine "sequenza" per indicare un percorso diretto in questo DAG. Ora, se scomponiamo il DAG in sequenze, dobbiamo solo sapere a quali sequenze appartiene ciascuna `EXPECT_CALL()` per poter ricostruire il DAG originale.

Quindi, per specificare l'ordine parziale sulle expectation dobbiamo fare due cose: prima definire degli oggetti `Sequence`, e poi per ciascuna `EXPECT_CALL()` dire si quale oggetto `Sequence` fa parte.

Le expectation nella stessa sequenza devono verificarsi nell'ordine in cui sono scritte. Per esempio,

```cpp
using ::testing::Sequence;
...
  Sequence s1, s2;
  EXPECT_CALL(foo, A())
      .InSequence(s1, s2);
  EXPECT_CALL(bar, B())
      .InSequence(s1);
  EXPECT_CALL(bar, C())
      .InSequence(s2);

  EXPECT_CALL(foo, D())
      .InSequence(s2);

```

specifica il seguente DAG (dove `s1` è `A -> B` e `s2` è `A -> C -> D`):

```text
       +---> B
       |
  A ---|
       |
       +---> C ---> D

```

Ciò significa che A deve verificarsi prima di B e C, e C deve verificarsi prima di D. Non ci sono restrizioni sull'ordine diverso da questi.

### Controllare Quando una Expectation viene Ritirata

Quando viene chiamato un metodo mock, gMock considera solo le expectation ancora attive. Una expectation è attiva quando viene creata e diventa inattiva (ovvero *ritirata*) quando si verifica una chiamata che deve avvenire in seguito. Ad esempio, in

```cpp
using ::testing::_;
using ::testing::Sequence;
...
  Sequence s1, s2;
  EXPECT_CALL(log, Log(WARNING, _, "File too large."))      // #1
      .Times(AnyNumber())
      .InSequence(s1, s2);
  EXPECT_CALL(log, Log(WARNING, _, "Data set is empty."))   // #2
      .InSequence(s1);
  EXPECT_CALL(log, Log(WARNING, _, "User not found."))      // #3
      .InSequence(s2);

```

non appena il #2 o il #3 verranno abbinati [match], il #1 verrà ritirato. Se successivamente viene loggato un warning `"File too large."`, si tratterà di un errore.

Notare che una expectation viene ritirata automaticamente quando è saturata. Per esempio,

```cpp
using ::testing::_;
...
  EXPECT_CALL(log, Log(WARNING, _, _));                     // #1
  EXPECT_CALL(log, Log(WARNING, _, "File too large."));     // #2

```

dice che ci sarà esattamente un warning con il messaggio`"File too large."`. Se anche il secondo warning contiene questo messaggio, #2 corrisponderà [match] nuovamente e genererà un errore di violazione del limite superiore [upper-bound-violated].

Se questo non è quello che si desidera, si può a chiedere una expectation ritirarsi non appena diventa satura:

```cpp
using ::testing::_;
...
  EXPECT_CALL(log, Log(WARNING, _, _));                     // #1
  EXPECT_CALL(log, Log(WARNING, _, "File too large."))      // #2
      .RetiresOnSaturation();

```

Qui #2 può essere utilizzato solo una volta, quindi se si hanno due warning con il messaggio `"File too large."`, il primo corrisponderà [match] a #2 e il secondo corrisponderà a #1: non ci sarà errore.

## Usare le Action

### Restituire Riferimenti dai Metodi Mock

Se il tipo di ritorno di una funzione mock è un riferimento, si deve usare `ReturnRef()` anziché `Return()` per restituire un risultato:

```cpp
using ::testing::ReturnRef;
class MockFoo : public Foo {
 public:
  MOCK_METHOD(Bar&, GetBar, (), (override));
};
...
  MockFoo foo;
  Bar bar;
  EXPECT_CALL(foo, GetBar())
      .WillOnce(ReturnRef(bar));
...

```

### Restituire Valori Live dai Metodi Mock

L'azione `Return(x)` salva una copia di `x` quando l'azione viene creata e restituisce sempre lo stesso valore ogni volta che viene eseguita. A volte si vorrebbe restituire invece il valore *live* di `x` (ovvero il suo valore nel momento in cui l'azione viene *eseguita*.). Si usa o`ReturnRef()` oppure `ReturnPointee()` per questo.

Se il tipo restituito dalla funzione mock è un riferimento, lo si può fare utilizzando `ReturnRef(x)`, come mostrato nella ricetta precedente ("Restituire Riferimenti dai Metodi Mock"). Tuttavia, gMock non consente di utilizzare `ReturnRef()` in una funzione mock il cui tipo restituito non è un riferimento, poiché ciò di solito indica un errore dell'utente. Allora, cosa si farà?

Anche se si potrebbe essere tentati, NON USARE `std::ref()`:

```cpp
using ::testing::Return;
class MockFoo : public Foo {
 public:
  MOCK_METHOD(int, GetValue, (), (override));
};
...
  int x = 0;
  MockFoo foo;
  EXPECT_CALL(foo, GetValue())
      .WillRepeatedly(Return(std::ref(x)));  // Sbagliato!
  x = 42;
  EXPECT_EQ(foo.GetValue(), 42);

```

Sfortunatamente, qui non funziona. Il codice precedente fallirà con errore:

```text
Value of: foo.GetValue()
  Actual: 0
Expected: 42

```

Il motivo è che `Return(*value*)` converte `value` nel tipo restituito effettivo della funzione mock nel momento in cui l'azione viene *creata*, non quando viene *eseguita*. (Questo comportamento è stato scelto perché l'azione fosse sicura quando `value` è un oggetto proxy che fa riferimento ad alcuni oggetti temporanei). Di conseguenza, `std::ref(x)` è convertito in un valore `int` (anziché un `const int&`) quando la expectation è impostata e `Return(std::ref(x))` restituirà sempre 0.

`ReturnPointee(pointer)` è stato fornito per risolvere specificamente questo problema. Restituisce il valore puntato da `pointer` nel momento in cui l'azione viene *eseguita*:

```cpp
using ::testing::ReturnPointee;
...
  int x = 0;
  MockFoo foo;
  EXPECT_CALL(foo, GetValue())
      .WillRepeatedly(ReturnPointee(&x));  // Notare qui la &.
  x = 42;
  EXPECT_EQ(foo.GetValue(), 42);  // This will succeed now.

```

### Combinazione di Azioni

Si vuol fare più di una cosa quando viene chiamata una funzione? Va bene. `DoAll()` consente di eseguire una sequenza di azioni ogni volta. Verrà utilizzato solo il valore restituito dell'ultima azione nella sequenza.

```cpp
using ::testing::_;
using ::testing::DoAll;
class MockFoo : public Foo {
 public:
  MOCK_METHOD(bool, Bar, (int n), (override));
};
...
  EXPECT_CALL(foo, Bar(_))
      .WillOnce(DoAll(action_1,
                      action_2,
                      ...
                      action_n));

```

Il valore restituito dell'ultima azione **deve** corrispondere al tipo restituito del metodo mock-ato. Nell'esempio sopra, `action_n` potrebbe essere `Return(true)` o una lambda che restituisce un `bool`, ma non `SaveArg`, che restituisce `void`. Altrimenti la firma [signature] di `DoAll` non corrisponderebbe a quella prevista da `WillOnce`, che è la firma del metodo mock-ato, e non verrebbe compilato.

### Verifica di argomenti Complessi {#SaveArgVerify}

Per verificare che un metodo venga chiamato con un argomento particolare ma i criteri di corrispondenza [match] sono complessi, può essere difficile distinguere tra errori di cardinalità (chiamare il metodo il numero sbagliato di volte) e gli errori di corrispondenza [match] dell'argomento. Allo stesso modo, se si c'è il "match" di più parametri, potrebbe non essere facile distinguere quale argomento non è riuscito a corrispondere. Per esempio:

```cpp
  // Non ideale: potrebbe fallire a causa di un problema con arg1 o arg2, o forse
  // semplicemente il metodo non è stato chiamato.
  EXPECT_CALL(foo, SendValues(_, ElementsAre(1, 4, 4, 7), EqualsProto( ... )));

```

Si possono invece salvare gli argomenti e testarli individualmente:

```cpp
  EXPECT_CALL(foo, SendValues)
      .WillOnce(DoAll(SaveArg<1>(&actual_array), SaveArg<2>(&actual_proto)));
  ... run the test
  EXPECT_THAT(actual_array, ElementsAre(1, 4, 4, 7));
  EXPECT_THAT(actual_proto, EqualsProto( ... ));

```

### Effetti Collaterali dei Mock {#MockingSideEffects}

A volte un metodo mostra il suo effetto non restituendo un valore ma tramite degli effetti collaterali. Ad esempio, potrebbe modificare alcuni stati globali o modificare un argomento di output. Per mock-are gli oggetti collaterali, in generale si può definire la propria azione implementando `::testing::ActionInterface`.

Se tutto ciò che si deve fare è modificare un argomento di output, conviene la "action" nativa `SetArgPointee()`:

```cpp
using ::testing::_;
using ::testing::SetArgPointee;
class MockMutator : public Mutator {
 public:
  MOCK_METHOD(void, Mutate, (bool mutate, int* value), (override));
  ...
}
...
  MockMutator mutator;
  EXPECT_CALL(mutator, Mutate(true, _))
      .WillOnce(SetArgPointee<1>(5));

```

In questo esempio, quando viene chiamato `mutator.Mutate()`, assegneremo 5 alla variabile `int` puntata dall'argomento #1 (in base 0).

`SetArgPointee()` crea comodamente una copia interna del valore che gli si passa, eliminando la necessità di mantenere il valore nello scope e in vita [alive]. L'implicazione tuttavia è che il valore deve avere un costruttore di copia e un operatore di assegnazione.

Se anche il metodo mock deve restituire un valore, si può concatenare `SetArgPointee()` con `Return()` usando `DoAll()`, ricordando di mettere l'istruzione `Return()` in ultimo:

```cpp
using ::testing::_;
using ::testing::DoAll;
using ::testing::Return;
using ::testing::SetArgPointee;
class MockMutator : public Mutator {
 public:
  ...
  MOCK_METHOD(bool, MutateInt, (int* value), (override));
}
...
  MockMutator mutator;
  EXPECT_CALL(mutator, MutateInt(_))
      .WillOnce(DoAll(SetArgPointee<0>(5),
                      Return(true)));

```

Notare, tuttavia, che se si usa il metodo `ReturnOKWith()`, esso sovrascriverà [override] i valori forniti da `SetArgPointee()` nei parametri di risposta della chiamata di funzione.

Se l'argomento di output è un array, si usa invece l'azione `SetArrayArgument<N>(first, last)`. Questa copia gli elementi nell'intervallo di origine `[first, last)` nell'array puntato dall'argomento `N`-esimo (in base 0):

```cpp
using ::testing::NotNull;
using ::testing::SetArrayArgument;
class MockArrayMutator : public ArrayMutator {
 public:
  MOCK_METHOD(void, Mutate, (int* values, int num_values), (override));
  ...
}
...
  MockArrayMutator mutator;
  int values[5] = {1, 2, 3, 4, 5};
  EXPECT_CALL(mutator, Mutate(NotNull(), 5))
      .WillOnce(SetArrayArgument<0>(values, values + 5));

```

Funziona anche quando l'argomento è un iteratore di output:

```cpp
using ::testing::_;
using ::testing::SetArrayArgument;
class MockRolodex : public Rolodex {
 public:
  MOCK_METHOD(void, GetNames, (std::back_insert_iterator<vector<string>>),
              (override));
  ...
}
...
  MockRolodex rolodex;
  vector<string> names = {"George", "John", "Thomas"};
  EXPECT_CALL(rolodex, GetNames(_))
      .WillOnce(SetArrayArgument<0>(names.begin(), names.end()));

```

### Modifica del Comportamento di un Oggetto Mock in Base allo Stato

Se si prevede che una chiamata modifichi il comportamento di un oggetto mock, si può usare `::testing::InSequence` per specificare comportamenti diversi prima e dopo la chiamata:

```cpp
using ::testing::InSequence;
using ::testing::Return;
...
  {
     InSequence seq;
     EXPECT_CALL(my_mock, IsDirty())
         .WillRepeatedly(Return(true));
     EXPECT_CALL(my_mock, Flush());
     EXPECT_CALL(my_mock, IsDirty())
         .WillRepeatedly(Return(false));
  }

  my_mock.FlushIfDirty();

```

Questo fa sì che `my_mock.IsDirty()` restituisca `true` prima che `my_mock.Flush()` venga chiamato e restituisca `false` successivamente.

Se la modifica del comportamento è più complessa, se ne possono memorizzare gli effetti in una variabile e fare in modo che un metodo mock ottenga il valore restituito da quella variabile:

```cpp
using ::testing::_;
using ::testing::SaveArg;
using ::testing::Return;
ACTION_P(ReturnPointee, p) { return *p; }
...
  int previous_value = 0;
  EXPECT_CALL(my_mock, GetPrevValue)
      .WillRepeatedly(ReturnPointee(&previous_value));
  EXPECT_CALL(my_mock, UpdateValue)
      .WillRepeatedly(SaveArg<0>(&previous_value));
  my_mock.DoSomethingToUpdateValue();

```

Qui `my_mock.GetPrevValue()` restituirà sempre l'argomento dell'ultima chiamata `UpdateValue()`.

### Impostazione del Valore di Default per un Tipo Restituito {#DefaultValue}

Se il tipo restituito di un metodo mock è un tipo o puntatore C++ nativo, per default restituirà 0 quando richiamato. Inoltre, in C++ 11 e versioni successive, un metodo mock il cui tipo restituito ha un costruttore di default, restituirà di default un valore costruito per default. Si deve solo specificare un'azione se questo valore di default non corrisponde alle proprie esigenze.

A volte, si vuole modificare questo valore di default o specificare un valore di default per i tipi di cui gMock non è a conoscenza. Lo si può fare utilizzando la classe template `::testing::DefaultValue`:

```cpp
using ::testing::DefaultValue;
class MockFoo : public Foo {
 public:
  MOCK_METHOD(Bar, CalculateBar, (), (override));
};
...
  Bar default_bar;
  // Imposta il valore restituito di default per il tipo Bar.
  DefaultValue<Bar>::Set(default_bar);
  MockFoo foo;
  // Non è necessario specificare un'azione qui, poiché per noi
  // funziona il valore restituito di default.
  EXPECT_CALL(foo, CalculateBar());
  foo.CalculateBar();  // Questo dovrebbe restituire default_bar.
  // Annulla l'impostazione del valore restituito di default.
  DefaultValue<Bar>::Clear();

```

Notare che la modifica del valore di default per un tipo può rendere difficile la comprensione dei test. Consigliamo di utilizzare questa funzione con giudizio. Ad esempio, per assicurarsi che le chiamate `Set()` e `Clear()` siano proprio accanto al codice che utilizza il mock.

### Impostazione delle Azioni di Default per un Metodo Mock

Abbiamo imparato come modificare il valore di default di un determinato tipo. Tuttavia, questo potrebbe essere troppo grossolano per i propri scopi: forse ci sono due metodi mock con lo stesso tipo di ritorno e si vuole che abbiano comportamenti diversi. La macro `ON_CALL()` consente di personalizzare il comportamento del mock a livello del metodo:

```cpp
using ::testing::_;
using ::testing::AnyNumber;
using ::testing::Gt;
using ::testing::Return;
...
  ON_CALL(foo, Sign(_))
      .WillByDefault(Return(-1));
  ON_CALL(foo, Sign(0))
      .WillByDefault(Return(0));
  ON_CALL(foo, Sign(Gt(0)))
      .WillByDefault(Return(1));
  EXPECT_CALL(foo, Sign(_))
      .Times(AnyNumber());

  foo.Sign(5);   // Questo dovrebbe restituire 1.
  foo.Sign(-9);  // Questo dovrebbe restituire -1.
  foo.Sign(0);   // Questo dovrebbe restituire 0.

```

Come intuito, quando ci sono più istruzioni `ON_CALL()`, quelle più recenti nell'ordine hanno la precedenza su quelle più vecchie. In altre parole, verrà utilizzato l'**ultimo** che corrisponde agli argomenti della funzione. Questo ordine di corrispondenza consente di impostare il comportamento comune nel costruttore di un oggetto mock o nella fase di impostazione della fixture e di specializzare il comportamento del mock in seguito.

Notare che sia `ON_CALL` che `EXPECT_CALL` hanno la stessa regola "le istruzioni successive hanno la precedenza", ma non interagiscono. Cioè, le `EXPECT_CALL` hanno il proprio ordine di precedenza distinto da quello di `ON_CALL`.

### Utilizzo di Funzioni/Metodi/Funtori/Lambda come Azioni {#FunctionsAsActions}

Se le azioni native non soddisfano, si può utilizzare un chiamabile [callable] esistente (funzione, `std::function`, metodo, funtore, lambda) come azione.

```cpp
using ::testing::_; using ::testing::Invoke;
class MockFoo : public Foo {
 public:
  MOCK_METHOD(int, Sum, (int x, int y), (override));
  MOCK_METHOD(bool, ComplexJob, (int x), (override));
};
int CalculateSum(int x, int y) { return x + y; }
int Sum3(int x, int y, int z) { return x + y + z; }
class Helper {
 public:
  bool ComplexJob(int x);
};
...
  MockFoo foo;
  Helper helper;
  EXPECT_CALL(foo, Sum(_, _))
      .WillOnce(&CalculateSum)
      .WillRepeatedly(Invoke(NewPermanentCallback(Sum3, 1)));
  EXPECT_CALL(foo, ComplexJob(_))
      .WillOnce(Invoke(&helper, &Helper::ComplexJob))
      .WillOnce([] { return true; })
      .WillRepeatedly([](int x) { return x > 0; });
  foo.Sum(5, 6);         // Invoca CalculateSum(5, 6).
  foo.Sum(2, 3);         // Invoca Sum3(1, 2, 3).
  foo.ComplexJob(10);    // Invoca helper.ComplexJob(10).
  foo.ComplexJob(-1);    // Invoca la lambda inline.

```

L'unico requisito è che il tipo della funzione, ecc. deve essere *compatibile* con la firma della funzione mock, il che significa che gli argomenti di quest'ultima (se ne accetta qualcuno) possono essere convertiti implicitamente negli argomenti corrispondenti del primo e il tipo restituito del primo possono essere convertiti implicitamente in quello del secondo. Quindi, si può invocare qualcosa il cui tipo *non* sia esattamente lo stesso della funzione mock, purché sia sicuro farlo: bello, eh?

Notare che:

*   The action takes ownership of the callback and will delete it when the
    action itself is destructed.
*   If the type of a callback is derived from a base callback type `C`, you need
    to implicitly cast it to `C` to resolve the overloading, e.g.

    ```cpp
    using ::testing::Invoke;
    ...
      ResultCallback<bool>* is_ok = ...;
      ... Invoke(is_ok) ...;  // Questo funziona.
      BlockingClosure* done = new BlockingClosure;
      ... Invoke(implicit_cast<Closure*>(done)) ...;  // Il cast è necessario.
    
    ```

### Uso di Funzioni con Informazioni Extra come Azioni

La funzione o il funtore che si chiama utilizzando `Invoke()` deve avere lo stesso numero di argomenti della funzione mock per cui la si usa. A volte si potrebbe avere una funzione che accetta più argomenti e si è disposti a passare manualmente gli argomenti extra per colmare il divario. In gMock lo si può fare utilizzando le callback con argomenti pre-associati [pre-bound]. Ecco un esempio:

```cpp
using ::testing::Invoke;
class MockFoo : public Foo {
 public:
  MOCK_METHOD(char, DoThis, (int n), (override));
};
char SignOfSum(int x, int y) {
  const int sum = x + y;
  return (sum > 0) ? '+' : (sum < 0) ? '-' : '0';
}
TEST_F(FooTest, Test) {
  MockFoo foo;
  EXPECT_CALL(foo, DoThis(2))
      .WillOnce(Invoke(NewPermanentCallback(SignOfSum, 5)));
  EXPECT_EQ(foo.DoThis(2), '+');  // Invokes SignOfSum(5, 2).
}

```

### Invcare una Funzione/Metodo/Funtore/Lambda/Callback Senza Argomenti

`Invoke()` passa gli argomenti della funzione mock alla funzione, ecc. invocata in modo tale che il chiamato abbia l'intero contesto della chiamata con cui lavorare. Se la funzione invocata non è interessata ad alcuni o a tutti gli argomenti, può semplicemente ignorarli.

Tuttavia, un pattern comune è che l'autore di un test desidera invocare una funzione senza gli argomenti della funzione mock. Potrebbe farlo utilizzando una funzione wrapper che elimina gli argomenti prima di invocare una [nullary function].
Inutile dire che questo può essere noioso e oscurare lo scopo del test.

Ci sono due soluzioni a questo problema. Innanzitutto, si può passare qualsiasi "callable" di zero arg come azione. In alternativa, si usa `InvokeWithoutArgs()`, che è come `Invoke()` tranne per il fatto che non passa gli argomenti della funzione fittizia al chiamato. Ecco un esempio di ciascuno:

```cpp
using ::testing::_;
using ::testing::InvokeWithoutArgs;
class MockFoo : public Foo {
 public:
  MOCK_METHOD(bool, ComplexJob, (int n), (override));
};
bool Job1() { ... }
bool Job2(int n, char c) { ... }
...
  MockFoo foo;
  EXPECT_CALL(foo, ComplexJob(_))
      .WillOnce([] { Job1(); });
      .WillOnce(InvokeWithoutArgs(NewPermanentCallback(Job2, 5, 'a')));
  foo.ComplexJob(10);  // Invoca Job1().
  foo.ComplexJob(20);  // Invoca Job2(5, 'a').

```

Notare che:

*   The action takes ownership of the callback and will delete it when the
    action itself is destructed.
*   If the type of a callback is derived from a base callback type `C`, you need
    to implicitly cast it to `C` to resolve the overloading, e.g.

    ```cpp
    using ::testing::InvokeWithoutArgs;
    ...
      ResultCallback<bool>* is_ok = ...;
      ... InvokeWithoutArgs(is_ok) ...;  // Questo funziona.
      BlockingClosure* done = ...;
      ... InvokeWithoutArgs(implicit_cast<Closure*>(done)) ...;
      // Il cast è necessario.
    
    ```

### Invocare un Argomento della Funzione Mock

A volte una funzione mock riceverà un puntatore a funzione, un funtore (in altre parole, un "callable") come argomento, ad es.

```cpp
class MockFoo : public Foo {
 public:
  MOCK_METHOD(bool, DoThis, (int n, (ResultCallback1<bool, int>* callback)),
              (override));
};

```

e si potrebbe invocare questo argomento richiamabile:

```cpp
using ::testing::_;
...
  MockFoo foo;
  EXPECT_CALL(foo, DoThis(_, _))
      .WillOnce(...);
      // Eseguirà callback->Run(5), dove callback è il
      // secondo argomento che riceve DoThis().

```

{: .callout .note}
NOTA: La sezione seguente è la documentazione di prima che il C++ avesse le lambda:

Arghh, si deve fare riferimento a un argomento di funzione mock ma il C++ non ha (ancora) le lambda, quindi si deve definire la propria azione. :-( Oh! veramente?

Beh, gMock ha un'azione per risolvere *esattamente* questo problema:

```cpp
InvokeArgument<N>(arg_1, arg_2, ..., arg_m)

```

invocherà l'`N`-esimo (0-based) argomento ricevuto dalla funzione mock, con `arg_1`, `arg_2`, ..., e `arg_m`. Non importa se l'argomento è un puntatore a funzione, un funtore o una callback. gMock li gestisce tutti.

Con ciò, si potrebbe scrivere:

```cpp
using ::testing::_;
using ::testing::InvokeArgument;
...
  EXPECT_CALL(foo, DoThis(_, _))
      .WillOnce(InvokeArgument<1>(5));
      // Eseguirà callback->Run(5), dove callback è il
      // secondo argomento che riceve DoThis().

```

Cosa succede se il "callable" accetta un argomento per riferimento? Nessun problema: basta racchiuderlo all'interno di `std::ref()`:

```cpp
  ...
  MOCK_METHOD(bool, Bar,
              ((ResultCallback2<bool, int, const Helper&>* callback)),
              (override));
  ...
  using ::testing::_;
  using ::testing::InvokeArgument;
  ...
  MockFoo foo;
  Helper helper;
  ...
  EXPECT_CALL(foo, Bar(_))
      .WillOnce(InvokeArgument<0>(5, std::ref(helper)));
      // std::ref(helper) garantisce che al callback verrà passato un riferimento all'helper,
      // non una sua copia.

```

Cosa succede se il callable accetta un argomento per riferimento e **non** racchiudiamo l'argomento in `std::ref()`? In questo caso `InvokeArgument()` *creerà una copia* dell'argomento e passerà un *riferimento alla copia*, invece di un riferimento al valore originale, al richiamabile. Ciò è particolarmente utile quando l'argomento è un valore temporaneo:

```cpp
  ...
  MOCK_METHOD(bool, DoThat, (bool (*f)(const double& x, const string& s)),
              (override));
  ...
  using ::testing::_;
  using ::testing::InvokeArgument;
  ...
  MockFoo foo;
  ...
  EXPECT_CALL(foo, DoThat(_))
      .WillOnce(InvokeArgument<0>(5.0, string("Hi")));
      // Eseguirà (*f)(5.0, string("Hi")), dove f è il puntatore alla funzione
      // DoThat() riceve.
  Notare che i valori 5.0 e string("Hi") sono
      // temporanei e inattivi una volta terminata l'istruzione EXPECT_CALL().  Tuttavia
      // va bene eseguire questa azione in un secondo momento, poiché una copia dei valori
      // viene conservata all'interno dell'azione InvokeArgument.

```

### Ignorare un Risultato di un'Azione

A volte si ha un'azione che restituisce *qualcosa*, ma c'è bisogno di un'azione che restituisca `void` (forse per usarla in una funzione mock che restituisca `void`, o forse deve essere utilizzato in `DoAll()` e non è l'ultimo della lista). `IgnoreResult()` consente di farlo. Per esempio:

```cpp
using ::testing::_;
using ::testing::DoAll;
using ::testing::IgnoreResult;
using ::testing::Return;
int Process(const MyData& data);
string DoSomething();
class MockFoo : public Foo {
 public:
  MOCK_METHOD(void, Abc, (const MyData& data), (override));
  MOCK_METHOD(bool, Xyz, (), (override));
};
  ...
  MockFoo foo;
  EXPECT_CALL(foo, Abc(_))
      // .WillOnce(Invoke(Process));
      // La riga precedente non verrà compilata poiché Process() restituisce int ma Abc()
      // deve restituire void.
      .WillOnce(IgnoreResult(Process));
  EXPECT_CALL(foo, Xyz())
      .WillOnce(DoAll(IgnoreResult(DoSomething),
                      // Ignora la stringa restituita da DoSomething().
                      Return(true)));

```

Notare che **non si può** usare `IgnoreResult()` su un'azione che restituisce già `void`. Ciò porterà a brutti errori del compilatore.

### Selezionare gli Argomenti di un'Azione {#SelectingArgs}

Supponiamo che si abbia una funzione mock `Foo()` che accetta sette argomenti e che si abbia un'azione personalizzata che da invocare quando viene chiamata `Foo()`. Il problema è che l'azione personalizzata richiede solo tre argomenti:

```cpp
using ::testing::_;
using ::testing::Invoke;
...
  MOCK_METHOD(bool, Foo,
              (bool visible, const string& name, int x, int y,
               (const map<pair<int, int>>), double& weight, double min_weight,
               double max_wight));
...
bool IsVisibleInQuadrant1(bool visible, int x, int y) {
  return visible && x >= 0 && y >= 0;
}
...
  EXPECT_CALL(mock, Foo)
      .WillOnce(Invoke(IsVisibleInQuadrant1));  // Uh, non verrà compilato. :-(

```

Per compiacere il dio del compilatore, si deve definire un "adaptor" che abbia la stessa firma di `Foo()` e si chiama l'azione personalizzata con gli argomenti giusti:

```cpp
using ::testing::_;
using ::testing::Invoke;
...
bool MyIsVisibleInQuadrant1(bool visible, const string& name, int x, int y,
                            const map<pair<int, int>, double>& weight,
                            double min_weight, double max_wight) {
  return IsVisibleInQuadrant1(visible, x, y);
}
...
  EXPECT_CALL(mock, Foo)
      .WillOnce(Invoke(MyIsVisibleInQuadrant1));  // Ora funziona.

```

Ma non è imbarazzante?

gMock fornisce un *action adaptor* generico, così ci si può dedicare agli affari più importanti piuttosto che scrivere i propri adaptor. Ecco la sintassi:

```cpp
WithArgs<N1, N2, ..., Nk>(action)

```

crea un'azione che passa gli argomenti della funzione mock agli indici dati (in base 0) all'`action` interna e la esegue. Utilizzando `WithArgs`, l'esempio originale può essere scritto come:

```cpp
using ::testing::_;
using ::testing::Invoke;
using ::testing::WithArgs;
...
  EXPECT_CALL(mock, Foo)
      .WillOnce(WithArgs<0, 2, 3>(Invoke(IsVisibleInQuadrant1)));  // Non è necessario definire il proprio adaptor.

```

Per una migliore leggibilità, gMock offre anche:

*   `WithoutArgs(action)` quando l'`action` interna accetta *nessun* argomento, e
*   `WithArg<N>(action)` (nessuna `s` dopo `Arg`) quando l'`action` interna prende *un* argomento.

Si comprenderà che `InvokeWithoutArgs(...)` è solo zucchero sintattico per `WithoutArgs(Invoke(...))`.

Ecco ulteriori suggerimenti:

*   L'azione interna utilizzata in `WithArgs` e simili non deve essere necessariamente `Invoke()`: può essere qualsiasi cosa.
*   Se necessario è possibile ripetere un argomento nell'elenco, ad es. `WithArgs<2, 3, 3, 5>(...)`.
*   Si può cambiare l'ordine degli argomenti, p.es. `WithArgs<3, 2, 1>(...)`.
*   The types of the selected arguments do *not* have to match the signature of
    the inner action exactly. It works as long as they can be implicitly
    converted to the corresponding arguments of the inner action. Per esempio,
    if the 4-th argument of the mock function is an `int` and `my_action` takes
    a `double`, `WithArg<4>(my_action)` will work.

### Ignorare gli Argomenti nella Funzioni Azioni

La ricetta [selecting-an-action's-arguments](#SelectingArgs) ci ha mostrato un modo per far combaciare una funzione mock e un'azione con elenchi di argomenti incompatibili. Lo svantaggio è che racchiudere l'azione in `WithArgs<...>()` può diventare noioso per le persone che scrivono i test.

Se si sta definendo una funzione (o metodo, funtore, lambda, callback) da utilizzare con `Invoke*()` e non si è interessati ad alcuni dei suoi argomenti, un'alternativa a `WithArgs` consiste nel dichiarare gli argomenti non interessanti come `Unused`.
Ciò rende la definizione meno confusa e meno fragile nel caso in cui cambino i tipi di argomenti poco interessanti. Potrebbe anche aumentare la possibilità che la funzione dell'azione possa essere riutilizzata. Per esempio, dato

```cpp
 public:
  MOCK_METHOD(double, Foo, double(const string& label, double x, double y),
              (override));
  MOCK_METHOD(double, Bar, (int index, double x, double y), (override));

```

invece di

```cpp
using ::testing::_;
using ::testing::Invoke;
double DistanceToOriginWithLabel(const string& label, double x, double y) {
  return sqrt(x*x + y*y);
}
double DistanceToOriginWithIndex(int index, double x, double y) {
  return sqrt(x*x + y*y);
}
...
  EXPECT_CALL(mock, Foo("abc", _, _))
      .WillOnce(Invoke(DistanceToOriginWithLabel));
  EXPECT_CALL(mock, Bar(5, _, _))
      .WillOnce(Invoke(DistanceToOriginWithIndex));

```

si può scrivere

```cpp
using ::testing::_;
using ::testing::Invoke;
using ::testing::Unused;
double DistanceToOrigin(Unused, double x, double y) {
  return sqrt(x*x + y*y);
}
...
  EXPECT_CALL(mock, Foo("abc", _, _))
      .WillOnce(Invoke(DistanceToOrigin));

  EXPECT_CALL(mock, Bar(5, _, _))
      .WillOnce(Invoke(DistanceToOrigin));

```

### Condivisione di Azioni

Proprio come i matcher, un oggetto azione gMock è costituito da un puntatore a un oggetto di implementazione con conteggio dei riferimenti. Pertanto anche le azioni di copia sono consentite e molto efficienti. Quando l'ultima azione che fa riferimento all'oggetto di implementazione muore, l'oggetto di implementazione verrà eliminato.

Se si ha un'azione complessa che da utilizzare più e più volte, si potrebbe non doverla creare da zero ogni volta. Se l'azione non ha uno stato interno (cioè se fa sempre la stessa cosa indipendentemente da quante volte è stata chiamata), si può assegnarla a una variabile di azione e utilizzare quella variabile ripetutamente. Per esempio:

```cpp
using ::testing::Action;
using ::testing::DoAll;
using ::testing::Return;
using ::testing::SetArgPointee;
...
  Action<bool(int*)> set_flag = DoAll(SetArgPointee<0>(5),
                                      Return(true));
  ... use set_flag in .WillOnce() and .WillRepeatedly() ...

```

Tuttavia, se l'azione ha un proprio stato, si potrebbe rimanere sorpresi se si condivide l'oggetto dell'azione. Supponiamo di avere una action factory `IncrementCounter(init)` che crea un'azione che incrementa e restituisce un contatore il cui valore iniziale è `init`, utilizzando due azioni create dalla stessa espressione e utilizzando un'azione condivisa mostrerà comportamenti diversi. Esempio:

```cpp
  EXPECT_CALL(foo, DoThis())
      .WillRepeatedly(IncrementCounter(0));
  EXPECT_CALL(foo, DoThat())
      .WillRepeatedly(IncrementCounter(0));
  foo.DoThis();  // Restituisce 1.
  foo.DoThis();  // Restituisce 2.
  foo.DoThat();  // Restituisce 1 - DoThat() usa un contatore
                 // diversa da quello di DoThis().

```

contro

```cpp
using ::testing::Action;
...
  Action<int()> increment = IncrementCounter(0);
  EXPECT_CALL(foo, DoThis())
      .WillRepeatedly(increment);
  EXPECT_CALL(foo, DoThat())
      .WillRepeatedly(increment);
  foo.DoThis();  // Restituisce 1.
  foo.DoThis();  // Restituisce 2.
  foo.DoThat();  // Restituisce 3 - il contatore è condiviso.

```

### Testare il Comportamento Asincrono

Un problema spesso riscontrato con gMock è che può essere difficile testare il comportamento asincrono. Supponiamo di avere una classe `EventQueue` da testare e che sia stata creata un'interfaccia `EventDispatcher` separata in modo da poterla facilmente renderla mock. Tuttavia, l'implementazione della classe ha attivato tutti gli eventi su un thread in background, rendendo difficile la tempistica dei test. Si potrebbero semplicemente inserire le istruzioni `sleep()` e sperare per il meglio, ma ciò rende il comportamento del test non deterministico. Un modo migliore è quello di utilizzare le azioni gMock e gli oggetti `Notification` per forzare il test asincrono a comportarsi in modo sincrono.

```cpp
class MockEventDispatcher : public EventDispatcher {
  MOCK_METHOD(bool, DispatchEvent, (int32), (override));
};
TEST(EventQueueTest, EnqueueEventTest) {
  MockEventDispatcher mock_event_dispatcher;
  EventQueue event_queue(&mock_event_dispatcher);
  const int32 kEventId = 321;
  absl::Notification done;
  EXPECT_CALL(mock_event_dispatcher, DispatchEvent(kEventId))
      .WillOnce([&done] { done.Notify(); });
  event_queue.EnqueueEvent(kEventId);
  done.WaitForNotification();
}

```

Nell'esempio sopra, impostiamo le nostre normali expectation gMock, ma poi aggiungiamo un'azione aggiuntiva per notificare l'oggetto `Notification`. Ora possiamo semplicemente chiamare `Notification::WaitForNotification()` nel thread principale per attendere il completamento della chiamata asincrona. Successivamente, la nostra suite di test è completa e possiamo uscire in sicurezza.

{: .callout .note}
Nota: questo esempio ha uno svantaggio: ovvero, se la expectation non viene soddisfatta, il test verrà eseguito all'infinito. Alla fine andrà in timeout e fallirà, ma richiederà più tempo e sarà leggermente più difficile eseguire il debug. Per alleviare questo problema, si può utilizzare `WaitForNotificationWithTimeout(ms)` invece di `WaitForNotification()`.

## Ricette Varie sull'Uso di gMock

### Mock di Metodi Che Usano Tipi Move-Only

Il C++11 ha introdotto i *tipi move-only* (tipi di solo spostamento). Un valore "move-only-typed" può essere spostato da un oggetto a un altro, ma non può essere copiato. `std::unique_ptr<T>` è probabilmente il tipo di solo spostamento [move-only] più comunemente utilizzato.

Il mock di un metodo che accetta e/o restituisce tipi move-only presenta alcune sfide, ma nulla di insormontabile. Questa ricetta mostra come lo si può fare.
Notare che il supporto per gli argomenti move-only di metodi è stato introdotto in gMock solo nell'aprile 2017; nel codice più vecchio si trovano dei [workaround](#LegacyMoveOnly) più complessi per la mancanza di questa funzionalità.

Diciamo che stiamo lavorando a un progetto immaginario che consente di pubblicare e condividere frammenti chiamati “buzzes”. Il codice utilizza questi tipi:

```cpp
enum class AccessLevel { kInternal, kPublic };
class Buzz {
 public:
  explicit Buzz(AccessLevel access) { ... }
  ...
};
class Buzzer {
 public:
  virtual ~Buzzer() {}
  virtual std::unique_ptr<Buzz> MakeBuzz(StringPiece text) = 0;
  virtual bool ShareBuzz(std::unique_ptr<Buzz> buzz, int64_t timestamp) = 0;
  ...
};

```

Un oggetto `Buzz` rappresenta un frammento [snippet] pubblicato. Una classe che implementa l'interfaccia `Buzzer` è in grado di creare e condividere dei `Buzz`. I metodi in `Buzzer` possono restituire un `unique_ptr<Buzz>` o ricevere un `unique_ptr<Buzz>`. Ora dobbiamo mock-are `Buzzer` nei nostri test.

Per il mock di un metodo che accetta o restituisce tipi move-only, si usa semplicemente la familiare sintassi `MOCK_METHOD`:

```cpp
class MockBuzzer : public Buzzer {
 public:
  MOCK_METHOD(std::unique_ptr<Buzz>, MakeBuzz, (StringPiece text), (override));
  MOCK_METHOD(bool, ShareBuzz, (std::unique_ptr<Buzz> buzz, int64_t timestamp),
              (override));
};

```

Ora che abbiamo definito la classe mock, possiamo usarla nei test. Nei seguenti esempi di codice, assumiamo di aver definito un oggetto `MockBuzzer` chiamato `mock_buzzer_`:

```cpp
  MockBuzzer mock_buzzer_;

```

Per prima cosa vediamo come possiamo impostare le expectation sul metodo `MakeBuzz()`, che restituisce un `unique_ptr<Buzz>`.

Come al solito, se si imposta una expectation senza un'azione (ad esempio la clausola `.WillOnce()` o la `.WillRepeatedly()`), quando si attiva la expectation, l'azione di default per quel metodo verrà intrapresa. Poiché `unique_ptr<>` ha un costruttore di default che restituisce un `unique_ptr` nullo, questo è ciò che si ottiene se non si specifica un'azione:

```cpp
using ::testing::IsNull;
...
  // Usa la action di default.
  EXPECT_CALL(mock_buzzer_, MakeBuzz("hello"));
  // Attiva la EXPECT_CALL precedente.
  EXPECT_THAT(mock_buzzer_.MakeBuzz("hello"), IsNull());

```

Se non si è soddisfatti dell'azione di default, la si può modificare come al solito; vedere [Impostazione delle Azioni di Default](#OnCall).

Se c'è solo da restituire un valore move-only, lo si può usare in combinazione con `WillOnce`. Per esempio:

```cpp
  EXPECT_CALL(mock_buzzer_, MakeBuzz("hello"))
      .WillOnce(Return(std::make_unique<Buzz>(AccessLevel::kInternal)));
  EXPECT_NE(nullptr, mock_buzzer_.MakeBuzz("hello"));

```

Tempo di quiz! Cosa accadrà se un'azione `Return` viene eseguita più di una volta (ad esempio scrivendo `... .WillRepeatedly(Return(std::move(...)));`)? Rifletteteci, dopo la prima volta che viene eseguita l'azione, il valore sorgente verrà consumato (poiché è un valore di solo spostamento [move-only]), quindi la volta successiva, non c'è alcun valore da spostare - si otterrà un errore a run-time secondo cui `Return(std::move(...))` può essere eseguito solo una volta.

Se c'è bisogno che il metodo mock faccia qualcosa di più del semplice spostamento di un valore di default, ricordarsi che si può sempre utilizzare un oggetto lambda o un richiamabile [callable], che può fare praticamente tutto:

```cpp
  EXPECT_CALL(mock_buzzer_, MakeBuzz("x"))
      .WillRepeatedly([](StringPiece text) {
        return std::make_unique<Buzz>(AccessLevel::kInternal);
      });

  EXPECT_NE(nullptr, mock_buzzer_.MakeBuzz("x"));

  EXPECT_NE(nullptr, mock_buzzer_.MakeBuzz("x"));

```

Ogni volta che questa `EXPECT_CALL` si attiva, verrà creato e restituito un nuovo `unique_ptr<Buzz>`. Non lo si può fare con `Return(std::make_unique<...>(...))`.

Ciò riguarda la restituzione di valori move-only; ma come lavoriamo con metodi che accettano argomenti move-only? La risposta è che funzionano normalmente, anche se alcune azioni non verranno compilate quando uno qualsiasi degli argomenti del metodo è move-only. Si può sempre usare `Return`, o una [lambda o un funtore](#FunctionsAsActions):

```cpp
  using ::testing::Unused;
  EXPECT_CALL(mock_buzzer_, ShareBuzz(NotNull(), _)).WillOnce(Return(true));
  EXPECT_TRUE(mock_buzzer_.ShareBuzz(std::make_unique<Buzz>(AccessLevel::kInternal)),
              0);
  EXPECT_CALL(mock_buzzer_, ShareBuzz(_, _)).WillOnce(
      [](std::unique_ptr<Buzz> buzz, Unused) { return buzz != nullptr; });
  EXPECT_FALSE(mock_buzzer_.ShareBuzz(nullptr, 0));

```

Molte azioni native (`WithArgs`, `WithoutArgs`,`DeleteArg`, `SaveArg`, ...) potrebbero in linea di principio supportare argomenti move-only, ma il supporto per questo non è ancora implementato. Se questo è bloccante, segnalare un bug.

Alcune azioni (ad esempio `DoAll`) copiano i loro argomenti internamente, quindi non possono mai funzionare con oggetti non copiabili; si dovranno usare invece i funtori.

#### Workarounds legacy per i tipi move-only {#LegacyMoveOnly}

Il supporto per gli argomenti move-only di funzioni è stato introdotto in gMock solo nell'aprile del 2017. Nel codice precedente, si potrebbe riscontrare la seguente soluzione alternativa per la mancanza di questa funzionalità (non è più necessaria: la includiamo solo come riferimento):

```cpp
class MockBuzzer : public Buzzer {
 public:
  MOCK_METHOD(bool, DoShareBuzz, (Buzz* buzz, Time timestamp));
  bool ShareBuzz(std::unique_ptr<Buzz> buzz, Time timestamp) override {
    return DoShareBuzz(buzz.get(), timestamp);
  }
};

```

Il trucco sta nel delegare il metodo `ShareBuzz()` a un metodo mock (chiamiamolo `DoShareBuzz()`) che non accetta parametri move-only. Poi, invece di impostare le expectation su `ShareBuzz()`, si impostano su l metodo mock `DoShareBuzz()`:

```cpp
  MockBuzzer mock_buzzer_;

  EXPECT_CALL(mock_buzzer_, DoShareBuzz(NotNull(), _));
  // Quando si chiama ShareBuzz() su MockBuzzer in questo modo, la
  // chiamata viene inoltrata a DoShareBuzz(), che viene mock-ato.  Pertanto questa istruzione
  // attiverà la precedente EXPECT_CALL.
  mock_buzzer_.ShareBuzz(std::make_unique<Buzz>(AccessLevel::kInternal), 0);

```

### Velocizzare la Compilazione

Che ci si creda o meno, la *stragrande maggioranza* del tempo impiegato nella compilazione di una classe mock è nella generazione del suo costruttore e del distruttore, poiché eseguono compiti non banali (ad esempio la verifica delle expectation). Inoltre, i metodi mock con firme diverse hanno tipi diversi e quindi i loro costruttori/distruttori devono essere generati separatamente dal compilatore. Di conseguenza, se ci sono molti tipi diversi di metodi mock, la compilazione della classe mock può diventare molto lenta.

Se si riscontra una compilazione lenta, si può spostare la definizione del costruttore e del distruttore della classe mock fuori dal corpo della classe e in un file `.cc`. In questo modo, anche se si `#include` la classe mock in N file, il compilatore dovrà generare il suo costruttore e distruttore solo una volta, ne risulterà una compilazione molto più veloce.

Illustriamo l'idea con un esempio. Ecco la definizione di una classe mock prima di applicare questa ricetta:

```cpp
// File mock_foo.h.
...
class MockFoo : public Foo {
 public:
  // Dato che non dichiariamo né il costruttore né il distruttore,
  // il compilatore li genererà in ogni unità di traduzione
  // in cui viene utilizzata questa classe mock.
  MOCK_METHOD(int, DoThis, (), (override));
  MOCK_METHOD(bool, DoThat, (const char* str), (override));
  ... altri metodi mock ...
};

```

Dopo la modifica, sarebbe simile a:

```cpp
// File mock_foo.h.
...
class MockFoo : public Foo {
 public:
  // Il costruttore e il distruttore sono dichiarati, ma non definiti, qui.
  MockFoo();
  virtual ~MockFoo();
  MOCK_METHOD(int, DoThis, (), (override));
  MOCK_METHOD(bool, DoThat, (const char* str), (override));
  ... altri metodi mock ...
};

```

e

```cpp
// File mock_foo.cc.
#include "path/to/mock_foo.h"
// The definitions may appear trivial, but the functions actually do a
// lot of things through the constructors/destructors of the member
// variables used to implement the mock methods.
MockFoo::MockFoo() {}
MockFoo::~MockFoo() {}

```

### Forzare una Verifica

Quando verrà distrutto, l'oggetto mock verificherà automaticamente che tutte le sue expectation siano state soddisfatte e, in caso contrario, genererà errori di googletest. Questo è conveniente perché lascia con una cosa in meno di cui preoccuparsi. Cioè, a meno che non si sia sicuri che l'oggetto mock verrà distrutto.

Come è possibile che l'oggetto mock alla fine non venga distrutto? Ebbene, potrebbe essere creato nell'heap e posseduto [own] dal codice che si sta testando Supponiamo che ci sia un bug in quel codice e che non si effettui correttamente il delete dell'oggetto mock: si potrebbe finire con un test positivo quando in realtà c'è un bug.

L'utilizzo di un "heap checker" è una buona idea e può alleviare i problemi, ma la sua implementazione non è affidabile al 100%. Quindi, a volte si vuole *forzare* gMock a verificare un oggetto mock prima che venga (si spera) distrutto. Lo si può fare con `Mock::VerifyAndClearExpectations(&mock_object)`:

```cpp
TEST(MyServerTest, ProcessesRequest) {
  using ::testing::Mock;
  MockFoo* const foo = new MockFoo;
  EXPECT_CALL(*foo, ...)...;
  // ... altre expectation ...
  // il server ora possiede foo.
  MyServer server(foo);
  server.ProcessRequest(...);
  // Nel caso in cui il distruttore di quel server si dimentichi il delete di foo,
  // questo verificherà comunque le expectation.
  Mock::VerifyAndClearExpectations(foo);
}  // qui il server viene distrutto quando esce dallo scope.

```

{: .callout .tip}
**Tip:** La funzione `Mock::VerifyAndClearExpectations()` restituisce un `bool` per indicare se la verifica ha avuto esito positivo (`true` per sì), quindi si può racchiudere la chiamata alla funzione all'interno di `ASSERT_TRUE()` se non ha senso andare oltre in caso quando la verifica non è riuscita.

Non stabilire nuove expectation dopo aver verificato e ripulito un mock dopo il suo utilizzo.
L'impostazione delle expectation dopo il codice che esercita il mock ha un comportamento indefinito.
Vedere [Uso dei Mock nei Test](gmock_for_dummies.md#using-mocks-in-tests) per ulteriori informazioni.

### Uso dei Checkpoint {#UsingCheckPoints}

A volte si deve testare il comportamento di un oggetto mock in fasi le cui dimensioni sono gestibili, oppure si devono impostare expectation più dettagliate su quali chiamate API richiamano quali funzioni mock.

Una tecnica utilizzabile è quella di mettere le expectation in una sequenza e inserire chiamate a una funzione fittizia di "checkpoint" in punti specifici. Poi si può verificare che le chiamate alle funzioni mock avvengano al momento giusto. Ad esempio, per testare il codice:

```cpp
  Foo(1);
  Foo(2);
  Foo(3);

```

e per verificare che `Foo(1)` e `Foo(3)` invochino entrambe `mock.Bar("a")`, ma che `Foo(2)` non invoca nulla, si può scrivere:

```cpp
using ::testing::MockFunction;
TEST(FooTest, InvokesBarCorrectly) {
  MyMock mock;
  // La classe MockFunction<F> ha esattamente un metodo mock.  È chiamato
  // Call() e ha il tipo F.
  MockFunction<void(string check_point_name)> check;
  {
    InSequence s;
    EXPECT_CALL(mock, Bar("a"));
    EXPECT_CALL(check, Call("1"));
    EXPECT_CALL(check, Call("2"));
    EXPECT_CALL(mock, Bar("a"));
  }

  Foo(1);
  check.Call("1");
  Foo(2);
  check.Call("2");
  Foo(3);
}

```

La specifica della expectation dice che la prima chiamata `Bar("a")` deve avvenire prima del checkpoint "1", la seconda chiamata `Bar("a")` deve avvenire dopo il checkpoint "2", e tra i due checkpoint non dovrebbe succedere nulla. I checkpoint espliciti chiariscono quale `Bar("a")` viene chiamata da quale chiamata a `Foo()`.

### Mock dei Distruttori

A volte si vuol verificare che un oggetto mock venga distrutto al momento giusto, ad es. dopo la chiamata a `bar->A()` ma prima di chiamare `bar->B()`. Sappiamo già che è possibile specificare vincoli sull'[ordine](#OrderedCalls) delle chiamate alla funzione mock, quindi tutto ciò che dobbiamo fare è avere il mock del distruttore della funzione mock.

Sembra semplice, tranne che per un problema: un distruttore è una funzione speciale con una sintassi e una semantica speciali e la macro `MOCK_METHOD` non funziona per questo:

```cpp
MOCK_METHOD(void, ~MockFoo, ());  // Non compila!

```

La buona notizia è che si può usare un semplice pattern per ottenere lo stesso effetto.
Innanzitutto, si aggiunge una funzione mock `Die()` alla classe mock e la si chiama nel distruttore, in questo modo:

```cpp
class MockFoo : public Foo {
  ...
  // Si aggiungono le seguenti due righe alla classe mock.
  MOCK_METHOD(void, Die, ());
  ~MockFoo() override { Die(); }
};
```

(Se il nome `Die()` entra in conflitto con un simbolo esistente, si sceglie un altro nome). Ora, abbiamo tradotto il problema di testare quando un oggetto `MockFoo` muore nel testare quando viene chiamato il metodo `Die()`:

```cpp
  MockFoo* foo = new MockFoo;
  MockBar* bar = new MockBar;
  ...
  {
    InSequence s;
    // Si aspetta che *foo muoia dopo bar->A() e prima di bar->B().
    EXPECT_CALL(*bar, A());
    EXPECT_CALL(*foo, Die());
    EXPECT_CALL(*bar, B());
  }

```

E questo è tutto.

### Usare gMock e i Thread {#UsingThreads}

In una **unit** test, è meglio isolare e testare una parte di codice in un contesto a thread singolo. Ciò evita condizioni di "race" e "dead lock" e semplifica molto il debug del test.

Eppure la maggior parte dei programmi sono multi-thread e talvolta per testare qualcosa abbiamo bisogno di lavorarci sopra da più di un thread. gMock funziona anche per questo scopo.

Si ricordano i passaggi per utilizzare un mock:

1.  Si crea un oggetto mock `foo`.
2.  Se ne impostano le azioni e le expectation con `ON_CALL()` e con `EXPECT_CALL()`.
3.  Il codice da testare chiama i metodi di `foo`.
4.  Facoltativamente, verificare e reimpostare il mock.
5.  Distruggere il mock manualmente o lasciare che sia il codice sotto test a farlo. The
    destructor will automatically verify it.

Seguendo queste semplici regole, i mock e i thread possono convivere felicemente:

*   Execute your *test code* (as opposed to the code being tested) in *one*
    thread. Ciò facilita il test da eseguire.
*   Ovviamente si può fare il passo #1 senza il locking.
*   Quando si eseguono i passi #2 e #5, nessun altro thread deve accedere a `foo`.
    Anch'esso ovvio, huh?
*   #3 e #4 possono essere eseguiti in un thread o in più thread,
    comunque sia. gMock takes care of the locking, so you don't have to do any -
        unless required by your test logic.

Se si violano le regole (ad esempio, se si impostano le expectation su un mock mentre un altro thread ne chiama i metodi), si otterrà un comportamento indefinito. Questo non è bello, quindi non farlo.

gMock garantisce che l'azione per una funzione mock venga eseguita nello stesso thread che ha chiamato la funzione mock. Ad esempio, in

```cpp
  EXPECT_CALL(mock, Foo(1))
      .WillOnce(action1);
  EXPECT_CALL(mock, Foo(2))
      .WillOnce(action2);

```

se `Foo(1)` viene chiamato nel thread 1 e `Foo(2)` viene chiamato nel thread 2, gMock eseguirà `action1` nel thread 1 e `action2` nel thread 2.

gMock *non* impone una sequenza sulle azioni eseguite in thread diversi (farlo potrebbe creare situazioni di stallo poiché le azioni potrebbero dover cooperare). Ciò significa che l'esecuzione di `action1` e di `action2` nell'esempio precedente *può* interlacciarsi. Se questo è un problema, si deve aggiungere una logica di sincronizzazione adeguata ad `action1` e ad `action2` per rendere il test thread-safe.

Ricordarsi, inoltre, che `DefaultValue<T>` è una risorsa globale che potenzialmente influenza *tutti* gli oggetti mock attivi nel programma. Naturalmente, non ci si vorrà ingarbugliare con più thread o quando ci sono ancora mock in azione.

### Controllare la Quantità di Informazioni che Scrive gMock

Quando gMock vede qualcosa che potrebbe essere un errore (ad esempio viene chiamata una funzione mock senza una expectation, ovvero una chiamata poco interessante, che è consentita ma forse si è dimenticato di vietare esplicitamente la chiamata), stampa alcuni messaggi di warning, incluso gli argomenti della funzione, il valore restituito e il trace dello stack. Si spera che questo ricordi di dare un'occhiata e vedere se c'è davvero un problema.

A volte si è sicuri che i test siano corretti e si potrebbe non apprezzare messaggi così amichevoli. Altre volte, si sta eseguendo il debug dei test o si sta imparando il comportamento del codice in esame e si vorrebbe poter osservare ogni chiamata mock che avviene (inclusi i valori degli argomenti, il valore restituito e il trace dello stack). Chiaramente, una sola taglia non va bene per tutti.

Si può controllare quanto gMock stampa utilizzando il flag della riga di comando `--gmock_verbose=LEVEL`, dove `LEVEL` è una stringa con tre possibili valori:

*   `info`: gMock will print all informational messages, warnings, and errors
    (most verbose). Con questa impostazione, gMock loggerà anche tutte le chiamate alle macro `ON_CALL/EXPECT_CALL`. It will include a stack trace in
    "uninteresting call" warnings.
*   `warning`: gMock will print both warnings and errors (less verbose); it will
    omit the stack traces in "uninteresting call" warnings. Questo è il default.
*   `error`: gMock stamperà solo gli errori (i meno dettagliati).

In alternativa, si può aggiustare il valore del flag dai test in questo modo:

```cpp
  ::testing::FLAGS_gmock_verbose = "error";

```

Se si trova che gMock stampa troppi stack frame con i suoi messaggi informativi o di warning, se ne può controllare la quantità con il flag `--gtest_stack_trace_depth=max_depth`.

Ora, usare giudiziosamente il flag giusto per consentire a gMock di servire al meglio!

### Ottenere la Supervisione nelle Chiamate Mock

Abbiamo un test che usa gMock. Fallisce: gMock ti dice che alcune expectation non sono soddisfatte. Tuttavia, non si è sicuri del perché: c'è un errore di battitura da qualche parte nei matcher? È sbagliato l'ordine delle `EXPECT_CALL`? Oppure il codice sotto test sta facendo qualcosa di sbagliato? Come scoprirne la causa?

Non sarebbe bello se si avesse la vista a raggi X e si potessi effettivamente vedere la traccia di tutte le `EXPECT_CALL` e delle chiamate dei metodo mock mentre vengono effettuate? Per ogni chiamata, si potrebbero vedere i valori effettivi degli argomenti e a quale `EXPECT_CALL` gMock crede che corrisponda [match]? Se c'è ancora bisogno di aiuto per capire chi ha effettuato queste chiamate, potrebbe essere utile poter vedere lo stack trace completo ad ogni chiamata mock?

Si può sbloccare questo potere eseguendo il test con il flag `--gmock_verbose=info`. Ad esempio, dato il programma di test:

```cpp
#include <gmock/gmock.h>
using ::testing::_;
using ::testing::HasSubstr;
using ::testing::Return;
class MockFoo {
 public:
  MOCK_METHOD(void, F, (const string& x, const string& y));
};
TEST(Foo, Bar) {
  MockFoo mock;
  EXPECT_CALL(mock, F(_, _)).WillRepeatedly(Return());
  EXPECT_CALL(mock, F("a", "b"));
  EXPECT_CALL(mock, F("c", HasSubstr("d")));
  mock.F("a", "good");
  mock.F("a", "b");
}

```

se lo si esegue con `--gmock_verbose=info`, si vedrà questo output:

```shell
[ RUN       ] Foo.Bar
foo_test.cc:14: EXPECT_CALL(mock, F(_, _)) invoked
Stack trace: ...
foo_test.cc:15: EXPECT_CALL(mock, F("a", "b")) invoked
Stack trace: ...
foo_test.cc:16: EXPECT_CALL(mock, F("c", HasSubstr("d"))) invoked
Stack trace: ...
foo_test.cc:14: Mock function call matches EXPECT_CALL(mock, F(_, _))...
    Function call: F(@0x7fff7c8dad40"a",@0x7fff7c8dad10"good")
Stack trace: ...
foo_test.cc:15: Mock function call matches EXPECT_CALL(mock, F("a", "b"))...
    Function call: F(@0x7fff7c8dada0"a",@0x7fff7c8dad70"b")
Stack trace: ...
foo_test.cc:16: Failure
Actual function call count doesn't match EXPECT_CALL(mock, F("c", HasSubstr("d")))...
         Expected: to be called once
           Actual: never called - unsatisfied and active
[  FAILED  ] Foo.Bar

```

Supponiamo che il bug sia che la `"c"` nella terza `EXPECT_CALL` sia un errore di battitura e in realtà dovrebbe essere `"a"`. Col messaggio precedente, si vedrebbe che l'effettiva chiamata `F("a", "good")` corrisponde alla prima `EXPECT_CALL`, non alla terza come si pensava. Da ciò dovrebbe essere ovvio che il terzo `EXPECT_CALL` è scritto in modo errato. Caso risolto.

Se si è interessati alla call trace dei mock ma non a quelle dello stack, si può combinare `--gmock_verbose=info` con `--gtest_stack_trace_depth=0` sulla riga di comando del test.

### Esecuzione di Test in Emacs

Se si creano ed eseguono i test in Emacs utilizzando il comando `M-x google-compile` (come fanno molti utenti di googletest), le posizioni dei sorgenti di gMock e gli errori di googletest verranno evidenziati. Basta premere `<Enter>` su uno di essi e si verrà indirizzati alla riga incriminata. Oppure si può semplicemente digitare `C-x` per passare all'errore successivo.

Per semplificarlo ulteriormente, si possono aggiungere le seguenti righe al file `~/.emacs`:

```text
(global-set-key "\M-m"  'google-compile)  ; m is for make
(global-set-key [M-down] 'next-error)
(global-set-key [M-up]  '(lambda () (interactive) (next-error -1)))

```

Poi si può digitare `M-m` per avviare una build (se si vuole eseguire anche il test, assicurarsi solo che `foo_test.run` o `runtests` sia nel comando di compilazione fornito dopo aver digitato `M-m`), o `M-up`/`M-down` per spostarsi avanti e indietro tra gli errori.

## Estendere gMock

### Scrivere Rapidamente Nuovi Matcher {#NewMatchers}

{: .callout .warning}
ATTENZIONE: gMock non garantisce quando o quante volte un matcher verrà invocato. Pertanto, tutti i matcher devono essere funzionalmente puri. Consultare [questa sezione](#PureMatchers) per ulteriori dettagli.

La famiglia delle macro `MATCHER*` può essere utilizzata per definire facilmente dei matcher custom.
La sintassi:

```cpp
MATCHER(name, description_string_expression) { statements; }

```

definirà un matcher con il nome dato che esegue le istruzioni, che deve restituire un `bool` per indicare se la corrispondenza ha successo. All'interno delle istruzioni, si può fare riferimento al valore a cui corrisponde `arg` e fare riferimento al suo tipo tramite `arg_type`.

La *description string* è un'espressione di tipo `string` che documenta ciò che fa il matcher e viene utilizzata per generare il messaggio di errore quando la corrispondenza fallisce.
Può (e dovrebbe) fare riferimento alla variabile `bool` speciale `negation` e dovrebbe valutare la descrizione del matcher quando `negation` è `false`, o quello della negazione del matcher quando `negation` è `true`.

Per comodità, supponiamo che la stringa della descrizione sia vuota (`""`), nel qual caso gMock utilizzerà la sequenza di parole nel nome del matcher come descrizione.

Per esempio:

```cpp
MATCHER(IsDivisibleBy7, "") { return (arg % 7) == 0; }

```

consente di scrivere

```cpp
  // Expects mock_foo.Bar(n) to be called where n is divisible by 7.
  EXPECT_CALL(mock_foo, Bar(IsDivisibleBy7()));

```

o,

```cpp
  using ::testing::Not;
  ...
  // Verifica che un valore sia divisibile per 7 e l'altro no.
  EXPECT_THAT(some_expression, IsDivisibleBy7());
  EXPECT_THAT(some_other_expression, Not(IsDivisibleBy7()));

```

Se le affermazioni di cui sopra falliscono, stamperanno qualcosa come:

```shell
  Value of: some_expression
  Expected: is divisible by 7
    Actual: 27
  ...
  Value of: some_other_expression
  Expected: not (is divisible by 7)
    Actual: 21

```

dove le descrizioni `"is divisible by 7"` e `"not (is divisible by 7)"` vengono calcolate automaticamente dal nome del matcher `IsDivisibleBy7`.

Come notato, le descrizioni generate automaticamente (specialmente quelle per la negazione) potrebbero non essere così eccezionali. Si possono sempre sovrascriverle con un'espressione `string` a scelta:

```cpp
MATCHER(IsDivisibleBy7,
        absl::StrCat(negation ? "isn't" : "is", " divisible by 7")) {
  return (arg % 7) == 0;
}

```

Facoltativamente, si possono trasmettere informazioni aggiuntive a un argomento nascosto denominato `result_listener` per spiegare il risultato della corrispondenza [match]. Ad esempio, una definizione migliore di `IsDivisibleBy7` è:

```cpp
MATCHER(IsDivisibleBy7, "") {
  if ((arg % 7) == 0)
    return true;
  *result_listener << "the remainder is " << (arg % 7);
  return false;
}

```

Con questa definizione, l’affermazione di cui sopra darà un messaggio migliore:

```shell
  Value of: some_expression
  Expected: is divisible by 7
    Actual: 27 (the remainder is 6)

```

Si dovrebbe consentire a `MatchAndExplain()` di stampare *qualsiasi informazione aggiuntiva* che possa aiutare un utente a comprendere il risultato della corrispondenza [match]. Notare che dovrebbe spiegare perché la corrispondenza ha successo in caso di successo (a meno che non sia ovvio) - questo è utile quando il matcher viene utilizzato all'interno di `Not()`. Non è necessario stampare il valore dell'argomento stesso, poiché gMock lo stampa già.

{: .callout .note}
NOTA: Il il tipo del valore da abbinare [match] (`arg_type`) è determinato dal contesto in cui si usa il matcher e viene fornito dal compilatore, quindi non ci si deve preoccupare di dichiararlo (e nemmeno si può). Ciò consente al matcher di essere polimorfico. Ad esempio, `IsDivisibleBy7()` può essere utilizzato per corrispondere [match] a qualsiasi tipo in cui il valore di `(arg % 7) == 0` può essere convertito implicitamente in un `bool`. Nell'esempio `Bar(IsDivisibleBy7())` sopra, se il metodo `Bar()` accetta un `int`, `arg_type` sarà `int`; se richiede un `unsigned long`, `arg_type` sarà `unsigned long`; e così via.

### Scrivere Rapidamente Nuovi Matcher Parametrizzati

A volte servirà un matcher che abbia parametri. Per questo si può usare la macro:

```cpp
MATCHER_P(name, param_name, description_string) { statements; }

```

dove la description string può essere `""` o un'espressione `string` che fa riferimento a `negation` e a `param_name`.

Per esempio:

```cpp
MATCHER_P(HasAbsoluteValue, value, "") { return abs(arg) == value; }

```

consentirà di scrivere:

```cpp
  EXPECT_THAT(Blah("a"), HasAbsoluteValue(n));

```

che può portare a questo messaggio (assumendo che `n` sia 10):

```shell
  Value of: Blah("a")
  Expected: has absolute value 10
    Actual: -9

```

Notare che vengono stampati sia la descrizione del matcher che il suo parametro, rendendo il messaggio di facile comprensione.

Nel corpo della definizione del matcher, si può scrivere `foo_type` per fare riferimento al tipo di un parametro chiamato `foo`. Ad esempio, nel corpo di `MATCHER_P(HasAbsoluteValue, value)` sopra, si può scrivere `value_type` per fare riferimento al tipo di `value`.

gMock fornisce anche `MATCHER_P2`, `MATCHER_P3`, ..., fino a `MATCHER_P10` per supportare i matcher multiparametro:

```cpp
MATCHER_Pk(name, param_1, ..., param_k, description_string) { statements; }

```

Notare che la stringa di descrizione personalizzata è per una particolare *istanza* del matcher, in cui i parametri sono stati associati a valori effettivi. Pertanto di solito i valori dei parametri faranno parte della descrizione. gMock consente di farlo facendo riferimento ai parametri del matcher nell'espressione della stringa della descrizione.

Per esempio,

```cpp
using ::testing::PrintToString;
MATCHER_P2(InClosedRange, low, hi,
           absl::StrFormat("%s in range [%s, %s]", negation ? "isn't" : "is",
                           PrintToString(low), PrintToString(hi))) {
  return low <= arg && arg <= hi;
}
...
EXPECT_THAT(3, InClosedRange(4, 6));

```

genererebbe un errore che contiene il messaggio:

```shell
  Expected: is in range [4, 6]

```

Specificando `""` come descrizione, il messaggio di errore conterrà la sequenza di parole nel nome del matcher seguita dai valori dei parametri stampati come una tupla. Per esempio,

```cpp
  MATCHER_P2(InClosedRange, low, hi, "") { ... }
  ...
  EXPECT_THAT(3, InClosedRange(4, 6));

```

genererebbe un errore che contiene il testo:

```shell
  Expected: in closed range (4, 6)

```

Ai fini della tipizzazione, è possibile visualizzare

```cpp
MATCHER_Pk(Foo, p1, ..., pk, description_string) { ... }

```

come abbreviazione di

```cpp
template <typename p1_type, ..., typename pk_type>
FooMatcherPk<p1_type, ..., pk_type>
Foo(p1_type p1, ..., pk_type pk) { ... }

```

Scrivendo `Foo(v1, ..., vk)`, il compilatore deduce i tipi dei parametri `v1`, ..., e `vk` autonomamente. Se non soddisfa il risultato dell'inferenza del tipo, si possono specificare i tipi istanziando esplicitamente il template, come in `Foo<long, bool>(5, false)`. Come detto in precedenza, non si può (né si deve) specificare `arg_type` poiché viene determinato dal contesto in cui viene utilizzato il matcher.

Si può assegnare il risultato dell'espressione `Foo(p1, ..., pk)` ad una variabile di tipo `FooMatcherPk<p1_type, ..., pk_type>`. Questo può essere utile quando si compongono i matcher. I matcher che non hanno un parametro o ne hanno solo uno hanno tipi speciali: si può assegnare `Foo()` a una variabile di tipo `FooMatcher` e assegnare `Foo(p)` a una variabile di tipo `FooMatcherP<p_type>`.

Sebbene sia possibile creare un'istanza di un template matcher con tipi riferimento, il passaggio dei parametri tramite puntatore in genere rende il codice più leggibile. Se però si deve comunque passare un parametro per riferimento, si tenga presente che nel messaggio di errore generato dal matcher si vedrà il valore dell'oggetto referenziato ma non il suo indirizzo.

Si può avere l'overload dei matcher con diversi numeri di parametri:

```cpp
MATCHER_P(Blah, a, description_string_1) { ... }
MATCHER_P2(Blah, a, b, description_string_2) { ... }

```

Sebbene sia forte la tentazione di utilizzare sempre le macro `MATCHER*` quando si definisce un nuovo matcher, di dovrebbe anche considerare di implementare direttamente l'interfaccia del matcher (vedere le ricette che seguono), soprattutto se c'è bisogno di usare molto il matcher. Sebbene questi approcci richiedano più lavoro, offrono un maggiore controllo sui tipi del valore da abbinare e sui parametri del matcher, il che in generale porta a messaggi di errore del compilatore migliori che ripagano nel lungo periodo.
Consentono inoltre l'overloading di matcher in base ai tipi di parametri (invece che basarsi solo sul numero di parametri).

### Scrivere Nuovi Matcher Monomorfici

Un matcher di tipo argomento `T` implementa l'interfaccia del matcher per `T` e fa due cose: verifica se un valore di tipo `T` corrisponde al matcher, e può descrivere il tipo di valori a cui corrisponde. Quest'ultima capacità viene utilizzata per generare messaggi di errore leggibili quando le expectation vengono violate.

Un matcher di `T` deve dichiarare un typedef come:

```cpp
using is_gtest_matcher = void;

```

e supporta le seguenti operazioni:

```cpp
// Match di un valore e facoltativamente lo spiega in un ostream.
bool matched = matcher.MatchAndExplain(value, maybe_os);
// dove `value` è di tipo `T` e
// `maybe_os` è di tipo `std::ostream*`, dove può essere null se il chiamante
// non è interessato alla spiegazione testuale.
matcher.DescribeTo(os);
matcher.DescribeNegationTo(os);
// dove `os` è di tipo `std::ostream*`.

```

Se c'è bisogno di un matcher personalizzato ma `Truly()` non è una buona opzione (ad esempio, non soddisfa il modo in cui `Truly(predicate)` si descrive, oppure per rendere il matcher polimorfico come lo è `Eq(value)`), si può definire un matcher in due passaggi: prima si implementa l'interfaccia del matcher e poi si definisce una funzione factory per creare un'istanza del matcher. Il secondo passaggio non è strettamente necessario ma rende più gradevole la sintassi dell'utilizzo del matcher.

Ad esempio, si può definire un matcher per verificare se un `int` è divisibile per 7 e poi usarlo in questo modo:

```cpp
using ::testing::Matcher;
class DivisibleBy7Matcher {
 public:
  using is_gtest_matcher = void;

  bool MatchAndExplain(int n, std::ostream*) const {
    return (n % 7) == 0;
  }

  void DescribeTo(std::ostream* os) const {
    *os << "is divisible by 7";
  }

  void DescribeNegationTo(std::ostream* os) const {
    *os << "is not divisible by 7";
  }
};
Matcher<int> DivisibleBy7() {
  return DivisibleBy7Matcher();
}
...
  EXPECT_CALL(foo, Bar(DivisibleBy7()));

```

Il messaggio del matcher è migliorabile trasmettendo informazioni aggiuntive all'argomento `os` in `MatchAndExplain()`:

```cpp
class DivisibleBy7Matcher {
 public:
  bool MatchAndExplain(int n, std::ostream* os) const {
    const int remainder = n % 7;
    if (remainder != 0 && os != nullptr) {
      *os << "the remainder is " << remainder;
    }

    return remainder == 0;
  }

  ...
};

```

Poi, `EXPECT_THAT(x, DivisibleBy7());` può generare un messaggio come questo:

```shell
Value of: x
Expected: is divisible by 7
  Actual: 23 (the remainder is 2)

```

{: .callout .tip}
Tip: per comodità, `MatchAndExplain()` può accettare un `MatchResultListener*` invece di `std::ostream*`.

### Scrivere Nuovi Matcher Polimorfici

Estendere ciò che abbiamo appreso sopra riguardo i matcher *polimorfici* risulta ora semplice come aggiungere i template nel posto giusto.

```cpp
class NotNullMatcher {
 public:
  using is_gtest_matcher = void;

  // Per implementare un matcher polimorfico, dobbiamo solo far diventare MatchAndExplain un
  // template sul suo primo argomento.
  // In questo esempio, vogliamo utilizzare NotNull() con qualsiasi puntatore, quindi
  // MatchAndExplain() accetta un puntatore di qualsiasi tipo come primo argomento.
  // In generale, si può definire MatchAndExplain() come un metodo ordinario oppure
  // un metodo template, o addirittura farne un overload.
  template <typename T>
  bool MatchAndExplain(T* p, std::ostream*) const {
    return p != nullptr;
  }

  // Descrive la proprietà di un valore che corrisponde a questo matcher.
  void DescribeTo(std::ostream* os) const { *os << "is not NULL"; }
  // Descrive la proprietà di un valore che NON corrisponde a questo matcher.
  void DescribeNegationTo(std::ostream* os) const { *os << "is NULL"; }
};
NotNullMatcher NotNull() {
  return NotNullMatcher();
}
...
  EXPECT_CALL(foo, Bar(NotNull()));  // L'argomento deve essere un puntatore non NULL.

```

### Implementazione di Matcher Legacy

La definizione dei matcher era un po' più complicata, in quanto richiedeva diverse classi di supporto e funzioni virtuali. Per implementare un matcher per il tipo `T` utilizzando l'API legacy si deve derivare da `MatcherInterface<T>` e chiamare `MakeMatcher` per costruire l'oggetto.

L'interfaccia è simile alla seguente:

```cpp
class MatchResultListener {
 public:
  ...
  // Trasmette x allo ostream; non fa nulla se ostream
  // è NULL.
  template <typename T>
  MatchResultListener& operator<<(const T& x);
  // Restituisce lo ostream di interesse.
  std::ostream* stream();
};
template <typename T>
class MatcherInterface {
 public:
  virtual ~MatcherInterface();
  // Restituisce true se e solo se il matcher corrisponde a x; spiega anche il risultato
  // della corrispondenza a 'listener'.
  virtual bool MatchAndExplain(T x, MatchResultListener* listener) const = 0;
  // Descrive questo matcher a un ostream.
  virtual void DescribeTo(std::ostream* os) const = 0;
  // Descrive la negazione di questo matcher a un ostream.
  virtual void DescribeNegationTo(std::ostream* os) const;
};

```

Fortunatamente, la maggior parte delle volte si può definire facilmente un matcher polimorfico con l'aiuto di `MakePolymorphicMatcher()`. Ecco un esempio di come si possa definire `NotNull()`:

```cpp
using ::testing::MakePolymorphicMatcher;
using ::testing::MatchResultListener;
using ::testing::PolymorphicMatcher;
class NotNullMatcher {
 public:
  // Per implementare un matcher polimorfico, definire prima una classe COPYABLE
  // che abbia tre membri MatchAndExplain(), DescribeTo(), e
  // DescribeNegationTo(), come il seguente.
  // In questo esempio, vogliamo utilizzare NotNull() con qualsiasi puntatore, quindi
  // MatchAndExplain() accetta un puntatore di qualsiasi tipo come primo argomento.
  // In generale, si può definire MatchAndExplain() come un metodo ordinario oppure
  // un metodo template, o addirittura farne un overload.
  template <typename T>
  bool MatchAndExplain(T* p,
                       MatchResultListener* /* listener */) const {
    return p != NULL;
  }

  // Descrive la proprietà di un valore che corrisponde a questo matcher.
  void DescribeTo(std::ostream* os) const { *os << "is not NULL"; }
  // Descrive la proprietà di un valore che NON corrisponde a questo matcher.
  void DescribeNegationTo(std::ostream* os) const { *os << "is NULL"; }
};
// To construct a polymorphic matcher, pass an instance of the class
// to MakePolymorphicMatcher().  Notare il tipo restituito.
PolymorphicMatcher<NotNullMatcher> NotNull() {
  return MakePolymorphicMatcher(NotNullMatcher());
}
...
  EXPECT_CALL(foo, Bar(NotNull()));  // L'argomento deve essere un puntatore non NULL.

```

{: .callout .note}
**Nota:** La classe matcher polimorfica **non** ha bisogno di ereditare da `MatcherInterface` o qualsiasi altra classe, e i suoi metodi **non** devono essere virtuali.

Come in un matcher monomorfico, si può spiegare il risultato della corrispondenza trasmettendo informazioni aggiuntive all'argomento `listener` in `MatchAndExplain()`.

### Scrivere Nuove Cardinalità

Una cardinalità viene utilizzata in `Times()` per dire a gMock quante volte ci si aspetta che avvenga una chiamata. Non deve essere esatta. Ad esempio, si può dire `AtLeast(5)` o `Between(2, 4)`.

Se l'[insieme nativo](gmock_cheat_sheet.md#CardinalityList) delle cardinalità non è sufficiente, se ne può definire uno implementando la seguente interfaccia (nel namespace `testing`):

```cpp
class CardinalityInterface {
 public:
  virtual ~CardinalityInterface();
  // Restituisce true se e solo se le chiamate call_count soddisfano questa cardinalità.
  virtual bool IsSatisfiedByCallCount(int call_count) const = 0;
  // Restituisce true se e solo se le chiamate call_count satureranno
  // questa cardinalità.
  virtual bool IsSaturatedByCallCount(int call_count) const = 0;
  // Descrive sé stesso [self] a un ostream.
  virtual void DescribeTo(std::ostream* os) const = 0;
};

```

Ad esempio, per specificare che una chiamata deve avvenire un numero pari di volte, è possibile scrivere

```cpp
using ::testing::Cardinality;
using ::testing::CardinalityInterface;
using ::testing::MakeCardinality;
class EvenNumberCardinality : public CardinalityInterface {
 public:
  bool IsSatisfiedByCallCount(int call_count) const override {
    return (call_count % 2) == 0;
  }

  bool IsSaturatedByCallCount(int call_count) const override {
    return false;
  }

  void DescribeTo(std::ostream* os) const {
    *os << "called even number of times";
  }
};
Cardinality EvenNumber() {
  return MakeCardinality(new EvenNumberCardinality);
}
...
  EXPECT_CALL(foo, Bar(3))
      .Times(EvenNumber());

```

### Scrivere Nuove Action {#QuickNewActions}

Se le azioni [action] native non funzionano, se ne può facilmente definirne una propria.
Tutto ciò di cui si ha bisogno è un operatore di chiamata con una firma compatibile con la funzione mock-ata. Poi si può usare una lambda:

```cpp
MockFunction<int(int)> mock;
EXPECT_CALL(mock, Call).WillOnce([](const int input) { return input * 7; });
EXPECT_EQ(mock.AsStdFunction()(2), 14);

```

O una struct con un operatore di chiamata (anche uno basato su template):

```cpp
struct MultiplyBy {
  template <typename T>
  T operator()(T arg) { return arg * multiplier; }
  int multiplier;
};
// Then use:
// EXPECT_CALL(...).WillOnce(MultiplyBy{7});
```

Va bene anche che il callable non accetti argomenti, ignorando gli argomenti forniti alla funzione mock:

```cpp
MockFunction<int(int)> mock;
EXPECT_CALL(mock, Call).WillOnce([] { return 17; });
EXPECT_EQ(mock.AsStdFunction()(0), 17);

```

Se utilizzato con `WillOnce`, il callable può presupporre che verrà chiamato al massimo una volta e può essere di tipo move-only:

```cpp
// Una action che contiene tipi move-only e ha un operatore qualificato &&,
// esige nel [type system] che sia chiamata al massimo una volta. Può essere
// utilizzato con WillOnce, ma il compilatore lo rifiuterà se passato a
// WillRepeatedly.
struct MoveOnlyAction {
  std::unique_ptr<int> move_only_state;
  std::unique_ptr<int> operator()() && { return std::move(move_only_state); }
};
MockFunction<std::unique_ptr<int>()> mock;
EXPECT_CALL(mock, Call).WillOnce(MoveOnlyAction{std::make_unique<int>(17)});
EXPECT_THAT(mock.AsStdFunction()(), Pointee(Eq(17)));
```

Più in generale, da utilizzare con una funzione mock la cui firma è `R(Args...)` l'oggetto può essere qualsiasi cosa convertibile in `OnceAction<R(Args...)>` o `Action<R(Args...)`>. La differenza tra i due è che `OnceAction` ha requisiti più deboli (`Action` richiede un input con costruttore-copia che può essere chiamato ripetutamente mentre `OnceAction` richiede un costruttore-move e supporta operatori di chiamata qualificati `&&`), ma può essere utilizzato solo con `WillOnce`.
`OnceAction` è in genere rilevante solo quando si supportano tipi o azioni move-only che richiedono che un type-system garantisca che verranno chiamati al massimo una volta.

In genere non è necessario fare riferimento direttamente ai template `OnceAction` e `Action` nelle action: basta una struct o una classe con un operatore di chiamata, come negli esempi precedenti. Ma azioni polimorfiche più sofisticate che necessitano di conoscere il tipo di ritorno specifico della funzione mock possono definire operatori di conversione basati su template per renderlo possibile. Per gli esempi consultare `gmock-actions.h`.

#### Action Legacy basate su macro

Prima di C++11 le azioni basate su funtori non erano supportate; il vecchio modo di scriverle era attraverso una serie di macro `ACTION*`. Suggeriamo di evitarle nel nuovo codice; si nasconde molta logica dietro la macro, portando potenzialmente a errori del compilatore difficili da comprendere. Tuttavia, li descriviamo qui per completezza.

Scrivendo

```cpp
ACTION(nome) { istruzioni; }

```

nello scope di un namespace (cioè non all'interno di una classe o funzione), si definirà un'azione con il nome dato che esegue le istruzioni. Il valore restituito dalle `istruzioni` verrà utilizzato come valore di ritorno dell'azione. All'interno delle istruzioni, si può fare riferimento all'argomento K-esimo (in base 0) della funzione mock come `argK`. Per esempio:

```cpp
ACTION(IncrementArg1) { return ++(*arg1); }

```

consente di scrivere

```cpp
... WillOnce(IncrementArg1());

```

Notare che non è necessario specificare i tipi degli argomenti della funzione mock.
Sicuramente il codice è type-safe: si riceverà un errore del compilatore se `*arg1` non supporta l'operatore `++`, o se il tipo di `++(*arg1)` non è compatibile con il tipo restituito della funzione mock.

Un altro esempio:

```cpp
ACTION(Foo) {
  (*arg2)(5);
  Blah();
  *arg1 = 0;
  return arg0;
}

```

definisce un'azione `Foo()` che invoca l'argomento #2 (un puntatore a funzione) con 5, chiama la funzione `Blah()`, imposta il valore puntato dall'argomento #1 a 0 e restituisce l'argomento #0.

Per maggiore comodità e flessibilità, si possono utilizzare i seguenti simboli predefiniti nel corpo di `ACTION`:

| `argK_type` | Il tipo dell'argomento K-esimo (in base 0) della funzione mock |
:-------------- | :-----------------------------------------------------------
| `args` | Tutti gli argomenti della funzione mock come una tupla |
| `args_type` | Il tipo di tutti gli argomenti della funzione mock come tupla |
| `return_type` | Il tipo restituito della funzione mock |
| `function_type` | Il tipo della funzione mock |

Ad esempio, quando si utilizza `ACTION` come azione stub per la funzione mock:

```cpp
int DoSomething(bool flag, int* ptr);

```

abbiamo:

| Simbolo Pre-definito | è [Bound] A  |
------------------ | ---------------------------------
| `arg0` | il valore di `flag` |
| `arg0_type` | il tipo `bool` |
| `arg1` | il valore di `ptr` |
| `arg1_type` | il tipo `int*` |
| `args` | la tuple `(flag, ptr)` |
| `args_type` | il tipo `std::tuple<bool, int*>` |
| `return_type` | il tipo `int` |
| `function_type` | il tipo `int(bool, int*)` |

#### Azioni legacy parametrizzate basate su macro

Talvolta si vuole parametrizzare una action che si definisce. Per questo abbiamo un'altra macro

```cpp
ACTION_P(name, param) { statements; }

```

Per esempio,

```cpp
ACTION_P(Add, n) { return arg0 + n; }

```

permetterà di scrivere

```cpp
// Restituisce l'argomento #0 + 5.
... WillOnce(Add(5));

```

Per comodità, utilizziamo il termine *argomenti* per i valori utilizzati per invocare la funzione mock e il termine *parametri* per i valori utilizzati per istanziare un'azione.

Notare che non è necessario fornire nemmeno il tipo del parametro. Supponiamo che il parametro si chiami `param`, si può anche utilizzare il simbolo definito da gMock `param_type` per fare riferimento al tipo del parametro come dedotto dal compilatore.
Ad esempio, nel corpo di `ACTION_P(Add, n)` sopra, si può scrivere `n_type` per il tipo di `n`.

gMock fornisce anche `ACTION_P2`, `ACTION_P3` e così via per supportare azioni multi-parametro. Per esempio,

```cpp
ACTION_P2(ReturnDistanceTo, x, y) {
  double dx = arg0 - x;
  double dy = arg1 - y;
  return sqrt(dx*dx + dy*dy);
}

```

permette di scrivere

```cpp
... WillOnce(ReturnDistanceTo(5.0, 26.5));

```

Si può vedere `ACTION` come un'azione parametrizzata degenerata in cui il numero di parametri è 0.

Si possono anche definire facilmente overload di azioni sul numero di parametri:

```cpp
ACTION_P(Plus, a) { ... }
ACTION_P2(Plus, a, b) { ... }

```

### Restrizioni sul tipo dell'argomento o del parametro in una ACTION

Per la massima brevità e riusabilità, le macro `ACTION*` non chiedono di fornire i tipi degli argomenti della funzione mock né i parametri dell'azione.
Lasciamo invece che sia il compilatore a dedurre i tipi.

A volte, tuttavia, potremmo voler essere più espliciti riguardo ai tipi. Ci sono diversi trucchi per farlo. Per esempio:

```cpp
ACTION(Foo) {
  // Si assicura che arg0 possa essere convertito in int.
  int n = arg0;
  ... use n instead of arg0 here ...
}
ACTION_P(Bar, param) {
  // Si assicura che il tipo di arg1 sia const char*.
  ::testing::StaticAssertTypeEq<const char*, arg1_type>();
  // Si assicura che param possa essere convertito in bool.
  bool flag = param;
}

```

dove `StaticAssertTypeEq` è un'asserzione in fase di compilazione in googletest che verifica che due tipi siano uguali.

### Scrivere Rapidamente una Nuove Template di Action

A volte è necessario fornire a un'azione parametri template espliciti che non possono essere dedotti dai parametri del valore.
`ACTION_TEMPLATE()` supports that and can be
viewed as an extension to `ACTION()` and `ACTION_P*()`.

La sintassi:

```cpp
ACTION_TEMPLATE(ActionName,
                HAS_m_TEMPLATE_PARAMS(kind1, name1, ..., kind_m, name_m),
                AND_n_VALUE_PARAMS(p1, ..., p_n)) { statements; }

```

definisce una action template che accetta *m* parametri template espliciti e *n* parametri di valore, dove *m* è in [1, 10] e *n* è in [0, 10]. `name_i` è il nome dell'*i*-esimo parametro template, e `kind_i` specifica se si tratta di un `typename`, un integrale costante o un template. `p_i` è il nome del parametro valore *i*-esimo.

Esempio:

```cpp
// DuplicateArg<k, T>(output) converte il k-esimo argomento della funzione mock
// nel tipo T e lo copia in *output.
ACTION_TEMPLATE(DuplicateArg,
                // Notare la virgola tra int e k:
                HAS_2_TEMPLATE_PARAMS(int, k, typename, T),
                AND_1_VALUE_PARAMS(output)) {
  *output = T(std::get<k>(args));
}

```

Per creare un'istanza di una action template, si scrive:

```cpp
ActionName<t1, ..., t_m>(v1, ..., v_n)

```

dove le `t` sono gli argomenti template e le `v` sono gli argomenti valore.
I tipi degli argomenti valore vengono dedotti dal compilatore. Per esempio:

```cpp
using ::testing::_;
...
  int n;
  EXPECT_CALL(mock, Foo).WillOnce(DuplicateArg<1, unsigned char>(&n));

```

Per specificare esplicitamente i tipi degli argomenti valore, si possono fornire argomenti template aggiuntivi:

```cpp
ActionName<t1, ..., t_m, u1, ..., u_k>(v1, ..., v_n)

```

dove `u_i` è il tipo desiderato di `v_i`.

`ACTION_TEMPLATE` e `ACTION`/`ACTION_P*` si possono overload-are sul numero di parametri valore, ma non sul numero di parametri template. Senza la restrizione, il significato di quanto segue non è chiaro:

```cpp
  OverloadedAction<int, bool>(x);

```

Stiamo utilizzando un'azione con parametro tempale singolo in cui `bool` si riferisce al tipo di `x`, o un'azione con due parametri template in cui al compilatore viene chiesto di dedurre il tipo di `x`?

### Usare il Tipo dell'Oggetto ACTION

Per scrivere una funzione che restituisce un oggetto `ACTION`, se ne deve conoscere il tipo. Il tipo dipende dalla macro utilizzata per definire l'azione e i tipi dei parametri. La regola è relativamente semplice:


| Definizione Data | Espressione | Ha il Tipo |
| ----------------------------- | ------------------- | --------------------- |
| `ACTION(Foo)` | `Foo()` | `FooAction` |
| `ACTION_TEMPLATE(Foo, HAS_m_TEMPLATE_PARAMS(...), AND_0_VALUE_PARAMS())` | `Foo<t1, ..., t_m>()` | `FooAction<t1, ..., t_m>` |
| `ACTION_P(Bar, param)` | `Bar(int_value)` | `BarActionP<int>` |
| `ACTION_TEMPLATE(Bar, HAS_m_TEMPLATE_PARAMS(...), AND_1_VALUE_PARAMS(p1))` | `Bar<t1, ..., t_m>(int_value)` | `BarActionP<t1, ..., t_m, int>` |
| `ACTION_P2(Baz, p1, p2)` | `Baz(bool_value, int_value)` | `BazActionP2<bool, int>` |
| `ACTION_TEMPLATE(Baz, HAS_m_TEMPLATE_PARAMS(...), AND_2_VALUE_PARAMS(p1, p2))` | `Baz<t1, ..., t_m>(bool_value, int_value)` | `BazActionP2<t1, ..., t_m, bool, int>` |
| ... | ... | ... |


Notare che dobbiamo scegliere suffissi diversi (`Action`, `ActionP`, `ActionP2`, ecc.) per azioni con numeri diversi di parametri valore, oppure non si possono avere overload delle definizioni delle azioni rispetto al loro numero.

### Scrivere Nuove Azioni Monomorfiche {#NewMonoActions}

Sebbene le macro `ACTION*` siano molto comode, a volte sono inappropriate. Ad esempio, nonostante i trucchi mostrati nelle ricette precedenti, non consentono di specificare direttamente i tipi degli argomenti della funzione mock e dei parametri dell'azione, il che in generale porta a messaggi di errore del compilatore non ottimizzati che possono confondere gli utenti non esperti. Inoltre, non consentono overload di azioni basate sui tipi di parametri senza eseguire alcuni passaggi.

Un'alternativa alle macro `ACTION*` è implementare `::testing::ActionInterface<F>`, dove `F` è il tipo della funzione mock in cui verrà utilizzata l'azione. Per esempio:

```cpp
template <typename F>
class ActionInterface {
 public:
  virtual ~ActionInterface();
  // Esegue la action.  Result è il tipo restituito della funzione di tipo
  // F, e ArgumentTuple è la tupla di argomenti di F.
  //
  // Ad esempio, se F è int(bool, const string&), allora Result sarà
  // int e ArgumentTuple sarà std::tuple<bool, const string&>.
  virtual Result Perform(const ArgumentTuple& args) = 0;
};
```

```cpp
using ::testing::_;
using ::testing::Action;
using ::testing::ActionInterface;
using ::testing::MakeAction;
typedef int IncrementMethod(int*);
class IncrementArgumentAction : public ActionInterface<IncrementMethod> {
 public:
  int Perform(const std::tuple<int*>& args) override {
    int* p = std::get<0>(args);  // Cattura il primo argomento.
    return *p++;
  }
};
Action<IncrementMethod> IncrementArgument() {
  return MakeAction(new IncrementArgumentAction);
}
...
  EXPECT_CALL(foo, Baz(_))
      .WillOnce(IncrementArgument());
  int n = 5;
  foo.Baz(&n);  // Dovrebbe restituire 5 e cambiare n in 6.

```

### Scrivere Nuove Action Polimorfiche {#NewPolyActions}

La ricetta precedente ha mostrato come definire una propria azione. Va tutto bene, tranne che è necessario conoscere il tipo della funzione in cui verrà utilizzata l'azione. A volte questo può essere un problema. Ad esempio, per utilizzare l'azione in funzioni con tipi *diversi* (ad esempio come `Return()` e `SetArgPointee()`).

Se un'azione può essere utilizzata in diversi tipi di funzioni mock, diciamo che è *polimorfica*. La funzione template `MakePolymorphicAction()` semplifica la definizione di tale azione:

```cpp
namespace testing {
template <typename Impl>
PolymorphicAction<Impl> MakePolymorphicAction(const Impl& impl);
}  // namespace testing

```

Come esempio, definiamo un'azione che restituisce il secondo argomento nell'elenco degli argomenti della funzione mock. Il primo passo è definire una classe di implementazione:

```cpp
class ReturnSecondArgumentAction {
 public:
  template <typename Result, typename ArgumentTuple>
  Result Perform(const ArgumentTuple& args) const {
    // Per ottenere l'i-esimo argomento (basato su 0), utilizzare std::get(args).
    return std::get<1>(args);
  }
};

```

Questa classe di implementazione *non* ha bisogno di ereditare da una classe particolare.
Ciò che conta è che deve avere un metodo template `Perform()`. Questo metodo template accetta gli argomenti della funzione mock come una tupla in un argomento **singolo** e restituisce il risultato dell'azione. Può essere `const` o meno, ma deve essere invocabile esattamente con un argomento template, che è il tipo del risultato. In altre parole, si deve essere in grado di chiamare `Perform<R>(args)` dove `R` è il tipo restituito dalla funzione mock e `args` è il suo argomenti in una tupla.

Poi, usiamo `MakePolymorphicAction()` per trasformare un'istanza della classe di implementazione nell'azione polimorfica di cui abbiamo bisogno.
 Sarà conveniente avere un wrapper per questo:

```cpp
using ::testing::MakePolymorphicAction;
using ::testing::PolymorphicAction;
PolymorphicAction<ReturnSecondArgumentAction> ReturnSecondArgument() {
  return MakePolymorphicAction(ReturnSecondArgumentAction());
}

```

Ora si può utilizzare questa azione polimorfica nello stesso modo in cui si usano quelle native:

```cpp
using ::testing::_;
class MockFoo : public Foo {
 public:
  MOCK_METHOD(int, DoThis, (bool flag, int n), (override));
  MOCK_METHOD(string, DoThat, (int x, const char* str1, const char* str2),
              (override));
};

  ...
  MockFoo foo;
  EXPECT_CALL(foo, DoThis).WillOnce(ReturnSecondArgument());
  EXPECT_CALL(foo, DoThat).WillOnce(ReturnSecondArgument());
  ...
  foo.DoThis(true, 5);  // Restituirà 5.
  foo.DoThat(1, "Hi", "Bye");  // Restituirà "Hi".

```

### Insegnare a gMock Come Stampare i Propri Valori

Quando avviene una chiamata [uninteresting] o inaspettata [unexpected], gMock stampa i valori degli argomenti e lo stack trace come aiuto al debug. Anche le macro di asserzione come `EXPECT_THAT` e `EXPECT_EQ` stampano i valori in questione quando l'asserzione fallisce. gMock e googletest lo fanno utilizzando la stampante di valori estensibile dall'utente di googletest.

Questa stampante sa come stampare i tipi nativi di C++, gli array, i contenitori STL e qualsiasi tipo che supporti l'operatore `<<`. Per gli altri tipi, stampa i byte grezzi nel valore e spera che l'utente possa capirlo.
[La Guida Avanzata di GoogleTest](advanced.md#teaching-googletest-how-to-print-your-values) spiega come estendere la stampante per eseguire un lavoro migliore stampando il tipo particolare piuttosto che il dump dei byte.

## Mock Utili Creati Con gMock

<!--#include file="includes/g3_testing_LOGs.md"-->
<!--#include file="includes/g3_mock_callbacks.md"-->

### Mock std::function {#MockFunction}

`std::function` è un tipo di funzione generale introdotto in C++11. È un modo preferito per passare le callback a nuove interfacce. Le funzioni sono copiabili e di solito non vengono passate tramite puntatore, il che le rende difficili da rendere mock.
Niente paura - `MockFunction` è d'aiuto.

`MockFunction<R(T1, ..., Tn)>` ha un metodo mock `Call()` con la signature:

```cpp
  R Call(T1, ..., Tn);

```

C'è anche il metodo `AsStdFunction()`, che crea un proxy `std::function` che inoltra a Call:

```cpp
  std::function<R(T1, ..., Tn)> AsStdFunction();

```

Per utilizzare `MockFunction`, si crea prima un oggetto `MockFunction` e si impostano le expectation sul suo metodo `Call`. Poi si passa il proxy ottenuto da `AsStdFunction()` al codice da testare. Per esempio:

```cpp
TEST(FooTest, RunsCallbackWithBarArgument) {
  // 1. Crea un oggetto mock.
  MockFunction<int(string)> mock_function;
  // 2. Imposta le expectation sul metodo Call().
  EXPECT_CALL(mock_function, Call("bar")).WillOnce(Return(1));
  // 3. Codice di esercizio che usa std::function.
  Foo(mock_function.AsStdFunction());
  // La firma di Foo può essere:
  // void Foo(const std::function<int(string)>& fun);
  // void Foo(std::function<int(string)> fun);
  // 4. Tutte le expectation verranno verificate quando mock_function
  //     uscirà dallo scope e verrà distrutto.
}

```

Da ricordare che gli oggetti funzione creati con `AsStdFunction()` sono solo [forwarder]. Se se ne creano di più, condivideranno lo stesso insieme di expectation.

Sebbene `std::function` supporti un numero illimitato di argomenti, l'implementazione di `MockFunction` è limitata a dieci. Se mai si raggiungesse questo limite... beh, la richiamata ha problemi più grandi del poter essere mock. :-)
