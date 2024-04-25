from pathlib import Path


class Forger:
    """A class that contains forge functions."""

    @staticmethod
    def _forge_dir(
        path: Path,
        mode: int = 511,
        parents: bool = True,
        exist_ok: bool = True,
    ) -> Path:
        """Forge a directory if it does not exist.

        Args:
            path (Path): The path to the directory.
            mode (int): The mode of the directory.
            parents (bool): Whether to create parent directories.
            exist_ok (bool): Whether to raise an error if the directory exists.

        Returns:
            Path: The path to the directory.

        Raises:
            OSError: If the directory could not be created.
        """
        try:
            path.mkdir(mode, parents, exist_ok)
        except Exception as e:
            raise OSError(
                f"Failed to forge directory: {path}. Error: {str(e)}"
            )
        return path

    dir = _forge_dir

    @staticmethod
    def _forge_file(
        path: Path, mode: int = 438, exist_ok: bool = True
    ) -> Path:
        """Forge a file if it does not exist.

        Args:
            path (Path): The path to the file.
            mode (int): The mode of the file.
            exist_ok (bool): Whether to raise an error if the file exists.

        Returns:
            Path: The path to the file.

        Raises:
            OSError: If the file could not be created.
        """
        try:
            path.touch(mode, exist_ok)
        except Exception as e:
            raise OSError(f"Failed to forge file: {path}. Error: {str(e)}")
        return path

    file = _forge_file
