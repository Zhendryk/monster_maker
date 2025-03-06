from __future__ import annotations
import pandas as pd
from pathlib import Path
from enum import Enum, auto
from monster_forge.dnd.enums import Size, CreatureType
from collections.abc import Sequence

MonsterDataType = str | float | int | bool | Size | CreatureType


class OperationType(Enum):
    MEAN = auto()
    MEDIAN = auto()
    MODE = auto()
    MIN = auto()
    MAX = auto()

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @classmethod
    def from_display_name(cls, name: str) -> OperationType:
        for e in cls:
            if e.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return e
        raise ValueError(f"Invalid {cls.__name__}: {name}")


class MonsterManual2024Database:
    def __init__(self) -> None:
        self._filepath = Path(__file__).resolve().parent / "data" / "mm_2024_stats.csv"
        self._column_names = [
            "Monster Name",
            "CR",
            "AC",
            "Min HP",
            "Max HP",
            "Avg HP",
            "Number of Attacks",
            "Size",
            "Creature Type",
            "STR",
            "DEX",
            "CON",
            "INT",
            "WIS",
            "CHA",
            "Legendary",
            "Swarm",
        ]
        self._df = self._read_monster_csv(self._filepath)
        if self._df is None:
            raise RuntimeError

    def _read_monster_csv(self, file_path: str) -> pd.DataFrame | None:
        """
        Reads a CSV file containing monster data and ensures correct data types.

        :param file_path: Path to the CSV file.
        :return: Pandas DataFrame with the correctly typed monster data.
        """
        try:
            df = pd.read_csv(
                file_path,
                dtype={column_name: "string" for column_name in self._column_names},
            )

            # Convert to correct types manually to handle errors
            for column in self._column_names:
                match column:
                    case "Monster Name":
                        df[column] = df[column].astype(str)
                    case "CR":
                        df[column] = df[column].astype(float)
                    case "AC":
                        df[column] = df[column].astype(int)
                    case "Min HP" | "Max HP" | "Avg HP" | "Number of Attacks" | "STR" | "DEX" | "CON" | "INT" | "WIS" | "CHA":
                        df[column] = df[column].astype(int)
                    case "Legendary" | "Swarm":
                        df[column] = (
                            df[column]
                            .astype(str)
                            .str.lower()
                            .map({"1": True, "0": False})
                        )
                    case "Size":
                        df[column] = df[column].apply(
                            lambda cell: [
                                Size.from_display_name(s.strip())
                                for s in cell.split(",")
                            ]
                        )
                    case "Creature Type":
                        df[column] = df[column].apply(
                            lambda cell: [
                                CreatureType.from_display_name(ct.strip())
                                for ct in cell.split(",")
                            ]
                        )
                    case _:
                        raise NotImplementedError
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

    def query(
        self,
        filters: dict[str, MonsterDataType],
        aggregate_column_name: str,
        operation: OperationType = OperationType.MEAN,
    ) -> tuple[float, int]:
        try:
            query_df = self._df.copy()
            for column_name, value in filters.items():
                match column_name:
                    case "Size" | "Creature Type":
                        query_df = query_df[
                            query_df[column_name].apply(lambda cell: value in cell)
                        ]
                    case _:
                        query_df = query_df[query_df[column_name] == value]
            sample_size = len(query_df[aggregate_column_name])
            match operation:
                case OperationType.MEAN:
                    return query_df[aggregate_column_name].mean(), sample_size
                case OperationType.MEDIAN:
                    return query_df[aggregate_column_name].median(), sample_size
                case OperationType.MODE:
                    return query_df[aggregate_column_name].mode(), sample_size
                case OperationType.MIN:
                    return query_df[aggregate_column_name].min(), sample_size
                case OperationType.MAX:
                    return query_df[aggregate_column_name].max(), sample_size
                case _:
                    raise NotImplementedError
        except Exception as e:
            raise ValueError(f"Error querying database: {e}") from e

    @property
    def column_names(self) -> Sequence[str]:
        return self._column_names
