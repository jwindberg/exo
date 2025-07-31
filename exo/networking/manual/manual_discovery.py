import asyncio

from exo.networking.discovery import Discovery


class ManualDiscovery(Discovery):
    def __init__(self):
        self._node = None
        self._cancelled = False

    async def discover(self):
        from exo.topology.device_capabilities import DeviceCapabilities  # moved here to avoid circular import

        while not self._cancelled and self._node is None:
            await asyncio.sleep(0.5)

        if self._node is None:
            raise Exception("ManualDiscovery was cancelled before a peer was added.")

        capabilities = self._node.capabilities
        if isinstance(capabilities, dict):
            capabilities = DeviceCapabilities(**capabilities)

        return self._node, capabilities

    def add_peer(self, connection):
        self._node = connection

    def cancel(self):
        self._cancelled = True
