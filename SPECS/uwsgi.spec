%global		_libuwsgi	%{_libdir}/uwsgi

Name:           uwsgi
Version:        1.2.5
Release:        4.vortex%{?dist}
Summary:        application server

Group:          System Environment/Daemons
License:        GPLv2
URL:            http://projects.unbit.it/uwsgi
Vendor:		Vortex RPM
Source0:        %{name}-%{version}.tar.gz
Source1:	build.ini
Source2:	%{name}.sysconfig
Source3:	%{name}.init
Source4:	%{name}.logrotate
Patch0:		plugin_dest.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel, python27-devel, libedit-devel, bzip2-devel, pcre-devel, gmp-devel
BuildRequires:	krb5-devel, openssl-devel, php54-embedded, php54-devel, libxml2-devel
Requires(post):	chkconfig
Requires(preun):	chkconfig, initscripts

%package python
Summary:	python plugin for uwsgi
Requires:       uwsgi, python

%package python27
Summary:	python27 plugin for uwsgi
Requires:       uwsgi, python27

%package php
Summary:	php plugin for uwsgi
Requires:	uwsgi, php54


%description
uWSGI is a fast, self-healing and developer/sysadmin-friendly application
container server coded in pure C.

Born as a WSGI-only server, over time it has evolved in a complete stack for
networked/clustered web applications, implementing message/object passing,
caching, RPC and process management.

It uses the uwsgi (all lowercase, already included by default in the Nginx and
Cherokee releases) protocol for all the networking/interprocess communications,
but it can speak other protocols as well (http, fastcgi, mongrel2...)

It can be run in preforking mode, threaded, asynchronous/evented and supports
various forms of green threads/coroutines (such as uGreen, Greenlet, Stackless,
Gevent and Fiber).

Sysadmins will love it as it can be configured via several methods: command
line, environment variables, XML, .ini, yaml, json, sqlite3 database and
via LDAP.

On top of all this, it is designed to be fully modular. This means that
different plugins can be used in order to add compatibility with tons of
different technology on top of the same core.


%description python
Python plugin for uwsgi.


%description python27
Python 2.7 plugin for uwsgi.


%description php
PHP plugin for uwsgi.


%prep
%setup -q
%patch0 -p0
sed -i 's#__PLUGIN_DIR__#%{_libuwsgi}#g' %{SOURCE1}


%build
python27 uwsgiconfig.py --plugin plugins/python build python27
python uwsgiconfig.py --plugin plugins/python build python
python uwsgiconfig.py --plugin plugins/php build php


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}.d
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}
install -D -m 0755 %{name} $RPM_BUILD_ROOT/%{_sbindir}/%{name}
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/%{name}
install -D -m 0755 %{SOURCE3} $RPM_BUILD_ROOT/%{_initddir}/%{name}
install -D -m 0644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/%{name}
install -D -m 0644 python_plugin.so $RPM_BUILD_ROOT/%{_libuwsgi}/python_plugin.so
install -D -m 0644 python27_plugin.so $RPM_BUILD_ROOT/%{_libuwsgi}/python27_plugin.so
install -D -m 0644 php_plugin.so $RPM_BUILD_ROOT/%{_libuwsgi}/php_plugin.so


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/%{name}.d
%{_localstatedir}/log/%{name}
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%doc README


%files python
%{_libuwsgi}/python_plugin.so


%files python27
%{_libuwsgi}/python27_plugin.so


%files php
%{_libuwsgi}/php_plugin.so


%post
/sbin/chkconfig --add %{name}


%preun
if [ $1 -eq 0 ] ; then
	/sbin/service %{name} stop >/dev/null 2>&1
	/sbin/chkconfig --del %{name}
fi


%postun
if [ "$1" -ge "1" ] ; then
	/sbin/service %{name} restart >/dev/null 2>&1
fi


%changelog
* Wed Feb 20 2013 Ilya A. Otyutskiy <sharp@thesharp.ru> - 1.2.5-4.vortex
- rebuilt

* Sat Feb 16 2013 Ilya A. Otyutskiy <sharp@thesharp.ru> - 1.2.5-3.vortex
- Add uwsgi-python27 for Python 2.7 support.

* Thu Dec 13 2012 Ilya A. Otyutskiy <sharp@thesharp.ru> - 1.2.5-2.vortex
- Rebuild against php54 5.4.9.
- Add php54 to uwsgi-php requirements.

* Sun Sep 04 2012 Ilya A. Otyutskiy <sharp@thesharp.ru> - 1.2.5-1.vortex
- Initial packaging.

