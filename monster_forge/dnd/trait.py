from dataclasses import dataclass, field
from monster_forge.dnd.enums import LimitedUsageType
from typing import Final
from monster_forge.dnd.constants import PHRASES_TO_CAPITALIZE

MACRO_MON: Final[str] = "[MON]"


@dataclass
class Trait:
    host_creature_name: str
    title: str
    description: str
    limited_use_type: LimitedUsageType = field(default=LimitedUsageType.UNLIMITED)
    limited_use_charges: dict[str, int] = field(default_factory=dict)
    has_lair: bool = field(default=False)
    lair_charge_bonuses: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.host_creature_name = " ".join(
            [c.capitalize() for c in self.host_creature_name.split(" ")]
        )
        self.title = " ".join([c.capitalize() for c in self.title.split(" ")])
        self._format_description()
        if (
            self.limited_use_type == LimitedUsageType.X_PER_DAY
            and "x" not in self.limited_use_charges
        ):
            raise ValueError(
                "x required in limited use charges if making a X_PER_DAY trait"
            )
        if self.limited_use_type == LimitedUsageType.RECHARGE_X_Y and (
            "x" not in self.limited_use_charges or "y" not in self.limited_use_charges
        ):
            raise ValueError(
                "x and y required in limited use charges if making a RECHARGE_X_Y trait"
            )

    def _format_description(self) -> None:
        self.description = self.description.strip().rstrip(".")
        self.description = self.description.replace(MACRO_MON, self.host_creature_name)
        for phrase_to_capitalize in PHRASES_TO_CAPITALIZE:
            self.description = self.description.replace(
                phrase_to_capitalize, phrase_to_capitalize.capitalize()
            )

    @property
    def limited_usage_str(self) -> str:
        if self.limited_use_type == LimitedUsageType.UNLIMITED:
            return ""
        match self.limited_use_type:
            case LimitedUsageType.X_PER_DAY:
                x = self.limited_use_charges["x"]
                if self.has_lair:
                    x_bonus = self.lair_charge_bonuses["x"]
                    return f"({x}/Day, or {x + x_bonus}/Day in Lair)"
                return f"({x}/Day)"
            case LimitedUsageType.RECHARGE_X_Y:
                x = self.limited_use_charges["x"]
                y = self.limited_use_charges["y"]
                return f"(Recharge {x}-{y})"
            case LimitedUsageType.RECHARGE_AFTER_SHORT_OR_LONG_REST:
                return "(Recharge after a Short or Long Rest)"
            case _:
                raise NotImplementedError

    def as_homebrewery_v3_2024_markdown(self) -> str:
        return f"***{self.title}{' ' + self.limited_usage_str if self.limited_usage_str else ''}.*** {self.description}."

    def display_str(self) -> str:
        return f"{self.title}{' ' + self.limited_usage_str if self.limited_usage_str else ''}. {self.description}."


@dataclass
class LegendaryResistance(Trait):
    title: str = field(default="Legendary Resistance")
    description: str = field(
        default="If the [MON] fails a saving throw, it can choose to succeed instead."
    )
    limited_use: bool = field(default=True)
    limited_use_type: LimitedUsageType = field(default=LimitedUsageType.X_PER_DAY)
    limited_use_charges: dict[str, int] = field(default_factory=lambda: {"x": 3})
