"""Mock dotenv module for testing when actual python-dotenv is not available."""

def load_dotenv(dotenv_path=None, stream=None, verbose=False, override=False, interpolate=True, encoding="utf-8"):
    """Mock load_dotenv function that does nothing."""
    pass

def find_dotenv(filename=".env", raise_error_if_not_found=False, usecwd=False):
    """Mock find_dotenv function."""
    return filename

def dotenv_values(dotenv_path=None, stream=None, verbose=False, interpolate=True, encoding="utf-8"):
    """Mock dotenv_values function that returns empty dict.""" 
    return {}

def set_key(dotenv_path, key_to_set, value_to_set, quote_mode="always", export=False, encoding="utf-8"):
    """Mock set_key function."""
    return (True, key_to_set, value_to_set)

def get_key(dotenv_path, key_to_get, encoding="utf-8"):
    """Mock get_key function."""
    return None

def unset_key(dotenv_path, key_to_unset, quote_mode="always", encoding="utf-8"):
    """Mock unset_key function."""
    return (True, key_to_unset)