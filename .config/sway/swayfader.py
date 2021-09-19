import asyncio
import dataclasses
from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Dict, List, Optional

from i3ipc.aio import Connection
from i3ipc import Con, Event
import toml


@dataclass
class Rule:
    app_id: str
    floating: Optional[bool]
    focused: float
    unfocused: float


@dataclass
class Config:
    focused: float = 1
    unfocused: float = 0.98
    rate: float = 0.016
    steps: float = 14
    rules: List[Rule] = field(default_factory=list)


cfg = Config()
cfg_basedir = Path(os.getenv("XDG_CONFIG_HOME") or (Path.home() / ".config"))
cfg_path = cfg_basedir / "swayfade.toml"


if cfg_path.exists():
    with open(cfg_path) as f:
        cfg_dict = toml.load(f)
        default_rule = Rule(app_id="", floating=None, focused=1, unfocused=1)
        cfg_dict["rules"] = [
            dataclasses.replace(default_rule, **r) for r in cfg_dict["rules"]
        ]
        cfg = dataclasses.replace(cfg, **cfg_dict)

cfg.steps = 1 / cfg.steps


def lerp(start: float, end: float, step: float):
    return start + step * (end - start)


async def set_opacity(c: Con, f: float):
    await c.command(f"opacity {f}")


@dataclass
class Container:
    opacity: float
    task: Optional[asyncio.Task]
    focused: float
    unfocused: float


# globals
focused: Con
container: Dict[int, Container] = dict()


def get_opacity_rule(win: Con):
    floating = win.type == "floating_con"
    rules = [
        r
        for r in cfg.rules
        if (not r.app_id or win.app_id == r.app_id)
        and (
            (r.floating is None) or (r.floating is not None and floating == r.floating)
        )
    ]
    return (
        (rules[0].focused, rules[0].unfocused)
        if rules
        else (cfg.focused, cfg.unfocused)
    )


async def init_container(con):
    if con.type in ["con", "floating_con"]:
        f, u = get_opacity_rule(con)
        opacity = f if con == focused else u
        container[con.id] = Container(
            opacity=opacity, task=None, focused=f, unfocused=u
        )
        await set_opacity(con, opacity)


async def fade(con: Con, con_data: Container, focused: bool):
    start = con_data.opacity
    end = con_data.focused if focused else con_data.unfocused
    o = start
    step = 0.0
    while abs(o - end) > cfg.steps:
        o = lerp(start, end, step)
        step += cfg.steps
        await set_opacity(con, o)
        con_data.opacity = o
        await asyncio.sleep(cfg.rate)
    await set_opacity(con, end)
    con_data.opacity = end


def reset_fade(con: Con, focused: bool):
    # create container data if it doesn't exist
    global container
    con_data = container.get(con.id)
    if con_data is None:
        focused, unfocused = get_opacity_rule(con)
        con_data = Container(
            opacity=unfocused, focused=focused, unfocused=unfocused, task=None
        )
        container[con.id] = con_data

    # cancel an existing fade task if one exists
    task = con_data.task
    if task:
        task.cancel()
    con_data.task = asyncio.create_task(fade(con, con_data, focused))


def on_window_focus(c: Connection, e: Event):
    global focused
    # skips firing when focusing from parent
    if focused is None or focused.id == e.container.id:
        return

    reset_fade(focused, False)
    reset_fade(e.container, True)
    focused = e.container


def on_window_floating(c: Connection, e: Event):
    asyncio.create_task(init_container(e.container))


async def main():
    connection = await Connection(auto_reconnect=True).connect()
    tree = await connection.get_tree()
    global focused
    focused = [con for con in tree if con.focused][0]
    await asyncio.gather(*[init_container(con) for con in tree])
    connection.on(Event.WINDOW_FOCUS, on_window_focus)
    connection.on(Event.WINDOW_FLOATING, on_window_floating)
    await connection.main()


asyncio.get_event_loop().run_until_complete(main())


