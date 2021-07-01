import subprocess
from collections import deque
import yaml
import time
import logging
import sys


class Expe:
    """
    Class repesenting an Expe
    """
    def __init__(self, config):
        self.params = deque(config["params"])
        self.running_expes = {}
        self.max_concurrent_expe = config["max_concurrent_expe"]
        self.script_path = config["script_path"]
        self.sleep_time = config["sleep_time"]
        logging.basicConfig(format="%(asctime)s %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def start_next_expe(self):
        """
        Start the next expe
        """
        param = self.params.popleft()
        proc = subprocess.Popen(["sh", self.script_path, str(param)], stdout = subprocess.DEVNULL)
        self.running_expes[param] = proc
        self.logger.info("Starting expe: '%s %s'", self.script_path, param)

    def restart_expe(self, param):
        """
        Restart an expe
        """
        proc = subprocess.Popen([self.script_path, param])
        self.running_expes[param] = proc

    def get_terminated_expes(self):
        """
        Returns the params of the terminated expes
        """
        terminated_expes = []
        for param, proc in self.running_expes.items():
            if proc.poll() is not None:
                # the expe is terminated
                terminated_expes.append((param, proc.returncode))
        return terminated_expes

    def run(self):
        """
        Run the expe
        """

        while len(self.params) > 0:
            self.logger.info("Still %s expe remaining", len(self.params))
            terminated_expes = self.get_terminated_expes()
            for (param, code) in terminated_expes:
                self.running_expes.pop(param)
                if code != 0:
                    self.params.append(param)
                    self.logger.warning("Expe '%s %s' has exited with code %s",
                                        self.script_path,
                                        param,
                                        code)
                else:
                    self.logger.info("Expe '%s %s' has exited with code %s",
                                     self.script_path,
                                     param,
                                     code)
            nb_free_spots = min(self.max_concurrent_expe - len(self.running_expes), len(self.params))
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
        print(config)
        expe = Expe(config)
        expe.run()

if __name__ == "__main__":
    main()
