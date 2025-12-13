Name:           john-jumbo
Summary:        John the Ripper password cracker
Version:        1.9.0
Release:        2%{?dist}

%bcond_without  check

URL:            https://www.openwall.com/john
License:        GPL-2.0-or-later
Source0:        https://www.openwall.com/john/k/john-%{version}-jumbo-1.tar.xz
Patch0:         gcc11-align.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gnupg2
BuildRequires:  libxcrypt-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel

%description
John the Ripper is a fast password cracker (password security auditing
tool). Its primary purpose is to detect weak Unix passwords, but a number
of other hash types are supported as well.


%prep
%autosetup -p 1 -n john-%{version}-jumbo-1

chmod 0644 doc/*
sed -i 's#\$JOHN/john.conf#%{_sysconfdir}/john.conf#' src/params.h

%build
pushd src
%configure
%make_build -s clean
%make_build
popd

%install
install -d -m 755 %{buildroot}%{_sysconfdir}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_datadir}/john
install -p -m 755 run/mailer %{buildroot}%{_bindir}
install -p -m 644 run/{*.chr,password.lst} %{buildroot}%{_datadir}/john
install -p -m 644 run/john.conf %{buildroot}%{_sysconfdir}


install -d -m 755 %{buildroot}%{_libexecdir}/john
install -p -m 755 run/john* %{buildroot}%{_libexecdir}/john/

pushd %{buildroot}%{_bindir}
ln -s %{_libexecdir}/john/john john
ln -s john unafs
ln -s john unique
ln -s john unshadow
ln -s john base64conv
ln -s john gpg2john
ln -s john rar2john
ln -s john undrop
ln -s john zip2john
popd

rm doc/INSTALL

%files
%doc doc/*
%config(noreplace) %{_sysconfdir}/john.conf
%{_bindir}/john
%{_bindir}/mailer
%{_bindir}/unafs
%{_bindir}/unique
%{_bindir}/unshadow
%{_bindir}/base64conv
%{_bindir}/gpg2john
%{_bindir}/rar2john
%{_bindir}/undrop
%{_bindir}/zip2john
%{_datadir}/john/
%{_libexecdir}/john/

# https://src.fedoraproject.org/rpms/john/blob/rawhide/f/john.spec
# https://build.opensuse.org/projects/openSUSE:Factory/packages/john/files/john.spec

%changelog
* Sat Dec 13 2025 ntnayrb 1.9.0-2
- new package built with tito

* Mon Dec 8 2025 Bryant Niederriter <43710787+ntnayrb@users.noreply.github.com> - 1.9.0-1
- Initial build derived from the main Fedora package, with influence from OpenSUSE:Factory
