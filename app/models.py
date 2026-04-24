from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SensorInfo:
    key: str
    name: str
    pins: str
    note: str
    default_gpio: Optional[int] = None
    micropython_hint: str = ""


@dataclass
class FeatureInfo:
    key: str
    name: str
    description: str
    micropython_hint: str = ""


@dataclass
class ParsedRequest:
    original_text: str
    normalized_text: str
    sensors: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    gpio_candidates: List[int] = field(default_factory=list)
    seconds: Optional[int] = None
    milliseconds: Optional[int] = None
    notes: List[str] = field(default_factory=list)
