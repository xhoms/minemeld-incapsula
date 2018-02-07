import logging
import requests

from minemeld.ft.basepoller import BasePollerFT
from netaddr import IPNetwork, AddrFormatError

LOG = logging.getLogger(__name__)


class Miner(BasePollerFT):
    url = None

    def configure(self):
        super(Miner, self).configure()
        self.url = self.config.get('url', 'https://my.incapsula.com/api/integration/v1/ips')

    def _detect_ip_version(self, ip_addr):
        try:
            parsed = IPNetwork(ip_addr)
        except (AddrFormatError, ValueError):
            LOG.error('{} - Unknown IP version: {}'.format(self.name, ip_addr))
            return None

        if parsed.version == 4:
            return 'IPv4'

        if parsed.version == 6:
            return 'IPv6'

        return None

    def _build_iterator(self, item):
        payload = {'resp_format': 'text'}
        r = requests.post(self.url, payload)
        i = r.text.splitlines()
        return i

    def _process_item(self, item):
        indicator = item
        value = {
            'type': self._detect_ip_version(item),
        }
        return [[indicator, value]]
