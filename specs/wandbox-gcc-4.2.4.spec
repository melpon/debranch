Summary: gcc for wandbox
Name: wandbox-gcc-4.2.4
Version: 4.2.4
Release: 3
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libgmp-dev libmpfr-dev libmpc-dev libc6-dev-i386 realpath
Source0: http://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Source1: gcc-4.5.4-multiarch.patch
Source2: gcc-4.4.7-multiarch.patch
Source3: gcc-4.3.6-multiarch.patch
Source4: gcc-4.2.4-multiarch.patch
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/gcc-%{version}
%define _configure ../gcc-%{version}/configure
%define _libexecdir %{_prefix}/libexec

%description
a component of wandbox service

%prep
%setup -q -c -T -a 0
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .
cd gcc-%{version}
find .. -maxdepth 1 -name 'gcc-4.2.4*.patch' -print0 | xargs -0 cat | patch -p1
cd ..

%build
mkdir -p build
cd build
%{configure} --enable-languages=c,c++   --enable-checking=release --disable-nls --disable-multilib
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
%{_prefix}/lib
%{_prefix}/lib64
%{_prefix}/libexec

%changelog
 * Sat Feb 8 2014 kikairoya <kikairoya@gmail.com>
 - add patches and other tweaks

 * Mon Feb 3 2014 kikairoya <kikairoya@gmail.com>
 - generate from script

 * Sun Dec 29 2013 kikairoya <kikairoya@gmail.com>
 - Initial build

