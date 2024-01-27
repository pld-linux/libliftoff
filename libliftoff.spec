#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Lightweight KMS plane library
Name:		libliftoff
Version:	0.4.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://gitlab.freedesktop.org/emersion/libliftoff/-/releases/v%{version}/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	5c5ef466a63cf7e00822341e424d7412
URL:		https://gitlab.freedesktop.org/emersion/libliftoff
BuildRequires:	libdrm-devel >= 2.4.108
BuildRequires:	meson >= 0.52.0
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
Requires:	libdrm >= 2.4.108
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libliftoff eases the use of KMS planes from userspace without standing
in your way. Users create "virtual planes" called layers, set KMS
properties on them, and libliftoff will pick hardware planes for these
layers if possible.

%package devel
Summary:	Header files for libliftoff library
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libdrm-devel >= 2.4.108

%description devel
Header files for libliftoff library.

%package static
Summary:	Static libliftoff library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libliftoff library.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libliftoff.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libliftoff.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libliftoff.so
%{_includedir}/libliftoff.h
%{_pkgconfigdir}/libliftoff.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libliftoff.a
%endif
