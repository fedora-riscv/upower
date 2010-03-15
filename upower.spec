Summary:        Power Management Service
Name:           upower
Version:        0.9.1
Release:        2%{?dist}
License:        GPLv2+
Group:          System Environment/Libraries
URL:            http://hal.freedesktop.org/releases/
Source0:        http://hal.freedesktop.org/releases/UPower-%{version}.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  sqlite-devel
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  libgudev1-devel
BuildRequires:  libusb-devel
BuildRequires:  glib2-devel >= 2.6.0
BuildRequires:  dbus-devel  >= 1.2
BuildRequires:  dbus-glib-devel >= 0.82
BuildRequires:  polkit-devel >= 0.92
BuildRequires:  gobject-introspection-devel
Requires:       polkit >= 0.92
Requires:       udev
Requires:       pm-utils >= 1.2.2.1
Requires:       gobject-introspection

%description
UPower (formerly DeviceKit-power) provides a daemon, API and command
line tools for managing power devices attached to the system.

%package devel
Summary: Headers and libraries for UPower
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtk-doc

%description devel
Headers and libraries for UPower.

%prep
%setup -q -n UPower-%{version}

%build
%configure --enable-gtk-doc  --disable-static --enable-introspection
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang UPower

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f UPower.lang
%defattr(-,root,root,-)
%doc NEWS COPYING AUTHORS HACKING README
%{_libdir}/libdevkit-power-gobject*.so.*
%{_libdir}/libupower-glib.so.*
%{_sysconfdir}/dbus-1/system.d/*.conf
/lib/udev/rules.d/*.rules
%dir %{_localstatedir}/lib/upower
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service

%files devel
%defattr(-,root,root,-)
%{_datadir}/dbus-1/interfaces/*.xml
%dir %{_datadir}/gtk-doc/html/UPower
%{_datadir}/gtk-doc/html/UPower/*
%{_libdir}/libdevkit-power-gobject*.so
%{_libdir}/libupower-glib.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/DeviceKit-power/devkit-power-gobject
%{_includedir}/DeviceKit-power/devkit-power-gobject/*.h
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/gir-1.0/*.gir
%dir %{_includedir}/libupower-glib
%{_includedir}/libupower-glib/up-*.h
%{_includedir}/libupower-glib/upower.h

%changelog
* Mon Mar 15 2010 Richard Hughes <rhughes@redhat.com> - 0.9.1-2
- Actually enable the introspection support.

* Wed Mar 03 2010 Richard Hughes <rhughes@redhat.com> - 0.9.1-1
- Initial release of 0.9.1

