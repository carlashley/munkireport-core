"""Wrappers for certain CFPreferences implementations."""
from typing import Any, Callable, Optional

try:
    from Foundation import CFPreferencesCopyAppValue
except ImportError:
    pass

try:
    from Foundation import (
        CFPreferencesAppSynchronize,
        CFPreferencesSetValue,
        kCFPreferencesAnyUser,
        kCFPreferencesCurrentHost,
    )
except ImportError:
    pass


try:
    from PyObjCTools.Conversion import pythonCollectionFromPropertyList
except ImportError:
    pass


def _o2p(obj: Any, helper: Optional[Callable]) -> Any:
    """Internal method for converting *most* PyObjC data types to native Python data types.
    :param obj: object to convert
    :param helper: optional helper function to use if the conversion fails"""
    try:
        result = pythonCollectionFromPropertyList(obj, conversionHelper=helper)
    except NameError:
        return None
    finally:
        return result


def read(bundle_id: str, key: str) -> Optional[Any]:
    """Wrapper for the PyObjC Foundation implementation of CFPreferencesCopyAppValue.
    Read a preference key from a given bundle id. Preference heirarchy is:
        - MCX/Configuration profile
        - /var/root/Library/Preferences/ByHost
        - /var/root/Library/Preferences
        - /Library/Preferences
        - ~/Library/Preferences
        - .GlobalPreferences (defined at various levels by host, user, system)
    :param bundle_id: preference domain/preference path
    :param key: the preference key to read"""
    try:
        result = CFPreferencesCopyAppValue(key, bundle_id)
    except NameError:
        return None
    finally:
        try:
            return _o2p(result)
        except Exception:
            return result


def write(key: str, value: Any, bundle_id: str) -> None:
    """Wrapper for writing preferences to a given bundle id.
    :param key: the name of the key being written
    :param value: the value to write
    :param bundle_id: preference domain/preference path"""
    try:
        CFPreferencesSetValue(key, value, bundle_id, kCFPreferencesAnyUser, kCFPreferencesCurrentHost)
        CFPreferencesAppSynchronize(bundle_id)  # required for 'cfprefs' to actually sync the change
    except NameError:
        pass
