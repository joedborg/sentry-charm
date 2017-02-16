import subprocess
from charmhelpers.core import hookenv
from charmhelpers.fetch import apt_install
from charms.reactive import when, when_not, set_state
from charmhelpers.contrib.python.packages import pip_install
from charmhelpers.core.host import service_running, service_start, service_restart


@when_not('sentry.installed')
def install_sentry():
    conf = hookenv.config()
    version = conf.get('version', '8.13.0')

    apt_install(['libpq-dev', 'libjpeg-dev'])

    pip_install('sentry==%s' % version)

    set_state('sentry.installed')


@when('database.available')
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

    set_state('sentry.available')

