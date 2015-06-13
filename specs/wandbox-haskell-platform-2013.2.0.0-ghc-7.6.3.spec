%define _ghcver 7.6.3
Summary: haskell platform for wandbox
Name: wandbox-haskell-platform-2013.2.0.0-ghc-7.6.3
Version: 2013.2.0.0
Release: 2
License: ?
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
Requires: wandbox-ghc-%{version}
BuildRequires: libgl1-mesa-dev libglu1-mesa-dev freeglut3-dev
Source0: http://www.haskell.org/platform/download/%{version}/haskell-platform-%{version}.tar.gz
Source1: haskell-platform-install.patch
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/ghc-%{_ghcver}

%description
a component of wandbox service

%prep
%setup -q -n haskell-platform-%{version}
patch -p1 < %{SOURCE1}

%build
%{configure} --with-ghc=%{_bindir}/ghc --with-ghc-pkg=%{_bindir}/ghc-pkg
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_datadir}
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}/load

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/lib


%changelog
* Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Tue Jan 28 2014 kikairoya <kikairoya@gmail.com>
- Initial build
