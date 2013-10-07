import socket

from os import path

from fabric.api import run, env
from fabric.colors import green, yellow
from fabric.contrib.files import append, contains, exists, sed
from fabric.decorators import task
from fabric.operations import put, reboot
from fabric.utils import abort


@task
def write_hosts():
    """ 
    Set a /etc/hosts file based on the hosts provided with the -H parameter
    """

    if 'systems' not in env.keys():
        env.systems = {}
        for host in env.all_hosts:
            ip = str(socket.gethostbyname(host))
            if ip in env.systems.keys():
                env.systems[ip].append(host)
            else:
                env.systems[ip] = [host]

    if not contains("/etc/hosts", "## Added from fabric configurator"):
        ip = str(socket.gethostbyname(env.host))
        
        hostnames = ' '.join(env.systems[ip])

        run('mv /etc/hosts /etc/hosts.old')
        append("/etc/hosts", "## Added from fabric configurator")
        append('/etc/hosts', "127.0.0.1 %s" % hostnames)
        #append('/etc/hosts', "::1 %s" % hostnames)
        append('/etc/hosts', "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4")
        append('/etc/hosts', "::1         localhost localhost.localdomain localhost6 localhost6.localdomain6")

        for system in env.systems.items():
            if not env.host in system[1]:
                append('/etc/hosts', "%s %s" % (system[0], ' '.join(system[1])))

        print(green("/etc/hosts of the system %s configured" % env.host))

    else:
        print(yellow("The system %s had the /etc/hosts already configured" % env.host))


@task
def write_hostname():
    """ 
    Set the hostname of the system
    """

    hostname = run('hostname')
    if hostname != env.host and not hostname in env.all_hosts:
        run("hostname %s" % env.host)
        sed("/etc/sysconfig/network", "^HOSTNAME=.*$", "HOSTNAME=%s" % env.host)
        print(green("The system %s now has the hostname defined" % env.host))
    else:
        print(yellow("The system %s had the hostname already configured" % env.host))


@task
def disable_selinux():
    """ 
    Disable the selinux of the system
    """
    run('lokkit --selinux=disabled')
    print(green('The system %s has now the SELinux disable'))


@task
def ssh_keys(force=False):
    """ 
    Copy an authorized_keys file in the .ssh folder of the root user
    """
    run('mkdir -p ~/.ssh/ && chmod 700 ~/.ssh/')
    if not path.exists('authorized_keys'):
        abort('authorized_keys file not found')

    if (not exists('~/.ssh/authorized_keys') or force):
        put(local_path='authorized_keys', remote_path='~/.ssh/authorized_keys', mode=0644)
        print(green("SSH keys provided to %s" % env.host))
    else:
        print(yellow("Already exists an authorized_keys file on %s, not changes taken" % env.host))


@task
def prepare():
    """ 
    Script that prepare the system: Set hostname, /etc/hosts, disable selinux,
    copy authorized_keys (ssh credentials) and reboot the system
    """
    if not exists('/root/.fabric.prepared'): 
        write_hosts()
        write_hostname()
        disable_selinux()
        ssh_keys()
        append('/root/.fabric.prepared', '')
        reboot()
    else:
        print(yellow("Skipped system %s " % env.host))
