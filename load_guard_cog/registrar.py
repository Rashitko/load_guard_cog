from up.registrar import UpRegistrar


class Registrar(UpRegistrar):

    NAME = 'load_guard_cog'
    CONFIG_NAME = 'load_guard.yml'

    PANIC_THRESHOLD_KEY = 'panic threshold'
    CALM_DOWN_THRESHOLD_KEY = 'calm down threshold'
    INTERVAL_KEY = 'interval'

    CONFIG_TEMPLATE = """\
%s: 80
%s: 65
%s: 0.5
""" % (PANIC_THRESHOLD_KEY, CALM_DOWN_THRESHOLD_KEY, INTERVAL_KEY)

    def __init__(self):
        super().__init__(self.NAME)

    def register(self):
        external_modules = self._load_external_modules()
        if external_modules is not None:
            self._register_modules_from_file()
            self._create_config(self.CONFIG_NAME, self.CONFIG_TEMPLATE)
            return True
        return False
