# exo/networking/peer_handle.py

from typing import Optional


class PeerHandle:
    def __init__(self, peer_id, capabilities, other_metadata=None):
        self.peer_id = peer_id

        # Safe import to avoid circular import
        from exo.topology.device_capabilities import DeviceCapabilities

        # Convert dict to DeviceCapabilities if needed
        if isinstance(capabilities, dict):
            self.capabilities = DeviceCapabilities(**capabilities)
        else:
            self.capabilities = capabilities

        self.other_metadata = other_metadata or {}

    def get_flops_score(self) -> Optional[float]:
        from exo.topology.device_capabilities import DeviceCapabilities

        if isinstance(self.capabilities, DeviceCapabilities):
            flops = self.capabilities.flops
            return flops.fp16 + flops.int8 + flops.fp32
        return None

    def to_dict(self):
        return {
            "peer_id": self.peer_id,
            "capabilities": self.capabilities.to_dict() if hasattr(self.capabilities, "to_dict") else self.capabilities,
            "other_metadata": self.other_metadata,
        }

    def __str__(self):
        return f"<PeerHandle {self.peer_id}: {self.capabilities}>"
