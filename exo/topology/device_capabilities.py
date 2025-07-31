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
    flops=DeviceFlops(fp32=0, fp16=0, int8=0),
  )
