%define debug_package %{nil}
%define _empty_manifest_terminate_build 0
%global srcname rosa-imagewriter
%global _qt6_bindir %{_libdir}/qt6/bin/
# lto causes crash
%define _disable_lto 1

Summary:	Tool for writing installer to USB drive
Name:		om-imagewriter
Version:	2.6.4.1
Release:	1
License:	GPLv3+
Group:		File tools
# Original (seemingly dead) upstream: https://abf.io/soft/rosa-imagewriter
# Another interesting fork: https://github.com/KaOSx/isowriter
Url:		https://github.com/OpenMandrivaSoftware/om-imagewriter
Source0:	https://github.com/OpenMandrivaSoftware/om-imagewriter/archive/refs/tags/%{version}.tar.gz
BuildRequires:	qmake-qt6
BuildRequires:	pkgconfig(Qt6Linguist)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(udev)
Suggests:	%mklibname udev 1
# (tpg) needed for kdesu
Suggests:	kde-cli-tools >= 6.0.0
%rename rosa-imagewriter

%description
OpenMandriva Image Writer is a tool for creating bootable installation USB flash
drives.

%files
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_docdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/kio/servicemenus/*.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
qmake-qt6

make
%{_qt6_bindir}/lrelease RosaImageWriter.pro

# for lrelease
export PATH=%{_qt6_bindir}:$PATH
lang/build-translations

%install
mkdir -p                                                   \
	%{buildroot}%{_bindir}                             \
	%{buildroot}%{_libdir}/%{name}/lang                \
	%{buildroot}%{_docdir}/%{name}                     \
	%{buildroot}%{_iconsdir}/hicolor/scalable/apps     \
	%{buildroot}%{_datadir}/applications               \
	%{buildroot}%{_datadir}/kio/servicemenus
install -m 0755 RosaImageWriter %{buildroot}%{_libdir}/%{name}/%{name}
install -m 0644 lang/*.qm %{buildroot}%{_libdir}/%{name}/lang/
install -m 0644 doc/* %{buildroot}%{_docdir}/%{name}/
install -m 0644 res/icon-rosa.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
ln -sf %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Version=1.0
Name=OM Image Writer
Comment=Tool for writing installer to USB drive
Comment[ru]=Инструментарий записи загрузочных образов на USB-флэш
Exec=%{_libdir}/%{name}/%{name} %%U
Icon=%{name}
Terminal=false
Type=Application
Categories=System;
MimeType=application/x-iso;application/x-cd-image
EOF

cat > %{buildroot}%{_datadir}/kio/servicemenus/riw_write_iso_image.desktop <<EOF
[Desktop Entry]
Type=Service
Actions=WriteIsoImageToUsb;
ServiceTypes=KonqPopupMenu/Plugin
MimeType=application/x-iso;application/x-cd-image;inode/ISO-image

[Desktop Action WriteIsoImageToUsb]
Exec=%{_libdir}/%{name}/%{name} %%U
Name=Write to USB using OM ImageWriter
Name[ru]=Записать на USB, используя OM ImageWriter
Icon=%{name}
EOF

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop
