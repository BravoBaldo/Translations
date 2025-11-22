# Quickstart: Il Building con Bazel

Questo tutorial ha lo scopo rendere operativi con l'uso di GoogleTest col sistema di build Bazel. Se è la prima volta che si usa GoogleTest, o c'è bisogno di un ripasso, consigliamo questo tutorial come punto di partenza.

## Prerequisiti

Per questo tutorial, c'è bisogno di:

*   Un sistema operativo compatibile (ad esempio Linux, macOS, Windows).
*   Un compilatore C++ compatibile che supporti almeno C++14.
*   [Bazel](https://bazel.build/), the preferred build system used by the
    GoogleTest team.

Vedere [Supported Platforms](platforms.md) per ulteriori informazioni sulle piattaforme compatibili con GoogleTest.

Se Bazel non è ancora installato, consultare la [Bazel installation guide](https://bazel.build/install).

{: .callout .note} Nota: I comandi del terminale in questo tutorial mostrano un prompt della shell Unix, ma funzionano anche sulla riga di comando di Windows.

## Configurare un workspace Bazel

Un [workspace Bazel](https://docs.bazel.build/versions/main/build-ref.html#workspace) è una directory sul file system che si utilizza per gestire i file sorgenti per il software che si desideri creare. Ciascuna directory del workspace ha un file di testo chiamato `WORKSPACE` che può essere vuoto o contenere riferimenti a dipendenze esterne necessarie per buildare gli output.

Innanzitutto, si crea una directory per il workspace:

```
$ mkdir my_workspace && cd my_workspace

```

Poi, si crea il file `WORKSPACE` per specificare le dipendenze. Un modo comune e consigliato per dipendere da GoogleTest è quello di utilizzare una [Bazel external dependency](https://docs.bazel.build/versions/main/external.html) tramite la [regola `http_archive`](https://docs.bazel.build/versions/main/repo/http.html#http_archive).
Per farlo, nella directory principale del workspace (`my_workspace/`), si crea un file chiamato `WORKSPACE` col seguente contenuto:

```
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
  name = "com_google_googletest",
  urls = ["https://github.com/google/googletest/archive/5ab508a01f9eb089207ee87fd547d290da39d015.zip"],
  strip_prefix = "googletest-5ab508a01f9eb089207ee87fd547d290da39d015",
)

```

La configurazione precedente dichiara una dipendenza da GoogleTest che viene scaricato come archivio ZIP da GitHub. Nell'esempio precedente, `5ab508a01f9eb089207ee87fd547d290da39d015` è l'hash del commit Git della versione di GoogleTest da utilizzare; consigliamo di aggiornare spesso l'hash in modo che punti alla versione più recente. Utilizzare un hash recente sul branch `main`.

Ora si è pronti per creare codice C++ che utilizza GoogleTest.

## Crea ed eseguire un file binario

Una volta configurato il workspace Bazel, si può utilizzare il codice GoogleTest all'interno del progetto.

Come esempio, si crea un file denominato `hello_test.cc` nella directory `my_workspace` col seguente contenuto:

```cpp
#include <gtest/gtest.h>
// Demonstrate some basic assertions.
TEST(HelloTest, BasicAssertions) {
  // Si aspetta che le due stringhe non siano uguali.
  EXPECT_STRNE("hello", "world");
  // Si aspetta l'uguaglianza.
  EXPECT_EQ(7 * 6, 42);
}

```

GoogleTest fornisce [asserzioni](primer.md#assertions) utilizzate per testare il comportamento del codice. L'esempio precedente include il file header principale di GoogleTest e mostra alcune asserzioni di base.

Per buildare il codice, si crea un file denominato `BUILD` nella stessa directory con il seguente contenuto:

```
cc_test(
  name = "hello_test",
  size = "small",
  srcs = ["hello_test.cc"],
  deps = ["@com_google_googletest//:gtest_main"],
)

```

Questa regola `cc_test` dichiara il file binario di test C++ che si vuole buildare e lo collega [link] a GoogleTest (`//:gtest_main`) utilizzando il prefisso specificato nel file `WORKSPACE` (`@com_google_googletest`). Per ulteriori informazioni sui file `BUILD`, vedere il [Bazel C++ Tutorial](https://docs.bazel.build/versions/main/tutorial/cpp.html).

{: .callout .note}
NOTA: Nell'esempio seguente, assumiamo Clang o GCC e impostiamo `--cxxopt=-std=c++14` per garantire che GoogleTest sia compilato come C++14 anziché come il default del compilatore (che potrebbe essere C++11). Per MSVC, l'equivalente sarebbe `--cxxopt=/std:c++14`. Vedere [Supported Platforms](platforms.md) per ulteriori dettagli sulle versioni dei linguaggi supportate.

Ora si possono buildare ed eseguire il test:

<pre>
<strong>my_workspace$ bazel test --cxxopt=-std=c++14 --test_output=all //:hello_test</strong>
INFO: Analyzed target //:hello_test (26 packages loaded, 362 targets configured).
INFO: Found 1 test target...
INFO: From Testing //:hello_test:
==================== Test output for //:hello_test:
Running main() from gmock_main.cc
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from HelloTest
[ RUN      ] HelloTest.BasicAssertions
[       OK ] HelloTest.BasicAssertions (0 ms)
[----------] 1 test from HelloTest (0 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (0 ms total)
[  PASSED  ] 1 test.
================================================================================
Target //:hello_test up-to-date:
  bazel-bin/hello_test
INFO: Elapsed time: 4.190s, Critical Path: 3.05s
INFO: 27 processes: 8 internal, 19 linux-sandbox.
INFO: Build completed successfully, 27 total actions
//:hello_test                                                     PASSED in 0.1s

INFO: Build completed successfully, 27 total actions
</pre>

Congratulazioni! È stato creato ed eseguito correttamente un file binario di prova utilizzando GoogleTest.

## Passi successivi

*   [Check out the Primer](primer.md) to start learning how to write simple
    tests.
*   [See the code samples](samples.md) for more examples showing how to use a
    variety of GoogleTest features.
