%define ghcver 7.6.3
Summary: ghc for wandbox
Name: wandbox-ghc-head
Version: %(eval date +%Y%m%d)
Release: 1
License: custom
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
Requires: wandbox-ghc-7.6.3 wandbox-haskell-platform-2013.2.0.0-ghc-7.6.3
BuildRequires: libgmp-dev libffi-dev xsltproc libncurses5-dev
Source0: cabal.config.in
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/ghc-head
%define ghcdir /opt/wandbox/ghc-7.6.3

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/ghc/ghc.git --depth 1 . -b master
./sync-all -r https://github.com/ghc get
export PATH=$PWD/cabal/bin:%{ghcdir}/bin:$PATH
mkdir cabal
sed -e "s#@@BUILD@@#$PWD#" -e "s#@@PREFIX@@#$PWD/cabal#" %{SOURCE0} > cabal/config
ghc-pkg recache --user -f "$PWD/cabal"
CABAL_CONFIG="$PWD/cabal/config" cabal update
CABAL_CONFIG="$PWD/cabal/config" cabal install alex happy --package-db="$PWD/cabal" --prefix="$PWD/cabal"

%build
export PATH=$PWD/cabal/bin:%{ghcdir}/bin:$PATH
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
perl boot
./configure --prefix=%{_prefix} --libdir=%{_libdir} --with-ghc=%{ghcdir}/bin/ghc
%{__make} %{_smp_mflags}

%install
export PATH=$PWD/cabal/bin:%{ghcdir}/bin:$PATH
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
 * Sat Jun 21 2014 kikairoya <kikairoya@gmail.com>
 - Initial build
