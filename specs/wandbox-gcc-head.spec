Summary: gcc for wandbox
Name: wandbox-gcc-head
Version: %(eval date +%Y%m%d)
Release: 3
Epoch: 2
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: libgmp-dev libmpfr-dev libmpc-dev bison flex m4 curl unzip
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/gcc-head
%define _configure ../gcc-master/configure
%define _libexecdir %{_prefix}/libexec

%description
a component of wandbox service

%prep
%setup -q -c -T %{name}-head-%{release}
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/gcc-mirror/gcc.git` gcc-master

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
%{_prefix}/lib64
%{_prefix}/libexec

%changelog
* Sat Dec 12 2015 kikairoya <kikairoya@gmail.com>
- use debranch repository cache

* Wed Oct 21 2015 kikairoya <kikairoya@gmail.com>
- use github's pre-archived zip

* Mon May 26 2014 kikairoya <kikairoya@gmail.com>
- separate gdc

* Mon Feb 3 2014 kikairoya <kikairoya@gmail.com>
- add gdc
- use git+ssh instead of svn

* Mon Dec 30 2013 kikairoya <kikairoya@gmail.com>
- Initial build
