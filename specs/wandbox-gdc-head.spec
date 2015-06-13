Summary: gcc for wandbox
Name: wandbox-gcc-head
Version: %(eval date +%Y%m%d)
Release: 1
Epoch: 2
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: libgmp-dev libmpfr-dev libmpc-dev git subversion bison flex m4
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/gcc-head
%define _configure ../gcc/configure
%define _libexecdir %{_prefix}/libexec

%description
a component of wandbox service

%prep
%setup -q -c -T %{name}-head-%{release}
rm -rf gcc gdc
git clone https://github.com/D-Programming-GDC/GDC.git gdc --depth 1
svn co https://gcc.gnu.org/svn/gcc/trunk gcc -r $(TZ=UTC svn log https://gcc.gnu.org/svn/gcc/trunk -r \{$( date "+%Y%m%d" -d "$(cut -d- -f3 < gdc/gcc.version) next day")\}:HEAD -l 1 --xml --with-revprop logentry | sed -n '/revision/{s/.*revision="\([0-9]\+\)".*/\1/p;d};d')
cd gdc
./setup-gcc.sh ../gcc
cd ..


%build
mkdir -p build
cd build
%{configure} --enable-languages=c,c++,d --enable-lto --disable-multilib --without-ppl --without-cloog-ppl --enable-checking=release --disable-nls
%{__make} %{_smp_mflags}

%install
cd build
%{make_install}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs
rm -rf %{buildroot}/usr/share

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/include
%{_prefix}/lib64
%{_prefix}/libexec

%changelog
 * Mon May 26 2014 kikairoya <kikairoya@gmail.com>
 - separate from gcc-head

 * Mon Feb 3 2014 kikairoya <kikairoya@gmail.com>
 - add gdc
 - use git+ssh instead of svn

 * Mon Dec 30 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
