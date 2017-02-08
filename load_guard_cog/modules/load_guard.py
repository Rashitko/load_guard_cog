import os
from time import sleep

import psutil
import yaml
from up.base_thread_module import BaseThreadModule
from up.registrar import UpRegistrar

from load_guard_cog.commands.panic_command import PanicCommandFactory, PanicCommand, PanicCommandHandler
from load_guard_cog.registrar import Registrar


class LoadGuard(BaseThreadModule):

    DEFAULT_INTERVAL = 1
    DEFAULT_PANIC_THRESHOLD = 80
    DEFAULT_CALM_DOWN_THRESHOLD = 65

    def __init__(self):
        super().__init__()
        self.__interval = self.DEFAULT_INTERVAL
        self.__cpu_utilization = None
        self.__ram = None
        self.__panic_threshold = self.DEFAULT_PANIC_THRESHOLD
        self.__calm_down_threshold = self.DEFAULT_CALM_DOWN_THRESHOLD
        self.__in_panic = False
        self.__handle = None

    def _execute_start(self):
        self.__handle = self.up.command_executor.register_command(PanicCommand.NAME, PanicCommandHandler())
        super()._execute_start()
        return True

    def _execute_stop(self):
        super()._execute_stop()
        if self.__handle is not None:
            self.up.command_executor.unregister_command(PanicCommand.NAME, PanicCommandHandler())

    def _execute_initialization(self):
        self.__init_from_config()
        super()._execute_initialization()

    def _loop(self):
        while self._run:
            self.__cpu_utilization = psutil.cpu_percent()
            if not self.in_panic and self.cpu_utilization >= self.panic_threshold:
                self.__enter_panic()
            if self.in_panic and self.cpu_utilization <= self.calm_down_threshold:
                self.__leave_panic()
            virtual_mem = psutil.virtual_memory()
            self.__ram = virtual_mem.percent
            sleep(self.interval)

    def load(self):
        return True

    def __init_from_config(self):
        config_path = os.path.join(os.getcwd(), UpRegistrar.CONFIG_PATH, Registrar.CONFIG_NAME)
        if os.path.isfile(config_path):
            with open(config_path) as f:
                config = yaml.load(f)
                self.__interval = config.get(Registrar.INTERVAL_KEY, self.DEFAULT_INTERVAL)
                self.__panic_threshold = float(config.get(Registrar.PANIC_THRESHOLD_KEY, self.DEFAULT_PANIC_THRESHOLD))
                self.__calm_down_threshold = float(config.get(
                    Registrar.CALM_DOWN_THRESHOLD_KEY, self.DEFAULT_CALM_DOWN_THRESHOLD
                ))

    def __enter_panic(self):
        self.__in_panic = True
        self.__send_panic_command()

    def __leave_panic(self):
        self.__in_panic = False
        self.__send_panic_command()

    def __send_panic_command(self):
        cmd = PanicCommandFactory.create(self.in_panic, self.cpu_utilization)
        self.up.command_executor.execute_command(cmd)

    @property
    def telemetry_content(self):
        return {
            'load': {
                'cpu': self.cpu_utilization,
                'ram': self.ram
            }
        }

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        self.__interval = value

    @property
    def panic_threshold(self):
        return self.__panic_threshold

    @panic_threshold.setter
    def panic_threshold(self, value):
        self.__panic_threshold = value

    @property
    def calm_down_threshold(self):
        return self.__calm_down_threshold

    @calm_down_threshold.setter
    def calm_down_threshold(self, value):
        self.__calm_down_threshold = value

    @property
    def cpu_utilization(self):
        return self.__cpu_utilization

    @property
    def ram(self):
        return self.__ram

    @property
    def in_panic(self):
        return self.__in_panic
