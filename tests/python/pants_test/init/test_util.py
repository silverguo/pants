# Copyright 2018 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).
import os
from contextlib import contextmanager

from pants.fs.fs import safe_filename_from_path
from pants.init.util import init_workdir
from pants.option.option_value_container import OptionValueContainer
from pants.testutil.test_base import TestBase
from pants.util.contextutil import temporary_dir
from pants.util.dirutil import safe_mkdir


class UtilTest(TestBase):
    @contextmanager
    def physical_workdir_base(self) -> OptionValueContainer:
        with temporary_dir() as physical_workdir_base:
            bootstrap_options = self.get_bootstrap_options(
                [f"--pants-physical-workdir-base={physical_workdir_base}"]
            )
            yield bootstrap_options

    def assertExists(self, path):
        self.assertTrue(os.path.exists(path))

    def physical_workdir(self, bootstrap_options):
        if bootstrap_options.pants_physical_workdir_base:
            return os.path.join(
                bootstrap_options.pants_physical_workdir_base,
                safe_filename_from_path(self.pants_workdir),
            )
        else:
            return self.pants_workdir

    def test_init_workdir(self) -> None:
        with self.physical_workdir_base() as bootstrap_options:
            init_workdir(bootstrap_options)
            self.assertExists(os.path.join(self.physical_workdir(bootstrap_options)))

    def test_source_control_repo(self):
        source_control_dirname = ".git"
        with self.physical_workdir_base() as bootstrap_options:
            safe_mkdir(os.path.join(self.build_root, source_control_dirname))
            init_workdir(bootstrap_options)
            self.assertExists(
                os.path.join(self.physical_workdir(bootstrap_options), source_control_dirname)
            )
