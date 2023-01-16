#!/usr/bin/python3

import unittest
import os
import copy
import tempfile

import apt_pkg
import aptsources.sourceslist
import aptsources.distro

import testcommon


class TestAptSources(testcommon.TestCase):
    def setUp(self):
        testcommon.TestCase.setUp(self)
        if apt_pkg.config["APT::Architecture"] not in ("i386", "amd64"):
            apt_pkg.config.set("APT::Architecture", "i386")
        apt_pkg.config.set("Dir::Etc", os.getcwd())
        apt_pkg.config.set("Dir::Etc::sourceparts", tempfile.mkdtemp())
        if os.path.exists("./build/data/templates"):
            self.templates = os.path.abspath("./build/data/templates")
        elif os.path.exists("../build/data/templates"):
            self.templates = os.path.abspath("../build/data/templates")
        else:
            self.templates = "/usr/share/python-apt/templates/"

    def tearDown(self):
        aptsources.distro._OSRelease.OS_RELEASE_FILE = (
            aptsources.distro._OSRelease.DEFAULT_OS_RELEASE_FILE
        )
        if "LSB_ETC_LSB_RELEASE" in os.environ:
            del os.environ["LSB_ETC_LSB_RELEASE"]

    def testIsMirror(self):
        """aptsources: Test mirror detection."""
        yes = aptsources.sourceslist.is_mirror(
            "http://archive.ubuntu.com", "http://de.archive.ubuntu.com"
        )
        no = aptsources.sourceslist.is_mirror(
            "http://archive.ubuntu.com", "http://ftp.debian.org"
        )
        self.assertTrue(yes)
        self.assertFalse(no)

    def testSourcesListReading(self):
        """aptsources: Test sources.list parsing."""
        apt_pkg.config.set("Dir::Etc::sourcelist", "data/aptsources/" "sources.list")
        sources = aptsources.sourceslist.SourcesList(True, self.templates)
        self.assertEqual(len(sources.list), 10)
        # test load
        sources.list = []
        sources.load("data/aptsources/sources.list")
        self.assertEqual(len(sources.list), 10)

    def testSourcesListReading_deb822(self):
        """aptsources: Test sources.list parsing."""
        apt_pkg.config.set("Dir::Etc::sourceparts", "data/aptsources/" "sources.list.d")
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        self.assertEqual(len(sources.list), 5)
        # test load
        sources.list = []
        sources.load("data/aptsources/sources.list.d/main.sources")
        self.assertEqual(len(sources.list), 5)

        for entry in sources.list:
            self.assertFalse(entry.invalid)
            self.assertFalse(entry.disabled)
            self.assertEqual(entry.types, ["deb"])
            self.assertEqual(entry.type, "deb")
            self.assertEqual(entry.uris, ["http://de.archive.ubuntu.com/ubuntu/"])
            self.assertEqual(entry.uri, "http://de.archive.ubuntu.com/ubuntu/")

        self.assertEqual(sources.list[0].comps, ["main"])
        self.assertEqual(sources.list[1].comps, ["restricted"])
        self.assertEqual(sources.list[2].comps, ["universe"])
        self.assertEqual(sources.list[3].comps, ["main"])
        self.assertEqual(sources.list[4].comps, ["main"])

        for entry in sources.list[:-1]:
            self.assertIsNone(entry.trusted)

        self.assertTrue(sources.list[-1].trusted)

        for entry in sources.list[:-2]:
            self.assertEqual(entry.architectures, [])
            self.assertEqual(entry.suites, ["edgy"])
            self.assertEqual(entry.dist, "edgy")

        for entry in sources.list[-2:]:
            self.assertEqual(entry.suites, ["natty"])
            self.assertEqual(entry.dist, "natty")
            self.assertEqual(entry.architectures, ["amd64", "i386"])

    def testSourcesListWriting_deb822(self):
        """aptsources: Test sources.list parsing."""
        apt_pkg.config.set("Dir::Etc::sourceparts", "data/aptsources/" "sources.list.d")
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            for entry in sources.list:
                entry.file = os.path.join(tmpdir, os.path.basename(entry.file))

            sources.save()

            maxDiff = self.maxDiff
            self.maxDiff = None
            for file in os.listdir("data/aptsources/sources.list.d"):
                with open(os.path.join("data/aptsources/sources.list.d", file)) as a:
                    with open(os.path.join(tmpdir, file)) as b:
                        self.assertEqual(a.read(), b.read(), f"file {file}")
            self.maxDiff = maxDiff

    def testSourcesListAdding(self):
        """aptsources: Test additions to sources.list"""
        apt_pkg.config.set("Dir::Etc::sourcelist", "data/aptsources/" "sources.list")
        sources = aptsources.sourceslist.SourcesList(True, self.templates)
        # test to add something that is already there (main)
        before = copy.deepcopy(sources)
        sources.add("deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["main"])
        self.assertTrue(sources.list == before.list)
        # test to add something that is already there (restricted)
        before = copy.deepcopy(sources)
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["restricted"]
        )
        self.assertTrue(sources.list == before.list)

        before = copy.deepcopy(sources)
        sources.add(
            "deb",
            "http://de.archive.ubuntu.com/ubuntu/",
            "natty",
            ["main"],
            architectures=["amd64", "i386"],
        )
        self.assertTrue(sources.list == before.list)

        # test to add something new: multiverse
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["multiverse"]
        )
        found = False
        for entry in sources:
            if (
                entry.type == "deb"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and entry.dist == "edgy"
                and "multiverse" in entry.comps
            ):
                found = True
                break
        self.assertTrue(found)

        # add a new natty entry without architecture specification
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "natty", ["multiverse"]
        )
        found = False
        for entry in sources:
            if (
                entry.type == "deb"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and entry.dist == "natty"
                and entry.architectures == []
                and "multiverse" in entry.comps
            ):
                found = True
                break
        self.assertTrue(found)

        # Add universe to existing multi-arch line
        sources.add(
            "deb",
            "http://de.archive.ubuntu.com/ubuntu/",
            "natty",
            ["universe"],
            architectures=["i386", "amd64"],
        )
        found = False
        for entry in sources:
            if (
                entry.type == "deb"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and entry.dist == "natty"
                and set(entry.architectures) == set(["amd64", "i386"])
                and set(entry.comps) == set(["main", "universe"])
            ):
                found = True
                break
        self.assertTrue(found)
        # test to add something new: multiverse *and*
        # something that is already there
        before = copy.deepcopy(sources)
        sources.add(
            "deb",
            "http://de.archive.ubuntu.com/ubuntu/",
            "edgy",
            ["universe", "something"],
        )
        found_universe = 0
        found_something = 0
        for entry in sources:
            if (
                entry.type == "deb"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and entry.dist == "edgy"
            ):
                for c in entry.comps:
                    if c == "universe":
                        found_universe += 1
                    if c == "something":
                        found_something += 1
        # print "\n".join([s.str() for s in sources])
        self.assertEqual(found_something, 1)
        self.assertEqual(found_universe, 1)

    def testSourcesListAdding_deb822(self):
        """aptsources: Test additions to sources.list"""
        apt_pkg.config.set("Dir::Etc::sourceparts", "data/aptsources/" "sources.list.d")

        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        # test to add something that is already there (main)
        before = copy.deepcopy(sources)
        sources.add("deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["main"])
        self.assertEqual(sources.list, before.list)
        # test to add something that is already there (restricted)
        before = copy.deepcopy(sources)
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["restricted"]
        )
        self.assertTrue(sources.list == before.list)

        before = copy.deepcopy(sources)
        sources.add(
            "deb",
            "http://de.archive.ubuntu.com/ubuntu/",
            "natty",
            ["main"],
            architectures=["amd64", "i386"],
        )
        self.assertEqual(
            [e.str() for e in sources.list], [e.str() for e in before.list]
        )

        # test to add something new: multiverse
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["multiverse"]
        )
        found = False
        for entry in sources:
            if (
                entry.type == "deb"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and entry.dist == "edgy"
                and "multiverse" in entry.comps
            ):
                found = True
                break
        self.assertTrue(found)

        # add a new natty entry without architecture specification
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "natty", ["multiverse"]
        )
        found = False
        for entry in sources:
            if (
                entry.type == "deb"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and entry.dist == "natty"
                and entry.architectures == []
                and "multiverse" in entry.comps
            ):
                found = True
                break
        self.assertTrue(found)

        # Add universe to existing multi-arch line
        sources.add(
            "deb",
            "http://de.archive.ubuntu.com/ubuntu/",
            "natty",
            ["universe"],
            architectures=["i386", "amd64"],
        )
        found = False
        for entry in sources:
            if (
                entry.type == "deb"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and entry.dist == "natty"
                and set(entry.architectures) == set(["amd64", "i386"])
                and set(entry.comps) == set(["main", "universe"])
            ):
                found = True
                break
        self.assertTrue(found)
        # test to add something new: multiverse *and*
        # something that is already there
        before = copy.deepcopy(sources)
        sources.add(
            "deb",
            "http://de.archive.ubuntu.com/ubuntu/",
            "edgy",
            ["universe", "something"],
        )
        found_universe = 0
        found_something = 0
        for entry in sources:
            if (
                entry.type == "deb"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and entry.dist == "edgy"
            ):
                for c in entry.comps:
                    if c == "universe":
                        found_universe += 1
                    if c == "something":
                        found_something += 1
        # print "\n".join([s.str() for s in sources])
        self.assertEqual(found_something, 1)
        self.assertEqual(found_universe, 1)

    def testAddingWithComment_deb822(self):
        apt_pkg.config.set("Dir::Etc::sourceparts", "data/aptsources/" "sources.list.d")
        self._commonTestAddingWithComment()

    def testAddingWithComment_short(self):
        apt_pkg.config.set("Dir::Etc::sourcelist", "data/aptsources/" "sources.list")
        self._commonTestAddingWithComment()

    def _commonTestAddingWithComment(self):
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)

        # test to add something that is already there (main); loses comment
        before = copy.deepcopy(sources)
        sources.add(
            "deb",
            "http://de.archive.ubuntu.com/ubuntu/",
            "edgy",
            ["main"],
            comment="this will be lost",
        )
        self.assertTrue(sources.list == before.list)
        for entry in sources:
            self.assertNotEqual(entry.comment, "this will be lost")

        # test to add component to existing entry: multiverse; loses comment
        sources.add(
            "deb",
            "http://de.archive.ubuntu.com/ubuntu/",
            "edgy",
            ["multiverse"],
            comment="this will be lost",
        )
        for entry in sources:
            self.assertNotEqual(entry.comment, "this will be lost")

        before = copy.deepcopy(sources)
        # test to add entirely new entry; retains comment
        sources.add(
            "deb-src",
            "http://de.archive.ubuntu.com/ubuntu/",
            "edgy",
            ["main"],
            comment="this will appear",
            file=sources.list[0].file,  # make sure we test the deb822 code path
        )
        self.assertNotEqual(sources.list, before.list)
        self.assertEqual(len(sources.list), len(before.list) + 1)
        found = False
        for entry in sources:
            if (
                entry.type == "deb-src"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and entry.dist == "edgy"
                and entry.comment == "this will appear"
                and "main" in entry.comps
            ):
                found = True
                break
        self.assertTrue(found)

    def testInsertion_deb822(self):
        apt_pkg.config.set("Dir::Etc::sourceparts", "data/aptsources/" "sources.list.d")
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)

        # test to insert something that is already there (universe); does not
        # move existing entry (remains at index 2)
        before = copy.deepcopy(sources)
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["universe"], pos=0
        )
        self.assertTrue(sources.list == before.list)
        entry = list(sources)[2]
        self.assertEqual(entry.type, "deb")
        self.assertEqual(entry.uri, "http://de.archive.ubuntu.com/ubuntu/")
        self.assertEqual(entry.dist, "edgy")
        self.assertIn("universe", entry.comps)

        # test add component to existing entry: multiverse; does not move
        # entry to which it is appended (remains at index 0)
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["multiverse"], pos=2
        )
        entry = list(sources)[0]
        self.assertTrue(
            entry.type == "deb"
            and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
            and entry.dist == "edgy"
            and {"main", "multiverse"} <= set(entry.comps)
        )

        # test to add entirely new entry; inserted at 0
        sources.add(
            "deb-src", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["main"], pos=0
        )
        entry = list(sources)[0]
        self.assertTrue(
            entry.type == "deb-src"
            and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
            and entry.dist == "edgy"
            and "main" in entry.comps
        )

    def testInsertion(self):
        apt_pkg.config.set("Dir::Etc::sourcelist", "data/aptsources/" "sources.list")
        sources = aptsources.sourceslist.SourcesList(True, self.templates)

        # test to insert something that is already there (universe); does not
        # move existing entry (remains at index 2)
        before = copy.deepcopy(sources)
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["universe"], pos=0
        )
        self.assertTrue(sources.list == before.list)
        entry = list(sources)[5]
        self.assertTrue(
            entry.type == "deb"
            and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
            and entry.dist == "edgy"
            and "universe" in entry.comps
        )

        # test add component to existing entry: multiverse; does not move
        # entry to which it is appended (remains at index 0)
        sources.add(
            "deb", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["multiverse"], pos=2
        )
        entry = list(sources)[1]
        self.assertTrue(
            entry.type == "deb"
            and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
            and entry.dist == "edgy"
            and {"main", "multiverse"} <= set(entry.comps)
        )

        # test to add entirely new entry; inserted at 0
        sources.add(
            "deb-src", "http://de.archive.ubuntu.com/ubuntu/", "edgy", ["main"], pos=0
        )
        entry = list(sources)[0]
        self.assertTrue(
            entry.type == "deb-src"
            and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
            and entry.dist == "edgy"
            and "main" in entry.comps
        )

    def testDuplication_short(self):
        apt_pkg.config.set(
            "Dir::Etc::sourcelist", "data/aptsources/sources.list.testDuplication"
        )
        return self.commonTestDuplication()

    def testDuplication_deb822(self):
        apt_pkg.config.set(
            "Dir::Etc::sourceparts", "data/aptsources/sources.list.d.testDuplication"
        )
        return self.commonTestDuplication()

    def commonTestDuplication(self):
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        test_url = "http://ppa.launchpad.net/me/myproject/ubuntu"
        # test to add something that is already there (enabled)
        before = copy.deepcopy(sources)
        sources.add("deb", test_url, "xenial", ["main"])
        self.assertEqual(sources.list, before.list)
        # test to add something that is already there (disabled)
        sources.add("# deb-src", test_url, "xenial", ["main"])
        self.assertEqual(sources.list, before.list)
        # test to enable something that is already there
        sources.add("deb-src", test_url, "xenial", ["main"])
        found = False
        self.assertEqual(len(sources.list), 2)
        for entry in sources:
            if (
                entry.type == "deb-src"
                and not entry.disabled
                and entry.uri == test_url
                and entry.dist == "xenial"
                and entry.architectures == []
                and entry.comps == ["main"]
            ):
                found = True
                break
        self.assertTrue(found)

    def testMatcher_short(self):
        """aptsources: Test matcher"""
        apt_pkg.config.set(
            "Dir::Etc::sourcelist", "data/aptsources/" "sources.list.testDistribution"
        )
        return self.commonTestMatcher()

    def testMatcher_deb822(self):
        """aptsources: Test matcher"""
        apt_pkg.config.set(
            "Dir::Etc::sourceparts",
            "data/aptsources/" "sources.list.d.testDistribution",
        )
        return self.commonTestMatcher()

    def commonTestMatcher(self):
        """aptsources: Test matcher"""
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        distro = aptsources.distro.get_distro(
            id="Ubuntu",
            codename="bionic",
            description="Ubuntu 18.04 LTS",
            release="18.04",
        )
        distro.get_sources(sources)
        # test if all suits of the current distro were detected correctly
        self.assertNotEqual(sources.list, [])
        for s in sources:
            if not s.template:
                self.fail("source entry '%s' has no matcher" % s)

        # Hack in a check for splitting of fields here.
        if sources.list[-1].file.endswith(".sources"):
            self.assertEqual(
                sources.list[-1].uris, ["cdrom:[Ubuntu 8.04 _Hardy Heron_]"]
            )
        self.assertEqual(sources.list[-1].uri, "cdrom:[Ubuntu 8.04 _Hardy Heron_]")

    def testMultiArch(self):
        """aptsources: Test multi-arch parsing"""

        apt_pkg.config.set("Dir::Etc::sourcelist", "data/aptsources/" "sources.list")
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        assert not sources.list[8].invalid
        assert sources.list[8].type == "deb"
        assert sources.list[8].architectures == ["amd64", "i386"]
        assert sources.list[8].uri == "http://de.archive.ubuntu.com/ubuntu/"
        assert sources.list[8].dist == "natty"
        assert sources.list[8].comps == ["main"]
        assert sources.list[8].line.strip() == str(sources.list[8])
        assert sources.list[8].trusted is None

    def testMultiArch_deb822(self):
        """aptsources: Test multi-arch parsing"""

        apt_pkg.config.set("Dir::Etc::sourceparts", "data/aptsources/" "sources.list.d")
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        assert not sources.list[3].invalid
        assert sources.list[3].type == "deb"
        assert sources.list[3].architectures == ["amd64", "i386"]
        assert sources.list[3].uri == "http://de.archive.ubuntu.com/ubuntu/"
        assert sources.list[3].dist == "natty"
        assert sources.list[3].comps == ["main"]
        self.assertEqual(sources.list[3].line.strip(), str(sources.list[3]))
        self.assertIsNone(sources.list[3].trusted)

    def testMultipleOptions(self):
        """aptsources: Test multi-arch parsing"""

        apt_pkg.config.set("Dir::Etc::sourcelist", "data/aptsources/" "sources.list")
        sources = aptsources.sourceslist.SourcesList(True, self.templates)
        assert sources.list[9].invalid is False
        assert sources.list[9].type == "deb"
        assert sources.list[9].architectures == ["amd64", "i386"]
        self.assertEqual(sources.list[9].uri, "http://de.archive.ubuntu.com/ubuntu/")
        assert sources.list[9].dist == "natty"
        assert sources.list[9].comps == ["main"]
        assert sources.list[9].trusted
        assert sources.list[9].line.strip() == str(sources.list[9])

    def testMultipleOptions_deb822(self):
        """aptsources: Test multi-arch parsing"""

        apt_pkg.config.set("Dir::Etc::sourceparts", "data/aptsources/" "sources.list.d")
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        assert sources.list[4].invalid is False
        assert sources.list[4].type == "deb"
        assert sources.list[4].architectures == ["amd64", "i386"]
        self.assertEqual(sources.list[4].uri, "http://de.archive.ubuntu.com/ubuntu/")
        assert sources.list[4].dist == "natty"
        assert sources.list[4].comps == ["main"]
        assert sources.list[4].trusted
        assert sources.list[4].line.strip() == str(sources.list[4])

    def test_enable_component(self):
        target = "./data/aptsources/sources.list.enable_comps"
        line = "deb http://archive.ubuntu.com/ubuntu lucid main\n"
        with open(target, "w") as target_file:
            target_file.write(line)
        apt_pkg.config.set("Dir::Etc::sourcelist", target)
        sources = aptsources.sourceslist.SourcesList(True, self.templates)
        distro = aptsources.distro.get_distro(id="Ubuntu")
        # make sure we are using the right distro
        distro.codename = "lucid"
        distro.id = "Ubuntu"
        distro.release = "10.04"
        # and get the sources
        distro.get_sources(sources)
        # test enable_component
        comp = "multiverse"
        distro.enable_component(comp)
        comps = set()
        for entry in sources:
            comps = comps.union(set(entry.comps))
        self.assertTrue("multiverse" in comps)
        self.assertTrue("universe" in comps)

    def test_enable_component_deb822(self):
        target = (
            apt_pkg.config.find_dir("dir::etc::sourceparts") + "enable_comps.sources"
        )
        line = "Types: deb\nURIs: http://archive.ubuntu.com/ubuntu\nSuites: lucid\nComponents: main\n"
        with open(target, "w") as target_file:
            target_file.write(line)
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        distro = aptsources.distro.get_distro(id="Ubuntu")
        # make sure we are using the right distro
        distro.codename = "lucid"
        distro.id = "Ubuntu"
        distro.release = "10.04"
        # and get the sources
        distro.get_sources(sources)
        # test enable_component
        comp = "multiverse"
        distro.enable_component(comp)
        comps = set()
        for entry in sources:
            comps = comps.union(set(entry.comps))
        self.assertTrue("multiverse" in comps)
        self.assertTrue("universe" in comps)

    def testDistribution_short(self):
        """aptsources: Test distribution detection."""
        apt_pkg.config.set(
            "Dir::Etc::sourcelist", "data/aptsources/" "sources.list.testDistribution"
        )
        return self.commonTestDistribution()

    def testDistribution_deb822(self):
        """aptsources: Test distribution detection."""
        apt_pkg.config.set(
            "Dir::Etc::sourceparts",
            "data/aptsources/" "sources.list.d.testDistribution",
        )
        return self.commonTestDistribution()

    def commonTestDistribution(self):
        """aptsources: Test distribution detection."""
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        distro = aptsources.distro.get_distro(
            id="Ubuntu",
            codename="bionic",
            description="Ubuntu 18.04 LTS",
            release="18.04",
        )
        distro.get_sources(sources)
        # test if all suits of the current distro were detected correctly
        dist_templates = set()
        for s in sources:
            if s.template:
                dist_templates.add(s.template.name)
        # print dist_templates
        for d in (
            "hardy",
            "hardy-security",
            "hardy-updates",
            "intrepid",
            "hardy-backports",
        ):
            self.assertTrue(d in dist_templates)
        # test enable
        comp = "restricted"
        distro.enable_component(comp)
        found = {}
        for entry in sources:
            if (
                entry.type == "deb"
                and entry.uri == "http://de.archive.ubuntu.com/ubuntu/"
                and "edgy" in entry.dist
            ):
                for c in entry.comps:
                    if c == comp:
                        if entry.dist not in found:
                            found[entry.dist] = 0
                        found[entry.dist] += 1
        # print "".join([s.str() for s in sources])
        for key in found:
            self.assertEqual(found[key], 1)

        # add a not-already available component
        comp = "multiverse"
        distro.enable_component(comp)
        found = {}
        for entry in sources:
            if entry.type == "deb" and entry.template and entry.template.name == "edgy":
                for c in entry.comps:
                    if c == comp:
                        if entry.dist not in found.has_key:
                            found[entry.dist] = 0
                        found[entry.dist] += 1
        # print "".join([s.str() for s in sources])
        for key in found:
            self.assertEqual(found[key], 1)

    @unittest.skip("lsb-release test broken when it was added")
    def test_os_release_distribution(self):
        """os-release file can be read and is_like is populated accordingly"""
        os.environ["LSB_ETC_LSB_RELEASE"] = os.path.abspath(
            "./data/aptsources/lsb-release"
        )
        aptsources.distro._OSRelease.OS_RELEASE_FILE = os.path.abspath(
            "./data/aptsources/os-release"
        )
        distro = aptsources.distro.get_distro()
        # Everything but is_like comes from lsb_release, see TODO in
        # get_distro.
        self.assertEqual("Ubuntu", distro.id)
        self.assertEqual("xenial", distro.codename)
        self.assertEqual("Ubuntu 16.04.1 LTS", distro.description)
        self.assertEqual("16.04", distro.release)
        self.assertEqual(["ubuntu", "debian"], distro.is_like)

    def test_enable_disabled_short(self):
        """LP: #1042916: Test enabling disabled entry."""
        apt_pkg.config.set("Dir::Etc::sourcelist", "data/aptsources/" "sources.list")
        return self.common_test_enable_disabled()

    def test_enable_disabled_deb822(self):
        """LP: #1042916: Test enabling disabled entry."""
        apt_pkg.config.set("Dir::Etc::sourceparts", "data/aptsources/" "sources.list.d")
        return self.common_test_enable_disabled()

    def common_test_enable_disabled(self):
        """LP: #1042916: Test enabling disabled entry."""
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        disabled = sources.add(
            "deb",
            "http://fi.archive.ubuntu.com/ubuntu/",
            "precise",
            ["main"],
            file=sources.list[0].file,  # if we use deb822, enable deb822
        )
        disabled.set_enabled(False)
        enabled = sources.add(
            "deb",
            "http://fi.archive.ubuntu.com/ubuntu/",
            "precise",
            ["main"],
            file=sources.list[0].file,  # if we use deb822, enable deb822
        )
        self.assertEqual(disabled, enabled)
        self.assertFalse(disabled.disabled)

    def test_duplicate_uri_with_trailing_slash_short(self):
        """Test replacing entry with same uri except trailing slash"""
        apt_pkg.config.set("Dir::Etc::sourcelist", "data/aptsources/" "sources.list")
        return self.common_test_duplicate_uri_with_trailing_slash()

    def test_duplicate_uri_with_trailing_slash_deb822(self):
        """Test replacing entry with same uri except trailing slash"""
        apt_pkg.config.set("Dir::Etc::sourceparts", "data/aptsources/" "sources.list.d")
        return self.common_test_duplicate_uri_with_trailing_slash()

    def common_test_duplicate_uri_with_trailing_slash(self):
        """Test replacing entry with same uri except trailing slash"""
        sources = aptsources.sourceslist.SourcesList(True, self.templates, deb822=True)
        line_wslash = "deb http://rslash.ubuntu.com/ubuntu/ precise main"
        line_woslash = "deb http://rslash.ubuntu.com/ubuntu precise main"
        entry_wslash = aptsources.sourceslist.SourceEntry(line_wslash)
        entry_woslash = aptsources.sourceslist.SourceEntry(line_woslash)
        self.assertEqual(entry_wslash, entry_woslash)
        count = len(sources.list)
        sourceslist_wslash = sources.add(
            entry_wslash.type, entry_wslash.uri, entry_wslash.dist, entry_wslash.comps
        )
        self.assertEqual(count + 1, len(sources.list))
        count = len(sources.list)
        sourceslist_woslash = sources.add(
            entry_woslash.type,
            entry_woslash.uri,
            entry_woslash.dist,
            entry_woslash.comps,
        )
        self.assertEqual(count, len(sources.list))
        self.assertEqual(sourceslist_wslash, sourceslist_woslash)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    unittest.main()
