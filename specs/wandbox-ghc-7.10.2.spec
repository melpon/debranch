Summary: ghc for wandbox
Name: wandbox-ghc-7.10.2
Version: 7.10.2
Release: 1
Epoch: 2
License: ?
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: wget libgmp-dev wandbox-ghc-7.8.3 libffi-dev xsltproc libncurses5-dev
Source0: http://www.haskell.org/ghc/dist/%{version}/ghc-%{version}-src.tar.bz2
Source1: https://hackage.haskell.org/package/cabal-install-1.22.6.0/cabal-install-1.22.6.0.tar.gz
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
PATH=/opt/wandbox/ghc-7.8.3/bin:$PATH ./configure --prefix=%{_prefix} --libdir=%{_libdir}
PATH=/opt/wandbox/ghc-7.8.3/bin:$PATH %{__make} %{_smp_mflags}
rm -rf "$top/cabal"
mkdir -p cabal
(
  cd cabal-install-1.22.6.0
  CURL="disable_curl_downloading" PATH="$top/inplace/bin:$PATH" PREFIX="$top/cabal" GHC=ghc-stage2 sh ./bootstrap.sh --global --no-doc
)
ln -sf ghc-stage2 inplace/bin/ghc
sed -e "s#@@BUILD@@#$top#" -e "s#@@PREFIX@@#$top/cabal#" %{SOURCE2} > cabal/config
(
  export PATH="$top/inplace/bin:$top/cabal/bin:$PATH"
  export CABAL_CONFIG="$top/cabal/config"
  ghc-pkg recache -f "$top/cabal"
  cabal update
  cabal install alex-3.1.4 array-0.5.1.0 async-2.0.2 attoparsec-0.13.0.1 base-4.8.1.0 bytestring-0.10.6.0 Cabal-1.22.4.0 cabal-install-1.22.6.0 case-insensitive-1.2.0.4 cgi-3001.2.2.2 containers-0.5.6.2 deepseq-1.4.1.1 directory-1.2.2.0 exceptions-0.8.0.2 fgl-5.5.2.1 filepath-1.4.0.0 GLURaw-1.5.0.1 GLUT-2.7.0.1 happy-1.19.5 hashable-1.2.3.3 haskell-src-1.0.2.0 hpc-0.6.0.2 hscolour-1.23 html-1.0.1.2 HTTP-4000.2.20 HUnit-1.2.5.2 mtl-2.2.1 multipart-0.1.2 network-2.6.2.1 network-uri-2.6.0.3 ObjectName-1.1.0.0 old-locale-1.0.0.7 old-time-1.1.0.3 OpenGL-2.12.0.1 OpenGLRaw-2.5.1.0 parallel-3.2.0.6 parsec-3.1.9 pretty-1.1.2.0 primitive-0.6 process-1.2.3.0 QuickCheck-2.8.1 random-1.1 regex-base-0.93.2 regex-compat-0.95.1 regex-posix-0.95.2 scientific-0.3.3.8 split-0.2.2 StateVar-1.1.0.0 stm-2.4.4 syb-0.5.1 template-haskell-2.10.0.0 text-1.2.1.3 tf-random-0.5 time-1.5.0.1 transformers-0.4.2.0 transformers-compat-0.4.0.4 unix-2.7.1.0 unordered-containers-0.2.5.1 vector-0.11.0.0 xhtml-3000.2.1 zlib-0.5.4.2 --global --prefix="$top/cabal" --force-reinstalls
)

%install
top=$PWD
PATH=/opt/wandbox/ghc-7.8.3/bin:$PATH %{make_install}
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
