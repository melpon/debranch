Summary: clisp for wandbox
Name: wandbox-clisp-2.49
Version: 2.49
Release: 2
License: GPL
Group: wandbox
BuildRequires: libsigsegv-dev libffcall1-dev
Requires: libsigsegv2 libffcall1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: http://downloads.sourceforge.net/sourceforge/clisp/clisp-%{version}.tar.bz2
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/clisp-%{version}

%description
a component of wandbox service

%prep
%setup -q -n clisp-%{version}

%build
./configure --prefix=%{_prefix} --without-readline --with-ffcall src
cd src
./makemake --prefix=%{_prefix} --without-readline --with-ffcall --with-dynamic-ffi > Makefile
%{__make}
sed -i 's,http://www.lisp.org/HyperSpec/,http://www.lispworks.com/reference/HyperSpec/,g' config.lisp
%{__make}
cd ..

%install
cd src
%{make_install}
cd ..
rm -rf %{buildroot}%{_prefix}/share

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_bindir}
%{_prefix}/lib

%changelog
* Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
- Initial build
