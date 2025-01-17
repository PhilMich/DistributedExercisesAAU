import random

from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub


class GossipMessage(MessageStub):

    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        x = 0
        while x < 10:
            x = x + 1
            message = GossipMessage(self.index(), random.randint(0, self.number_of_devices()), self._secrets)

            self.medium().send(message)

            if len(self._secrets) == self.number_of_devices():
                continue

            ingoing = self.medium().receive()
            if ingoing is None:
                continue
            else:
                self._secrets.update(ingoing.secrets)
        # the following is your termination condition, but where should it be placed?
        return

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')
