from django.core.management.utils import get_random_secret_key
from django.core.checks.security.base import SECRET_KEY_INSECURE_PREFIX

if __name__ == "__main__":
    secret_key = SECRET_KEY_INSECURE_PREFIX + get_random_secret_key()
    print(secret_key)
