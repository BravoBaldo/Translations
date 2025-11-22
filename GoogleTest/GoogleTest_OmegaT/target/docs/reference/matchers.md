# Riferimenti ai Matcher

Un **matcher** si abbina ad un *singolo* argomento. Lo si può usare in una `ON_CALL()` o in una `EXPECT_CALL()`, oppure usarlo per convalidare un valore direttamente utilizzando due macro:

| Macro | Descrizione |
| :----------------------------------- | :------------------------------------ |
| `EXPECT_THAT(actual_value, matcher)` | Afferma che `actual_value` corrisponde al `matcher`. |
| `ASSERT_THAT(actual_value, matcher)` | Uguale a `EXPECT_THAT(actual_value, matcher)`, tranne per il fatto che genera un errore **fatale**. |

{: .callout .warning}
**WARNING:** È supportata la corrispondenza dell'uguaglianza tramite `EXPECT_THAT(actual_value, expected_value)`, tuttavia si tenga presente che le conversioni implicite possono causare risultati sorprendenti. Per esempio, `EXPECT_THAT(some_bool, "some string")` verrà compilato e potrebbe passare involontariamente.

**BEST PRACTICE:** È preferibile rendere esplicito il confronto tramite `EXPECT_THAT(actual_value, Eq(expected_value))` o `EXPECT_EQ(actual_value, expected_value)`.

I matcher nativi (dove `argument` è l'argomento della funzione, ad esempio `actual_value` nell'esempio sopra, o quando utilizzato nel contesto di `EXPECT_CALL(mock_object, method(matchers))`, gli argomenti di `method`) sono divisi in diverse categorie. Tutti i matcher sono definiti nel namespace `::testing` se non diversamente specificato.

## Jolly [Wildcard]

| Matcher | Descrizione |
:-------------------------- | :-----------------------------------------------
| `_` | `argument` può essere qualsiasi valore del tipo corretto. |
| `A<type>()` o `An<type>()` | `argument` può essere qualsiasi valore di tipo `type`. |

## Confronto Generico

| Matcher | Descrizione |
| :--------------------- | :-------------------------------------------------- |
| `Eq(value)` o `value` | `argument == value` |
| `Ge(value)` | `argument >= value` |
| `Gt(value)` | `argument > value` |
| `Le(value)` | `argument <= value` |
| `Lt(value)` | `argument < value` |
| `Ne(value)` | `argument != value` |
| `IsFalse()` | `argument` valutato `false` in un contesto booleano. |
| `IsTrue()` | `argument` valuatato `true` in un contesto booleano. |
| `IsNull()` | `argument` è un puntatore `NULL` (raw o smart). |
| `NotNull()` | `argument` è un puntatore non-null (raw o smart). |
| `Optional(m)` | `argument` è `optional<>` che contiene un valore che coincide con `m`. (Per testare se è impostato un `optional<>`, verificare l'uguaglianza con `nullopt`. Potrebbe essere necessario utilizzare `Eq(nullopt)` se il tipo interno non ha `==`.) |
| `VariantWith<T>(m)` | `argument` è un `variant<>` che contiene l'alternativa di tipo T con un valore corrispondente a `m`. |
| `Ref(variable)` | `argument` è un riferimento a `variable`. |
| `TypedEq<type>(value)` | `argument` ha tipo `type` ed è uguale a `value`. Potrebbe essere necessario utilizzarlo al posto di `Eq(value)` quando la funzione mock è un overload. |

Ad eccezione di `Ref()`, questi matcher creano una *copia* di `value` nel caso in cui venga modificato o distrutto in seguito. Se il compilatore lamenta che `value` non ha un costruttore di copia pubblica, provare a racchiuderlo in `std::ref()`, ad es. `Eq(std::ref(non_copyable_value))`. Se lo si fa, `non_copyable_value` non deve essere modificato in seguito, altrimenti il significato del matcher verrà cambiato.

`IsTrue` e `IsFalse` sono utili quando è necessario utilizzare un matcher o per tipi che possono essere convertiti esplicitamente in booleano, ma non lo sono implicitamente. In altri casi, si possono utilizzare le asserzioni di base [`EXPECT_TRUE` e `EXPECT_FALSE`](assertions.md#boolean).

## Matcher in Virgola Mobile {#FpMatchers}

| Matcher | Descrizione |
| :------------------------------- | :--------------------------------- |
| `DoubleEq(a_double)` | `argument` è un valore `double` approssimativamente uguale a `a_double`, trattando due NaN come diversi. |
| `FloatEq(a_float)` | `argument` è un valore `float` approssimativamente uguale a `a_float`, trattando due NaN come diversi. |
| `NanSensitiveDoubleEq(a_double)` | `argument` è un valore `double` approssimativamente uguale a `a_double`, trattando due NaN uguali. |
| `NanSensitiveFloatEq(a_float)` | `argument` è un valore `float` approssimativamente uguale a `a_float`, trattando due NaN uguali. |
| `IsNan()` | `argument` è di tipo a virgola mobile con un valore NaN. |

I matcher precedenti utilizzano il confronto basato su ULP (lo stesso utilizzato in googletest).
Scelgono automaticamente un limite di errore ragionevole in base al valore assoluto del valore atteso. `DoubleEq()` e `FloatEq()` sono conformi allo standard IEEE, che richiede il confronto di due NaN affinché l'uguaglianza restituisca false. La versione `NanSensitive*` tratta invece due NaN come uguali, che spesso è ciò che un utente desidera.

| Matcher | Descrizione |
| :------------------------------------------------ | :----------------------- |
| `DoubleNear(a_double, max_abs_error)` | `argument` è un valore `double` vicino a `a_double` (errore assoluto <= `max_abs_error`), considera due NaN come diversi. |
| `FloatNear(a_float, max_abs_error)` | `argument` è un valore `float` vicio a `a_float` (errore assoluto <= `max_abs_error`), considera due NaN come diversi.
 |
| `NanSensitiveDoubleNear(a_double, max_abs_error)` | `argument` è un valore `double` vicino a `a_double` (errore assoluto <= `max_abs_error`), considera due NaN come uguali. |
| `NanSensitiveFloatNear(a_float, max_abs_error)` | `argument` è un valore `float` vicino a `a_float` (errore assoluto <= `max_abs_error`), considera due NaN come uguali. |

## Matcher di Stringhe

`argument` può essere una stringa C o un oggetto stringa C++:

| Matcher | Descrizione |
| :---------------------- | :------------------------------------------------- |
| `ContainsRegex(string)` | `argument` corrisponde all'espressione regolare data. |
| `EndsWith(suffix)` | `argument` termina con la stringa `suffix`. |
| `HasSubstr(string)` | `argument` contiene la sotto-stringa `string`. |
| `IsEmpty()` | `argument` è una stringa vuota. |
| `MatchesRegex(string)` | `argument` corrisponde all'espressione regolare data con la corrispondenza che inizia con il primo carattere e termina con l'ultimo carattere. |
| `StartsWith(prefix)` | `argument` inizia con la stringa `prefix`. |
| `StrCaseEq(string)` | `argument` è uguale a `string`, ignorando maiuscole e minuscole. |
| `StrCaseNe(string)` | `argument` è diverso da `string`, ignorando maiuscole e minuscole. |
| `StrEq(string)` | `argument` è uguale a `string`. |
| `StrNe(string)` | `argument` è diverso da `string`. |
| `WhenBase64Unescaped(m)` | `argument` è una stringa con escape in base 64 la cui stringa senza escape corrisponde a `m`.  È supportato il formato 'safe' per il Web [RFC 4648](https://www.rfc-editor.org/rfc/rfc4648#section-5). |

`ContainsRegex()` e `MatchesRegex()` assumono la proprietà dell'oggetto `RE`. Usano la sintassi delle espressioni regolari definita [qui](../advanced.md#regular-expression-syntax). Tutti questi matcher, tranne `ContainsRegex()` e `MatchesRegex()` funzionano anche per stringhe "wide".

## Matcher di Contenitori

La maggior parte dei contenitori in stile STL supportano `==`, quindi si può usare `Eq(expected_container)` o semplicemente `expected_container` per match-are esattamente un contenitore. Per scrivere gli elementi in linea, abbinarli in modo più flessibile o ricevere messaggi più informativi, si possono utilizzare:

| Matcher | Descrizione |
| :---------------------------------------- | :------------------------------- |
| `BeginEndDistanceIs(m)` | `argument` è un contenitore i cui iteratori `begin()` e `end()` sono separati da un numero di incrementi pari a `m`. Per esempio `BeginEndDistanceIs(2)` o `BeginEndDistanceIs(Lt(2))`. Per i contenitori che definiscono un metodo `size()`, `SizeIs(m)` potrebbe essere più efficiente. |
| `ContainerEq(container)` | Lo stesso di `Eq(container)` tranne per il fatto che il messaggio di errore include anche quali elementi si trovano in un contenitore ma non nell'altro. |
| `Contains(e)` | `argument` contiene un elemento che corrisponde a `e`, che può essere un valore o un matcher. |
| `Contains(e).Times(n)` | `argument` contiene elementi che corrispondono a `e`, che può essere un valore o un matcher, e il numero di corrispondenze è `n`, che può essere un valore o un matcher. A differenza dei semplici `Contains` e `Each` questo consente di verificare la presenza di occorrenze arbitrarie, incluso il test per l'assenza con `Contains(e).Times(0)`. |
| `Each(e)` | `argument` è un contenitore in cui *ogni* elemento corrisponde a `e`, che può essere un valore o un matcher. |
| `ElementsAre(e0, e1, ..., en)` | `argument` ha `n + 1` elementi, dove l'*i*-esimo elemento corrisponde a `ei`, che può essere un valore o un matcher. |
| `ElementsAreArray({e0, e1, ..., en})`, `ElementsAreArray(a_container)`, `ElementsAreArray(begin, end)`, `ElementsAreArray(array)`, o `ElementsAreArray(array, count)` | Lo stesso di `ElementsAre()` tranne per il fatto che gli elementi valori/matcher attesi provengono da una lista di inizializzatori, un contenitore in stile STL, un iteratore range o da un array in stile C. |
| `IsEmpty()` | `argument` è un contenitore vuoto (`container.empty()`). |
| `IsSubsetOf({e0, e1, ..., en})`, `IsSubsetOf(a_container)`, `IsSubsetOf(begin, end)`, `IsSubsetOf(array)` o `IsSubsetOf(array, count)` | `argument` corrisponde a `UnorderedElementsAre(x0, x1, ..., xk)` per qualche sottoinsieme `{x0, x1, ..., xk}` dei matcher attesi. |
| `IsSupersetOf({e0, e1, ..., en})`, `IsSupersetOf(a_container)`, `IsSupersetOf(begin, end)`, `IsSupersetOf(array)` o `IsSupersetOf(array, count)` | Alcuni sottoinsiemi di `argument` corrispondono a `UnorderedElementsAre(`matcher attesi`)`. |
| `Pointwise(m, container)`, `Pointwise(m, {e0, e1, ..., en})` | `argument` contiene lo stesso numero di elementi di `container` e per tutti gli i, (l'i-esimo elemento in `argument`, l'i-esimo elemento `container`) corrisponde a `m`, che è un matcher su delle 2-tuple. Per esempio `Pointwise(Le(), upper_bounds)` verifica che ciascun elemento in `argument` non superi l'elemento corrispondente in `upper_bounds`. Maggiori dettagli di seguito. |
| `SizeIs(m)` | `argument` è un contenitore la cui dimensione corrisponde a `m`. Per esempio `SizeIs(2)` o `SizeIs(Lt(2))`. |
| `UnorderedElementsAre(e0, e1, ..., en)` | `argument` ha `n + 1` elementi e, con *qualche* permutazione degli elementi, ogni elemento corrisponde a `ei` (per un diverso `i`), che può essere un valore o un matcher. |
| `UnorderedElementsAreArray({e0, e1, ..., en})`, `UnorderedElementsAreArray(a_container)`, `UnorderedElementsAreArray(begin, end)`, `UnorderedElementsAreArray(array)` o `UnorderedElementsAreArray(array, count)` | Lo stesso di `UnorderedElementsAre()` tranne per il fatto che gli elementi valori/matcher attesi provengono da una lista di inizializzatori, un contenitore in stile STL, un iteratore range o da un array in stile C.
 |
| `UnorderedPointwise(m, container)`, `UnorderedPointwise(m, {e0, e1, ..., en})` | Come `Pointwise(m, container)`, ma ignora l'ordine degli elementi. |
| `WhenSorted(m)` | Quando `argument` viene ordinato utilizzando l'operatore `<`, corrisponde al matcher contenitore `m`. Per esempio `WhenSorted(ElementsAre(1, 2, 3))` verifica che `argument` contenga gli elementi 1, 2 e 3, ignorando l'ordine. |
| `WhenSortedBy(comparator, m)` | Uguale a `WhenSorted(m)`, tranne per il fatto che il comparatore indicato invece di `<` viene utilizzato per ordinare `argument`. Per esempio `WhenSortedBy(std::greater(), ElementsAre(3, 2, 1))`. |

**Note:**

*   Questi matcher possono anche corrispondere a:
    1.  a native array passed by reference (e.g. in `Foo(const int (&a)[5])`),
            e
    2.  un array passato come puntatore e un conteggio (ad esempio in `Bar(const T* buffer, int len)` -- vedere [Matcher Multi-argomento](#MultiArgMatchers)).
*   The array being matched may be multi-dimensional (i.e. its elements can be
    arrays).
*   `m` in `Pointwise(m, ...)` and `UnorderedPointwise(m, ...)` should be a
    matcher for `::std::tuple<T, U>` where `T` and `U` are the element type of
    the actual container and the expected container, respectively. Per esempio,
    to compare two `Foo` containers where `Foo` doesn't support `operator==`,
    one might write:

    ```cpp
    MATCHER(FooEq, "") {
      return std::get<0>(arg).Equals(std::get<1>(arg));
    }
    ...
    EXPECT_THAT(actual_foos, Pointwise(FooEq(), expected_foos));
    
    ```

## Matcher di Membri

| Matcher | Descrizione |
| :------------------------------ | :----------------------------------------- |
| `Field(&class::field, m)` | `argument.field` (o `argument->field` quando `argument` è un puntatore semplice) corrisponde al matcher `m`, dove `argument` è un oggetto di tipo _class_. |
| `Field(field_name, &class::field, m)` | Uguale alla versione a due parametri, ma fornisce un messaggio di errore migliore. |
| `Key(e)` | `argument.first` corrisponde a `e`, che può essere un valore o un matcher. Perr esempio `Contains(Key(Le(5)))` può verificare che una `map` contenga una chiave `<= 5`. |
| `Pair(m1, m2)` | `argument` è una `std::pair` il cui `primo` campo corrisponde a `m1` e il `secondo` campo corrisponde a `m2`. |
| `FieldsAre(m...)` | `argument` è un oggetto compatibile in cui ogni campo corrisponde a pezzi con i matcher `m...`. Un oggetto compatibile è qualsiasi oggetto che supporti il protocollo `std::tuple_size<Obj>`+`get<I>(obj)`. In C++17 e versioni successive supporta anche tipi compatibili con 'binding' strutturate, come gli aggregati. |
| `Property(&class::property, m)` | `argument.property()` (o `argument->property()` quando `argument` è un puntatore semplice) corrisponde al matcher `m`, dove `argument` è un oggetto di tipo _class_. Il metodo `property()` non deve accettare argomenti ed essere dichiarato come `const`. |
| `Property(property_name, &class::property, m)` | Uguale alla versione a due parametri, ma fornisce un messaggio di errore migliore. |

**Note:**

*   You can use `FieldsAre()` to match any type that supports structured
    bindings, such as `std::tuple`, `std::pair`, `std::array`, and aggregate
    types. Per esempio:

    ```cpp
    std::tuple<int, std::string> my_tuple{7, "hello world"};
    EXPECT_THAT(my_tuple, FieldsAre(Ge(0), HasSubstr("hello")));
    struct MyStruct {
      int value = 42;
      std::string greeting = "aloha";
    };
    MyStruct s;
    EXPECT_THAT(s, FieldsAre(42, "aloha"));
    
    ```

*   Don't use `Property()` against member functions that you do not own, because
    taking addresses of functions is fragile and generally not part of the
    contract of the function.

## Corrispondenza del Risultato di una Funzione, Funtore o Callback

| Matcher | Descrizione |
| :--------------- | :------------------------------------------------ |
| `ResultOf(f, m)` | `f(argument)` corrisponde al matcher `m`, dove `f` è una funzione o un funtore. |
| `ResultOf(result_description, f, m)` | Uguale alla versione a due parametri, ma fornisce un messaggio di errore migliore. |

## Matcher di Puntatori

| Matcher | Descrizione |
| :------------------------ | :---------------------------------------------- |
| `Address(m)` | il risultato di `std::addressof(argument)` corrisponde a `m`. |
| `Pointee(m)` | `argument` (un puntatore intelligente o un puntatore semplice) punta a un valore che corrisponde al matcher `m`. |
| `Pointer(m)` | `argument` (un puntatore intelligente o un puntatore semplice) contiene un puntatore che corrisponde a `m`. `m` corrisponderà al puntatore semplice indipendentemente dal tipo di `argument`. |
| `WhenDynamicCastTo<T>(m)` | quando `argument` viene passato attraverso `dynamic_cast<T>()`, corrisponde al matcher `m`. |

## Matcher Multi-argomento {#MultiArgMatchers}

Tecnicamente, tutti i matcher corrispondono a un *singolo* valore. Un matcher"multi-argomento" è semplicemente quello che corrisponde a una *tupla*. I seguenti matcher possono essere utilizzati per corrispondere a una tupla `(x, y)`:

| Matcher | Descrizione |
:------ | :----------
| `Eq()` | `x == y` |
| `Ge()` | `x >= y` |
| `Gt()` | `x > y` |
| `Le()` | `x <= y` |
| `Lt()` | `x < y` |
| `Ne()` | `x != y` |

Si possono utilizzare i seguenti selettori per scegliere un sottoinsieme di argomenti (o riordinarli) per partecipare alla corrispondenza:

| Matcher | Descrizione |
| :------------------------- | :---------------------------------------------- |
| `AllArgs(m)` | Equivalente a `m`. Utile come "zucchero" sintattico in `.With(AllArgs(m))`. |
| `Args<N1, N2, ..., Nk>(m)` | La tupla degli argomenti `k` selezionati (utilizzando indici a base 0) corrisponde a `m`, ad es. `Args<1, 2>(Eq())`. |

## Matcher Compositi

Si possono creare un matcher da uno o più altri matcher:


| Matcher | Descrizione |
| :------------------------------- | :-------------------------------------- |
| `AllOf(m1, m2, ..., mn)` | `argument` corrisponde a tutti i matcher da `m1` a `mn`. |
| `AllOfArray({m0, m1, ..., mn})`, `AllOfArray(a_container)`, `AllOfArray(begin, end)`, `AllOfArray(array)` o `AllOfArray(array, count)` | Lo stesso di `AllOf()` tranne per il fatto che i matcher provengono da un elenco di inizializzatori, da una lista di inizializzatori, un contenitore in stile STL, un iteratore range o da un array in stile C. |
| `AnyOf(m1, m2, ..., mn)` | `argument` corrisponde ad almeno uno dei matcher da `m1` a `mn`. |
| `AnyOfArray({m0, m1, ..., mn})`, `AnyOfArray(a_container)`, `AnyOfArray(begin, end)`, `AnyOfArray(array)` o `AnyOfArray(array, count)` | Lo stesso di `AnyOf()` tranne per il fatto che i matcher provengono da un elenco di inizializzatori, da una lista di inizializzatori, un contenitore in stile STL, un iteratore range o da un array in stile C. |
| `Not(m)` | `argument` non corrisponde al matcher `m`. |
| `Conditional(cond, m1, m2)` | Corrisponde al matcher `m1` se `cond` restituisce true, altrimenti corrisponde a `m2`. |

## Adattatori per i Matcher

| Matcher | Descrizione |
| :---------------------- | :------------------------------------ |
| `MatcherCast<T>(m)` | cast del matcher `m` nel tipo `Matcher<T>`. |
| `SafeMatcherCast<T>(m)` | [cast in modo sicuro](../gmock_cook_book.md#SafeMatcherCast) il matcher `m` nel tipo `Matcher<T>`. |
| `Truly(predicate)` | `predicate(argument)` restituisce qualcosa considerato true dal C++, dove `predicate` è una funzione o un funtore. |

`AddressSatisfies(callback)` e `Truly(callback)` prendono la proprietà di `callback`, che deve essere una callback permanente.

## Uso dei Matcher come Predicati {#MatchersAsPredicatesCheat}

| Matcher | Descrizione |
| :---------------------------- | :------------------------------------------ |
| `Matches(m)(value)` | restituisce `true` se `value` corrisponde a `m`. Si può usare `Matches(m)` da solo come funtore unario. |
| `ExplainMatchResult(m, value, result_listener)` | restituisce `true` se `value` corrisponde a `m`, spiegando il risultato a `result_listener`. |
| `Value(value, m)` | restituisce `true` se `value` corrisponde a `m`. |

## Definizione dei Matcher

| Macro | Descrizione |
| :----------------------------------- | :------------------------------------ |
| `MATCHER(IsEven, "") { return (arg % 2) == 0; }` | Definisce un matcher `IsEven()` per abbinare un numero pari. |
| `MATCHER_P(IsDivisibleBy, n, "") { *result_listener << "where the remainder is " << (arg % n); return (arg % n) == 0; }` | Definisce un matcher `IsDivisibleBy(n)` per trovare la corrispondenza con un numero divisibile per `n`. |
| `MATCHER_P2(IsBetween, a, b, absl::StrCat(negation ? "isn't" : "is", " between ", PrintToString(a), " and ", PrintToString(b))) { return a <= arg && arg <= b; }` | Definisce un matcher `IsBetween(a, b)` per far corrispondere un valore nell'intervallo [`a`, `b`]. |

**Note:**

1.  Le macro `MATCHER*` non possono essere utilizzate all'interno di una funzione o di una classe.
2.  The matcher body must be *purely functional* (i.e. it cannot have any side
    effect, and the result must not depend on anything other than the value
    being matched and the matcher parameters).
3.  You can use `PrintToString(x)` to convert a value `x` of any type to a
    string.
4.  You can use `ExplainMatchResult()` in a custom matcher to wrap another
    matcher, for example:

    ```cpp
    MATCHER_P(NestedPropertyMatches, matcher, "") {
      return ExplainMatchResult(matcher, arg.nested().property(), result_listener);
    }
    
    ```

5.  Si può usare `DescribeMatcher<>` per descrivere un altro matcher. Per esempio:

    ```cpp
    MATCHER_P(XAndYThat, matcher,
              "X that " + DescribeMatcher<int>(matcher, negation) +
                  (negation ? " or" : " and") + " Y that " +
                  DescribeMatcher<double>(matcher, negation)) {
      return ExplainMatchResult(matcher, arg.x(), result_listener) &&
             ExplainMatchResult(matcher, arg.y(), result_listener);
    }
    
    ```
