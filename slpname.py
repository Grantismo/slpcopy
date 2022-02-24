# -*- coding: UTF-8 -*-
import slippi
import dataclasses
import unicodedata
from collections import defaultdict
import glob
import traceback
import os
import re


CSSCharacter = slippi.id.CSSCharacter
Stage = slippi.id.Stage
PlayerType = slippi.event.Start.Player.Type


@dataclasses.dataclass
class Character:
    id: CSSCharacter
    name: str
    short_name: str
    colors: list


@dataclasses.dataclass
class Player:
    player: slippi.event.Start.Player
    character: Character
    metadata_player: slippi.metadata.Metadata.Player

    def team(self):
        return self.player.team

    def type(self):
        return self.player.type

    def color(self):
        return self.character.colors[self.player.costume]

    def character_name(self):
        return self.character.name

    def tag(self):
        return unicodedata.normalize('NFKD', self.player.tag)

    def netplay_code(self):
        if not self.metadata_player:
            return None
        return self.metadata_player.netplay.code

    def netplay_name(self):
        if not self.metadata_player:
            return None
        return self.metadata_player.netplay.name


DEFAULT_COLOR = "Default"
ID_TO_STAGE_NAME = {Stage.FOUNTAIN_OF_DREAMS: "Fountain of Dreams",
                    Stage.POKEMON_STADIUM: "Pokémon Stadium",
                    Stage.PRINCESS_PEACHS_CASTLE: "Princess Peach's Castle",
                    Stage.KONGO_JUNGLE: "Kongo Jungle",
                    Stage.BRINSTAR: "Brinstar",
                    Stage.CORNERIA: "Corneria",
                    Stage.YOSHIS_STORY: "Yoshi's Story",
                    Stage.ONETT: "Onett",
                    Stage.MUTE_CITY: "Mute City",
                    Stage.RAINBOW_CRUISE: "Rainbow Cruise",
                    Stage.JUNGLE_JAPES: "Jungle Japes",
                    Stage.GREAT_BAY: "Great Bay",
                    Stage.HYRULE_TEMPLE: "Hyrule Temple",
                    Stage.BRINSTAR_DEPTHS: "Brinstar Depths",
                    Stage.YOSHIS_ISLAND: "Yoshi's Island",
                    Stage.GREEN_GREENS: "Green Greens",
                    Stage.FOURSIDE: "Fourside",
                    Stage.MUSHROOM_KINGDOM_I: "Mushroom Kingdom I",
                    Stage.MUSHROOM_KINGDOM_II: "Mushroom Kingdom II",
                    Stage.VENOM: "Venom",
                    Stage.POKE_FLOATS: "Poké Floats",
                    Stage.PRINCESS_PEACHS_CASTLE: "Princess Peach's Castle",
                    Stage.BIG_BLUE: "Big Blue",
                    Stage.ICICLE_MOUNTAIN: "Icicle Mountain",
                    Stage.ICETOP: "Icetop",
                    Stage.FLAT_ZONE: "Flat Zone",
                    Stage.DREAM_LAND_N64: "Dream Land N64",
                    Stage.YOSHIS_ISLAND_N64: "Yoshi's Island N64",
                    Stage.KONGO_JUNGLE_N64: "Kongo Jungle N64",
                    Stage.BATTLEFIELD: "Battlefield",
                    Stage.FINAL_DESTINATION: "Final Destination"}

CHARACTERS = [
    Character(
        id=CSSCharacter.CAPTAIN_FALCON,
        name="Captain Falcon",
        short_name="Falcon",
        colors=[DEFAULT_COLOR, "Black", "Red", "White", "Green", "Blue"],
    ),
    Character(
        id=CSSCharacter.DONKEY_KONG,
        name="Donkey Kong",
        short_name="DK",
        colors=[DEFAULT_COLOR, "Black", "Red", "Blue", "Green"],
    ),
    Character(
        id=CSSCharacter.FOX,
        name="Fox",
        short_name="Fox",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green"],
    ),
    Character(
        id=CSSCharacter.GAME_AND_WATCH,
        name="Mr. Game & Watch",
        short_name="G&W",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green"],
    ),
    Character(
        id=CSSCharacter.KIRBY,
        name="Kirby",
        short_name="Kirby",
        colors=[DEFAULT_COLOR, "Yellow", "Blue", "Red", "Green", "White"],
    ),
    Character(
        id=CSSCharacter.BOWSER,
        name="Bowser",
        short_name="Bowser",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Black"],
    ),
    Character(
        id=CSSCharacter.LINK,
        name="Link",
        short_name="Link",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Black", "White"],
    ),
    Character(
        id=CSSCharacter.LUIGI,
        name="Luigi",
        short_name="Luigi",
        colors=[DEFAULT_COLOR, "White", "Blue", "Red"],
    ),
    Character(
        id=CSSCharacter.MARIO,
        name="Mario",
        short_name="Mario",
        colors=[DEFAULT_COLOR, "Yellow", "Black", "Blue", "Green"],
    ),
    Character(
        id=CSSCharacter.MARTH,
        name="Marth",
        short_name="Marth",
        colors=[DEFAULT_COLOR, "Red", "Green", "Black", "White"],
    ),
    Character(
        id=CSSCharacter.MEWTWO,
        name="Mewtwo",
        short_name="Mewtwo",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green"],
    ),
    Character(
        id=CSSCharacter.NESS,
        name="Ness",
        short_name="Ness",
        colors=[DEFAULT_COLOR, "Yellow", "Blue", "Green"],
    ),
    Character(
        id=CSSCharacter.PEACH,
        name="Peach",
        short_name="Peach",
        colors=[DEFAULT_COLOR, "Daisy", "White", "Blue", "Green"],
    ),
    Character(
        id=CSSCharacter.PIKACHU,
        name="Pikachu",
        short_name="Pikachu",
        colors=[DEFAULT_COLOR, "Red", "Party Hat", "Cowboy Hat"],
    ),
    Character(
        id=CSSCharacter.ICE_CLIMBERS,
        name="Ice Climbers",
        short_name="ICs",
        colors=[DEFAULT_COLOR, "Green", "Orange", "Red"],
    ),
    Character(
        id=CSSCharacter.JIGGLYPUFF,
        name="Jigglypuff",
        short_name="Puff",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Headband", "Crown"],
    ),
    Character(
        id=CSSCharacter.SAMUS,
        name="Samus",
        short_name="Samus",
        colors=[DEFAULT_COLOR, "Pink", "Black", "Green", "Purple"],
    ),
    Character(
        id=CSSCharacter.YOSHI,
        name="Yoshi",
        short_name="Yoshi",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Yellow", "Pink", "Cyan"],
    ),
    Character(
        id=CSSCharacter.ZELDA,
        name="Zelda",
        short_name="Zelda",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green", "White"],
    ),
    Character(
        id=CSSCharacter.SHEIK,
        name="Sheik",
        short_name="Sheik",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green", "White"],
    ),
    Character(
        id=CSSCharacter.FALCO,
        name="Falco",
        short_name="Falco",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green"],
    ),
    Character(
        id=CSSCharacter.YOUNG_LINK,
        name="Young Link",
        short_name="YLink",
        colors=[DEFAULT_COLOR, "Red", "Blue", "White", "Black"],
    ),
    Character(
        id=CSSCharacter.DR_MARIO,
        name="Dr. Mario",
        short_name="Doc",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green", "Black"],
    ),
    Character(
        id=CSSCharacter.ROY,
        name="Roy",
        short_name="Roy",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green", "Yellow"],
    ),
    Character(
        id=CSSCharacter.PICHU,
        name="Pichu",
        short_name="Pichu",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green"],
    ),
    Character(
        id=CSSCharacter.GANONDORF,
        name="Ganondorf",
        short_name="Ganon",
        colors=[DEFAULT_COLOR, "Red", "Blue", "Green", "Purple"],
    )
]
ID_TO_CHARACTER = {c.id: c for c in CHARACTERS}


def description(player):
    if player.netplay_name():
        return player.netplay_name()
    if player.tag():
        return player.tag()
    if player.color() != DEFAULT_COLOR:
        return player.color()
    return None


def player_name(player):
    name = player.character_name()
    desc = description(player)
    if player.type() == PlayerType.CPU:
        name = "CPU " + name
    if not desc:
        return name
    return f"{name} ({desc})"


def teams_name(players):
    teams = defaultdict(list)
    for player in players:
        teams[player.team()].append(player_name(player))
    names = [" & ".join(name) for name in teams.values()]
    return " vs ".join(names)


def timestamp(path):
    match = re.search(r"\d{8}T\d{6}", path)  # YYYYmmddThhmmss
    if match:
        return match.group(0)
    return None


def get_players(game):
    metadata_players = game.metadata.players if game.metadata else [None] * 4
    return [Player(
        player=player,
        character=ID_TO_CHARACTER[player.character], metadata_player=metadata_player)
        for player, metadata_player in zip(game.start.players, metadata_players) if player]


def descriptive_filename(path):
    g = slippi.Game(path, skip_frames=True)
    players = get_players(g)
    if g.start.is_teams:
        name = teams_name(players)
    else:
        name = " vs ".join([player_name(p) for p in players])
    stage = ID_TO_STAGE_NAME[g.start.stage]
    file_name = f"{name} - {stage}.slp"
    ts = timestamp(path)
    if not ts:
        return file_name
    return f"{ts} - {file_name}"
