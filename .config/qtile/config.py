#### Qtile config.py
## V3

### Imports

## User imports
# Import the os and subprocess modules, allowing us to interact with the system.
import os
import subprocess

## Default imports
from typing import List  # noqa: F401

# Append the hook module to be imported from the libqtile lib.
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

### Variables

## Default variables
# [mod] key, usually defaulted to windows key or alike.
mod = "mod4"

# Define terminal. Allows users and programs to use the variable data,
#   without having to know the specific terminal.
terminal = guess_terminal()

## User variables
# Define different options for nvim, here the 'desired' dir, into variables.
#   Also allows for alacritty -e to accept multiple arguments, with the help
#   of formatters, such as %s, to use the variables data.
nvim_config = 'nvim /home/ghost/.config/'
nvim_python = 'nvim /home/ghost/Python/'

##! But thats alot of defining !#

### Lists
# nvim
local_dirs = [ 
    '--working-directory /home/ghost/.config/',
    '--working-directory /home/ghost/Python/',
    '--working-directory /home/ghost/Python/Education/Practice/',
    '--working-directory /home/ghost/Notes/',
    ]
# Alacritty Variations
alacritty_var = [
    'alacritty',
    'alacritty %s -e nvim' % local_dirs[0],
    'alacritty %s -e nvim' % local_dirs[1],
    'alacritty %s -e nvim' % local_dirs[2],
    'alacritty %s -e nvim' % local_dirs[3],
    'alacritty --working-directory /home/ghost/Wallpapers/ -e ranger',
    ]

# Autostart.sh hook
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

keys = [
    Key([mod], "6", lazy.spawn(alacritty_var[1])),
    Key([mod], "7", lazy.spawn(alacritty_var[2])),
    Key([mod], "8", lazy.spawn(alacritty_var[3])),
    Key([mod], "9", lazy.spawn(alacritty_var[4])),

    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "m", lazy.layout.next(),
        desc="Move window focus to other window"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

groups = [
    Group('1',
        label='',
        init=True,
        persist=True,
        spawn=[alacritty_var[1], alacritty_var[3]],
        layout='Stack',
        ),

    Group('2',
        label='',
        spawn='firefox-bin',
        layout='max',
        ),

    Group('3',
        label='',
        spawn='spotify',
        layout='max',
        ),

    Group('4',
        label='',
        layout='max',
        ),

    Group('5',
        label='',
        ),
    ]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [

    layout.Stack(num_stacks=2, border_width=0, margin=0),
    layout.Max(margin=0, border_width=0),

]

widget_defaults = dict(

    font='SourceCodePro Bold',
    fontsize=12,
    padding=3,

)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [

                #widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.Spacer(),
                widget.WindowName(width=bar.CALCULATED),
                widget.Spacer(),
                widget.Systray(),
                widget.Clock(format='%a %I:%M %p'),

            ],
            25,
            margin=0,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

auto_fullscreen = True
focus_on_window_activation = "never"

wmname = "LG3D"
