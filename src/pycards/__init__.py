import importlib
import pkgutil
from pathlib import Path

_PKG_DIR = Path(__file__).parent
_CARD_TYPES = ("creature", "Instant", "land", "sorcery")

for _type in _CARD_TYPES:
    _type_pkg = f"{__name__}.{_type}"
    
    for _info in pkgutil.iter_modules([str(_PKG_DIR / _type)]):

        if not _info.ispkg:
            continue
        try:
            importlib.import_module(f"{_type_pkg}.{_info.name}.model")
        except Exception as e:
            print(f"[pycards] skip {_type}/{_info.name}: {e}")

        try:
            importlib.import_module(f"{_type_pkg}.{_info.name}.simulate")
        except Exception as e:
            pass