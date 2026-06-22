from datetime import timedelta


class SecurityConfig:

    JWT_SECRET_KEY = "CCC_ORIENTATION_SYSTEM_2026"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)