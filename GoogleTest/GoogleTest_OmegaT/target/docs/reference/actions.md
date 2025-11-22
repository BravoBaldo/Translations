# Riferimenti alle Action

Le [**action**](../gmock_for_dummies.md#actions-what-should-it-do) specificano cosa dovrebbe fare una funzione mock quando viene invocata. Questa pagina elenca le azioni native di GoogleTest. Tutte le azioni sono definite nel namespace `::testing`.

## Restituzione di un Valore

| Action | Descrizione |
| :-------------------------------- | :-------------------------------------------- |
| `Return()` | Ritorno da una funzione mock`void`. |
| `Return(value)` | Restituisce `value`. If the type of `value` is     different to the mock function's return type, `value` is converted to the latter type <i>at the time the expectation is set</i>, not when the action is executed. |
| `ReturnArg<N>()` | Restituisce l'argomento `N`-esimo (in base 0). |
| `ReturnNew<T>(a1, ..., ak)` | Restituisce `new T(a1, ..., ak)`; ogni volta viene creato un oggetto diverso. |
| `ReturnNull()` | Restituisce un puntatore null. |
| `ReturnPointee(ptr)` | Restituisce il valore puntato da `ptr`. |
| `ReturnRef(variable)` | Restituisce un riferimento alla `variable`. |
| `ReturnRefOfCopy(value)` | Restituisce un riferimento a una copia di `value`; la copia vive quanto l'azione. |
| `ReturnRoundRobin({a1, ..., ak})` | Ogni chiamata restituirà il successivo `ai` nell'elenco, iniziando dall'inizio quando viene raggiunta la fine dell'elenco. |

## Effetti Collaterali

| Action | Descrizione |
| :--------------------------------- | :-------------------------------------- |
| `Assign(&variable, value)` | Assegna `value` a variable. |
| `DeleteArg<N>()` | Esegue il delete dell'argomento `N`-esimo (in base 0), che deve essere un puntatore. |
| `SaveArg<N>(pointer)` | Salva l'argomento `N`-esimo (in base 0) in `*pointer`. |
| `SaveArgPointee<N>(pointer)` | Salva il valore puntato dall'argomento `N`-esimo (in base 0) in `*pointer`. |
| `SetArgReferee<N>(value)` | Assegna `value` alla variabile a cui fa riferimento l'argomento `N`-esimo (in base 0). |
| `SetArgPointee<N>(value)` | Assegna `value` alla variabile puntata dall'argomento `N`-esimo (in base 0). |
| `SetArgumentPointee<N>(value)` | Uguale a `SetArgPointee<N>(value)`. Deprecato. Verrà rimosso nella v1.7.0. |
| `SetArrayArgument<N>(first, last)` | Copia gli elementi nell'intervallo di origine [`first`, `last`) nell'array puntato dall'argomento `N`-esimo (in base 0), che può essere un puntatore o un iteratore. L'azione non assume la proprietà degli elementi nell'intervallo di origine. |
| `SetErrnoAndReturn(error, value)` | Setta `errno` a `error` e restituisce `value`. |
| `Throw(exception)` | Genera l'eccezione specificata, che può essere qualsiasi valore copiabile. Disponibile dalla v1.1.0. |

## Usare un Funzione, Funtore o una Lambda come Action

Di seguito, con "callable" (chiamabile) intendiamo una funzione libera, `std::function`, un funtore o una lambda.

| Action | Descrizione |
| :---------------------------------- | :------------------------------------- |
| `f` | Invoca `f` con gli argomenti passati alla funzione mock, dove `f` è un "callable". |
| `Invoke(f)` | Invoca `f` con gli argomenti passati alla funzione mock, dove `f`può essere una funzione globale/statica o un funtore. |
| `Invoke(object_pointer, &class::method)` | Invoca il metodo sull'oggetto con gli argomenti passati alla funzione mock. |
| `InvokeWithoutArgs(f)` | Invoca `f`, che può essere una funzione globale/statica o un funtore. `f` non deve accettare argomenti. |
| `InvokeWithoutArgs(object_pointer, &class::method)` | Invoca il metodo sull'oggetto, che non accetta argomenti. |
| `InvokeArgument<N>(arg1, arg2, ..., argk)` | Invoca l'argomento `N`-esimo (basato su 0) della funzione mock, che deve essere una funzione o un funtore, con gli argomenti `k`. |

Il valore restituito della funzione richiamata viene utilizzato come valore restituito dell'azione.

Quando si definisce un callable da utilizzare con `Invoke*()`, si può dichiarare qualsiasi parametro inutilizzato come `Unused`:

```cpp
using ::testing::Invoke;
double Distance(Unused, double x, double y) { return sqrt(x*x + y*y); }
...
EXPECT_CALL(mock, Foo("Hi", _, _)).WillOnce(Invoke(Distance));

```

`Invoke(callback)` e `InvokeWithoutArgs(callback)` assumono la proprietà di `callback`, che deve essere permanente. Il tipo di `callback` deve essere un tipo di callback di base anziché derivato, ad es.

```cpp
  BlockingClosure* done = new BlockingClosure;
  ... Invoke(done) ...;  // Questo non verrà compilato!
  Closure* done2 = new BlockingClosure;
  ... Invoke(done2) ...;  // Questo funziona.

```

In `InvokeArgument<N>(...)`, se un argomento deve essere passato per riferimento, racchiuderlo all'interno di `std::ref()`. Per esempio,

```cpp
using ::testing::InvokeArgument;
...
InvokeArgument<2>(5, string("Hi"), std::ref(foo))

```

chiama l'argomento #2 della funzione mock, passandogli `5` e `string("Hi")` per valore e `foo` per riferimento.

## Action di Default

| Action | Descrizione |
| :------------ | :----------------------------------------------------- |
| `DoDefault()` | Esegue l'azione di default (specificata da `ON_CALL()` o quella nativa). |

{: .callout .note}
**Nota:** per motivi tecnici, `DoDefault()` non può essere utilizzato all'interno di un'azione composita: facendolo comporterà un errore a runtime.

## Action Composite

| Action | Descrizione |
| :----------------------------- | :------------------------------------------ |
| `DoAll(a1, a2, ..., an)` | Esegue tutte le azioni da `a1` a `an` e restituisce il risultato di `an` in ogni invocazione. Le prime `n - 1` sotto-azioni devono restituire void e riceveranno una vista di sola lettura degli argomenti. |
| `IgnoreResult(a)` | Esegui l'azione `a` e ne ignora il risultato. `a` non deve restituire void. |
| `WithArg<N>(a)` | Passa l'argomento `N`-esimo (in base 0) della funzione mock all'azione `a` e la esegue. |
| `WithArgs<N1, N2, ..., Nk>(a)` | Passa gli argomenti selezionati (a base 0) della funzione mock all'azione `a` e la esegue. |
| `WithoutArgs(a)` | Esegue l'azione `a` senza argomenti. |

## Definizione delle Action

| Macro | Descrizione |
| :--------------------------------- | :-------------------------------------- |
| `ACTION(Sum) { return arg0 + arg1; }` | Definisce un'azione `Sum()` per restituire la somma degli argomenti #0 e #1 della funzione mock. |
| `ACTION_P(Plus, n) { return arg0 + n; }` | Definisce un'azione `Plus(n)` per restituire la somma degli argomenti #0 e `n`. |
| `ACTION_Pk(Foo, p1, ..., pk) { statements; }` | Definisce un'azione parametrizzata `Foo(p1, ..., pk)` per eseguire gli `statements` specificati. |

Le macro `ACTION*` non possono essere utilizzate all'interno di una funzione o di una classe.
