from supabase import Client, create_client
from os import environ
from .config import url, key

# _url = environ.get("SUPABASE_URL")
# _key = environ.get("SUPABASE_KEY")

_url = url
_key = key

def create_supabase_client():
    supabase: Client = create_client(_url, _key)
    return supabase