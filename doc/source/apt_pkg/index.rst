:mod:`apt_pkg` --- The low-level bindings for apt-pkg
=====================================================
.. module:: apt_pkg

The apt_pkg extensions provides a more low-level way to work with apt. It can
do everything apt can, and is written in C++. It has been in python-apt since
the beginning.


.. toctree::
    :maxdepth: 2
    :glob:

    *


Module Initialization
---------------------

Initialization is needed for most functions, but not for all of them. Some can
be called without having run init*(), but will not return the expected value.

.. function:: initConfig

    Initialize the configuration of apt. This is needed for most operations.

.. function:: initSystem

    Initialize the system.

.. function:: init

    Deprecated function. Use initConfig() and initSystem() instead.

Object initialization
----------------------
.. function:: GetCache([progress])

    Return a :class:`pkgCache` object. The optional parameter *progress*
    specifies an instance of :class:`apt.progress.OpProgress()` which will
    display the open progress.

.. function:: GetCdrom()

    Return a Cdrom object with the following methods:

    .. method:: Cdrom.Ident(progress)

        Identify the cdrom. The parameter *progress* refers to an
        :class:`apt.progress.CdromProgress()` object.

    .. method:: Cdrom.Add(progress)

        Add the cdrom to the sources.list file. The parameter *progress*
        refers to an :class:`apt.progress.CdromProgress()` object.


.. function:: GetDepCache(cache)

    Return a :class:`pkgDepCache` object. The parameter *cache* specifies an
    instance of :class:`pkgCache` (see :func:`GetCache()`).


.. function:: GetPkgSourceList()

    Return a :class:`PkgSourceList` object.

.. function:: GetPackageManager(depcache)

    Return a new :class:`PkgManager` object. The parameter *depcache* specifies
    a :class:`pkgDepCache` object as returned by :func:`GetDepCache`.

.. function:: GetPkgActionGroup(depcache)

    Return a new :class:`ActionGroup` object. The parameter *depcache*
    specifies a :class:`pkgDepCache` object as returned by :func:`GetDepCache`.

.. function:: GetPkgProblemResolver(depcache)

    Return a new :class:`ProblemResolver` object. The parameter *depcache*
    specifies a :class:`pkgDepCache` object as returned by :func:`GetDepCache`.

.. function:: GetPkgRecords(cache)

    Return a new :class:`PkgRecords` object.

    The parameter *cache* refers to an :class:`pkgCache` object, as returned
    by :func:`GetCache`.

.. function:: GetPkgSrcRecords()

    Return a new :class:`PkgSrcRecords` object.



The Acquire interface
----------------------
.. function:: GetAcquire([progress])

    Return an :class:`Acquire` object. This is a class which allows you
    to fetch files, or archive contents. The parameter *progress* refers to
    an :class:`apt.progress.FetchProgress()` object.

    Acquire items have multiple methods:

    .. method:: Acquire.Run()

        Fetch all the items which have been added by :func:`GetPkgAcqFile`.

    .. method:: Acquire.Shutdown()

        Shut the fetcher down.

    .. attribute:: Acquire.TotalNeeded

        The total amount of bytes needed (including those of files which are
        already present)

    .. attribute:: Acquire.FetchNeeded

        The total amount of bytes which need to be fetched.

    .. attribute:: Acquire.PartialPresent

        Whether some files have been acquired already. (???)


.. function:: GetPkgAcqFile(aquire, uri[, md5, size, descr, shortDescr, destDir, destFile])

    Create a new :class:`PkgAcqFile()` object and register it with *acquire*,
    so it will be fetched.

    The parameter *acquire* refers to an :class:`Acquire()` object as returned
    by :func:`GetAcquire`. The file will be added to the Acquire queue
    automatically.

    The parameter *uri* refers to the location of the file, any protocol
    of apt is supported.

    The parameter *md5* refers to the md5sum of the file. This can be used
    for checking the file.

    The parameter *size* can be used to specify the size of the package,
    which can then be used to calculate the progress and validate the download.

    The parameter *descr* is a descripition of the download. It may be
    used to describe the item in the progress class. *shortDescr* is the
    short form of it.

    You can use *destDir* to manipulate the directory where the file will
    be saved in. Instead of *destDir*, you can also specify the full path to
    the file using the parameter *destFile*. You can not combine both.



Hash functions
--------------
The apt_pkg module also provides several hash functions. If you develop
applications with python-apt it is often easier to use these functions instead
of the ones provides in Python's :mod:`hashlib` module.

.. function:: md5sum(object)

    Return the md5sum of the object. *object* may either be a string, in
    which case the md5sum of the string is returned, or a :class:`file()`
    object (or a file descriptor), in which case the md5sum of its contents is
    returned.

    .. versionchanged:: 0.8.0
        Added support for using file descriptors.

.. function:: sha1sum(object)

    Return the sha1sum of the object. *object* may either be a string, in
    which case the sha1sum of the string is returned, or a :class:`file()`
    object (or a file descriptor), in which case the sha1sum of its contents
    is returned.

    .. versionchanged:: 0.8.0
        Added support for using file descriptors.

.. function:: sha256sum(object)

    Return the sha256sum of the object. *object* may either be a string, in
    which case the sha256sum of the string is returned, or a :class:`file()`
    object  (or a file descriptor), in which case the sha256sum of its contents
    is returned.

    .. versionchanged:: 0.8.0
        Added support for using file descriptors.

Debian control files
--------------------
.. function:: ParseSection(text)

    Parse the string given in the parameter *text* and return a
    :class:`TagSection` object.

.. function:: ParseTagFile(file)

    Parse the given *file* and return a :class:`TagFile()` object. *file* may
    be a :class:`file()` object, a file descriptor, or anything providing a
    :meth:`fileno()` method.

    .. versionchanged:: 0.8.0
        Added support for using file descriptors.

.. autofunction:: RewriteSection(section, order, rewrite_list)

.. data:: RewritePackageOrder

    The order in which the information for binary packages should be rewritten,
    i.e. the order in which the fields should appear.

.. data:: RewriteSourceOrder

    The order in which the information for source packages should be rewritten,
    i.e. the order in which the fields should appear.

Dependencies
------------
.. function:: CheckDep(pkgver, op, depver)

    Check that the dependency requirements consisting of op and depver can be
    satisfied by the version pkgver.

    Example::

        >>> bool(apt_pkg.CheckDep("1.0", ">=", "1"))
        True

.. function:: ParseDepends(depends)

    Parse the string *depends* which contains dependency information as
    specified in Debian Policy, Section 7.1.

    Returns a list. The members of this list are lists themselves and contain
    one or more tuples in the format ``(package,version,operation)`` for every
    'or'-option given, e.g.::

        >>> apt_pkg.ParseDepends("PkgA (>= VerA) | PkgB (>= VerB)")
        [[('PkgA', 'VerA', '>='), ('PkgB', 'VerB', '>=')]]

.. function:: ParseSrcDepends(depends)

    Parse the string *depends* which contains dependency information as
    specified in Debian Policy, Section 7.1.

    Returns a list. The members of this list are lists themselves and contain
    one or more tuples in the format ``(package,version,operation)`` for every
    'or'-option given, e.g.::

        >>> apt_pkg.ParseDepends("PkgA (>= VerA) | PkgB (>= VerB)")
        [[('PkgA', 'VerA', '>='), ('PkgB', 'VerB', '>=')]]


    Furthemore, this function also supports to limit the architectures, as
    used in e.g. Build-Depends::

        >>> apt_pkg.ParseSrcDepends("a (>= 01) [i386 amd64]")
        [[('a', '01', '>=')]]


Configuration
-------------

.. data:: Config

    A :class:`Configuration()`-like object with the default configuration. This
    is implemented in the :class:`ConfigurationPtr` class, which has the same
    API like the :class:`Configuration` class.

.. function:: newConfiguration()

    Return a new :class:`Configuration` object.

.. function:: ReadConfigFile(configuration, filename)

    Read the configuration file specified by the parameter *filename* and add
    the settings therein to the :class:`Configuration()` object specified by
    the parameter *configuration*

.. function:: ReadConfigDir(configuration, dirname)

    Read configuration files in the directory specified by the parameter
    *dirname* and add the settings therein to the :class:`Configuration()`
    object specified by the parameter *configuration*.

.. function:: ReadConfigFileISC(configuration, filename)

    Read the configuration file specified by the parameter *filename* and add
    the settings therein to the :class:`Configuration()` object specified by
    the parameter *configuration*

.. function:: ParseCommandLine(configuration,options,argv)

    This function is like getopt except it manipulates a configuration space.
    output is a list of non-option arguments (filenames, etc). *options* is a
    list of tuples of the form ``(‘c’,”long-opt or None”,
    ”Configuration::Variable”,”optional type”)``.

    Where ``type`` may be one of HasArg, IntLevel, Boolean, InvBoolean,
    ConfigFile, or ArbItem. The default is Boolean.

Locking
--------

.. function:: GetLock(filename)

    Create an empty file at the path specified by the parameter *filename* and
    lock it.

    While the file is locked by a process, calling this function in another
    process returns ``-1``.

    When the lock is not required anymore, the file descriptor should be closed
    using :func:`os.close`.

.. function:: PkgSystemLock()

    Lock the global pkgsystem.

.. function:: PkgSystemUnLock()

    Unlock the global pkgsystem.

Other functions
----------------
.. function:: Base64Encode(string)

    Encode the given string using base64, e.g::

        >>> apt_pkg.Base64Encode(u"A")
        'QQ=='


.. function:: CheckDomainList(host, list)

    See if Host is in a ',' seperated list, e.g.::

        apt_pkg.CheckDomainList("alioth.debian.org","debian.net,debian.org")

.. function:: DeQuoteString(string)

    Dequote the string specified by the parameter *string*, e.g.::

        >>> apt_pkg.DeQuoteString("%61%70%74%20is%20cool")
        'apt is cool'

.. function:: QuoteString(string, repl)

    For every character listed in the string *repl*, replace all occurences in
    the string *string* with the correct HTTP encoded value:

        >>> apt_pkg.QuoteString("apt is cool","apt")
        '%61%70%74%20is%20cool'

.. function:: SizeToStr(size)

    Return a string presenting the human-readable version of the integer
    *size*. When calculating the units (k,M,G,etc.) the size is divided by the
    factor 1000.

    Example::

        >>> apt_pkg.SizeToStr(10000)
        '10.0k'

.. function:: StringToBool(input)

    Parse the string *input* and return one of **-1**, **0**, **1**.

    .. table:: Return values

        ===== =============================================
        Value      Meaning
        ===== =============================================
         -1   The string *input* is not recognized.
          0   The string *input* evaluates to **False**.
         +1   The string *input* evaluates to **True**.
        ===== =============================================

    Example::

        >>> apt_pkg.StringToBool("yes")
        1
        >>> apt_pkg.StringToBool("no")
        0
        >>> apt_pkg.StringToBool("not-recognized")
        -1

.. function:: StrToTime(rfc_time)

    Convert the :rfc:`1123` conforming string *rfc_time* to the unix time, and
    return the integer. This is the opposite of :func:`TimeRFC1123`.

    Example::

        >> apt_pkg.StrToTime('Thu, 01 Jan 1970 00:00:00 GMT')
        0

.. function:: TimeRFC1123(seconds)

    Format the unix time specified by the integer *seconds*, according to the
    requirements of :rfc:`1123`.

    Example::

        >>> apt_pkg.TimeRFC1123(0)
        'Thu, 01 Jan 1970 00:00:00 GMT'


.. function:: TimeToStr(seconds)

    Format a given duration in a human-readable manner. The parameter *seconds*
    refers to a number of seconds, given as an integer. The return value is a
    string with a unit like 's' for seconds.

    Example::

        >>> apt_pkg.TimeToStr(3601)
        '1h0min1s'

.. function:: UpstreamVersion(version)

    Return the string *version*, eliminating everything following the last
    '-'. Thus, this should be equivalent to ``version.rsplit('-', 1)[0]``.

.. function:: URItoFileName(uri)

    Take a string *uri* as parameter and return a filename which can be used to
    store the file, based on the URI.

    Example::

        >>> apt_pkg.URItoFileName('http://debian.org/index.html')
        'debian.org_index.html'


.. function:: VersionCompare(a, b)

    Compare two versions, *a* and *b*, and return an integer value which has
    the same characteristic as the built-in :func:`cmp` function.

    .. table:: Return values

        ===== =============================================
        Value      Meaning
        ===== =============================================
        > 0   The version *a* is greater than version *b*.
        = 0   Both versions are equal.
        < 0   The version *a* is less than version *b*.
        ===== =============================================




.. _CurStates:

Package States
---------------
.. data:: CurStateConfigFiles
.. data:: CurStateHalfConfigured
.. data:: CurStateHalfInstalled
.. data:: CurStateInstalled
.. data:: CurStateNotInstalled
.. data:: CurStateUnPacked




Dependency types
----------------
.. data:: DepConflicts
.. data:: DepDepends
.. data:: DepObsoletes
.. data:: DepPreDepends
.. data:: DepRecommends
.. data:: DepReplaces
.. data:: DepSuggests

.. _InstStates:

Installed states
-----------------
.. data:: InstStateHold
.. data:: InstStateHoldReInstReq
.. data:: InstStateOk
.. data:: InstStateReInstReq

.. _Priorities:

Priorities
----------
.. data:: PriExtra
.. data:: PriImportant
.. data:: PriOptional
.. data:: PriRequired
.. data:: PriStandard


.. _SelStates:

Select states
--------------
.. data:: SelStateDeInstall
.. data:: SelStateHold
.. data:: SelStateInstall
.. data:: SelStatePurge
.. data:: SelStateUnknown


Build information
-----------------
.. data:: Date

    The date on which this extension has been compiled.

.. data:: LibVersion

    The version of the apt_pkg library. This is **not** the version of apt,
    nor the version of python-apt.

.. data:: Time

    The time this extension has been built.

.. data:: Version

    The version of apt (not of python-apt).
