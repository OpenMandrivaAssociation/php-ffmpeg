%define modname ffmpeg
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A30_%{modname}.ini

Summary:	The ffmpeg module for PHP
Name:		php-%{modname}
Version:	0.6.0
Release:	%mkrel 13
Group:		Development/PHP
License:	GPL
URL:		http://sourceforge.net/projects/ffmpeg-php/
Source:		http://downloads.sourceforge.net/ffmpeg-php/ffmpeg-php-%version.tbz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	ffmpeg-devel >= 0.4.9-0.pre1.4mdk
BuildRequires:	gd-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ffmpeg-php is an extension for PHP that adds an easy to use, object-oriented
API for accessing and retrieving information from movies and audio files. It
has methods for returning frames from movie files as images that can be
manipulated using PHP's image functions. This works well for automatically
creating thumbnail images from movie files, and it's fast enough to extract
thumbnails on the fly so that thumbnail images don't need to be stored.
ffmpeg-php is also useful for reporting the duration and bitrate of audio files
(mp3, wma...). ffmpeg-php can access many of the video formats supported by
ffmpeg (mov, avi, mpg, wmv...) 

%prep
%setup -q -n %{modname}-php-%{version}

# use system gd header
rm -f gd.h

perl -pi -e "s|PIX_FMT_RGBA32|PIX_FMT_RGB32|g" ffmpeg_frame.c

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .
chrpath -d %{soname}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS ChangeLog EXPERIMENTAL INSTALL tests
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
