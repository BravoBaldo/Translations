## Utilizzo di GoogleTest da vari sistemi di build

GoogleTest viene fornito con file pkg-config utilizzabili per determinare tutti i flag necessari per la compilazione e il link a GoogleTest (e a GoogleMock).
Pkg-config è un semplice formato di testo standardizzato contenente

*   Il path di includedir (-I)
*   le definizioni di macro necessarie (-D)
*   ulteriori flag richiesti (-pthread)
*   il path della libreria (-L)
*   la libreria da linkare (-l)

Tutti i sistemi di build attuali supportano pkg-config in un modo o nell'altro. Per tutti gli esempi qui assumiamo che si voglia compilare l'esempio `samples/sample3_unittest.cc`.

### CMake

L'uso di `pkg-config` in CMake è abbastanza semplice:

```cmake
find_package(PkgConfig)
pkg_search_module(GTEST REQUIRED gtest_main)
add_executable(testapp)
target_sources(testapp PRIVATE samples/sample3_unittest.cc)
target_link_libraries(testapp PRIVATE ${GTEST_LDFLAGS})
target_compile_options(testapp PRIVATE ${GTEST_CFLAGS})
enable_testing()
add_test(first_and_only_test testapp)
```

In genere è consigliabile utilizzare `target_compile_options` + `_CFLAGS` su `target_include_directories` + `_INCLUDE_DIRS` poiché il primo include non solo i flag -I (GoogleTest potrebbe richiedere una macro che indichi agli header interni che tutte le librerie sono state compilate con il threading abilitato. Inoltre, GoogleTest potrebbe anche richiedere `-pthread` nella fase di compilazione e, di conseguenza, dividere la variabile `Cflags` di pkg-config in include dir e macro per `target_compile_definitions()` potrebbe ancora perderlo). La stessa raccomandazione vale per l'utilizzo di `_LDFLAGS` al posto del più comune `_LIBRARIES`, che scarta i flag `-L` e `-pthread`.

### Aiuto! pkg-config non trova GoogleTest!

Supponiamo che si abbia un `CMakeLists.txt` sulla falsariga di quello in questo tutorial e si provi a eseguire `cmake`. È molto probabile che si verifichi un problema sulla falsariga di:

```
-- Checking for one of the modules 'gtest_main'
CMake Error at /usr/share/cmake/Modules/FindPkgConfig.cmake:640 (message):
  None of the required 'gtest_main' found

```

Questi errori sono comuni se GoogleTest è stato installato da solo e non lo fa parte di una distribuzione o di un altro gestore di pacchetti. Se è così, si deve dire a pkg-config dove può trovare i file `.pc` contenenti le informazioni. Supponiamo che GoogleTest sia installato su `/usr/local`, è possibile che i file `.pc` siano installati in `/usr/local/lib64/pkgconfig`. Se si imposta

```
export PKG_CONFIG_PATH=/usr/local/lib64/pkgconfig

```

pkg-config proverà anche a cercare in `PKG_CONFIG_PATH` per trovare `gtest_main.pc`.

### Uso di pkg-config in una impostazione di cross-compilazione

Pkg-config è utilizzabile anche in un ambiente di cross-compilazione. Per farlo, supponiamo che il prefisso finale dell'installazione cross-compilata sia `/usr` e che il sysroot sia `/home/MYUSER/sysroot`. Configurare e installare GTest con

```
mkdir build && cmake -DCMAKE_INSTALL_PREFIX=/usr ..

```

Installare in sysroot con `DESTDIR`:

```
make -j install DESTDIR=/home/MYUSER/sysroot

```

Prima di continuare, si consiglia di definire **sempre** le seguenti due variabili per pkg-config in un'impostazione di cross-compilazione:

```
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=yes
export PKG_CONFIG_ALLOW_SYSTEM_LIBS=yes

```

altrimenti `pkg-config` filtrerà i flag `-I` e `-L` rispetto ai prefissi standard come `/usr` (vedere https://bugs.freedesktop.org/show_bug.cgi?id=28264#c3 per i motivi per cui di solito è necessario eseguire questa rimozione).

Guardando il file pkg-config generato, sarà simile a

```
libdir=/usr/lib64
includedir=/usr/include
Name: gtest
Description: GoogleTest (without main() function)
Version: 1.11.0
URL: https://github.com/google/googletest
Libs: -L${libdir} -lgtest -lpthread
Cflags: -I${includedir} -DGTEST_HAS_PTHREAD=1 -lpthread
```

Notare che sysroot non è incluso in `libdir` e in `includedir`! Provando ad eseguire `pkg-config` col `PKG_CONFIG_LIBDIR=/home/MYUSER/sysroot/usr/lib64/pkgconfig` corretto rispetto a questo file `.pc`, si ottiene

```
$ pkg-config --cflags gtest
-DGTEST_HAS_PTHREAD=1 -lpthread -I/usr/include
$ pkg-config --libs gtest
-L/usr/lib64 -lgtest -lpthread

```

che è ovviamente sbagliato e punta alla radice di `CBUILD` e non di `CHOST`. Per usarlo in un'impostazione di cross-compilazione, dobbiamo dire a pkg-config di inserire l'attuale sysroot nelle variabili `-I` e `-L`. Diciamo ora a pkg-config il vero sysroot

```
export PKG_CONFIG_DIR=
export PKG_CONFIG_SYSROOT_DIR=/home/MYUSER/sysroot
export PKG_CONFIG_LIBDIR=${PKG_CONFIG_SYSROOT_DIR}/usr/lib64/pkgconfig

```

ed eseguendo nuovamente `pkg-config` otteniamo

```
$ pkg-config --cflags gtest
-DGTEST_HAS_PTHREAD=1 -lpthread -I/home/MYUSER/sysroot/usr/include
$ pkg-config --libs gtest
-L/home/MYUSER/sysroot/usr/lib64 -lgtest -lpthread

```

che ora contiene il sysroot corretto. Per una guida più completa su come includere anche `${CHOST}` nelle chiamate di sistema della build, vedere l'eccellente tutorial di Diego
Elio Pettenò: <https://autotools.io/pkgconfig/cross-compiling.html>
