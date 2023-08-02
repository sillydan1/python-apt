-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 3.0 (native)
Source: python-apt
Binary: python-apt-doc, python-apt-dev, python-apt-common, python3-apt, python3-apt-dbg
Architecture: any all
Version: 2.4.0ubuntu2
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Uploaders: Michael Vogt <mvo@debian.org>, Julian Andres Klode <jak@debian.org>
Standards-Version: 4.5.0
Vcs-Browser: https://salsa.debian.org/apt-team/python-apt
Vcs-Git: https://salsa.debian.org/apt-team/python-apt.git
Testsuite: autopkgtest
Testsuite-Triggers: apt-utils, binutils, dirmngr, distro-info-data, fakeroot, gnupg, intltool, pycodestyle, pyflakes3, python3-all
Build-Depends: apt (>= 1.0.9.4), apt-utils <!nocheck>, debhelper-compat (= 12), dh-python, distro-info-data <!nocheck>, fakeroot, libapt-pkg-dev (>= 1.9.11~), python3-all (>= 3.3), python3-all-dev (>= 3.3), python3-all-dbg (>= 3.3), python3-distutils, python3-distutils-extra (>= 2.0), python3-setuptools, python3-sphinx (>= 0.5), gnupg <!nocheck>, dirmngr <!nocheck> | gnupg (<< 2) <!nocheck>, pycodestyle <!nocheck>, pyflakes3 <!nocheck>
Package-List:
 python-apt-common deb python optional arch=all
 python-apt-dev deb python optional arch=all
 python-apt-doc deb doc optional arch=all
 python3-apt deb python optional arch=any
 python3-apt-dbg deb debug optional arch=any
Checksums-Sha1:
 a944afeba31a7b2f9bb7a6519ef5f548236b9be6 345652 python-apt_2.4.0ubuntu2.tar.xz
Checksums-Sha256:
 cc01c1a6bec70017890cc91e3626642057f3a6d2efa5adf2a063ae1ffc93fd31 345652 python-apt_2.4.0ubuntu2.tar.xz
Files:
 6fc02590212c2d59513d3c4d7145a4ac 345652 python-apt_2.4.0ubuntu2.tar.xz
Original-Maintainer: APT Development Team <deity@lists.debian.org>

-----BEGIN PGP SIGNATURE-----

iQFGBAEBCgAwFiEEVhrVhe7XZpIbqN2W1lhhiD4BTbkFAmTKIuMSHHBhcmlkZUBk
ZWJpYW4ub3JnAAoJENZYYYg+AU25HHkH/3rSqnitTb2Rc4D/YVnlHSFdE0PXUGGd
/cSeyPFdhEkZL0idoqmy4AHUJsRPcxmTT6zms3bpTOkuL7iTiFz4eRr7rHFWrMUd
lM9Jf7Ppkh0qWQfD8WAlZ60bnexJMj+vChNH9ayQyNRKlS8+6zbmfyfDnf4Caa0g
O9J3xdvZMTC1exONtlWntPMwRk5N4Aw1+Mhpq9TKelg9HFjr0xYuaGXNuX/ZztPv
zeq82ihvmb8axIYwnbaRQgpcvv+KS5N0CocNsnsJzI4zRxtpz6ql8/kM7ikFJmZJ
CW9/YdUe77Zss6O7qjDKQJii5A8aXaISJ9L7HiaA6bZykWa4uLnmG7Q=
=h4k6
-----END PGP SIGNATURE-----
