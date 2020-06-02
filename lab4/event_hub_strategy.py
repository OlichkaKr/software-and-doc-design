import pandas as pd
import read_config
from sodapy import Socrata
from azure.eventhub import EventHubClient, EventData

from base_strategy import BaseStrategy

NUMBER_OF_MESSAGES = int(read_config.cfg.get('nulplabs', 'number_of_messages'))
ENCODING = read_config.cfg.get('nulplabs', 'encoding')
MESSAGES_PER_FETCH = int(read_config.cfg.get('nulplabs', 'messages_per_fetch'))


class EventHubStrategy(BaseStrategy):
    def __init__(self, url, filename):
        super(EventHubStrategy, self).__init__(url, filename)

    def execute(self):
        dataset_id = '{}_{}'.format(self.dataset_url, self.dataset_filename)
        latest_status = self.redis_client.get(dataset_id)
        if latest_status is not None:
            latest_status = latest_status.decode(ENCODING)

        client = EventHubClient(read_config.cfg.get('nulplabs', 'hub_address'),
                                debug=False,
                                username=read_config.cfg.get('nulplabs', 'hub_user'),
                                password=read_config.cfg.get('nulplabs', 'hub_passwd'))
        sender = client.add_sender(partition="0")
        client.run()

        if latest_status == 'COMPLETED' or latest_status == 'ATTEMPT TO REFILL':
            self.redis_client.set(dataset_id, 'ATTEMPT TO REFILL')
            print('ATTEMPT TO REFILL')
            return False

        client = Socrata(self.dataset_url, None)
        self.redis_client.set(dataset_id, 'STARTED')

        for i in range(int(NUMBER_OF_MESSAGES / MESSAGES_PER_FETCH)):
            results = client.get(self.dataset_filename, limit=MESSAGES_PER_FETCH, offset=MESSAGES_PER_FETCH * i)
            results_df = pd.DataFrame.from_records(results)

            current_progress = '{} - {}'.format(str(i * MESSAGES_PER_FETCH + 1), str((i + 1) * MESSAGES_PER_FETCH))
            message = EventData(body=results_df.to_json())
            sender.send(message)
            self.redis_client.set(dataset_id, current_progress)

            print('Progress {}'.format(current_progress))
            print(results_df)

        self.redis_client.set(self.dataset_url + "_" + self.dataset_filename, 'COMPLETED')
        print('COMPLETED')