from pathlib import Path

import pytest
from pytest import MonkeyPatch

from tests.runners import TestRunner


@pytest.fixture
def runner(tmp_path: Path, monkeypatch: MonkeyPatch) -> TestRunner:
    monkeypatch.chdir(tmp_path)
    return TestRunner(str(tmp_path))
