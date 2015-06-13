Summary: ghc for wandbox
Name: wandbox-ghc-7.6.3
Version: 7.6.3
Release: 2
License: ?
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: libgmp-dev ghc libffi-dev xsltproc libncurses5-dev
Source0: http://www.haskell.org/ghc/dist/%{version}/ghc-%{version}-src.tar.bz2
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/ghc-%{version}

%description
a component of wandbox service

%prep
%setup -q -n ghc-%{version}

%build
cat > mk/build.mk <<EOT
docdir = %{_defaultdocdir}/ghc
htmldir = %{_defaultdocdir}/ghc
BUILD_DOCBOOK_PDF = NO
BUILD_DOCBOOK_PS = NO
BUILD_DOCBOOK_HTML = NO
HADDOCK_DOCS = NO
SRC_HC_OPTS+=-w
INTEGER_LIBRARY=integer-gmp
SRC_CC_OPTS+=%{optflags}
EOT
./configure --prefix=%{_prefix} --libdir=%{_libdir}
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_datadir}
rm -rf %{buildroot}%{_mandir}
binprefix=$(sh config.guess)
for f in $(find '%{buildroot}%{_bindir}' -name "$binprefix-*"); do
  ln -s $(basename "") $(echo "$f" | sed 's/$binprefix-//')
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}
%{_libdir}

%changelog
* Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Tue Jan 28 2014 kikairoya <kikairoya@gmail.com>
- Initial build
