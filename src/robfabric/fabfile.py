# -*- coding: utf-8 -*-

import os
from glob import glob

from fabric.api import lcd, local, put, env, run, sudo, execute, task, abort
from setuptools_scm import get_version

env.use_ssh_config = True


def _find_project_root():
    curdir = os.getcwd()
    while not os.path.isdir('.git'):
        if curdir == os.path.expanduser('~'):
            abort('no .git dir found')
        os.chdir('..')
        curdir = os.getcwd()
    root = os.path.abspath(curdir)
    return root


@task(aliases=['inc_build', 'inc_patch'])
def inc_version_build(pkg='.'):
    with lcd(pkg):
        major, minor, build_num, _ = (get_version().split('.') + [''])[:4]
        build_num = int(build_num) + 1
        tag = "%s.%s.%d" % (major, minor, build_num)
        local('git tag %s -am "%s"' % (tag, tag))


@task(alias='inc_minor')
def inc_version_minor(pkg='.'):
    with lcd(pkg):
        major, minor, _ = get_version().split('.', 2)
        minor = int(minor) + 1
        tag = "%s.%d.0" % (major, minor)
        local('git tag %s -am "%s"' % (tag, tag))


@task(alias='inc_major')
def inc_version_major(pkg='.'):
    with lcd(pkg):
        major, _ = get_version().split('.', 2)
        major = int(major) + 1
        tag = "%d.0.0" % major
        local('git tag %s -am "%s"' % (tag, tag))


@task
def clean(pkg='.'):
    with lcd(pkg):
        local('python setup.py clean --all', capture=False)
        local('/bin/rm -rf build dist *.egg-info', capture=False)


@task
def wheel(pkg='.'):
    with lcd(pkg):
        local('python setup.py bdist_wheel', capture=False)


_dist_file_patterns = {
    'wheel': "*-%(version)s-py2-none-any.whl",
    "bdist": "*-%(version)s.tar.gz"
}


def _get_dist_file_name(dist_type='wheel'):
    pattern = os.path.join('dist', _dist_file_patterns[dist_type] % {'version': get_version()})
    return os.path.basename(glob(pattern)[0])


@task
def deploy(pkg='.'):
    with lcd(pkg):
        put(os.path.join('dist', _get_dist_file_name()), '.')


@task
def install(pkg='.', venv=None, as_root=False):
    # with lcd(pkg):
    #     dist = local('python setup.py --fullname', capture=True).strip()
    #     pkg_file = '%s.tar.gz' % dist
    # if venv:
    #     with prefix('. ~/.local/bin/virtualenvwrapper.sh'), prefix('workon %s' % venv):
    #         run('pip install %s --upgrade --no-cache-dir' % pkg_file)
    # else:
    #     run_or_sudo = sudo if as_root else run
    #     run_or_sudo('pip install %s --upgrade --no-cache-dir -v' % pkg_file)
    with lcd(pkg):
        dist_file = _get_dist_file_name()
        cmde = 'pip install %s --upgrade' % dist_file
        if as_root:
            sudo(cmde)
        else:
            run(cmde + " --user")


@task(default=True)
def all(pkg='.', venv=None, as_root=None):
    execute(wheel, pkg)
    execute(deploy, pkg)
    execute(install, pkg, venv, as_root)


@task
def doc(pkg='.', clean_before='n'):
    sphinx_build = local('which sphinx-build', capture=True)
    build_dir = '_build'

    with lcd(pkg):
        with lcd('doc'):
            if clean_before == 'y':
                local('rm -rf %s' % build_dir)
            local('python %(sphinx_build)s '
                  '-b html -d %(build_dir)s/doctrees source %(build_dir)s/html' % {
                'sphinx_build': sphinx_build,
                'build_dir': build_dir
            }, shell='/bin/bash')

