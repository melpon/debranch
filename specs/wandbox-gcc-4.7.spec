Summary: gcc for wandbox
Name: wandbox-gcc-4.7
Version: 4.7.3
Release: 1
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libgmp-dev libmpfr-dev libmpc-dev
Source0: http://ftp.tsukuba.wide.ad.jp/software/gcc/releases/gcc-%{version}/gcc-%{version}.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /usr/local/wandbox/gcc-%{version}
%define _configure ../gcc-%{version}/configure

%description
a component of wandbox service

%prep
%setup -q -c -T -a 0

%build
mkdir -p build
cd build
%{configure} --enable-languages=c,c++ --enable-lto --disable-multilib --without-ppl --without-cloog-ppl --enable-checking=release --disable-nls
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

%changelog
 * Sun Dec 29 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
