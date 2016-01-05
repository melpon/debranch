%define bootghcver 7.10.2
Summary: ghc for wandbox
Name: wandbox-ghc-head
Version: %(eval date +%Y%m%d)
Release: 3
License: custom
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
Requires: wandbox-ghc-%{bootghcver}
BuildRequires: libgmp-dev libffi-dev xsltproc libncurses5-dev
Source0: cabal.config.in
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/ghc-head
%define bootghcdir /opt/wandbox/ghc-%{bootghcver}

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone `/opt/wandbox/debranch/bin/debranch.sh https://git.haskell.org/ghc.git` . -b master
/opt/wandbox/debranch/bin/debranch.sh --git-submodule https://git.haskell.org/ghc.git
git submodule update
export PATH=$PWD/cabal/bin:%{bootghcdir}/bin:$PATH
mkdir cabal
sed -e "s#@@BUILD@@#$PWD#" -e "s#@@PREFIX@@#$PWD/cabal#" %{SOURCE0} > cabal/config
ghc-pkg recache --user -f "$PWD/cabal"
CABAL_CONFIG="$PWD/cabal/config" cabal update
CABAL_CONFIG="$PWD/cabal/config" cabal install alex happy --package-db="$PWD/cabal" --prefix="$PWD/cabal"

%build
export PATH=$PWD/cabal/bin:%{bootghcdir}/bin:$PATH
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
./boot
./configure --prefix=%{_prefix} --libdir=%{_libdir} --with-ghc=%{bootghcdir}/bin/ghc
%{__make} %{_smp_mflags}

%install
export PATH=$PWD/cabal/bin:%{bootghcdir}/bin:$PATH
%{make_install}
rm -rf %{buildroot}%{_datadir}
rm -rf %{buildroot}%{_mandir}
binprefix=$(sh config.guess)
for f in $(find '%{buildroot}%{_bindir}' -name "$binprefix-*"); do
  ln -s $(basename "$f") $(echo "$f" | sed 's/$binprefix-//')
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}
%{_libdir}

%changelog
* Sun Dec 27 2015 kikairoya <kikairoya@gmail.com>
- use debranch repository cache

* Wed Oct 21 2015 kikairoya <kikairoya@gmail.com>
- use newer ghc
- trac build procedure change

* Sat Jun 21 2014 kikairoya <kikairoya@gmail.com>
- Initial build
