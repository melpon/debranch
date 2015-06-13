Summary: groovy for wandbox
Name: wandbox-groovy-2.2.1
Version: 2.2.1
Release: 1
License: Apache
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: openjdk-7-jre-headless
#BuildRequires: wget zip unzip sharutils gawk cpio pkg-config procps time wdiff ant ant-optional libtool libxi-dev libxt-dev libxaw7-dev libxrender-dev libcups2-dev libasound2-dev liblcms2-dev libfreetype6-dev (>= 2.2.1), libgtk2.0-dev, libxinerama-dev, xsltproc, librhino-java (>= 1.7R3~), fonts-ipafont-mincho, libffi-dev, zlib1g-dev, libattr1-dev, libpng-dev, libjpeg8-dev, libgif-dev, libpulse-dev (>= 0.9.12), libnss3-dev (>= 3.12.9+ckbi-1.82-0ubuntu4), mauve, xvfb, xauth, xfonts-base, libgl1-mesa-dri, metacity | twm, dbus-x11, x11-xkb-utils
Source0: http://dist.codehaus.org/groovy/distributions/groovy-src-2.2.1.zip
URL: http://melpon.org/wandbox

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/elixir-lang/elixir.git --depth 1 . -b master

%build
PATH=%{erlangdir}/bin:$PATH %{__make} %{_smp_mflags}

%install
mkdir -p %{buildroot}%{_prefix}
PATH=%{erlangdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} install
rm -rf %{buildroot}%{_prefix}/share

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_prefix}/bin
%{_prefix}/lib

%changelog
 * Sat Jun 21 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

