Summary:	Simple and fun paint program for kids
Name: 		tuxpaint
Version:	0.9.17
Release:	%mkrel 1
#newer than 9.0 cvs build:
Epoch:		1
License:	GPL
Source: 	%{name}-%{version}.tar.bz2
Patch2:		tuxpaint-0.9.15b-lin_with_libpng.diff
Group:		Graphics
URL:		http://www.newbreedsoftware.com/tuxpaint/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  png-devel freetype2-devel cairo-devel librsvg-devel
BuildRequires:	gettext desktop-file-utils
BuildRequires:	SDL-devel SDL_mixer-devel SDL_ttf-devel SDL_image-devel
#for printing:
Requires: 	netpbm

%description
Tux Paint is a simple paint program gear towards young children. 
It provides a simple but entertaining interface, allows drawing
with brushes, lines, shapes, and 'stamps,' and has a 'magic' 
tool, for special effects. Loading and saving is done via a 
graphical interface, and the underlying environment's 
filesystem isn't exposed (much like programs on PDAs).

%prep
%setup -q 
%patch2 -p0 -b .saispo
rm -rf `find -name CVS`

%build
%make OPTFLAGS="%{optflags}" PREFIX=%{_prefix}

%install
rm -rf %{buildroot}
make install BUILDPREFIX="%{buildroot}" PKG_ROOT="%{buildroot}" PREFIX="%{_usr}" X11_ICON_PREFIX="%{buildroot}%{_includedir}/X11/pixmaps"


%find_lang %{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install	--vendor="" \
			--dir $RPM_BUILD_ROOT%{_datadir}/applications \
			--add-category="Education;Art;" \
			src/tuxpaint.desktop

install -m644 data/images/icon16x16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 data/images/icon32x32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 data/images/icon48x48.png -D %{buildroot}%{_liconsdir}/%{name}.png

#rm -f $RPM_BUILD_ROOT/%_datadir/%name/images/icon*x*.png $RPM_BUILD_ROOT/%_datadir/%{name}/images/icon-win32.png
rm -Rf %{buildroot}%{_datadir}/applnk

#Fix perms:
chmod -R go+r docs/

#Remove docs placed by an idiotic makefile
rm -Rf %{buildroot}/%{_datadir}/doc/%{name}
rm -Rf %{buildroot}/%{_datadir}/%{name}/images/icon32x32.xpm

%clean
rm -rf %{buildroot}

%post
%{update_menus}
#/sbin/ldconfig

%postun
%{clean_menus}
#/sbin/ldconfig

%files -f %{name}.lang
%defattr(755,root,root,755)
%{_bindir}/%{name}
%{_bindir}/%{name}-import
%defattr(644,root,root,755)
%doc docs/*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-import.1*
%lang(pl) %{_mandir}/pl/man1/%{name}.1*
%dir %{_sysconfdir}/tuxpaint
%config(noreplace) %{_sysconfdir}/tuxpaint/tuxpaint.conf
%{_datadir}/%{name}
%{_datadir}/applications/tuxpaint.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/pixmaps/*png
%{_includedir}/X11/pixmaps/tuxpaint.xpm
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
