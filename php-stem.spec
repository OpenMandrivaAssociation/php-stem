%define modname stem
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A45_%{modname}.ini

Summary:	A PHP extension that provides word stemming
Name:		php-%{modname}
Version:	1.4.3
Release:	%mkrel 12
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/stem/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini.bz2
BuildRequires:	php-devel >= 3:5.2.0
#BuildRequires:	libstemmer-devel

%description
This stem extension for PHP provides stemming capability for a variety of
languages using Dr. M.F. Porter's Snowball API, which can be found at:
http://snowball.tartarus.org

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

# this might work in the future
#%{_usrsrc}/php-devel/buildext stem "stem.c porter.c api.c" -DHAVE_CONFIG_H -L%{_libdir} -lstemmer

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

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
%doc package*.xml COPYING CREDITS ChangeLog EXPERIMENTAL README README.tests
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
