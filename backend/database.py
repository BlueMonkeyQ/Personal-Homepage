from supabase import Client, create_client
from os import environ

_url = environ.get("SUPABASE_URL")
_key = environ.get("SUPABASE_KEY")

supabase: Client = create_client(_url, _key)