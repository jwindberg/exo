import asyncio
from typing import Optional

from exo.networking.discovery import Discovery
from exo.networking.connection import NodeConnection
from exo.networking.transport import Transport
from exo.networking.discovery_result import DiscoveryResult


class ManualDiscovery(Discovery):
    def __init__(self):
        self._node: Optional[NodeConnection] = None
        self._cancelled = False

    async def discover(self) -> DiscoveryResult:
        from exo.topology.device_capabilities import DeviceCapabilities  # moved here

        while not self._cancelled and self._node is None:
            await asyncio.sleep(0.5)

        if self._node is None:
            raise Exception("ManualDiscovery was cancelled before a peer was added.")

        capabilities = self._node.capabilities
        if isinstance(capabilities, dict):
            capabilities = DeviceCapabilities(**capabilities)

        return DiscoveryResult(
            connection=self._node,
            capabilities=capabilities
        )

    def add_peer(self, connection: NodeConnection):
        self._node = connection

    def cancel(self):
        self._cancelled = True
