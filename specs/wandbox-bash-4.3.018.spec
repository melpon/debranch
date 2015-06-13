Summary: bash for wandbox
Name: wandbox-bash-4.3.018
Version: 4.3.018
Release: 2
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: http://ftp.gnu.org/gnu/bash/bash-4.3.tar.gz
Source1: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-001
Source2: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-002
Source3: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-003
Source4: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-004
Source5: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-005
Source6: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-006
Source7: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-007
Source8: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-008
Source9: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-009
Source10: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-010
Source11: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-011
Source12: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-012
Source13: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-013
Source14: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-014
Source15: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-015
Source16: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-016
Source17: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-017
Source18: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-018
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/bash-4.3.018
%define _sysconfdir %{_prefix}/etc

%description
a component of wandbox service

%prep
%setup -q -n bash-4.3
patch -p0 < %{SOURCE1}
patch -p0 < %{SOURCE2}
patch -p0 < %{SOURCE3}
patch -p0 < %{SOURCE4}
patch -p0 < %{SOURCE5}
patch -p0 < %{SOURCE6}
patch -p0 < %{SOURCE7}
patch -p0 < %{SOURCE8}
patch -p0 < %{SOURCE9}
patch -p0 < %{SOURCE10}
patch -p0 < %{SOURCE11}
patch -p0 < %{SOURCE12}
patch -p0 < %{SOURCE13}
patch -p0 < %{SOURCE14}
patch -p0 < %{SOURCE15}
patch -p0 < %{SOURCE16}
patch -p0 < %{SOURCE17}
patch -p0 < %{SOURCE18}

%build
export CFLAGS="$CFLAGS -DSYS_BASHRC=\"\\\"%{_sysconfdir}/bash.bashrc\\\"\" -DSYS_BASH_LOGOUT=\"\\\"%{_sysconfdir}/bash.bash_logout\\\"\""
%{configure} --without-curses --without-readline --without-bash-malloc
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}/usr/share

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_bindir}

%changelog
* Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
- Initial build
