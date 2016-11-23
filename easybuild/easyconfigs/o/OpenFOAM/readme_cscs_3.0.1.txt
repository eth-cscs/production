module use /apps/leone/UES/RH6.7_PE15.12/easybuild/modules/all/
module add CGAL/4.6-foss-2015b-Python-2.7.10
module add Autoconf/2.69-GNU-4.9.3-2.25
module add CMake/3.1.3-foss-2015b

edit the file

   wmake/rules/linux64Gcc/c++

   c++FLAGS    = $(GFLAGS) $(c++WARN) $(c++OPT) $(c++DBUG) $(ptFLAGS) $(LIB_HEADER_DIRS) -fPIC -L/apps/leone/UES/RH6.7_PE15.12/easybuild/software/MPFR/3.1.2-foss-2015b-GMP-6.0.0a/lib

edit etc/bashrc

   foamInstall=/apps/leone/UES/RH6.7_PE15.12/$WM_PROJECT

   export WM_MPLIB=OPENMPI

   #_foamSource `$WM_PROJECT_DIR/bin/foamEtcFile config/CGAL.sh`

source etc/bashrc

#mkdir ThirdParty-3.0.1/platforms/linux64Gcc/CGAL-4.7/lib/
#cd ThirdParty-3.0.1/platforms/linux64Gcc/CGAL-4.7/lib/
#ln -s /apps/leone/UES/RH6.7_PE15.12/easybuild/software/MPFR/3.1.2-foss-2015b-GMP-6.0.0a/lib/libmpfr.a
#ln -s /apps/leone/UES/RH6.7_PE15.12/easybuild/software/MPFR/3.1.2-foss-2015b-GMP-6.0.0a/lib/libmpfr.so
#ln -s /apps/leone/UES/RH6.7_PE15.12/easybuild/software/MPFR/3.1.2-foss-2015b-GMP-6.0.0a/lib/libmpfr.so.4
#ln -s /apps/leone/UES/RH6.7_PE15.12/easybuild/software/MPFR/3.1.2-foss-2015b-GMP-6.0.0a/lib/libmpfr.so.4.1.2

./Allwmake &> install_cscs.log
