-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 3.0 (native)
Source: python-apt
Binary: python-apt-doc, python-apt-dev, python-apt-common, python3-apt, python3-apt-dbg
Architecture: any all
Version: 2.3.0ubuntu2.1
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Uploaders: Michael Vogt <mvo@debian.org>, Julian Andres Klode <jak@debian.org>
Standards-Version: 4.5.0
Vcs-Browser: https://salsa.debian.org/apt-team/python-apt
Vcs-Git: https://salsa.debian.org/apt-team/python-apt.git
Testsuite: autopkgtest
Testsuite-Triggers: apt-utils, dirmngr, distro-info-data, fakeroot, gnupg, intltool, pycodestyle, pyflakes3, python3-all
Build-Depends: apt (>= 1.0.9.4), apt-utils <!nocheck>, debhelper-compat (= 12), dh-python, distro-info-data <!nocheck>, fakeroot, libapt-pkg-dev (>= 1.9.11~), python3-all (>= 3.3), python3-all-dev (>= 3.3), python3-all-dbg (>= 3.3), python3-distutils, python3-distutils-extra (>= 2.0), python3-setuptools, python3-sphinx (>= 0.5), gnupg <!nocheck>, dirmngr <!nocheck> | gnupg (<< 2) <!nocheck>, pycodestyle <!nocheck>, pyflakes3 <!nocheck>
Package-List:
 python-apt-common deb python optional arch=all
 python-apt-dev deb python optional arch=all
 python-apt-doc deb doc optional arch=all
 python3-apt deb python optional arch=any
 python3-apt-dbg deb debug optional arch=any
Checksums-Sha1:
 032152685f29f034dac5a79c80cba7ebdb2341ae 345300 python-apt_2.3.0ubuntu2.1.tar.xz
Checksums-Sha256:
 f9ff8f980a6cc5546b02f54fe0a123a92380de06f929b46d2aff96254bc305ad 345300 python-apt_2.3.0ubuntu2.1.tar.xz
Files:
 49b49e007b054a21ce3967bb0258ef6f 345300 python-apt_2.3.0ubuntu2.1.tar.xz
Original-Maintainer: APT Development Team <deity@lists.debian.org>

-----BEGIN PGP SIGNATURE-----

iQEzBAEBCgAdFiEEqx+XcX7ftBm4bj5/AhnKGdA0MwwFAmLZoCAACgkQAhnKGdA0
Mwxsuwf/ceojGBMrQFbpC8pkOx4UnNDU5ij4FrWPGQF3cwoN6DsemUoN12QD1trZ
pHDoHCIEePbhqDbqZ9jVE8SLxwf98vFfJjsWzG8LQ/Z364C+37Rrlh4oLvQJNNiK
nOdpBsJIhMDE91jG/qDQcW8AQS8pwrF85zhLg08sWOKvT7ThYI+NpAnb52EgUtej
71CPGt9LTU5I7wuPHHJ+q8G9ejbtVtLjtISZ7qLG2yY7x4hI6M3lm1d2wJsN+tAb
yCsCpPEu77PxYgpKt8B8k1ejaJ/iG+nktr40XdmD0Tg+UsKjSm6BCwLzZVdDvQv8
cgGYRy5VnlCnXqnM5pE+ZpoiIUxK5A==
=0no4
-----END PGP SIGNATURE-----
