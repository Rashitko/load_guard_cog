from up.commands.command import BaseCommand, BaseCommandHandler
from up.utils.up_logger import UpLogger


class PanicCommand(BaseCommand):
    NAME = 'load_guard.panic'

    PANIC_KEY = 'panic'
    UTILIZATION_KEY = 'utilization'

    def __init__(self):
        super().__init__(PanicCommand.NAME)


class PanicCommandFactory:
    @staticmethod
    def create(is_panic, utilization) -> PanicCommand:
        cmd = PanicCommand()
        cmd.data = {PanicCommand.PANIC_KEY: is_panic, PanicCommand.UTILIZATION_KEY: utilization}
        return cmd


class PanicCommandHandler(BaseCommandHandler):
    def __init__(self):
        super().__init__()
        self.__logger = UpLogger.get_logger()

    def run_action(self, command):
        in_panic = command.data.get(PanicCommand.PANIC_KEY, None)
        if in_panic is not None:
            if in_panic:
                self.__logger.warning('ENTERING Panic Mode')
            else:
                self.__logger.info('LEAVING Panic Mode')
