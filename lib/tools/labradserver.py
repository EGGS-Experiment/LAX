from labrad import util

class Labrad_Server(EnvExperiment):
    """
    Runs a labrad server through ARTIQ when run via either artiq_client or artiq_run
    """
    def __init__(self, server):
        self.server = server
        super(Labrad_Server, self).__init__()

    def build(self):
        pass

    def prepare(self):
        pass

    def run(self):
        util.runServer(Pulser_server(self))

    def analyze(self):
        pass
