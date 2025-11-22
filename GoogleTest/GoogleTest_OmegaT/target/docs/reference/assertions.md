# Riferimenti sulle Asserzioni

Questa pagina elenca le macro di asserzione fornite da GoogleTest per verificare il comportamento del codice. Per usarle, si aggiunge `#include <gtest/gtest.h>`.

La maggior parte delle macro elencate di seguito vengono fornite in coppia con una variante `EXPECT_` e una `ASSERT_`. In caso di errore, le macro `EXPECT_` generano errori nonfatal e consentono alla funzione corrente di continuare l'esecuzione, mentre le macro `ASSERT_` generano errori irreversibili e interrompono la funzione corrente.

Tutte le macro di asserzione supportano lo streaming di un messaggio di errore personalizzato con l'operatore `<<`, ad esempio:

```cpp
EXPECT_TRUE(my_condition) << "My condition is not true";

```

Tutto ciò che può essere inviato in streaming a un `ostream` può essere inviato in streaming a una macro di asserzione, in particolare le stringhe C e gli oggetti stringa. Se una stringa wide (`wchar_t*`, `TCHAR*` in modalità `UNICODE` su Windows, o `std::wstring`) viene inviata in streaming a un'asserzione, verrà tradotto in UTF-8 una volta stampato.

## Successo e Fallimento Espliciti {#success-failure}

Le asserzioni in questa sezione generano direttamente un successo o un fallimento invece di testare un valore o un'espressione. Questi sono utili quando il flusso di controllo, piuttosto che un'espressione booleana, determina il successo o il fallimento del test, come mostrato nell'esempio seguente:

```c++
switch(expression) {
  case 1:
    ... some checks ...
  case 2:
    ... some other checks ...
  default:
    FAIL() << "We shouldn't get here.";
}

```

### SUCCEED {#SUCCEED}

`SUCCEED()`

Genera un successo. Ciò *non* fa sì che il test complessivo abbia successo. Un test è considerato riuscito solo se nessuna delle sue asserzioni fallisce durante la sua esecuzione.

L'asserzione `SUCCEED` è puramente documentaria e attualmente non genera alcun output visibile all'utente. Tuttavia, in futuro potremmo aggiungere messaggi `SUCCEED` all'output di GoogleTest.

### FAIL {#FAIL}

`FAIL()`

Genera un errore fatale, che ritorna dalla funzione corrente.

Può essere utilizzato solo nelle funzioni che restituiscono `void`. Vedere [Posizionamento delle Asserzioni](../advanced.md#assertion-placement) per ulteriori informazioni.

### ADD_FAILURE {#ADD_FAILURE}

`ADD_FAILURE()`

Genera un errore nonfatal, che consente alla funzione corrente di continuare a funzionare.

### ADD_FAILURE_AT {#ADD_FAILURE_AT}

`ADD_FAILURE_AT(`*`file_path`*`,`*`line_number`*`)`

Genera un errore nonfatal nel file e nel numero di riga specificati.

## Asserzione Generalizzata {#generalized}

La seguente asserzione consente di utilizzare i [matcher](matchers.md) per verificare i valori.

### EXPECT_THAT {#EXPECT_THAT}

`EXPECT_THAT(`*`value`*`,`*`matcher`*`)` \
`ASSERT_THAT(`*`value`*`,`*`matcher`*`)`

Verifica che il *`value`* corrisponda al [matcher](matchers.md) *`corrispondente`*.

Ad esempio, il codice seguente verifica che la stringa `value1` inizi con `"Hello"`, che `value2` corrisponda a un'espressione regolare e `value3` sia compreso tra 5 e 10:

```cpp
#include <gmock/gmock.h>
using ::testing::AllOf;
using ::testing::Gt;
using ::testing::Lt;
using ::testing::MatchesRegex;
using ::testing::StartsWith;
...
EXPECT_THAT(value1, StartsWith("Hello"));
EXPECT_THAT(value2, MatchesRegex("Line \\d+"));
ASSERT_THAT(value3, AllOf(Gt(5), Lt(10)));

```

I matcher consentono alle asserzioni di questo modulo di leggere l'inglese e generare messaggi informativi di errore. Ad esempio, se l'asserzione precedente su `value1` fallisce, il messaggio risultante sarà simile al seguente:

```
Value of: value1
  Actual: "Hi, world!"
Expected: starts with "Hello"

```

GoogleTest fornisce una libreria nativa di matcher: consultare i [Riferimenti ai Matcher](matchers.md). È anche possibile scrivere i propri matcher: vedere [Scrivere Rapidamente Nuovi Matcher](../gmock_cook_book.md#NewMatchers).
L'uso dei matcher rende `EXPECT_THAT` un'asserzione potente ed estensibile.

*L'idea per questa asserzione è stata presa in prestito dal progetto Hamcrest di Joe Walnes, che aggiunge `assertThat()` a JUnit.*

## Condizioni Booleane {#boolean}

Le seguenti asserzioni verificano le condizioni Booleane.

### EXPECT_TRUE {#EXPECT_TRUE}

`EXPECT_TRUE(`*`condition`*`)` \
`ASSERT_TRUE(`*`condition`*`)`

Verifica che *`condition`* sia true.

### EXPECT_FALSE {#EXPECT_FALSE}

`EXPECT_FALSE(`*`condition`*`)` \
`ASSERT_FALSE(`*`condition`*`)`

Verifica che *`condition`* sia false.

## Confronti Binari {#binary-comparison}

Le seguenti asserzioni confrontano due valori. Gli argomenti del valore devono essere confrontabili dall'operatore di confronto dell'asserzione, altrimenti si verificherà un errore del compilatore.

Se un argomento supporta l'operatore `<<`, verrà chiamato per stampare l'argomento quando l'asserzione fallisce. Altrimenti, GoogleTest tenterà di stamparli nel miglior modo possibile: vedere [Insegnare a GoogleTest Come Stampare i Propri Valori](../advanced.md#teaching-googletest-how-to-print-your-values).

Gli argomenti vengono sempre valutati esattamente una volta, quindi va bene che abbiano effetti collaterali. Tuttavia, l'ordine di valutazione degli argomenti non è definito e i programmi non dovrebbero dipendere da alcun particolare ordine di valutazione degli argomenti.

Queste asserzioni funzionano sia con oggetti stringa "narrow" che "wide" (`string` e `wstring`).

Consultare anche le asserzioni di [Confronto in Virgola Mobile](#floating-point) per confrontare numeri in virgola evitando problemi causati dall'arrotondamento.

### EXPECT_EQ {#EXPECT_EQ}

`EXPECT_EQ(`*`val1`*`,`*`val2`*`)` \
`ASSERT_EQ(`*`val1`*`,`*`val2`*`)`

Verifica che *`val1`*`==`*`val2`*.

Fa l'uguaglianza dei puntatori sui puntatori. Se utilizzato su due stringhe C, verifica se si trovano nella stessa posizione di memoria, non se hanno lo stesso valore. Usare [`EXPECT_STREQ`](#EXPECT_STREQ) per confrontare stringhe C (ad esempio `const char*`) per valore.

Quando si confronta un puntatore con `NULL`, si usa `EXPECT_EQ(`*`ptr`*`, nullptr)` anziché `EXPECT_EQ(`*`ptr`*`, NULL)`.

### EXPECT_NE {#EXPECT_NE}

`EXPECT_NE(`*`val1`*`,`*`val2`*`)` \
`ASSERT_NE(`*`val1`*`,`*`val2`*`)`

Verifica che *`val1`*`!=`*`val2`*.

Fa l'uguaglianza dei puntatori sui puntatori. Se utilizzato su due stringhe C, verifica se si trovano in posizioni di memoria diverse, non se hanno valori diversi. Usare [`EXPECT_STRNE`](#EXPECT_STRNE) per confrontare stringhe C (ad esempio `const char*`) per valore.

Confrontando un puntatore con `NULL`, si usa `EXPECT_NE(`*`ptr`*`, nullptr)` anziché `EXPECT_NE(`*`ptr`*`, NULL)`.

### EXPECT_LT {#EXPECT_LT}

`EXPECT_LT(`*`val1`*`,`*`val2`*`)` \
`ASSERT_LT(`*`val1`*`,`*`val2`*`)`

Verifica che *`val1`*`<`*`val2`*.

### EXPECT_LE {#EXPECT_LE}

`EXPECT_LE(`*`val1`*`,`*`val2`*`)` \
`ASSERT_LE(`*`val1`*`,`*`val2`*`)`

Verifica che *`val1`*`<=`*`val2`*.

### EXPECT_GT {#EXPECT_GT}

`EXPECT_GT(`*`val1`*`,`*`val2`*`)` \
`ASSERT_GT(`*`val1`*`,`*`val2`*`)`

Verifica che *`val1`*`>`*`val2`*.

### EXPECT_GE {#EXPECT_GE}

`EXPECT_GE(`*`val1`*`,`*`val2`*`)` \
`ASSERT_GE(`*`val1`*`,`*`val2`*`)`

Verifica che *`val1`*`>=`*`val2`*.

## Confronto tra Stringhe {#c-strings}

Le seguenti asserzioni confrontano due **stringhe C**. Per confrontare due oggetti `string`, si usa invece [`EXPECT_EQ`](#EXPECT_EQ) o [`EXPECT_NE`](#EXPECT_NE).

Queste asserzioni accettano anche stringhe C "wide" (`wchar_t*`). Se il confronto tra due stringhe wide fallisce, i relativi valori verranno stampati come stringhe narrow UTF-8.

Per confrontare una stringa C con `NULL`, si usa `EXPECT_EQ(`*`c_string`*`, nullptr)` o `EXPECT_NE(`*`c_string`*`, nullptr)`.

### EXPECT_STREQ {#EXPECT_STREQ}

`EXPECT_STREQ(`*`str1`*`,`*`str2`*`)` \
`ASSERT_STREQ(`*`str1`*`,`*`str2`*`)`

Verifica che due stringhe C *`str1`* e *`str2`* abbiano lo stesso contenuto.

### EXPECT_STRNE {#EXPECT_STRNE}

`EXPECT_STRNE(`*`str1`*`,`*`str2`*`)` \
`ASSERT_STRNE(`*`str1`*`,`*`str2`*`)`

Verifica che due stringhe C *`str1`* e *`str2`* abbiano contenuto diverso.

### EXPECT_STRCASEEQ {#EXPECT_STRCASEEQ}

`EXPECT_STRCASEEQ(`*`str1`*`,`*`str2`*`)` \
`ASSERT_STRCASEEQ(`*`str1`*`,`*`str2`*`)`

Verifica che due stringhe C *`str1`* e *`str2`* abbiano lo stesso contenuto, ignorando maiuscole e minuscole.

### EXPECT_STRCASENE {#EXPECT_STRCASENE}

`EXPECT_STRCASENE(`*`str1`*`,`*`str2`*`)` \
`ASSERT_STRCASENE(`*`str1`*`,`*`str2`*`)`

Verifica che due stringhe C *`str1`* e *`str2`* abbiano contenuto diverso, ignorando maiuscole e minuscole.

## Confronto in Virgola Mobile {#floating-point}

Le seguenti asserzioni confrontano due valori a virgola mobile.

A causa degli errori di arrotondamento, è molto improbabile che due valori in virgola mobile corrispondano esattamente, quindi `EXPECT_EQ` non è adatta. In generale, affinché il confronto in virgola mobile abbia senso, l'utente deve scegliere con attenzione il limite dell'errore.

GoogleTest fornisce inoltre asserzioni che utilizzano un limite di errore predefinito basato sulle Unità nell'Ultimo Posto [Units in the Last Place] (ULP). Per ulteriori informazioni sugli ULP, consultare l'articolo [Confronto tra Numeri in Virgola Mobile](https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/).

### EXPECT_FLOAT_EQ {#EXPECT_FLOAT_EQ}

`EXPECT_FLOAT_EQ(`*`val1`*`,`*`val2`*`)` \
`ASSERT_FLOAT_EQ(`*`val1`*`,`*`val2`*`)`

Verifica che i due valori `float` *`val1`* e *`val2`* siano approssimativamente uguali, entro 4 ULP l'uno dall'altro.

### EXPECT_DOUBLE_EQ {#EXPECT_DOUBLE_EQ}

`EXPECT_DOUBLE_EQ(`*`val1`*`,`*`val2`*`)` \
`ASSERT_DOUBLE_EQ(`*`val1`*`,`*`val2`*`)`

Verifica che i due valori `double` *`val1`* e *`val2`* siano approssimativamente uguali, entro 4 ULP l'uno dall'altro.

### EXPECT_NEAR {#EXPECT_NEAR}

`EXPECT_NEAR(`*`val1`*`,`*`val2`*`,`*`abs_error`*`)` \
`ASSERT_NEAR(`*`val1`*`,`*`val2`*`,`*`abs_error`*`)`

Verifica che la differenza tra *`val1`* e *`val2`* non superi il limite di errore assoluto *`abs_error`*.

## Asserzioni di Eccezioni {#exceptions}

Le seguenti asserzioni verificano che una parte di codice lanci o non lanci un'eccezione. L'utilizzo richiede che le eccezioni siano abilitate nell'ambiente di compilazione.

Notare che la parte di codice da testare può essere un'istruzione composta, ad esempio:

```cpp
EXPECT_NO_THROW({
  int n = 5;
  DoSomething(&n);
});

```

### EXPECT_THROW {#EXPECT_THROW}

`EXPECT_THROW(`*`statement`*`,`*`exception_type`*`)` \
`ASSERT_THROW(`*`statement`*`,`*`exception_type`*`)`

Verifica che *`statement`* generi un'eccezione di tipo *`exception_type`*.

### EXPECT_ANY_THROW {#EXPECT_ANY_THROW}

`EXPECT_ANY_THROW(`*`statement`*`)` \
`ASSERT_ANY_THROW(`*`statement`*`)`

Verifica che *`statement`* generi un'eccezione di qualsiasi tipo.

### EXPECT_NO_THROW {#EXPECT_NO_THROW}

`EXPECT_NO_THROW(`*`statement`*`)` \
`ASSERT_NO_THROW(`*`statement`*`)`

Verifica che *`statement`* non generi alcuna eccezione.

## Asserzioni sui Predicati {#predicates}

Le seguenti affermazioni consentono di verificare predicati più complessi e stampano un messaggio di errore più chiaro rispetto a quando si usa il solo `EXPECT_TRUE`.

### EXPECT_PRED* {#EXPECT_PRED}

`EXPECT_PRED1(`*`pred`*`,`*`val1`*`)` \
`EXPECT_PRED2(`*`pred`*`,`*`val1`*`,`*`val2`*`)` \
`EXPECT_PRED3(`*`pred`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`)` \
`EXPECT_PRED4(`*`pred`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`,`*`val4`*`)` \
`EXPECT_PRED5(`*`pred`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`,`*`val4`*`,`*`val5`*`)`

`ASSERT_PRED1(`*`pred`*`,`*`val1`*`)` \
`ASSERT_PRED2(`*`pred`*`,`*`val1`*`,`*`val2`*`)` \
`ASSERT_PRED3(`*`pred`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`)` \
`ASSERT_PRED4(`*`pred`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`,`*`val4`*`)` \
`ASSERT_PRED5(`*`pred`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`,`*`val4`*`,`*`val5`*`)`

Verifica che il predicato *`pred`* restituisca `true`quando vengono passati i valori specificati come argomenti.

Il parametro *`pred`* è una funzione o un funtore che accetta tanti argomenti quanti sono i valori accettati dalla macro corrispondente. Se *`pred`* restituisce `true` per gli argomenti forniti, l'asserzione ha successo, altrimenti fallisce.

Quando l'asserzione fallisce, stampa il valore di ciascun argomento. Gli argomenti vengono sempre valutati esattamente una volta.

Ad esempio, vedere il seguente codice:

```cpp
// Restituisce true se m e n non hanno divisori comuni tranne 1.
bool MutuallyPrime(int m, int n) { ... }
...
const int a = 3;
const int b = 4;
const int c = 10;
...
EXPECT_PRED2(MutuallyPrime, a, b);  // Successo
EXPECT_PRED2(MutuallyPrime, b, c);  // Fallisce

```

Nell'esempio precedente, la prima asserzione ha esito positivo e la seconda fallisce con il seguente messaggio:

```
MutuallyPrime(b, c) is false, where
b is 4
c is 10

```

Si noti che se il predicato fornito è l'overload di una funzione o un funzione template, la macro di asserzione potrebbe non essere in grado di determinare quale versione utilizzare e potrebbe essere necessario specificare esplicitamente il tipo della funzione.
Ad esempio, per l'overload di una funzione booleana `IsPositive()` per accettare un singolo argomento `int` o `double`, sarebbe necessario scrivere uno dei seguenti:

```cpp
EXPECT_PRED1(static_cast<bool (*)(int)>(IsPositive), 5);
EXPECT_PRED1(static_cast<bool (*)(double)>(IsPositive), 3.14);

```

Scrivere semplicemente `EXPECT_PRED1(IsPositive, 5);` comporterebbe un errore del compilatore.
Allo stesso modo, per utilizzare una funzione template, specificare gli argomenti template:

```cpp
template <typename T>
bool IsNegative(T x) {
  return x < 0;
}
...
EXPECT_PRED1(IsNegative<int>, -5);  // È necessario specificare il tipo per IsNegative

```

Se un template ha più parametri, il predicato va racchiuso tra parentesi in modo che gli argomenti della macro vengano analizzati correttamente:

```cpp
ASSERT_PRED2((MyPredicate<int, int>), 5, 0);
```

### EXPECT_PRED_FORMAT* {#EXPECT_PRED_FORMAT}

`EXPECT_PRED_FORMAT1(`*`pred_formatter`*`,`*`val1`*`)` \
`EXPECT_PRED_FORMAT2(`*`pred_formatter`*`,`*`val1`*`,`*`val2`*`)` \
`EXPECT_PRED_FORMAT3(`*`pred_formatter`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`)` \
`EXPECT_PRED_FORMAT4(`*`pred_formatter`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`,`*`val4`*`)`
\
`EXPECT_PRED_FORMAT5(`*`pred_formatter`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`,`*`val4`*`,`*`val5`*`)`

`ASSERT_PRED_FORMAT1(`*`pred_formatter`*`,`*`val1`*`)` \
`ASSERT_PRED_FORMAT2(`*`pred_formatter`*`,`*`val1`*`,`*`val2`*`)` \
`ASSERT_PRED_FORMAT3(`*`pred_formatter`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`)` \
`ASSERT_PRED_FORMAT4(`*`pred_formatter`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`,`*`val4`*`)`
\
`ASSERT_PRED_FORMAT5(`*`pred_formatter`*`,`*`val1`*`,`*`val2`*`,`*`val3`*`,`*`val4`*`,`*`val5`*`)`

Verifica che il predicato *`pred_formatter`* abbia esito positivo quando vengono passati i valori specificati come argomenti.

Il parametro *`pred_formatter`* è un *predicate-formatter*, che è una funzione o un funtore con la firma:

```cpp
testing::AssertionResult PredicateFormatter(const char* expr1,
                                            const char* expr2,
                                            ...
                                            const char* exprn,
                                            T1 val1,
                                            T2 val2,
                                            ...
                                            Tn valn);

```

dove *`val1`*, *`val2`*, ..., *`valn`* sono i valori degli argomenti del predicato e *`expr1`*, *`expr2`*, ..., *`exprn`* sono le espressioni corrispondenti così come appaiono nel codice sorgente. I tipi `T1`, `T2`, ..., `Tn` possono essere tipi valore o tipi riferimento; se un argomento è di tipo `T`, può essere dichiarato come `T` o come `const T&`, a seconda di quale sia appropriato. Per ulteriori informazioni sul tipo `testing::AssertionResult` restituito, vedere [Utilizzo di una Funzione che Restituisce un AssertionResult](../advanced.md#using-a-function-that-returns-an-assertionresult).

Ad esempio, vedere il seguente codice:

```cpp
// Restituisce il più piccolo divisore primo comune di m e n,
// oppure 1 quando m e n sono reciprocamente primi.
int SmallestPrimeCommonDivisor(int m, int n) { ... }
// Returns true if m and n have no common divisors except 1.
bool MutuallyPrime(int m, int n) { ... }
// A predicate-formatter for asserting that two integers are mutually prime.
testing::AssertionResult AssertMutuallyPrime(const char* m_expr,
                                             const char* n_expr,
                                             int m,
                                             int n) {
  if (MutuallyPrime(m, n)) return testing::AssertionSuccess();
  return testing::AssertionFailure() << m_expr << " and " << n_expr
      << " (" << m << " and " << n << ") are not mutually prime, "
      << "as they have a common divisor " << SmallestPrimeCommonDivisor(m, n);
}
...
const int a = 3;
const int b = 4;
const int c = 10;
...
EXPECT_PRED_FORMAT2(AssertMutuallyPrime, a, b);  // Successo
EXPECT_PRED_FORMAT2(AssertMutuallyPrime, b, c);  // Fallisce

```

Nell'esempio precedente, l'asserzione finale fallisce e il predicate-formatter produce il seguente messaggio di errore:

```
b and c (4 and 10) are not mutually prime, as they have a common divisor 2

```

## Asserzioni su HRESULT di Windows {#HRESULT}

Le seguenti asserzioni verificano il successo o il fallimento di `HRESULT`. Per esempio:

```cpp
CComPtr<IShellDispatch2> shell;
ASSERT_HRESULT_SUCCEEDED(shell.CoCreateInstance(L"Shell.Application"));
CComVariant empty;
ASSERT_HRESULT_SUCCEEDED(shell->ShellExecute(CComBSTR(url), empty, empty, empty, empty));

```

L'output generato contiene il messaggio di errore leggibile associato al codice `HRESULT` restituito.

### EXPECT_HRESULT_SUCCEEDED {#EXPECT_HRESULT_SUCCEEDED}

`EXPECT_HRESULT_SUCCEEDED(`*`expression`*`)` \
`ASSERT_HRESULT_SUCCEEDED(`*`expression`*`)`


Verifica che *`expression`* sia un `HRESULT` di successo.

### EXPECT_HRESULT_FAILED {#EXPECT_HRESULT_FAILED}

`EXPECT_HRESULT_FAILED(`*`expression`*`)` \
`ASSERT_HRESULT_FAILED(`*`expression`*`)`


Verifica che *`expression`* sia un `HRESULT` di fallimento.

## Asserzioni Death {#death}

Le seguenti asserzioni verificano che un pezzo di codice causi la terminazione del processo. Per il contesto, consultare [I Death Test](../advanced.md#death-tests).

Queste asserzioni generano [spawn] un nuovo processo ed eseguono il codice in prova in quel processo. Il modo in cui ciò accade dipende dalla piattaforma e dalla variabile `::testing::GTEST_FLAG(death_test_style)`, che viene inizializzata dal flag della riga di comando `--gtest_death_test_style`.

*   On POSIX systems, `fork()` (or `clone()` on Linux) is used to spawn the
    child, after which:
    *   If the variable's value is `"fast"`, the death test statement is
            immediately executed.
    *   If the variable's value is `"threadsafe"`, the child process re-executes
            the unit test binary just as it was originally invoked, but with some
            extra flags to cause just the single death test under consideration to
            be run.
*   On Windows, the child is spawned using the `CreateProcess()` API, and
    re-executes the binary to cause just the single death test under
    consideration to be run - much like the `"threadsafe"` mode on POSIX.

Altri valori per la variabile sono illegali e causeranno il fallimento del death test.
Attualmente, il valore di default del flag è **`"fast"`**.

Se l'istruzione del death test viene completata senza 'morire, il processo figlio terminerà comunque e l'asserzione fallirà.

Notare che la parte di codice da testare può essere un'istruzione composta, ad esempio:

```cpp
EXPECT_DEATH({
  int n = 5;
  DoSomething(&n);
}, "Error on line .* of DoSomething()");

```

### EXPECT_DEATH {#EXPECT_DEATH}

`EXPECT_DEATH(`*`statement`*`,`*`matcher`*`)` \
`ASSERT_DEATH(`*`statement`*`,`*`matcher`*`)`

Verifica che *`statement`* provochi la terminazione del processo con uno stato di uscita diverso da zero e produca un output `stderr` che corrisponde al *`matcher`*.

Il parametro *`matcher`* è un [matcher](matchers.md) per una `const std::string&`, o un'espressione regolare (consultare [Sintassi delle Espressioni Regolari](../advanced.md#regular-expression-syntax))—una stringa semplice *`s`* (senza matcher) viene trattata come [`ContainsRegex(s)`](matchers.md#string-matchers), **non**
[`Eq(s)`](matchers.md#generic-comparison).

Ad esempio, il codice seguente verifica che la chiamata a `DoSomething(42)` provochi la terminazione del processo con un messaggio di errore che contiene il testo `My error`:

```cpp
EXPECT_DEATH(DoSomething(42), "My error");

```

### EXPECT_DEATH_IF_SUPPORTED {#EXPECT_DEATH_IF_SUPPORTED}

`EXPECT_DEATH_IF_SUPPORTED(`*`statement`*`,`*`matcher`*`)` \
`ASSERT_DEATH_IF_SUPPORTED(`*`statement`*`,`*`matcher`*`)`

Se i death test sono supportati, si comporta allo stesso modo di [`EXPECT_DEATH`](#EXPECT_DEATH). Altrimenti, non verifica nulla.

### EXPECT_DEBUG_DEATH {#EXPECT_DEBUG_DEATH}

`EXPECT_DEBUG_DEATH(`*`statement`*`,`*`matcher`*`)` \
`ASSERT_DEBUG_DEATH(`*`statement`*`,`*`matcher`*`)`

In modalità debug, si comporta allo stesso modo di [`EXPECT_DEATH`](#EXPECT_DEATH). Quando non è in modalità debug (cioè `NDEBUG` è definito), esegue semplicemente *`statement`*.

### EXPECT_EXIT {#EXPECT_EXIT}

`EXPECT_EXIT(`*`statement`*`,`*`predicate`*`,`*`matcher`*`)` \
`ASSERT_EXIT(`*`statement`*`,`*`predicate`*`,`*`matcher`*`)`

Verifica che *`statement`* faccia terminare il processo con uno stato di uscita che soddisfi *`predicate`* e produca l'output su `stderr` che corrisponde al *`matcher`*.

Il parametro *`predicate`* è una funzione o un funtore che accetta uno stato di uscita `int` e restituisce un `bool`. GoogleTest fornisce due predicati per gestire i casi comuni:

```cpp
// Restituisce true se il programma è uscito normalmente con il codice di stato di uscita specificato.
::testing::ExitedWithCode(exit_code);
// Returns true if the program was killed by the given signal.
// Non disponibile su Windows.
::testing::KilledBySignal(signal_number);

```

Il parametro *`matcher`* è un [matcher](matchers.md) per una `const std::string&`, o un'espressione regolare (consultare [Sintassi delle Espressioni Regolari](../advanced.md#regular-expression-syntax))—una stringa semplice *`s`* (senza matcher) viene trattata come [`ContainsRegex(s)`](matchers.md#string-matchers), **non**
[`Eq(s)`](matchers.md#generic-comparison).

Ad esempio, il codice seguente verifica che la chiamata a `NormalExit()` faccia sì che il processo stampi un messaggio contenente il testo `Success` su `stderr` e esca col codice di stato 0:

```cpp
EXPECT_EXIT(NormalExit(), testing::ExitedWithCode(0), "Success");

```
