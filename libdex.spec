#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	sysprof		# sysprof profiling information
#
Summary:	GNOME library for deferred execution
Summary(pl.UTF-8):	Biblioteka GNOME do odroczonego wykonywania kodu
Name:		libdex
Version:	0.2.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libdex/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	9bf5640e7c9011112eb95b91e7cfa23d
URL:		https://gitlab.gnome.org/GNOME/libdex
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 1:2.68
BuildRequires:	gobject-introspection-devel
BuildRequires:	liburing-devel >= 0.7
BuildRequires:	meson >= 0.62.0
BuildRequires:	ninja >= 1.5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.38}
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
Requires:	glib2 >= 1:2.68
Requires:	liburing >= 0.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dex provides Future-based programming (deferred execution) for
GLib-based applications.

Dex also provides Fibers which allow writing synchronous looking code
in C that uses asynchronous and future-based APIs.

%description -l pl.UTF-8
Dex pozwala na programowanie oparte na stanie przyszłym (odroczonym
wykonywaniu kodu) w aplikacjach opartych na bibliotece GLib.

Dex udostępnia także strukturę Fibera, pozwalającą na pisanie kodu w C
wyglądającego jak synchroniczny, ale wykorzystującego API
asynchronicznego, opartego na stanie przyszłym.

%package devel
Summary:	Header files for Dex library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Dex
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.68

%description devel
Header files for Dex library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Dex.

%package -n vala-libdex
Summary:	Vala API for Dex library
Summary(pl.UTF-8):	API języka Vala dla biblioteki Dex
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala

%description -n vala-libdex
Vala API for Dex library.

%description -n vala-libdex -l pl.UTF-8
API języka Vala dla biblioteki Dex.

%package apidocs
Summary:	API documentation for Dex library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Dex
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Dex library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Dex.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Ddocs=true} \
	%{?with_sysprof:-Dsysprof=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libdex-* $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md TODO.md
%attr(755,root,root) %{_libdir}/libdex-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdex-1.so.1
%{_libdir}/girepository-1.0/Dex-1.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdex-1.so
%{_includedir}/libdex-1
%{_datadir}/gir-1.0/Dex-1.gir
%{_pkgconfigdir}/libdex-1.pc

%files -n vala-libdex
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libdex.deps
%{_datadir}/vala/vapi/libdex.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libdex-1
%endif
