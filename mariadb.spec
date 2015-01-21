Name:           mariadb
Version:        10.0.25
Release:        35
URL:            http://mariadb.org
Source0:	https://downloads.mariadb.org/f/mariadb-10.0.25/source/mariadb-10.0.25.tar.gz
Source1:        mariadb.service
Source2:        mariadb.tmpfiles
Source3:        mysql-systemd-start
Patch0:         0002-Support-stateless-operation-by-migrating-to-usr-file.patch
Patch1:         0003-Support-includeoptdir-for-non-fatal-inclusion-of-dir.patch
Summary:        MariaDB is a drop-in replacement for MySQL.
Group:          Development/Tools
License:        GPL-2.0

BuildRequires:  Linux-PAM-dev
BuildRequires:  bison
BuildRequires:  boost-dev
BuildRequires:  cmake
BuildRequires:  jemalloc-dev
BuildRequires:  libaio-dev
BuildRequires:  libxml2-dev
BuildRequires:  ncurses-dev
BuildRequires:  openssl-dev
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  systemd
BuildRequires:  zlib-dev

Requires:       %{name}-config

%description
MariaDB is a community developed branch of MySQL.
MariaDB is a multi-user, multi-threaded SQL database server.
It is a client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MariaDB/MySQL client programs and generic MySQL files.

%package dev
Summary: dev components for the mariadb package.
Group: Development
Requires: %{name}
Requires: %{name}-server

%description dev
dev components for the mariadb package.

%package doc
Summary: doc components for the mariadb package.
Group: Documentation
Requires: %{name}

%description doc
doc components for the mariadb package.

%package config
Summary: config components for the mariadb package.
Group: Default

%description config
config components for the mariadb package.

%package test
Summary: test components for the mariadb package.
Group: Development/Tools
Requires: %{name}
Requires: %{name}-server

%description test
test components for the mariadb package.

%package embedded
Summary: MariaDB as an embeddable library
Group: Development/Tools
Requires: %{name}

%description embedded
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains a version of the MariaDB server that can be embedded
into a client application instead of running as a separate process.
MariaDB is a community developed branch of MySQL.

%package server
Summary:  The MariaDB server and related files
Group: Development/Tools
Requires: %{name}
Requires: %{name}-config

%description server
MariaDB is a multi-user, multi-threaded SQL database server. It is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MariaDB server and some accompanying files and directories.
MariaDB is a community developed branch of MySQL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
mkdir clr-build
cd clr-build
cmake .. -G "Unix Makefiles" \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DBUILD_CONFIG=mysql_release \
    -DCMAKE_C_FLAGS="-fPIC $CFLAGS -fno-strict-aliasing -DBIG_JOINS=1 -fomit-frame-pointer -fno-delete-null-pointer-checks -O3 " \
    -DCMAKE_CXX_FLAGS="-fPIC $CXXFLAGS -fno-strict-aliasing -DBIG_JOINS=1 -felide-constructors -fno-rtti -fno-delete-null-pointer-checks -O3 " \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DENABLED_LOCAL_INFILE=ON \
    -DINSTALL_DOCDIR="share/doc/mariadb" \
    -DINSTALL_DOCREADMEDIR="share/doc/mariadb" \
    -DINSTALL_INCLUDEDIR=include/mysql \
    -DINSTALL_INFODIR=share/info \
    -DINSTALL_LAYOUT=RPM \
    -DINSTALL_LIBDIR="lib64" \
    -DINSTALL_MANDIR=share/man \
    -DINSTALL_MYSQLSHAREDIR=share/mariadb \
    -DINSTALL_MYSQLTESTDIR=share/mysql-test \
    -DINSTALL_PLUGINDIR="lib64/mysql/plugin" \
    -DINSTALL_SBINDIR=sbin \
    -DINSTALL_SCRIPTDIR=bin \
    -DINSTALL_SHAREDIR=share/aclocal/mysql \
    -DINSTALL_SUPPORTFILESDIR=share/mariadb \
    -DINSTALL_SYSCONF2DIR="/usr/share/defaults/mariadb/my.cnf.d" \
    -DINSTALL_SYSCONFDIR="/usr/share/defaults/mariadb" \
    -DMYSQL_DATADIR="/var/lib/mysql" \
    -DMYSQL_UNIX_ADDR=/run/mariadb/mariadb.sock \
    -DTMPDIR=/var/tmp \
    -DWITH_EMBEDDED_SERVER=ON \
    -DWITH_JEMALLOC=yes \
    -DWITH_MYSQLD_LDFLAGS="-pie ${LDFLAGS} -Wl,-z,now" \
    -DWITH_SSL=system \
    -DWITH_ZLIB=system
make V=1 %{?_smp_mflags}

%check
cd clr-build
make test VERBOSE=1

%install
rm -rf %{buildroot}
cd clr-build
%make_install
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/mariadb.service
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
install -m 0644 %{SOURCE2} %{buildroot}/usr/lib/tmpfiles.d/mariadb.conf
install -m 0755 %{SOURCE3} %{buildroot}/usr/bin/mysql-systemd-start

%files
/usr/bin/msql2mysql
/usr/bin/my_print_defaults
/usr/bin/mysql
/usr/bin/mysql_find_rows
/usr/bin/mysql_plugin
/usr/bin/mysql_waitpid
/usr/bin/mysqlaccess
/usr/bin/mysqladmin
/usr/bin/mysqlbinlog
/usr/bin/mysqlcheck
/usr/bin/mysqldump
/usr/bin/mysqlimport
/usr/bin/mysqlshow
/usr/bin/mysqlslap
%exclude /usr/bin/mytop
/usr/lib64/libmysqlclient.so.*
%exclude /usr/share/mariadb/SELinux/RHEL4/mysql.fc
%exclude /usr/share/mariadb/SELinux/RHEL4/mysql.te
%exclude /usr/share/mariadb/binary-configure
/usr/share/mariadb/charsets
/usr/share/mariadb/*/errmsg.sys
/usr/share/mariadb/errmsg-utf8.txt
%exclude /usr/share/mariadb/magic
/usr/share/mariadb/mysql-log-rotate
%exclude /usr/share/mariadb/mysql.server
%exclude /usr/share/mariadb/mysqld_multi.server

%files config
/usr/share/defaults/mariadb/my.cnf
/usr/share/defaults/mariadb/my.cnf.d/client.cnf
/usr/share/defaults/mariadb/my.cnf.d/mysql-clients.cnf
%exclude /usr/share/defaults/mariadb/init.d/mysql
%exclude /usr/share/defaults/mariadb/logrotate.d/mysql

%files test
/usr/bin/mysql_client_test
/usr/share/mysql-test

%files embedded
/usr/bin/mysql_client_test_embedded
/usr/bin/mysql_embedded
/usr/bin/mysqltest_embedded

%files server
/usr/lib/systemd/system/mariadb.service
/usr/lib/tmpfiles.d/mariadb.conf
/usr/bin/mysql-systemd-start
/usr/bin/aria_chk
/usr/bin/aria_dump_log
/usr/bin/aria_ftdump
/usr/bin/aria_pack
/usr/bin/aria_read_log
/usr/bin/innochecksum
/usr/bin/myisam_ftdump
/usr/bin/myisamchk
/usr/bin/myisamlog
/usr/bin/myisampack
/usr/bin/mysql_convert_table_format
/usr/bin/mysql_fix_extensions
/usr/bin/mysql_install_db
/usr/bin/mysql_secure_installation
/usr/bin/mysql_setpermission
/usr/bin/mysql_tzinfo_to_sql
/usr/bin/mysql_upgrade
/usr/bin/mysql_zap
/usr/bin/mysqlbug
/usr/bin/mysqld
/usr/bin/mysqldumpslow
/usr/bin/mysqld_multi
/usr/bin/mysqld_safe
/usr/bin/mysqlhotcopy
/usr/bin/mysqltest
/usr/bin/perror
/usr/bin/replace
/usr/bin/resolve_stack_dump
/usr/bin/resolveip
/usr/bin/tokuft_logprint
/usr/bin/tokuftdump
/usr/share/defaults/mariadb/my.cnf.d/server.cnf
/usr/share/defaults/mariadb/my.cnf.d/tokudb.cnf
/usr/share/mariadb/fill_help_tables.sql
/usr/share/mariadb/install_spider.sql
/usr/share/mariadb/mysql_system_tables.sql
/usr/share/mariadb/mysql_system_tables_data.sql
/usr/share/mariadb/mysql_test_data_timezone.sql
/usr/share/mariadb/mysql_performance_tables.sql
/usr/share/mariadb/mroonga/install.sql
/usr/share/mariadb/mroonga/uninstall.sql
/usr/share/mariadb/my-*.cnf
/usr/lib64/libmysqld.so.*
/usr/lib64/mysql/plugin/daemon_example.ini
/usr/lib64/mysql/plugin/*.so

%files dev
/usr/share/aclocal/mysql/aclocal/mysql.m4
/usr/include/mysql/*.h
/usr/include/mysql/private/atomic/*.h
/usr/include/mysql/private/*.h
/usr/include/mysql/psi/*.h
/usr/lib64/libmysqld.so
/usr/lib64/libmysqlclient.so
/usr/lib64/libmysqlclient_r.so*
/usr/bin/mysql_config

%files doc
/usr/share/doc/mariadb
%{_mandir}/man1/*.1
%{_mandir}/man8/*.8
