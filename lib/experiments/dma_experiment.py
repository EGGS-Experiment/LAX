from artiq.experiment import *
import numpy as np

class DMA_Experiment(EnvExperiment):
    """Loads the experiment on DMA and runs it a given number of times"""
    def build(self):
        self.setattr_device('core')
        self.setattr_device('core_dma')
        self.call_child_method('build')

    @kernel
    def run(self):
        handle = self.core_dma.get_handle('default')
        self.core.reset()
        #run
        while self.numRuns < self.maxRuns:
            try:
                self.core.reset()
                self.core_dma.playback_handle(handle)
                self.numRuns += 1
                self.mutate_dataset('numRuns', 0, self.numRuns)
            except Exception as e:
                print('Pulse Sequence Interrupted')
                break
        print('Pulse Sequence Finished')

class PulseSequence(DMA_Experiment):
    """
    Pulse sequence that runs entirely from DMA.
    Runs a given number of times.
    """
    def build(self):
        self.numRuns = 0
        self.setattr_argument("linetrigger_enabled", BooleanValue(False))
        self.setattr_argument("linetrigger_delay_us", NumberValue(0, ndecimals=0, step=1, type='int'))
        self.setattr_argument("linetrigger_ttl_name", StringValue())
        self.setattr_argument("maxRuns", NumberValue(1, ndecimals=0, step=1, type = 'int'))
        self.set_dataset('numRuns', np.array([0]), broadcast=True)
        self.linetrigger_ttl = self.get_device(self.linetrigger_ttl_name)
        self.call_child_method('build')

    def run(self):
        #linetrigger
        while self.linetrigger_enabled:
            #wait in blocks of 10ms
            time_gate = self.linetrigger_ttl.gate_rising(10 * ms)
            time_trig = self.linetrigger_ttl.timestamp_mu(time_gate)
            #time_trig returns -1 if we dont receive a signal
            if time_trig > 0:
                #set time to now and do an offset delay
                delay(self.linetrigger_delay_us * us)
                break