import read_config

from event_hub_strategy import EventHubStrategy
from cmd_strategy import CMDStratedy


class StrategySelector(object):
    def __init__(self, url, filename):
        self.dataset_filename = filename.strip()
        self.dataset_url = url.strip()

        self.strategies = {
            'event_hub': EventHubStrategy(url=self.dataset_url, filename=self.dataset_filename),
            'terminal': CMDStratedy(url=self.dataset_url, filename=self.dataset_filename)
        }

    def execute(self):
        strategy_name = read_config.cfg.get('nulplabs', 'strategy_name')
        self.strategies[strategy_name].execute()