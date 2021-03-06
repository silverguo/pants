# Copyright 2020 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from typing import List, Type

from pants.backend.python.rules.importable_python_sources import ImportablePythonSources
from pants.backend.python.rules.importable_python_sources import (
    rules as importable_python_sources_rules,
)
from pants.core.target_types import Files
from pants.engine.addresses import Address
from pants.engine.selectors import Params
from pants.engine.target import Sources, Target, Targets
from pants.testutil.option.util import create_options_bootstrapper
from pants.testutil.test_base import TestBase


class MockTarget(Target):
    alias = "mock_target"
    core_fields = (Sources,)


class ImportablePythonSourcesTest(TestBase):
    @classmethod
    def rules(cls):
        return (*super().rules(), *importable_python_sources_rules())

    def create_target(
        self, *, parent_directory: str, files: List[str], target_cls: Type[Target] = MockTarget
    ) -> Target:
        self.create_files(parent_directory, files=files)
        address = Address(spec_path=parent_directory, target_name="target")
        return target_cls({Sources.alias: files}, address=address)

    def test_adds_missing_inits_and_strips_source_roots(self) -> None:
        target_with_init = self.create_target(
            parent_directory="src/python/project", files=["lib.py", "__init__.py"]
        )
        target_without_init = self.create_target(
            parent_directory="src/python/test_project", files=["f1.py", "f2.py"]
        )
        files_target = self.create_target(
            parent_directory="src/python/project/resources",
            files=["loose_file.txt"],
            target_cls=Files,
        )
        result = self.request_single_product(
            ImportablePythonSources,
            Params(
                Targets([target_with_init, target_without_init, files_target]),
                create_options_bootstrapper(),
            ),
        )
        assert sorted(result.snapshot.files) == sorted(
            [
                "project/lib.py",
                "project/__init__.py",
                "test_project/f1.py",
                "test_project/f2.py",
                "test_project/__init__.py",
                "src/python/project/resources/loose_file.txt",
            ]
        )
