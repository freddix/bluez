Summary:	Bluetooth protocol stack for Linux
Name:		bluez
Version:	5.28
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.gz
# Source0-md5:	b2532e89a7c829b62ca25f041b3df3cd
URL:		http://www.bluez.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	libical-devel
BuildRequires:	libnl-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	pkg-config
BuildRequires:	systemd-devel
BuildRequires:	udev-devel
Requires(post,preun,postun):	systemd-units
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	udev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# hardcoded /usr/lib
%define		cupsdir		/usr/lib/cups/backend

%description
Bluetooth protocol stack for Linux.

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%package -n cups-backend-bluez
Summary:	Bluetooth backend for CUPS
Group:		Applications/Printing
Requires:	bluez-libs >= %{epoch}:%{version}-%{release}
Requires:	cups

%description -n cups-backend-bluez
Bluetooth backend for CUPS.

%package libs
Summary:	Bluetooth libraries
Group:		Development/Libraries

%description libs
Libraries for use in Bluetooth applications.

%package libs-devel
Summary:	Header files for Bluetooth applications
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description libs-devel
bluez-libs-devel contains header files for use in Bluetooth
applications.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-test		\
	--enable-experimental	\
	--enable-library	\
	--enable-sixaxis
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/bluetooth/plugins,%{_sysconfdir}/bluetooth}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	cupsdir=%{cupsdir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{,*/*/}*.la

install profiles/input/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth
install profiles/network/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth
install profiles/proximity/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post bluetooth.service

%preun
%systemd_preun bluetooth.service

%postun
%systemd_postun

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/bccmd
%attr(755,root,root) %{_bindir}/bluemoon
%attr(755,root,root) %{_bindir}/bluetoothctl
%attr(755,root,root) %{_bindir}/btmon
%attr(755,root,root) %{_bindir}/ciptool
%attr(755,root,root) %{_bindir}/hciattach
%attr(755,root,root) %{_bindir}/hciconfig
%attr(755,root,root) %{_bindir}/hcidump
%attr(755,root,root) %{_bindir}/hcitool
%attr(755,root,root) %{_bindir}/hex2hcd
%attr(755,root,root) %{_bindir}/l2ping
%attr(755,root,root) %{_bindir}/l2test
%attr(755,root,root) %{_bindir}/mpris-proxy
%attr(755,root,root) %{_bindir}/rctest
%attr(755,root,root) %{_bindir}/rfcomm
%attr(755,root,root) %{_bindir}/sdptool

%dir %{_libdir}/bluetooth
%attr(755,root,root) %{_libdir}/bluetooth/bluetoothd
%attr(755,root,root) %{_libdir}/bluetooth/obexd

%dir %{_libdir}/bluetooth/plugins
%attr(755,root,root) %{_libdir}/bluetooth/plugins/sixaxis.so

%dir %{_sysconfdir}/bluetooth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/proximity.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/input.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/network.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/bluetooth.conf

%{systemdunitdir}/bluetooth.service
%{_prefix}/lib/systemd/user/obex.service
%{_datadir}/dbus-1/services/org.bluez.obex.service
%{_datadir}/dbus-1/system-services/org.bluez.service

%attr(755,root,root) %{_prefix}/lib/udev/hid2hci
%{_prefix}/lib/udev/rules.d/97-hid2hci.rules

%{_mandir}/man[18]/*

%files -n cups-backend-bluez
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/cups/backend/bluetooth

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libbluetooth.so.?
%attr(755,root,root) %{_libdir}/libbluetooth.so.*.*.*

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbluetooth.so
%{_includedir}/bluetooth
%{_pkgconfigdir}/bluez.pc

