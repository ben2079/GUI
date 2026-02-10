
'''Hier ist eine produktionsreife, lauffähige Lösung, die das CUDA-Initialisierungsproblem behebt, 
indem CUDA_VISIBLE_DEVICES garantiert VOR dem Import von torch gesetzt wird. 
Zudem fällt die App robust auf CPU zurück, wenn CUDA nicht korrekt initialisiert werden kann. 
Enthalten: Drop-in-Initialisierer + Qt6/PySide6 GUI zum Testen.

Datei: torch_init.py
---------------------
'''
import os
import sys
import logging
from typing import Optional

log = logging.getLogger("torch_init")
if not log.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

def init_torch_cuda(preferred_gpus: Optional[str] = None) -> None:
    """
    Muss so früh wie möglich im Prozess aufgerufen werden – VOR jedem 'import torch'!

    Fix:
    - Setzt CUDA_VISIBLE_DEVICES vor dem Import von torch.
    - Verhindert die typische Warnung: "CUDA initialization: CUDA unknown error ..."
      die entsteht, wenn CUDA_VISIBLE_DEVICES nach Programmstart oder nach torch-Import
      geändert wird.

    Parameter:
      preferred_gpus: z. B. "0" oder "0,1". None lässt die System-Defaults unangetastet.
    """
    if "torch" in sys.modules:
        # Zu spät – torch bereits geladen. Wir loggen deutlich und lassen CPU-Fallback zu.
        log.warning(
            "init_torch_cuda() wurde nach dem Import von torch aufgerufen. "
            "Änderungen an CUDA_VISIBLE_DEVICES greifen jetzt nicht mehr. "
            "Bitte rufen Sie init_torch_cuda() vor jedem 'import torch' auf."
        )
        return

    if preferred_gpus is not None:
        value = ",".join([p.strip() for p in preferred_gpus.split(",") if p.strip() != ""])
        os.environ["CUDA_VISIBLE_DEVICES"] = value
        log.info("CUDA_VISIBLE_DEVICES vor torch-Import gesetzt auf: %s", value)

def summarize_torch_environment(t):
    """
    Erzeugt eine robuste Zusammenfassung der Torch/CUDA-Umgebung.
    """
    info = {
        "torch_version": getattr(t, "__version__", "unknown"),
        "cuda_compiled_version": getattr(t.version, "cuda", None),
        "cuda_is_available": False,
        "device_count": 0,
        "devices": [],
        "cudnn_enabled": getattr(t.backends, "cudnn", None) and t.backends.cudnn.enabled,
    }
    try:
        info["cuda_is_available"] = bool(t.cuda.is_available())
    except Exception as e:
        info["cuda_is_available"] = False
        info["cuda_error"] = f"{type(e).__name__}: {e}"

    try:
        if info["cuda_is_available"]:
            cnt = int(t.cuda.device_count())
            info["device_count"] = cnt
            info["devices"] = [t.cuda.get_device_name(i) for i in range(cnt)]
    except Exception as e:
        info["device_count"] = 0
        info["devices_error"] = f"{type(e).__name__}: {e}"

    return info

def select_device(t, index: int = 0) -> str:
    """
    Wählt sicher ein Device-String ("cuda:<idx>" oder "cpu").
    """
    try:
        if t.cuda.is_available() and t.cuda.device_count() > index:
            return f"cuda:{index}"
    except Exception:
        pass
    return "cpu"

