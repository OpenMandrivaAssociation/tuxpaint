%define major   0
%define libname %mklibname %{name} %{major}
%define libnamedev %mklibname %{name} -d

Summary:	Simple and fun paint program for kids
Name:		tuxpaint
Version:	0.9.35
Release:	2
#newer than 9.0 cvs build:
Epoch:		1
License:	GPLv2+
Group:		Graphics
URL:		https://www.newbreedsoftware.com/tuxpaint/
Source0:	https://sourceforge.net/projects/tuxpaint/files/tuxpaint/%{version}/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
#Patch1:		tuxpaint-0.9.20-fix-makefile_lib64.patch
#Patch2:		desktop.patch
BuildRequires:	make
BuildRequires:	gettext
BuildRequires:	gperf
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	libpaper-devel
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_ttf)
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(SDL2_gfx)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(SDL2_Pango)
BuildRequires:	pkgconfig(imagequant)
#for printing:
Requires:	netpbm
Suggests:	tuxpaint-config
Suggests:	tuxpaint-stamps
Conflicts:	%{libnamedev} < %{EVRD}

%description
Tux Paint is a simple paint program gear towards young children. 
It provides a simple but entertaining interface, allows drawing
with brushes, lines, shapes, and 'stamps,' and has a 'magic' 
tool, for special effects. Loading and saving is done via a 
graphical interface, and the underlying environment's 
filesystem isn't exposed (much like programs on PDAs).

%package devel
Summary:	Headers and development libraries from %{name}
Group:		Development/Other
Obsoletes:	%{libnamedev} < 1:0.9.21-3

%description devel
%{name} development headers and libraries.

%prep
%setup -q
%autopatch -p1
# Fix unreadable files
find . -perm 0600 -exec chmod 0644 '{}' \;

%build
make OPTFLAGS="%{optflags}" PREFIX=%{_prefix} LIBDIR=%{_libdir}

%install
make install BUILDPREFIX="%{buildroot}" PKG_ROOT="%{buildroot}" PREFIX="%{_usr}" X11_ICON_PREFIX="%{buildroot}%{_includedir}/X11/pixmaps" LIBDIR=%{_libdir}

%find_lang %{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install	--vendor="" \
			--dir %{buildroot}%{_datadir}/applications \
			--remove-category="Art" \
			src/tuxpaint.desktop

install -m644 data/images/icon16x16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 data/images/icon32x32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 data/images/icon48x48.png -D %{buildroot}%{_liconsdir}/%{name}.png

rm -Rf %{buildroot}%{_datadir}/applnk

#Fix perms:
chmod -R go+r docs/

#Remove useless installed things 
rm -Rf %{buildroot}%{_datadir}/doc/%{name}
rm -Rf %{buildroot}%{_datadir}/%{name}/images/icon32x32.xpm

%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/%{name}-import
%doc docs/*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-import.1*
%{_mandir}/*/man1/%{name}.1*
%dir %{_sysconfdir}/tuxpaint
%config(noreplace) %{_sysconfdir}/tuxpaint/tuxpaint.conf
%{_sysconfdir}/bash_completion.d/010_tuxpaint-completion.bash
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/tuxpaint.desktop
%{_datadir}/pixmaps/*png
%{_includedir}/X11/pixmaps/tuxpaint.xpm
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/metainfo/*.xml

%files devel
%doc %{_datadir}/doc/%{name}-%{version}
%{_bindir}/tp-magic-config
%{_includedir}/%{name}/*.h
%{_mandir}/man1/tp-magic-config.1*
