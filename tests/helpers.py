import os
from pathlib import Path
from typing import List


def verify_generated_files(working_dir: str, files: List[str]) -> None:
    """Assert that the expected files to be generated are created."""
    for file in files:
        full_path = Path(os.path.join(working_dir, file))
        assert full_path.exists(), f"Templated file '{str(full_path)}' was not created"
