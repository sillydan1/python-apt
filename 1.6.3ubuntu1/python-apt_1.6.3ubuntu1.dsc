-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Format: 3.0 (native)
Source: python-apt
Binary: python-apt, python-apt-doc, python-apt-dbg, python-apt-dev, python-apt-common, python3-apt, python3-apt-dbg
Architecture: any all
Version: 1.6.3ubuntu1
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Uploaders: Michael Vogt <mvo@debian.org>, Julian Andres Klode <jak@debian.org>
Standards-Version: 3.9.8
Vcs-Browser: https://salsa.debian.org/apt-team/python-apt
Vcs-Git: https://salsa.debian.org/apt-team/python-apt.git
Testsuite: autopkgtest
Testsuite-Triggers: apt-utils, dirmngr, fakeroot, gnupg, intltool, pep8, pyflakes, python-all, python-debian, python3-all
Build-Depends: apt (>= 1.0.9.4), apt-utils, debhelper (>= 9), dh-python, fakeroot, libapt-pkg-dev (>= 1.6.5~), python-all-dev (>= 2.7), python-all-dbg, python3-all-dev (>= 3.3), python3-all-dbg (>= 3.3), python3-distutils | python3 (<< 3.6) | python3.6 (<< 3.6.4~rc1-2), python-distutils-extra (>= 2.0), python-sphinx (>= 0.5), gnupg, dirmngr | gnupg (<< 2), pep8, pyflakes
Package-List:
 python-apt deb python optional arch=any
 python-apt-common deb python optional arch=all
 python-apt-dbg deb debug extra arch=any
 python-apt-dev deb python optional arch=all
 python-apt-doc deb doc optional arch=all
 python3-apt deb python optional arch=any
 python3-apt-dbg deb debug extra arch=any
Checksums-Sha1:
 df6dbb1b3b21a530d1b23eed567e302c8d3ac5d3 324772 python-apt_1.6.3ubuntu1.tar.xz
Checksums-Sha256:
 906925b1c729de365ba402efe7b5770ac7b3e8c31f49d4c57dad9a3759cc57e7 324772 python-apt_1.6.3ubuntu1.tar.xz
Files:
 bf542aef81bb13999c690cdc37a09f16 324772 python-apt_1.6.3ubuntu1.tar.xz
Original-Maintainer: APT Development Team <deity@lists.debian.org>

-----BEGIN PGP SIGNATURE-----

iF0EARECAB0WIQSKFkvLzpqBrnEPtL0NMDBzkRH7NQUCXFOWNQAKCRANMDBzkRH7
NS/2AKDIJ46+3veuUVCy+mPAmPnnb2WeVACgixAlMxRNb6TLxHAPW/aKR5i0oMs=
=g0HU
-----END PGP SIGNATURE-----
