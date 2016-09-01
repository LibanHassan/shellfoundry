import os

import click

from shellfoundry.exceptions import WrongShellYmlException, ShellYmlMissingException
from shellfoundry.utilities.package_builder import PackageBuilder
from shellfoundry.utilities.shell_config_reader import ShellConfigReader
from shellfoundry.utilities.shell_package_builder import ShellPackageBuilder
from shellfoundry.utilities.shell_package import ShellPackage


class PackCommandExecutor(object):

    def __init__(self):
        self.config_reader = ShellConfigReader()
        self.package_builder = PackageBuilder()
        self.shell_package_builder = ShellPackageBuilder()

    def pack(self):

        current_path = os.getcwd()

        shell_package = ShellPackage(current_path)
        if shell_package.is_tosca():
            self.shell_package_builder.pack(current_path)
        else:
            self._pack_old_school_shell(current_path)

    def _pack_old_school_shell(self, current_path):
        try:
            config = self.config_reader.read()
            self.package_builder.build_package(current_path, config.name, config.driver_name)
        except ShellYmlMissingException:
            click.echo(u'shell.yml file is missing')
        except WrongShellYmlException:
            click.echo(u'shell.yml format is wrong')
