Summary: frontend of wandbox
Name: wandbox-kennel
Version: 0.1
Release: 1
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: ghc cabal-install happy alex rsync
Source0: cabal.config.in
Source1: kennel-sqlite.yml
URL: http://melpon.org/wandbox

%define _prefix /usr/local/wandbox/kennel
%define _sysconfdir %{_prefix}/etc
%define _datadir %{_prefix}/share

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/melpon/wandbox .
git submodule init
git submodule update

%build
cd kennel
mkdir cabal
sed -e "s#@@BUILD@@#$PWD#" -e "s#@@PREFIX@@#%{_prefix}#" %{SOURCE0} > cabal/config
ghc-pkg recache --user -f "$PWD/cabal"
CABAL_CONFIG="$PWD/cabal/config" cabal update
CABAL_CONFIG="$PWD/cabal/config" cabal install yesod-platform-1.2.5.2 --package-db="$PWD/cabal" --prefix="$PWD/cabal"
CABAL_CONFIG="$PWD/cabal/config" cabal install --package-db="$PWD/cabal" --prefix="$PWD/cabal"

%install
cd kennel
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 cabal/bin/kennel %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_datadir}/kennel
rsync -aL config static messages templates %{buildroot}%{_datadir}/kennel/
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/kennel/config/sqlite.yml
install -d -m 755 %{buildroot}/var/lib/kennel
touch %{buildroot}/var/lib/kennel/default.sqlite3
touch %{buildroot}/var/lib/kennel/test.sqlite3
touch %{buildroot}/var/lib/kennel/staging.sqlite3
touch %{buildroot}/var/lib/kennel/production.sqlite3

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}
%{_datadir}/kennel
/var/lib/kennel

%changelog
 * Tue Dec 31 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
