from pathlib import Path

from unstructured.staging.base import elements_from_json, elements_to_json


class ElementCache:
    """Handles caching and retrieval of unstructured elements as JSON files."""

    def __init__(self, base_dir: str | Path | None = None):
        """
        Initialize the cache. Optional base_dir can override the original file's path.
        """
        self.base_dir = Path(base_dir) if base_dir else None

    def get_norm_json_path(self, path: str | Path) -> Path:
        """Generates a normalized JSON file path by replacing spaces with underscores."""
        path = Path(path)
        json_name = path.with_suffix(".json").name.replace(" ", "_")

        # If a base directory is set, save cache there; otherwise, save next to original file
        parent_dir = self.base_dir if self.base_dir else path.parent
        return parent_dir / json_name

    def load(self, path: str | Path) -> list | None:
        """Loads elements from the cache if the file exists."""
        json_cache_path = self.get_norm_json_path(path)
        if json_cache_path.exists():
            try:
                return elements_from_json(filename=str(json_cache_path))
            except OSError as e:
                print(f"Error reading cache file {json_cache_path}: {e}")
                return None
        return None

    def store(self, elements: list, path: str | Path) -> bool:
        """Stores elements into the cache, creating directories if necessary."""
        try:
            json_cache_path = self.get_norm_json_path(path)
            json_cache_path.parent.mkdir(parents=True, exist_ok=True)
            elements_to_json(elements, filename=str(json_cache_path))
            return True
        except OSError as e:
            print(f"File system error caching elements to {path}: {e}")
            return False
        except (TypeError, ValueError) as e:
            print(f"Serialization error caching elements: {e}")
            return False
