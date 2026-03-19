import unittest
import os
import json
import tempfile
import shutil
from glftpd_installer_gui import (
    GlftpdInstallerGUI, VARIABLE_DEFAULTS, CACHE_SCHEMA,
    DEFAULT_SECTIONS, SCRIPT_VARS, _SECTIONS_MARKER,
)
from test_mocks import MockTk


class TestGlftpdInstallerGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls._original_dir = os.getcwd()
        os.chdir(cls.temp_dir)

        with open("install.sh", "w") as f:
            f.write('#!/bin/bash\necho "Test installation"\n')
        with open("requirements.txt", "w") as f:
            f.write("paramiko==3.4.0\n")

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._original_dir)
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def setUp(self):
        self.root = MockTk()
        self.app = GlftpdInstallerGUI(self.root, testing=True)

    def tearDown(self):
        self.root.destroy()

    # -- Basic init tests -------------------------------------------------------

    def test_initial_defaults(self):
        """All variables should match VARIABLE_DEFAULTS."""
        for attr, expected in VARIABLE_DEFAULTS.items():
            actual = getattr(self.app, attr).get()
            self.assertEqual(actual, expected,
                             f"{attr}: expected {expected!r}, got {actual!r}")

    def test_variable_set_get(self):
        self.app.ssh_host.set("10.0.0.1")
        self.assertEqual(self.app.ssh_host.get(), "10.0.0.1")
        self.app.sitename.set("MYSITE")
        self.assertEqual(self.app.sitename.get(), "MYSITE")

    def test_initial_state_flags(self):
        self.assertFalse(self.app.installation_running)
        self.assertEqual(self.app.current_step, 0)
        self.assertIsNone(self.app.ssh_client)
        self.assertIsNone(self.app.sftp_client)

    def test_ssh_keyfile_variable(self):
        self.assertEqual(self.app.ssh_keyfile.get(), "")
        self.app.ssh_keyfile.set("/path/to/key.pem")
        self.assertEqual(self.app.ssh_keyfile.get(), "/path/to/key.pem")

    # -- Dynamic sections -------------------------------------------------------

    def test_default_sections(self):
        """Should start with 3 default sections."""
        self.assertEqual(len(self.app.section_entries), 3)
        self.assertEqual(self.app.section_entries[0]["name"].get(), "MP3")
        self.assertEqual(self.app.section_entries[1]["name"].get(), "0DAY")
        self.assertEqual(self.app.section_entries[2]["name"].get(), "TV")

    def test_section_count_increase(self):
        """Changing sections count should add entries."""
        self.app.sections.set("5")
        self.assertEqual(len(self.app.section_entries), 5)
        # Original entries preserved
        self.assertEqual(self.app.section_entries[0]["name"].get(), "MP3")
        # New entries have defaults
        self.assertEqual(self.app.section_entries[3]["name"].get(), "")

    def test_section_count_decrease(self):
        """Decreasing sections should trim the list."""
        self.app.sections.set("1")
        self.assertEqual(len(self.app.section_entries), 1)
        self.assertEqual(self.app.section_entries[0]["name"].get(), "MP3")

    def test_section_count_clamped(self):
        """Section count should be clamped to 1-22."""
        self.app.sections.set("0")
        self.assertEqual(len(self.app.section_entries), 1)

        self.app.sections.set("30")
        self.assertEqual(len(self.app.section_entries), 22)

    def test_section_count_invalid_ignored(self):
        """Non-numeric section count should not crash."""
        original = len(self.app.section_entries)
        self.app.sections.set("abc")
        self.assertEqual(len(self.app.section_entries), original)

    # -- Cache generation -------------------------------------------------------

    def test_generate_cache_content(self):
        self.app.sitename.set("TESTSITE")
        self.app.port.set("2020")
        content = self.app.generate_cache_content()

        self.assertIn('sitename="TESTSITE"', content)
        self.assertIn('port="2020"', content)
        self.assertIn("# GLFTPD Unattended Installation Configuration",
                       content)
        self.assertIn('username="admin"', content)

    def test_cache_schema_attrs_valid(self):
        """Every 3-tuple attr in CACHE_SCHEMA should be a valid attribute."""
        for entry in CACHE_SCHEMA:
            if len(entry) == 3:
                _, attr, _ = entry
                self.assertTrue(hasattr(self.app, attr),
                                f"Missing attribute: {attr}")

    def test_cache_static_fields_present(self):
        """All static CACHE_SCHEMA keys should appear in output."""
        content = self.app.generate_cache_content()
        for entry in CACHE_SCHEMA:
            if len(entry) == 3:
                key, _, _ = entry
                self.assertIn(f'{key}=', content,
                              f"Cache key {key!r} missing from output")

    def test_cache_dynamic_sections(self):
        """Section entries should appear in generated cache."""
        self.app.sections.set("2")
        self.app.section_entries[0]["name"].set("FLAC")
        self.app.section_entries[0]["dated"].set("y")
        self.app.section_entries[0]["path"].set("/site/FLAC")
        self.app.section_entries[1]["name"].set("GAMES")
        self.app.section_entries[1]["path"].set("/site/GAMES")

        content = self.app.generate_cache_content()
        self.assertIn('section1="FLAC"', content)
        self.assertIn('section1dated="y"', content)
        self.assertIn('section2="GAMES"', content)
        self.assertIn('sectionpath1="/site/FLAC"', content)
        self.assertIn('sectionpath2="/site/GAMES"', content)

    def test_cache_preserves_special_characters(self):
        self.app.channame1.set("#test y s3cr3t!")
        content = self.app.generate_cache_content()
        self.assertIn('channame1="#test y s3cr3t!"', content)

    # -- Profile save/load ------------------------------------------------------

    def test_save_and_load_profile(self):
        """Round-trip: save profile then load it back."""
        self.app.sitename.set("ROUNDTRIP")
        self.app.port.set("9999")
        self.app.sections.set("2")
        self.app.section_entries[0]["name"].set("ANIME")

        path = os.path.join(self.temp_dir, "test_profile.json")
        self.app.save_profile_to(path)

        # Create fresh instance and load
        app2 = GlftpdInstallerGUI(MockTk(), testing=True)
        app2.load_profile_from(path)

        self.assertEqual(app2.sitename.get(), "ROUNDTRIP")
        self.assertEqual(app2.port.get(), "9999")
        self.assertEqual(len(app2.section_entries), 2)
        self.assertEqual(app2.section_entries[0]["name"].get(), "ANIME")

    def test_profile_preserves_all_fields(self):
        """Profile JSON should contain all VARIABLE_DEFAULTS keys."""
        path = os.path.join(self.temp_dir, "full_profile.json")
        self.app.save_profile_to(path)

        with open(path) as f:
            data = json.load(f)

        for attr in VARIABLE_DEFAULTS:
            self.assertIn(attr, data, f"Missing key in profile: {attr}")
        self.assertIn("section_entries", data)

    def test_profile_section_entries_format(self):
        """Section entries in profile should have name, path, dated."""
        path = os.path.join(self.temp_dir, "sec_profile.json")
        self.app.save_profile_to(path)

        with open(path) as f:
            data = json.load(f)

        for entry in data["section_entries"]:
            self.assertIn("name", entry)
            self.assertIn("path", entry)
            self.assertIn("dated", entry)

    # -- Cache import -----------------------------------------------------------

    def test_import_cache(self):
        """Import a shell-style install.cache file."""
        cache_content = (
            'sitename="IMPORTED"\n'
            'port="3030"\n'
            'sections="2"\n'
            'section1="FLAC"\n'
            'section1dated="y"\n'
            'section2="XXX"\n'
            'section2dated="n"\n'
            'sectionpath1="/site/FLAC"\n'
            'sectionpath2="/site/XXX"\n'
            'username="importadmin"\n'
        )
        path = os.path.join(self.temp_dir, "test.cache")
        with open(path, "w") as f:
            f.write(cache_content)

        self.app.import_cache_from(path)

        self.assertEqual(self.app.sitename.get(), "IMPORTED")
        self.assertEqual(self.app.port.get(), "3030")
        self.assertEqual(self.app.admin_username.get(), "importadmin")
        self.assertEqual(len(self.app.section_entries), 2)
        self.assertEqual(self.app.section_entries[0]["name"].get(), "FLAC")
        self.assertEqual(self.app.section_entries[0]["dated"].get(), "y")
        self.assertEqual(self.app.section_entries[1]["name"].get(), "XXX")
        self.assertEqual(self.app.section_entries[1]["path"].get(),
                         "/site/XXX")

    def test_import_cache_ignores_comments(self):
        """Lines that are pure comments should be skipped."""
        cache_content = (
            '# This is a comment\n'
            'sitename="TEST" # Name of site\n'
            '# Another comment\n'
        )
        path = os.path.join(self.temp_dir, "comment.cache")
        with open(path, "w") as f:
            f.write(cache_content)

        self.app.import_cache_from(path)
        self.assertEqual(self.app.sitename.get(), "TEST")

    def test_cache_roundtrip(self):
        """generate -> import should preserve values."""
        self.app.sitename.set("ROUNDTRIP")
        self.app.sections.set("2")
        self.app.section_entries[0]["name"].set("SEC_A")
        self.app.section_entries[1]["name"].set("SEC_B")

        content = self.app.generate_cache_content()
        path = os.path.join(self.temp_dir, "roundtrip.cache")
        with open(path, "w") as f:
            f.write(content)

        app2 = GlftpdInstallerGUI(MockTk(), testing=True)
        app2.import_cache_from(path)

        self.assertEqual(app2.sitename.get(), "ROUNDTRIP")
        self.assertEqual(len(app2.section_entries), 2)
        self.assertEqual(app2.section_entries[0]["name"].get(), "SEC_A")
        self.assertEqual(app2.section_entries[1]["name"].get(), "SEC_B")

    # -- Script toggles ---------------------------------------------------------

    def test_select_all_scripts(self):
        self.app._select_all_scripts()
        for name in SCRIPT_VARS:
            self.assertEqual(getattr(self.app, name).get(), "y",
                             f"{name} should be 'y'")

    def test_deselect_all_scripts(self):
        self.app._select_all_scripts()
        self.app._deselect_all_scripts()
        for name in SCRIPT_VARS:
            self.assertEqual(getattr(self.app, name).get(), "n",
                             f"{name} should be 'n'")

    # -- Misc -------------------------------------------------------------------

    def test_disconnect_ssh_without_connection(self):
        self.app.disconnect_ssh()
        self.assertIsNone(self.app.ssh_client)
        self.assertIsNone(self.app.sftp_client)

    def test_matrix_labels_empty_in_testing(self):
        self.assertEqual(self.app.matrix_labels, [])

    def test_noop_methods_in_testing(self):
        """GUI-only methods should not raise in testing mode."""
        self.app.log_message("test")
        self.app.update_progress(2, "TESTING")
        self.app.start_installation()

    def test_simple_var_independence(self):
        self.app.section_entries[0]["name"].set("FLAC")
        self.app.section_entries[1]["name"].set("GAMES")
        self.assertEqual(self.app.section_entries[0]["name"].get(), "FLAC")
        self.assertEqual(self.app.section_entries[1]["name"].get(), "GAMES")

    def test_suppress_rebuild_flag(self):
        """_suppress_rebuild should prevent section rebuilds during bulk ops."""
        self.app._suppress_rebuild = True
        original_count = len(self.app.section_entries)
        self.app.sections.set("10")
        self.assertEqual(len(self.app.section_entries), original_count)
        self.app._suppress_rebuild = False

    # -- SSH helpers ------------------------------------------------------------

    def test_check_ssh_alive_no_client(self):
        """_check_ssh_alive should raise when no SSH client."""
        self.app.ssh_client = None
        with self.assertRaises(ConnectionError):
            self.app._check_ssh_alive()

    def test_check_ssh_alive_dead_transport(self):
        """_check_ssh_alive should raise when transport is inactive."""
        class FakeTransport:
            def is_active(self):
                return False
        class FakeClient:
            def get_transport(self):
                return FakeTransport()
        self.app.ssh_client = FakeClient()
        with self.assertRaises(ConnectionError):
            self.app._check_ssh_alive()

    # -- Input validation -------------------------------------------------------

    def test_validate_inputs_empty_sitename(self):
        """Empty sitename should produce a validation error."""
        self.app.sitename.set("")
        errors = self.app._validate_inputs()
        self.assertTrue(any("Site name" in e for e in errors))

    def test_validate_inputs_sitename_with_spaces(self):
        """Sitename with spaces should produce a validation error."""
        self.app.sitename.set("MY SITE")
        errors = self.app._validate_inputs()
        self.assertTrue(any("spaces" in e for e in errors))

    def test_validate_inputs_invalid_port(self):
        """Non-numeric or out-of-range port should fail validation."""
        self.app.sitename.set("TESTSITE")
        self.app.port.set("abc")
        errors = self.app._validate_inputs()
        self.assertTrue(any("port" in e.lower() for e in errors))

        self.app.port.set("99999")
        errors = self.app._validate_inputs()
        self.assertTrue(any("port" in e.lower() for e in errors))

    def test_validate_inputs_valid(self):
        """Valid inputs should produce no errors."""
        self.app.sitename.set("TESTSITE")
        self.app.port.set("2010")
        self.app.sections.set("3")
        errors = self.app._validate_inputs()
        self.assertEqual(errors, [])

    def test_validate_inputs_empty_section_name(self):
        """Empty section name should produce a validation error."""
        self.app.sitename.set("TESTSITE")
        self.app.section_entries[0]["name"].set("")
        errors = self.app._validate_inputs()
        self.assertTrue(any("Section 1" in e for e in errors))

    def test_disconnect_clears_credentials(self):
        """disconnect_ssh with clear_credentials should wipe password."""
        self.app.ssh_password.set("secret123")
        self.app.disconnect_ssh(clear_credentials=True)
        self.assertEqual(self.app.ssh_password.get(), "")

    def test_disconnect_preserves_credentials_by_default(self):
        """disconnect_ssh without flag should keep password."""
        self.app.ssh_password.set("secret123")
        self.app.disconnect_ssh()
        self.assertEqual(self.app.ssh_password.get(), "secret123")


if __name__ == "__main__":
    unittest.main()
