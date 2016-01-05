Summary: gcc for wandbox
Name: wandbox-gcc-5.2.0
Version: 5.2.0
Release: 4
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libgmp-dev libmpfr-dev libmpc-dev libc6-dev-i386 realpath libtool
Source0: http://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Source1: gcc-4.5.4-multiarch.patch
Source2: gcc-4.4.7-multiarch.patch
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/gcc-%{version}
%define _configure ../gcc-%{version}/configure
%define _libexecdir %{_prefix}/libexec

%description
a component of wandbox service

%prep
%setup -q -c -T -a 0
cp %{SOURCE1} %{SOURCE2} .
cd gcc-%{version}
find .. -maxdepth 1 -name "gcc-5.2.0*.patch" -print0 | xargs -0 cat | patch -p1
cd ..

%build
mkdir -p build
cd build
LDFLAGS="-Wl,-rpath,%{_prefix}/lib,-rpath,%{_prefix}/lib64,-rpath,%{_prefix}/lib32"
%{configure} --enable-languages=c,c++ --enable-lto --without-ppl --without-cloog-ppl --enable-checking=release --disable-nls --disable-multilib LDFLAGS="-Wl,-rpath,%{_prefix}/lib,-rpath,%{_prefix}/lib64,-rpath,%{_prefix}/lib32"
%{__make} %{_smp_mflags}

%install
cd build
%{make_install}
mkdir -p %{buildroot}%{_prefix}/lib
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs
rm -rf %{buildroot}/usr/share

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/include
%{_prefix}/lib
%{_prefix}/lib64
%{_prefix}/libexec

%changelog
 * Mon May 26 2014 kikairoya <kikairoya@gmail.com>
 - ensure /lib exists

 * Sat Feb 8 2014 kikairoya <kikairoya@gmail.com>
 - add patches and other tweaks

 * Mon Feb 3 2014 kikairoya <kikairoya@gmail.com>
 - generate from script

 * Sun Dec 29 2013 kikairoya <kikairoya@gmail.com>
 - Initial build

