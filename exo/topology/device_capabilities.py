from typing import Any
from pydantic import BaseModel
import psutil
import pynvml
import platform

TFLOPS = 1.00

class DeviceFlops(BaseModel):
    fp32: float
    fp16: float
    int8: float

    def __str__(self):
        return f"fp32: {self.fp32 / TFLOPS:.2f} TFLOPS, fp16: {self.fp16 / TFLOPS:.2f} TFLOPS, int8: {self.int8 / TFLOPS:.2f} TFLOPS"

    def to_dict(self):
        return self.model_dump()

class DeviceCapabilities(BaseModel):
    model: str
    chip: str
    memory: int
    flops: DeviceFlops

    def __str__(self):
        return f"Model: {self.model}. Chip: {self.chip}. Memory: {self.memory}MB. Flops: {self.flops}"

    def model_post_init(self, __context: Any) -> None:
        if isinstance(self.flops, dict):
            self.flops = DeviceFlops(**self.flops)

    def to_dict(self):
        return {
            "model": self.model,
            "chip": self.chip,
            "memory": self.memory,
            "flops": self.flops.to_dict()
        }

UNKNOWN_DEVICE_CAPABILITIES = DeviceCapabilities(
    model="Unknown Model",
    chip="Unknown Chip",
    memory=0,
    flops=DeviceFlops(fp32=0, fp16=0, int8=0)
)

async def device_capabilities():
    gpu_total_mem = None
    gpu_free_mem = None

    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        try:
            gpu_memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            gpu_total_mem = gpu_memory_info.total
            gpu_free_mem = gpu_memory_info.free
        except pynvml.NVMLError_NotSupported:
            print("[WARN] NVML: Memory info not supported on this platform (likely Jetson)")
        except pynvml.NVMLError as e:
            print(f"[WARN] NVML: Other error fetching memory info: {e}")
    except pynvml.NVMLError_LibraryNotFound:
        print("[WARN] NVML: Library not found, skipping GPU info.")
    except pynvml.NVMLError as e:
        print(f"[WARN] NVML: Failed to initialize NVML: {e}")
    finally:
        try:
            pynvml.nvmlShutdown()
        except:
            pass

    memory_mb = (gpu_total_mem // 2**20) if gpu_total_mem else psutil.virtual_memory().total // 2**20

    return DeviceCapabilities(
        model="Jetson Orin Nano",
        chip="Jetson",
        memory=memory_mb,
        flops=DeviceFlops(fp32=0, fp16=0, int8=0)
    )