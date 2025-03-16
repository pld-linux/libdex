#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_with	sysprof		# sysprof profiling information
#
Summary:	GNOME library for deferred execution
Summary(pl.UTF-8):	Biblioteka GNOME do odroczonego wykonywania kodu
Name:		libdex
Version:	0.10.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libdex/0.10/%{name}-%{version}.tar.xz
# Source0-md5:	a8ce67002a0687c7ba0039216c2984cb
URL:		https://gitlab.gnome.org/GNOME/libdex
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 1:2.68
BuildRequires:	gobject-introspection-devel
BuildRequires:	liburing-devel >= 0.7
BuildRequires:	meson >= 1.0.0
BuildRequires:	ninja >= 1.5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
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

%package static
Summary:	Static Dex library
Summary(pl.UTF-8):	Biblioteka statyczna Dex
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Dex library.

%description static -l pl.UTF-8
Biblioteka statyczna Dex.

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
%meson \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Ddocs=true} \
	-Deventfd=enabled \
	-Dliburing=enabled \
	%{?with_sysprof:-Dsysprof=true}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libdex-* $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_libdir}/libdex-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdex-1.so.1
%{_libdir}/girepository-1.0/Dex-1.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdex-1.so
%{_includedir}/libdex-1
%{_datadir}/gir-1.0/Dex-1.gir
%{_pkgconfigdir}/libdex-1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdex-1.a
%endif

%files -n vala-libdex
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libdex-1.deps
%{_datadir}/vala/vapi/libdex-1.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libdex-1
%endif
