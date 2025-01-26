from decouple import config, Csv
server=config('AD_SERVER', default='ldaps://ip-or-dnsname')
admin=config('AD_ADMIN_USER', default='admin@yourdomain.com')
print(f'server= {server} - admin= {admin}')


from django.conf import settings
settings.configure(
    AD_SERVER=config('AD_SERVER', default='ldaps://ip-or-dnsname'),
    AD_ADMIN_USER=config('AD_ADMIN_USER', default='admin@yourdomain.com'),
)
print(f'settings.AD_SERVER= {settings.AD_SERVER} - settings.AD_ADMIN_USER= {settings.AD_ADMIN_USER}')
