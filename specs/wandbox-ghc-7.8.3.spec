Summary: ghc for wandbox
Name: wandbox-ghc-7.8.3
Version: 7.8.3
Release: 1
Epoch: 2
License: ?
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: wget libgmp-dev ghc libffi-dev xsltproc libncurses5-dev
Source0: http://www.haskell.org/ghc/dist/%{version}/ghc-%{version}-src.tar.bz2
Source1: https://hackage.haskell.org/package/cabal-install-1.18.0.5/cabal-install-1.18.0.5.tar.gz
Source2: cabal.config.in
Source3: ghc-7.10.2.patch
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/ghc-%{version}
%define _datadir %{_prefix}/share

%description
a component of wandbox service

%prep
%setup -q -n ghc-%{version} -a 1
for f in %{SOURCE3}; do
  if echo $f | grep -q %{version}; then
    patch -p1 < $f
  fi
done

%build
top=$PWD
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
PATH=/usr/bin:$PATH ./configure --prefix=%{_prefix} --libdir=%{_libdir}
PATH=/usr/bin:$PATH %{__make} %{_smp_mflags}
rm -rf "$top/cabal"
mkdir -p cabal
(
  cd cabal-install-1.18.0.5
  CURL="disable_curl_downloading" PATH="$top/inplace/bin:$PATH" PREFIX="$top/cabal" GHC=ghc-stage2 sh ./bootstrap.sh --global 
)
ln -sf ghc-stage2 inplace/bin/ghc
sed -e "s#@@BUILD@@#$top#" -e "s#@@PREFIX@@#$top/cabal#" %{SOURCE2} > cabal/config
(
  export PATH="$top/inplace/bin:$top/cabal/bin:$PATH"
  export CABAL_CONFIG="$top/cabal/config"
  ghc-pkg recache -f "$top/cabal"
  cabal update
  cabal install alex-3.1.3 array-0.5.0.0 async-2.0.1.5 attoparsec-0.10.4.0 base-4.7.0.1 bytestring-0.10.4.0 Cabal-1.18.1.3 cabal-install-1.18.0.5 case-insensitive-1.1.0.3 containers-0.5.5.1 deepseq-1.3.0.2 directory-1.2.1.0 fgl-5.5.0.1 filepath-1.3.0.2 GLURaw-1.4.0.1 GLUT-2.5.1.1 happy-1.19.4 hashable-1.2.2.0 haskell2010-1.1.2.0 haskell98-2.0.0.3 haskell-src-1.0.1.6 hpc-0.6.0.1 hscolour-1.20.3 html-1.0.1.2 HTTP-4000.2.10 HUnit-1.2.5.2 mtl-2.1.3.1 network-2.4.2.3 old-locale-1.0.0.6 old-time-1.1.0.2 OpenGL-2.9.2.0 OpenGLRaw-1.5.0.0 parallel-3.2.0.4 parsec-3.1.5 pretty-1.1.1.1 primitive-0.5.2.1 process-1.2.0.0 QuickCheck-2.6 random-1.0.1.1 regex-base-0.93.2 regex-compat-0.95.1 regex-posix-0.95.2 split-0.2.2 stm-2.4.2 syb-0.4.1 template-haskell-2.9.0.0 text-1.1.0.0 time-1.4.2 transformers-0.3.0.0 unix-2.7.0.1 unordered-containers-0.2.4.0 vector-0.10.9.1 xhtml-3000.2.1 zlib-0.5.4.1 --global --prefix="$top/cabal" --force-reinstalls
)

%install
top=$PWD
PATH=/usr/bin:$PATH %{make_install}
rm -rf %{buildroot}%{_mandir}
binprefix=$(sh config.guess)
for f in $(find '%{buildroot}%{_bindir}' -name "$binprefix-*"); do
  ln -s $(basename "$f") $(echo "$f" | sed 's/$binprefix-//')
done
for bin in alex cabal happy; do
  install -m 755 cabal/bin/$bin %{buildroot}%{_bindir}
done
s=""
for pkg in $(find inplace/lib/package.conf.d -name '*-inplace.conf' -printf '%f\n' | sed 's/-inplace\.conf$//'); do
  s="s#$pkg-inplace#$(find %{buildroot}%{_libdir}/ghc-%{version}/package.conf.d -name "$pkg*.conf" -printf '%f\n' | sed 's/\.conf$//')#g;$s"
done  
for pkgpath in $(find cabal/lib -mindepth 2 -maxdepth 2 -path '*ghc-%{version}*'); do
  pkgname=$(echo $pkgpath | sed 's#/[^/]*ghc-%{version}##;s#cabal/lib/##;s#-[0-9a-zA-Z_]\+$##')
  c=$(find inplace/lib/package.conf.d -regex ".+/$pkgname-[0-9a-zA-Z_]+\.conf")
  rsync -a $pkgpath/ %{buildroot}%{_libdir}/ghc-%{version}/$pkgname
  sed "s#$top/$pkgpath#%{_libdir}/ghc-%{version}/$pkgname#g;s#^\(haddock-.*:\).*#\1#;$s" $c > %{buildroot}%{_libdir}/ghc-%{version}/package.conf.d/$(basename $c)
done
inplace/bin/ghc-pkg -f %{buildroot}%{_libdir}/ghc-%{version}/package.conf.d recache
for f in `inplace/bin/ghc-pkg -f %{buildroot}%{_libdir}/ghc-%{version}/package.conf.d list --simple | tr " " "\n" | sort -n | sed 's/-\([0-9]\+\.\)*[0-9]\+$//g' | uniq -d`; do
  for g in `inplace/bin/ghc-pkg -f %{buildroot}%{_libdir}/ghc-%{version}/package.conf.d list --simple | tr " " "\n" | sort -n | sed -n "/$f-\([0-9]\+\.\)*[0-9]\+$/p" | head -n-1`; do
    inplace/bin/ghc-pkg -f %{buildroot}%{_libdir}/ghc-%{version}/package.conf.d unregister $g
    rm -rf %{buildroot}%{_libdir}/ghc-%{version}/$g
  done
done

%clean
rm -rf %{buildroot}

%post
%{_bindir}/ghc-pkg --global recache

%files
%defattr(-,root,root,-)
%{_bindir}
%{_libdir}
%{_datadir}

%changelog
* Mon Jan 4 2016 kikairoya <kikairoya@gmail.com>
- purge haskell-platform

* Thu Oct 22 2015 kikairoya <kikairoya@gmail.com>
- select version of boot ghc

* Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Tue Jan 28 2014 kikairoya <kikairoya@gmail.com>
- Initial build
