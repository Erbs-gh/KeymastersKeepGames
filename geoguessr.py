from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet
from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GeoGuessrArchipelagoOptions:
    geoguessr_platinum_medal_maps: GeoGuessrPlatinumMedalMaps
    geoguessr_gold_medal_maps: GeoGuessrGoldMedalMaps
    geoguessr_silver_medal_maps: GeoGuessrSilverMedalMaps
    geoguessr_bronze_medal_maps: GeoGuessrBronzeMedalMaps
    geoguessr_soloduels: GeoGuessrSoloDuels
    geoguessr_teamduels: GeoGuessrTeamDuels


class GeoGuessrGame(Game):
    # Made by @erbs. on Discord

    name = "GeoGuessr"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = GeoGuessrArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Limited to the following mode: MODES",
                data={
                    "MODES": (self.modes, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objective_list = [
            GameObjectiveTemplate(
                label="Play the daily Challenge",
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

        if self.bronzemaps:
            objective_list += [
                GameObjectiveTemplate(
                    label="Get a bronze medal (5k total points) on the MAP map.",
                    data={
                        "MAP": (self.bronzemaps, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Get a bronze medal round (1k points in at least one location) on the MAP map.",
                    data={
                        "MAP": (self.bronzemaps, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ]

        if self.silvermaps:
            objective_list += [
                GameObjectiveTemplate(
                    label="Get a silver medal (15k total points) on the MAP map.",
                    data={
                        "MAP": (self.silvermaps, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Get a silver medal round (3k points in at least one location) on the MAP map.",
                    data={
                        "MAP": (self.silvermaps, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            ]

        if self.goldmaps:
            objective_list += [
                GameObjectiveTemplate(
                    label="Get a gold medal (22.5k total points) on the MAP map.",
                    data={
                        "MAP": (self.goldmaps, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Get a gold medal round (4.5k points in at least one location) on the MAP map.",
                    data={
                        "MAP": (self.goldmaps, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
            ]

        if self.platinummaps:
            objective_list += [
                GameObjectiveTemplate(
                    label="Get a platinum medal (25k total points) on the MAP map.",
                    data={
                        "MAP": (self.platinummaps, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Get a platinum medal round (5k points in at least one location) on the MAP map.",
                    data={
                        "MAP": (self.platinummaps, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
            ]

        if self.soloduels:
            objective_list += [
                GameObjectiveTemplate(
                    label="Play AMOUNT games in solo ranked duels.",
                    data={
                        "AMOUNT": (self.sologames, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win AMOUNT games in solo ranked duels.",
                    data={
                        "AMOUNT": (self.solowins, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
            ]

        if self.teamduels:
            objective_list += [
                GameObjectiveTemplate(
                    label="Play AMOUNT games in ranked teamduels.",
                    data={
                        "AMOUNT": (self.duogames, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win AMOUNT games in ranked teamduels.",
                    data={
                        "AMOUNT": (self.duowins, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
            ]
        return objective_list

    @staticmethod
    def modes() -> List[str]:
        return [
            "Move",
            "No Move",
            "No Move Pan Zoom",
        ]

    @staticmethod
    def sologames() -> List[str]:
        return [
            "3",
            "5",
            "7",
        ]

    @staticmethod
    def solowins() -> List[str]:
        return [
            "2",
            "3",
            "4",
        ]

    @staticmethod
    def duogames() -> List[str]:
        return [
            "3",
            "5",
            "7",
        ]

    @staticmethod
    def duowins() -> List[str]:
        return [
            "2",
            "3",
            "4",
        ]

    def bronzemaps(self) -> List[str]:
        bronzemaps: List[str] = (
        self.archipelago_options.geoguessr_bronze_medal_maps.value
        | self.archipelago_options.geoguessr_silver_medal_maps.value
        | self.archipelago_options.geoguessr_gold_medal_maps.value
        | self.archipelago_options.geoguessr_platinum_medal_maps.value
        )
        return sorted(bronzemaps)

    def silvermaps(self) -> List[str]:
        silvermaps: List[str] = (
        self.archipelago_options.geoguessr_silver_medal_maps.value
        | self.archipelago_options.geoguessr_gold_medal_maps.value
        | self.archipelago_options.geoguessr_platinum_medal_maps.value
        )
        return sorted(silvermaps)

    def goldmaps(self) -> List[str]:
        goldmaps: List[str] = (
        self.archipelago_options.geoguessr_gold_medal_maps.value
        | self.archipelago_options.geoguessr_platinum_medal_maps.value
        | self.archipelago_options.geoguessr_platinum_medal_maps.value
        )
        return sorted(goldmaps)

    def platinummaps(self) -> List[str]:
        platinummaps: List[str] = (
        self.archipelago_options.geoguessr_platinum_medal_maps.value
        )
        return sorted(platinummaps)

    def soloduels(self) -> Boolean:
        return self.archipelago_options.geoguessr_soloduels.value

    def teamduels(self) -> Boolean:
        return self.archipelago_options.geoguessr_teamduels.value


# Archipelago Options
class GeoGuessrBronzeMedalMaps(OptionSet):
    """
    Indicates which Maps the player owns and wants to play with bronze medal requirements.
    """

    display_name = "Maps to get at least a bronze medal score (5k) on"
    default = [
        "World",
        "Famous Places",
        "Germany",
        "Europe",
        "United States",
        "Japan",
        "United Kingdom",
        "France",
        "Spain",
        "Canada",
        "Poland",
        "Italy",
        "Türkiye",
        "Russia",
        "Brazil",
        "Australia",
        "Netherlands",
        "Indonesia",
        "India",
        "Sweden",
        "Switzerland",
        "Norway",
        "Ukraine",
        "Argentina",
        "Finland",
        "New Zealand",
        "Portugal",
        "Greece",
        "Ireland",
        "Romania",
        "Serbia",
        "Denmark",
        "Mexico",
        "Belgium",
        "Croatia",
        "Israel",
        "Thailand",
        "Chile",
        "Austria",
        "Hungary",
        "Bulgaria",
        "Czech Republic",
        "Asia",
        "Taiwan",
        "Colombia",
        "South Korea",
        "Singapore",
        "Philippines",
        "Slovakia",
        "Malaysia",
        "South Africa",
        "Lithuania",
        "Iceland",
        "Slovenia",
        "Africa",
        "Estonia",
        "Latvia",
        "Hong Kong",
        "South America",
        "Peru",
        "Madagascar",
        "Uuruguay",
        "Ecuador",
        "Albania",
        "Greenland",
        "Luxembourg",
        "Puerto Rico",
        "Mongolia",
        "North Macedonia",
        "Monaco",
        "Tunisia",
        "Montenegro",
        "United Arab Emirates",
        "Guatemala",
        "North America",
        "Malta",
        "Nigeria",
        "Bangladesh",
        "Bolivia",
        "Faroe Islands",
        "Dominican Republic",
        "Botswana",
        "Kazakhstan",
        "Kyrgyzstan",
        "Isle of Man",
        "Sri Lanka",
        "Jordan",
        "Kenya",
        "Vietnam",
        "Andorra",
        "Guam",
        "Cambodia",
        "Christmas Island",
        "Oceania",
        "Senegal",
        "Jersey",
        "San Marino",
        "Qatar",
        "Uganda",
        "Ghana",
        "Laos",
        "Gibraltar",
        "Curacao",
        "Lebanon",
        "Liechtenstein",
        "Lesotho",
        "Panama",
        "Rwanda",
        "Bhutan",
        "American Samoa",
        "Eswatini",
        "United States Virgin Islands",
        "Northern Mariana Islands",
        "Sao Tomé and Príncipe",
        "Namibia",
        "Oman",
        "Nepal",
    ]


class GeoGuessrSilverMedalMaps(OptionSet):
    """
    Indicates which Maps the player owns and wants to play with silver medal requirements.
    """

    display_name = "Maps to get at least a silver medal score (15k) on"
    default = []


class GeoGuessrGoldMedalMaps(OptionSet):
    """
    Indicates which Maps the player owns and wants to play with gold medal requirements.
    """

    display_name = "Maps to get at least a gold medal score (22.5k) on"
    default = []


class GeoGuessrPlatinumMedalMaps(OptionSet):
    """
    Indicates which Maps the player owns and wants to play with platinum medal requirements.
    """

    display_name = "Maps to get a platinum medal score (25k) on"
    default = []


class GeoGuessrSoloDuels(Toggle):
    """
    Indicates whether to include solo ranked duels when generating GeoGuessr objectives.
    """

    display_name = "GeoGuessr include ranked soloduel objectives"


class GeoGuessrTeamDuels(Toggle):
    """
    Indicates whether to include solo ranked duels when generating GeoGuessr objectives.
    """

    display_name = "GeoGuessr include ranked teamduel objectives"
