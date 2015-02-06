%define modname stem
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A45_%{modname}.ini

Summary:	A PHP extension that provides word stemming
Name:		php-%{modname}
Version:	1.5.1
Release:	3
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/stem/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
BuildRequires:	php-devel >= 3:5.2.0
#BuildRequires:	libstemmer-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This stem extension for PHP provides stemming capability for a variety of
languages using Dr. M.F. Porter's Snowball API, which can be found at:
http://snowball.tartarus.org

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

# this might work in the future
#%%{_usrsrc}/php-devel/buildext stem "stem.c porter.c api.c utilities.c" -DHAVE_CONFIG_H -L%{_libdir} -Wl,-lstemmer

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

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
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml COPYING CREDITS ChangeLog README README.tests
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-2mdv2012.0
+ Revision: 795505
- rebuild for php-5.4.x

* Tue Mar 27 2012 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-1
+ Revision: 787465
- 1.5.1

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-20
+ Revision: 761299
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-19
+ Revision: 696474
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-18
+ Revision: 695469
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-17
+ Revision: 646689
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-16mdv2011.0
+ Revision: 629880
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-15mdv2011.0
+ Revision: 628194
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-14mdv2011.0
+ Revision: 600534
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-13mdv2011.0
+ Revision: 588872
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-12mdv2010.1
+ Revision: 514661
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-11mdv2010.1
+ Revision: 485487
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-10mdv2010.1
+ Revision: 468258
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-9mdv2010.0
+ Revision: 451361
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.5.0-8mdv2010.0
+ Revision: 397608
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-7mdv2010.0
+ Revision: 377031
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-6mdv2009.1
+ Revision: 346638
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-5mdv2009.1
+ Revision: 341809
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-4mdv2009.1
+ Revision: 323098
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-3mdv2009.1
+ Revision: 310311
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-2mdv2009.0
+ Revision: 238432
- rebuild

* Thu Jun 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-1mdv2009.0
+ Revision: 218255
- 1.5.0

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-14mdv2009.0
+ Revision: 200272
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-13mdv2008.1
+ Revision: 162245
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-12mdv2008.1
+ Revision: 107723
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-11mdv2008.0
+ Revision: 77579
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-10mdv2008.0
+ Revision: 39526
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-9mdv2008.0
+ Revision: 33878
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-8mdv2008.0
+ Revision: 21358
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-7mdv2007.0
+ Revision: 117633
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-6mdv2007.0
+ Revision: 78108
- rebuilt for php-5.2.0
- Import php-stem

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-5
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-4mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-3mdk
- rebuilt for php-5.1.4

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-2mdk
- rebuilt for php-5.1.3

* Sun Feb 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-1mdk
- initial Mandriva package

