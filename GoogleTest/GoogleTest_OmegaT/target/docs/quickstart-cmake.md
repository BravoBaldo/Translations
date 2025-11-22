# Quickstart: Il Building con CMake

Questo tutorial ha lo scopo rendere operativi con l'uso di GoogleTest con CMake. Se è la prima volta che si usa GoogleTest, o c'è bisogno di un ripasso, consigliamo questo tutorial come punto di partenza. Se il progetto utilizza Bazel, consultare invece [Quickstart for Bazel](quickstart-bazel.md).

## Prerequisiti

Per questo tutorial, c'è bisogno di:

*   Un sistema operativo compatibile (ad esempio Linux, macOS, Windows).
*   Un compilatore C++ compatibile che supporti almeno C++14.
*   [CMake](https://cmake.org/) and a compatible build tool for building the
    project.
    *   Compatible build tools include
        [Make](https://www.gnu.org/software/make/),
        [Ninja](https://ninja-build.org/), and others - see
        [CMake Generators](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html)
            for more information.

Vedere [Supported Platforms](platforms.md) per ulteriori informazioni sulle piattaforme compatibili con GoogleTest.

Se CMake non è ancora installato, consultare la [CMake installation guide](https://cmake.org/install).

{: .callout .note}
Nota: I comandi del terminale in questo tutorial mostrano un prompt della shell Unix, ma funzionano anche sulla riga di comando di Windows.

## Preparazione di un progetto

CMake usa un file chiamato `CMakeLists.txt` per configurare il sistema di build per un progetto. Si utilizzerà questo file per impostare il progetto e per dichiarare una dipendenza da GoogleTest.

Innanzitutto, si crea una directory per il progetto:

```
$ mkdir my_project && cd my_project
```

Poi, si creerà il file `CMakeLists.txt` e si dichiarerà una dipendenza da GoogleTest. Esistono molti modi per esprimere le dipendenze nell'ecosistema CMake; in questa guida rapida si userà [il modulo `FetchContent` di CMake](https://cmake.org/cmake/help/latest/module/FetchContent.html).
Per farlo, nella directory del progetto (`my_project`), si crea un file chiamato `CMakeLists.txt` con i seguenti contenuti:

```cmake
cmake_minimum_required(VERSION 3.14)
project(my_project)
# GoogleTest requires at least C++14
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# Per Windows: Previene l'overriding delle impostazioni del compilatore compiler/linker del progetto genitore
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)
```

La configurazione precedente dichiara una dipendenza da GoogleTest che viene scaricato da GitHub. Nell'esempio precedente, `03597a01ee50ed33e9dfd640b249b4be3799d395` è l'hash del commit Git della versione di GoogleTest da utilizzare; consigliamo di aggiornare spesso l'hash in modo che punti alla versione più recente.

Per ulteriori informazioni su come creare i file `CMakeLists.txt`, consultare il [Tutorial su CMake](https://cmake.org/cmake/help/latest/guide/tutorial/index.html).

## Crea ed eseguire un file binario

Con GoogleTest dichiarato come dipendenza, se ne può utilizzare il codice all'interno del progetto.

Per esempio, creare un file chiamato `hello_test.cc` nella directory `my_project` col seguente contenuto:

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

Per creare il codice, si aggiunge quanto segue alla fine del file `CMakeLists.txt`:

```cmake
enable_testing()
add_executable(
  hello_test
  hello_test.cc
)
target_link_libraries(
  hello_test
  GTest::gtest_main
)
include(GoogleTest)
gtest_discover_tests(hello_test)
```

La configurazione precedente abilita il test in CMake, dichiara il file binario di test C++ che si desidera buildare (`hello_test`) e lo "linka" a GoogleTest (`gtest_main`). Le ultime due righe consentono al runner dei test di CMake di scoprire i test inclusi nel file binario, utilizzando il [modulo `GoogleTest` di CMake](https://cmake.org/cmake/help/git-stage/module/GoogleTest.html).

Ora si possono buildare ed eseguire il test:

<pre>
<strong>my_project$ cmake -S . -B build</strong>
-- The C compiler identification is GNU 10.2.1
-- The CXX compiler identification is GNU 10.2.1
...
-- Build files have been written to: .../my_project/build

<strong>my_project$ cmake --build build</strong>
Scanning dependencies of target gtest
...
[100%] Built target gmock_main

<strong>my_project$ cd build &amp;&amp; ctest</strong>
Test project .../my_project/build
    Start 1: HelloTest.BasicAssertions
1/1 Test #1: HelloTest.BasicAssertions ........   Passed    0.00 sec

100% tests passed, 0 tests failed out of 1

Total Test time (real) =   0.01 sec
</pre>

Congratulazioni! È stato creato ed eseguito correttamente un file binario di prova utilizzando GoogleTest.

## Passi successivi

*   [Check out the Primer](primer.md) to start learning how to write simple
    tests.
*   [See the code samples](samples.md) for more examples showing how to use a
    variety of GoogleTest features.
