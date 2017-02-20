import os
import shutil
import subprocess
from charmhelpers.core import hookenv
from charmhelpers.fetch import apt_install
from charmhelpers.core.host import service_start
from charms.reactive import when, when_not, set_state, hook
from charmhelpers.contrib.python.packages import pip_install


def copy_service_files():
    for f in os.listdir('./files'):
        if f.endswith('.service'):
            shutil.copy(
                os.path.join('files', f),
                os.path.join('/usr/lib/systemd/user/', f)
            )


@when_not('sentry.installed')
def install_sentry():
    conf = hookenv.config()
    version = conf.get('version', '8.13.0')
    apt_install(['libffi-dev', 'libssl-dev', 'libpq-dev', 'libjpeg-dev'])
    pip_install(['cffi', 'cryptography', 'sentry==%s' % version])
    copy_service_files()

    set_state('sentry.installed')


@when('db.available')
@when('redis.available')
@when('sentry.installed')
def setup_sentry():
    conf = hookenv.config()
    admin_email = conf.get('admin_email', 'sentry@localhost')
    admin_password = conf.get('admin_password', 'sentry')

    # TODO Enter DB info into Sentry conf

    subprocess.check_output(
        ['sentry', 'upgrade', '--noinput']
    )

    subprocess.check_output(
        ['sentry', 'createuser', '--email', admin_email, '--password', admin_password, '--superuser']
    )

    service_start('sentry-worker')
    service_start('sentry-web')

    # TODO need both?
    set_state('sentry.available')
    set_state('website.available')


@when('website.available')
def website_available(website):
    conf = hookenv.config()
    # TODO non hardcoded port
    website.configure(9000)
