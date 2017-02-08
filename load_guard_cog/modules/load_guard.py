from time import sleep

import psutil
from up.base_thread_module import BaseThreadModule


class LoadGuard(BaseThreadModule):

    DEFAULT_DELAY = 1

    def __init__(self):
        super().__init__()
        self.__delay = self.DEFAULT_DELAY
        self.__cpu_utilization = None
        self.__ram = None

    def _execute_start(self):
        super()._execute_start()
        return True

    def _execute_stop(self):
        super()._execute_stop()

    def _execute_initialization(self):
        super()._execute_initialization()

    def _loop(self):
        while self._run:
            self.__cpu_utilization = psutil.cpu_percent()
            virtual_mem = psutil.virtual_memory()
            self.__ram = virtual_mem.percent
            sleep(self.delay)

    def load(self):
        return True

    @property
    def telemetry_content(self):
        return {
            'load': {
                'cpu': self.cpu_utilization,
                'ram': self.ram
            }
        }

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value

    @property
    def cpu_utilization(self):
        return self.__cpu_utilization

    @property
    def ram(self):
        return self.__ram
