"""
Broom: a simple, local parameter sweep runner
"""
import subprocess
from collections import deque
import csv
import logging
import sys
import time
import yaml

class Expe:
    """
    Class repesenting an Expe
    """
    def __init__(self, config):
        if "params" in config:
            self.params = dict(enumerate(config["params"]))
        elif "params_file" in config:
            csv_filename = config["params_file"]
            with open(csv_filename) as csv_file:
                spamreader = csv.reader(csv_file, delimiter=',')
                self.params = dict(enumerate(spamreader))
        else:
            sys.exit(1)
        self.remaining_expes = deque(range(len(self.params)))
        self.running_expes = {}
        self.max_concurrent_expe = config["max_concurrent_expe"]
        self.script_path = config["script_path"]
        self.sleep_time = config["sleep_time"]
        logging.basicConfig(format="%(asctime)s %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def get_command_str(self, param_id):
        """
        Returns the string of the command for a parameter
        """
        return " ".join(map(str, self.params[param_id]))

    def start_next_expe(self):
        """
        Start the next expe
        """
        param_id = self.remaining_expes.popleft()
        param = self.params[param_id]
        proc = subprocess.Popen(["sh", self.script_path] + list(map(str, param)),
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        self.running_expes[param_id] = proc
        self.logger.info("Starting expe %d: '%s %s'",
                         param_id,
                         self.script_path,
                         self.get_command_str(param_id))

    def get_terminated_expes(self):
        """
        Returns the params of the terminated expes
        """
        terminated_expes = []
        for param_id, proc in self.running_expes.items():
            if proc.poll() is not None:
                # the expe is terminated
                terminated_expes.append((param_id, proc.returncode))
        return terminated_expes

    def run(self):
        """
        Run the expe
        """
        while len(self.remaining_expes) > 0 or len(self.running_expes) > 0:
            self.logger.info("Still %s expe remaining (%f %%)",
                             len(self.remaining_expes),
                             int(100 * (1.0 - len(self.remaining_expes) / len(self.params))))
            terminated_expes = self.get_terminated_expes()
            for (param_id, code) in terminated_expes:
                self.running_expes.pop(param_id)
                if code != 0:
                    self.remaining_expes.append(param_id)
                    self.logger.warning("Expe #%d '%s %s' has exited with code %s",
                                        param_id,
                                        self.script_path,
                                        self.get_command_str(param_id),
                                        code)
                else:
                    self.logger.info("Expe #%d '%s %s' has exited with code %s",
                                     param_id,
                                     self.script_path,
                                     self.get_command_str(param_id),
                                     code)
            nb_free_spots = min(self.max_concurrent_expe - len(self.running_expes),
                                len(self.remaining_expes))
            for _ in range(nb_free_spots):
                self.start_next_expe()

            time.sleep(self.sleep_time)

def main():
    """
    main function
    """
    args = sys.argv
    filename = args[1]
    with open(filename, 'r') as config_file:
        config = yaml.load(config_file)
        expe = Expe(config)
        expe.run()

if __name__ == "__main__":
    main()
