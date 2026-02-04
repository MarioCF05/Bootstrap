import os
import subprocess
import socket

from libqtile import bar, layout, hook, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

# -----------------------
# AUTOSTART (feh)
# -----------------------
@hook.subscribe.startup_once
def autostart():
    wallpaper = "/home/y4g0ut/Downloads/Galery/Wallpaper/wallpaper.jpg"
    if os.path.exists(wallpaper):
        subprocess.Popen(["feh", "--bg-fill", wallpaper])
    else:
        print(f"Wallpaper no encontrado: {wallpaper}")

# -----------------------
# Función para obtener la IP
# -----------------------
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return f"IP: {ip}"
    except Exception:
        return "IP: N/A"

# -----------------------
# WIDGETS / BARRA
# -----------------------
widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=6,
)
extension_defaults = widget_defaults.copy()

def status_bar():
    return bar.Bar(
        [
            widget.GroupBox(highlight_method="block"),
            widget.WindowName(),
            widget.Spacer(),
            widget.GenPollText(func=get_ip, update_interval=10),
            widget.Battery(format="{percent:2.0%}"),
            widget.Clock(format="%Y-%m-%d %H:%M"),
        ],
        24,
        opacity=0.95,
    )

# -----------------------
# SCREENS (MULTIMONITOR)
# -----------------------
screens = [
    Screen(top=status_bar()),  # Pantalla principal
    Screen(top=status_bar()),  # Segunda pantalla
]

# -----------------------
# KEYBINDINGS
# -----------------------
keys = [
    # Mover foco (flechas)
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),

    # Mover ventanas dentro del layout
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),

    # Redimensionar
    Key([mod, "control"], "Left", lazy.layout.grow_left()),
    Key([mod, "control"], "Right", lazy.layout.grow_right()),
    Key([mod, "control"], "Down", lazy.layout.grow_down()),
    Key([mod, "control"], "Up", lazy.layout.grow_up()),

    Key([mod], "n", lazy.layout.normalize()),

    # Apps
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "r", lazy.spawn("rofi -show drun")),

    # Layout / ventanas
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),

    # Cambiar ventana dentro del layout
    Key([mod], "space", lazy.layout.next()),

    # -----------------------
    # Pantallas / Monitores
    # -----------------------
    # Cambiar foco entre pantallas
    Key([mod], "u", lazy.to_screen(0)),  # Ir a pantalla 1
    Key([mod], "i", lazy.to_screen(1)),  # Ir a pantalla 2
    Key([mod], "o", lazy.to_screen(2)),  # Ir a pantalla 3 (si hay)

    # Mover ventana actual a otra pantalla
    Key([mod, "shift"], "u", lazy.window.toscreen(0)),  # Mover ventana a pantalla 1
    Key([mod, "shift"], "i", lazy.window.toscreen(1)),  # Mover ventana a pantalla 2
    Key([mod, "shift"], "o", lazy.window.toscreen(2)),  # Mover ventana a pantalla 3

    # Qtile
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
]

# -----------------------
# WORKSPACES (5)
# -----------------------
groups = [Group(i) for i in "12345"]

for g in groups:
    keys.extend([
        Key([mod], g.name, lazy.group[g.name].toscreen(0)),  # Asigna grupo a pantalla 1
        Key([mod, "shift"], g.name, lazy.window.togroup(g.name, switch_group=True)),
    ])

# -----------------------
# LAYOUTS
# -----------------------
layouts = [
    layout.Columns(border_width=3, margin=6),
    layout.Max(),
]

# -----------------------
# MOUSE
# -----------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# -----------------------
# FLOATING RULES
# -----------------------
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(title="pinentry"),
        Match(wm_class="ssh-askpass"),
    ]
)

# -----------------------
# MISC
# -----------------------
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
cursor_warp = False

wmname = "LG3D"
