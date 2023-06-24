#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Atari and Amiga musics emulator
Summary(pl.UTF-8):	Emulator muzyki Atari i Amigi
Name:		sc68
Version:	2.2.1
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/sc68/%{name}-%{version}.tar.bz2
# Source0-md5:	58a79e793ac111eef2a82615b43ae911
Patch0:		%{name}-info.patch
Patch1:		%{name}-system-unice68.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-format.patch
Patch4:		%{name}-opt.patch
Patch5:		%{name}-devel.patch
URL:		http://sc68.atari.org/
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.7
BuildRequires:	libtool
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	texinfo
BuildRequires:	unice68-devel >= 2.0.0
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Atari ST and Amiga music player.

%description -l pl.UTF-8
Odtwarzacz muzyki z Atari ST i Amigi.

%package libs
Summary:	Shared sc68 libraries
Summary(pl.UTF-8):	Biblioteki współdzielone sc68
Group:		Libraries

%description libs
Shared libraries for sc68 - Atari ST and Amiga music player.

%description libs -l pl.UTF-8
Biblioteki współdzielone sc68 - odtwarzacza muzyki z Atari ST i Amigi.

%package devel
Summary:	Header files for sc68 libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek sc68
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	zlib-devel

%description devel
Header files for sc68 libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek sc68.

%package static
Summary:	Static sc68 libraries
Summary(pl.UTF-8):	Statyczne biblioteki sc68
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static sc68 libraries.

%description static -l pl.UTF-8
Statyczne biblioteki sc68.

%package apidocs
Summary:	API documentation for sc68 libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek sc68
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for sc68 libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek sc68.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make} \
	ECHO=echo

%if %{with apidocs}
%{__make} -C doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/as68
%attr(755,root,root) %{_bindir}/debug68
%attr(755,root,root) %{_bindir}/info68
%attr(755,root,root) %{_bindir}/sc68
%attr(755,root,root) %{_bindir}/sourcer68
%{_datadir}/sc68
%{_infodir}/sc68.info*
%{_mandir}/man1/as68.1*
%{_mandir}/man1/debug68.1*
%{_mandir}/man1/info68.1*
%{_mandir}/man1/sc68.1*
%{_mandir}/man1/sourcer68.1*
%{_mandir}/man1/tools68.1*
%{_mandir}/man1/unice68.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libapi68-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libapi68-%{version}.so.3
%attr(755,root,root) %{_libdir}/libdesa68-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdesa68-%{version}.so.2
%attr(755,root,root) %{_libdir}/libemu68-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libemu68-%{version}.so.2
%attr(755,root,root) %{_libdir}/libemu68dbg-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libemu68dbg-%{version}.so.2
%attr(755,root,root) %{_libdir}/libfile68-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfile68-%{version}.so.2
%attr(755,root,root) %{_libdir}/libio68-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libio68-%{version}.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sc68-config
%attr(755,root,root) %{_libdir}/libapi68.so
%attr(755,root,root) %{_libdir}/libdesa68.so
%attr(755,root,root) %{_libdir}/libemu68.so
%attr(755,root,root) %{_libdir}/libemu68dbg.so
%attr(755,root,root) %{_libdir}/libfile68.so
%attr(755,root,root) %{_libdir}/libio68.so
%{_libdir}/libapi68.la
%{_libdir}/libdesa68.la
%{_libdir}/libemu68.la
%{_libdir}/libemu68dbg.la
%{_libdir}/libfile68.la
%{_libdir}/libio68.la
%{_includedir}/sc68
%{_pkgconfigdir}/sc68.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libapi68.a
%{_libdir}/libdesa68.a
%{_libdir}/libemu68.a
%{_libdir}/libemu68dbg.a
%{_libdir}/libfile68.a
%{_libdir}/libio68.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
