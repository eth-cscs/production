diff -Nru OpenFOAM-5.x.BAK/etc/bashrc OpenFOAM-5.x/etc/bashrc
--- OpenFOAM-5.x.BAK/etc/bashrc	2021-03-29 22:59:42.000000000 +0200
+++ OpenFOAM-5.x/etc/bashrc	2021-03-29 23:04:58.000000000 +0200
@@ -86,7 +86,11 @@
 #- MPI implementation:
 #    WM_MPLIB = SYSTEMOPENMPI | OPENMPI | SYSTEMMPI | MPICH | MPICH-GM | HPMPI
 #               | MPI | FJMPI | QSMPI | SGIMPI | INTELMPI
-export WM_MPLIB=SYSTEMOPENMPI
+export WM_MPLIB=SYSTEMMPI
+export MPI_ROOT=${MPICH_DIR}
+export MPI_ARCH_FLAGS=" "
+export MPI_ARCH_INC=" "
+export MPI_ARCH_LIBS=" "
 
 #- Operating System:
 #    WM_OSTYPE = POSIX | ???
diff -Nru OpenFOAM-5.x.BAK/etc/config.sh/scotch OpenFOAM-5.x/etc/config.sh/scotch
--- OpenFOAM-5.x.BAK/etc/config.sh/scotch	2021-03-29 22:59:43.000000000 +0200
+++ OpenFOAM-5.x/etc/config.sh/scotch	2021-03-29 23:05:38.000000000 +0200
@@ -37,7 +37,6 @@
 #
 #------------------------------------------------------------------------------
 
-export SCOTCH_VERSION=scotch_6.0.3
-export SCOTCH_ARCH_PATH=$WM_THIRD_PARTY_DIR/platforms/$WM_ARCH$WM_COMPILER$WM_PRECISION_OPTION$WM_LABEL_OPTION/$SCOTCH_VERSION
+export SCOTCH_ARCH_PATH=${CRAY_TPSL_DIR}
 
 #------------------------------------------------------------------------------
diff -Nru OpenFOAM-5.x.BAK/etc/config.sh/settings OpenFOAM-5.x/etc/config.sh/settings
--- OpenFOAM-5.x.BAK/etc/config.sh/settings	2021-03-29 22:59:43.000000000 +0200
+++ OpenFOAM-5.x/etc/config.sh/settings	2021-03-29 23:06:10.000000000 +0200
@@ -61,8 +61,8 @@
         64)
             WM_ARCH=linux64
             export WM_COMPILER_LIB_ARCH=64
-            export WM_CC='gcc'
-            export WM_CXX='g++'
+            export WM_CC='cc'
+            export WM_CXX='CC'
             export WM_CFLAGS='-m64 -fPIC'
             export WM_CXXFLAGS='-m64 -fPIC -std=c++0x'
             export WM_LDFLAGS='-m64'
diff -Nru OpenFOAM-5.x.BAK/src/parallel/decompose/Allwmake OpenFOAM-5.x/src/parallel/decompose/Allwmake
--- OpenFOAM-5.x.BAK/src/parallel/decompose/Allwmake	2021-03-29 22:59:54.000000000 +0200
+++ OpenFOAM-5.x/src/parallel/decompose/Allwmake	2021-03-29 23:06:26.000000000 +0200
@@ -31,7 +31,7 @@
         [ -e "$whichmpi" -a -e "$whichscotch" ] || wclean $libName
         echo "wmake $targetType $libName"
         wmake $targetType $libName
-        touch "$whichmpi" "$whichscotch"
+        #touch "$whichmpi" "$whichscotch"
     )
     done
 }
diff -Nru OpenFOAM-5.x.BAK/src/parallel/decompose/ptscotchDecomp/ptscotchDecomp.C OpenFOAM-5.x/src/parallel/decompose/ptscotchDecomp/ptscotchDecomp.C
--- OpenFOAM-5.x.BAK/src/parallel/decompose/ptscotchDecomp/ptscotchDecomp.C	2021-03-29 22:59:54.000000000 +0200
+++ OpenFOAM-5.x/src/parallel/decompose/ptscotchDecomp/ptscotchDecomp.C	2021-03-29 23:07:07.000000000 +0200
@@ -29,11 +29,11 @@
 #include "OFstream.H"
 #include "globalIndex.H"
 #include "SubField.H"
+#include "mpi.h"
 
 extern "C"
 {
     #include <stdio.h>
-    #include <mpi.h>
     #include "ptscotch.h"
 }
 
diff -Nru OpenFOAM-5.x.BAK/src/Pstream/Allwmake OpenFOAM-5.x/src/Pstream/Allwmake
--- OpenFOAM-5.x.BAK/src/Pstream/Allwmake	2021-03-29 22:59:46.000000000 +0200
+++ OpenFOAM-5.x/src/Pstream/Allwmake	2021-03-29 23:07:24.000000000 +0200
@@ -17,7 +17,7 @@
         whichmpi="$WM_PROJECT_DIR/platforms/$WM_OPTIONS/src/Pstream/$libName/using:$FOAM_MPI"
         [ -e "$whichmpi" ] || wclean $libName
         wmake $targetType $libName
-        touch "$whichmpi"
+        #touch "$whichmpi"
     )
     done
 }
diff -Nru OpenFOAM-5.x.BAK/wmake/rules/linux64Gcc/c OpenFOAM-5.x/wmake/rules/linux64Gcc/c
--- OpenFOAM-5.x.BAK/wmake/rules/linux64Gcc/c	2021-03-29 23:00:36.000000000 +0200
+++ OpenFOAM-5.x/wmake/rules/linux64Gcc/c	2021-03-29 23:07:48.000000000 +0200
@@ -2,7 +2,7 @@
 
 cWARN        = -Wall
 
-cc          = gcc -m64
+cc          = cc -m64
 
 include $(DEFAULT_RULES)/c$(WM_COMPILE_OPTION)
 
diff -Nru OpenFOAM-5.x.BAK/wmake/rules/linux64Gcc/c++ OpenFOAM-5.x/wmake/rules/linux64Gcc/c++
--- OpenFOAM-5.x.BAK/wmake/rules/linux64Gcc/c++	2021-03-29 23:00:36.000000000 +0200
+++ OpenFOAM-5.x/wmake/rules/linux64Gcc/c++	2021-03-29 23:08:02.000000000 +0200
@@ -5,7 +5,7 @@
 # Suppress some warnings for flex++ and CGAL
 c++LESSWARN = -Wno-old-style-cast -Wno-unused-local-typedefs -Wno-array-bounds
 
-CC          = g++ -std=c++11 -m64
+CC          = CC -std=c++11 -m64
 
 include $(DEFAULT_RULES)/c++$(WM_COMPILE_OPTION)
 
