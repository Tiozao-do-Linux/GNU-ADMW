from decouple import config, Csv

# Retrieve the configuration parameters from .env:
ENV = {
        'AD_DOMAIN': config('AD_DOMAIN',default='yourdomain.com'),
        'AD_SERVER': config('AD_SERVER', default='ldaps://ip-or-dnsname'),
        'AD_ADMIN_USER': config('AD_ADMIN_USER', default='admin@yourdomain.com'),
        'AD_ADMIN_PASSWORD': config('AD_ADMIN_PASSWORD', default='password-of-admin'),

        'AD_USER_ATTRS': config('AD_USER_ATTRS', default=[], cast=Csv()),
        'AD_GROUP_ATTRS': config('AD_GROUP_ATTRS', default=[], cast=Csv()),

        'AD_SEARCH_BASE': config('AD_SEARCH_BASE', default='DC=yourdomain,DC=com'),
        'AD_SEARCH_USER': config('AD_SEARCH_USER', default='OU=Users,DC=yourdomain,DC=com'),
        'AD_SEARCH_GROUP': config('AD_SEARCH_GROUP', default='OU=Groups,DC=yourdomain,DC=com'),
        'AD_GROUP_REQUIRED': config('AD_GROUP_REQUIRED', default='CN=Turma da Monica,CN=Groups,DC=yourdomain,DC=com'),
        'AD_GROUP_DENY': config('AD_GROUP_DENY', default='CN=Deny,OU=Groups,DC=yourdomain,DC=com'),

        'SECRET_KEY': config('SECRET_KEY',default='your-secret-key-here'),
        'DEBUG': config('DEBUG',default=False, cast=bool),
        'ALLOWED_HOSTS': config('ALLOWED_HOSTS', default=['*'], cast=Csv()),
        'CSRF_TRUSTED_ORIGINS' : config('CSRF_TRUSTED_ORIGINS', default=['https://'], cast=Csv()),
        'DATABASE_URL': config('DATABASE_URL',default=None),
        'TIME_ZONE': config('TIME_ZONE',default='America/Campo_Grande'),
}
