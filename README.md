# Luna Neo

An updated Windows XP look for **Zorin OS 18**: XP's glossy taskbar, green Start button,
blue title bars and red close button, freshened up for a modern GNOME desktop.

- **7 colour variants**: the three XP shipped with (**Blue**, **Olive Green**, **Silver**)
  plus the later official ones (**Royale**, **Royale Noir**, **Zune**, **Embedded**)
- **A dark version of each** (`-Dark`), for 14 themes in total
- **A floating, content-width taskbar**: centred and only as wide as it needs to be, like
  the macOS dock, instead of running edge to edge
- **An XP Start button** with the Zorin logo painted in the four Windows-flag colours
- **The Zorin Menu keeps its layout** but gets XP colours: blue frame, white app column,
  tinted places column and orange divider
- **XP window controls**: square buttons with a white rim and bevel, and a red-orange close
  button
- **XP-style yellow tooltips** on the taskbar
- **Bundled Win11 icons** (see [Credits](#credits))

## Requirements

- Zorin OS 18 (GNOME Shell 46) with its default **Zorin Taskbar** and **Zorin Menu**
  extensions
- The **User Themes** extension (enabled by default on Zorin OS)
- `python3` (preinstalled)

Luna Neo is built on top of Zorin's own *ZorinBlue* themes. `install` copies their GTK files
from `/usr/share/themes` into each Luna Neo theme, so those must be present (they are on every
Zorin OS install).

## Install

```bash
git clone https://github.com/nidan2703/Zorin-dows-XP-Theme.git luna-neo
cd luna-neo
./luna-neo.sh install
./luna-neo.sh apply Blue
```

`install` copies the themes to `~/.themes` and the icons to `~/.local/share/icons`. No root
access is needed and no system files are touched.

## Switching and undoing

```bash
./luna-neo.sh list              # show all variants
./luna-neo.sh apply OliveGreen  # switch colours
./luna-neo.sh apply Silver-Dark # dark version of a variant
./luna-neo.sh revert            # restore your previous look
```

`apply` sets the shell, GTK and icon themes, switches the desktop to light or dark mode to
match, and sets the taskbar to content-width. The first time you run it, your current
settings are saved to `~/.config/luna-neo/`, and `revert` restores them.

Apps that are already open keep their old look until you restart them.

## Customising

All colours live in the `VARIANTS` table at the top of [`build.py`](build.py). Edit them,
then run `./luna-neo.sh install` again to rebuild and reinstall.

## Known limitations

- **Apps that draw their own title bar** keep their own look. These are mostly Electron and
  Chromium apps such as Chrome, VS Code, Slack and the Claude desktop app.
- **Flatpak apps** only use the theme if they can read `~/.themes`. Those that can't fall
  back to their default look. To give one access, run
  `flatpak override --user --filesystem=~/.themes:ro <app-id>`.
- **Newer GNOME apps (libadwaita)** take the XP colours and title bars, but not every
  detail of the theme.
- **The Start button can't show a "start" label**: the theme can only restyle what the
  Zorin Menu draws, and it only draws an icon.
- **Picking a layout in Zorin Appearance** can reset the taskbar to full width. Run
  `./luna-neo.sh apply <Variant>` again to fix it.

## Credits

- **Icons**: [Win11 icon theme](https://www.opendesktop.org/p/1546069/) by
  **yeyushengfan258** ([GitHub](https://github.com/yeyushengfan258/Win11-icon-theme)),
  licensed under GPL-3.0. Bundled unmodified in [`icons/`](icons), except that broken
  symlinks and the prebuilt icon cache were removed (the installer rebuilds the cache). See `icons/Win11-black/AUTHORS` and `icons/Win11-black/COPYING`.
- **Base themes**: the ZorinBlue GTK and GNOME Shell themes by Zorin OS Technologies Ltd.
  (GPL), taken from your own system during install and not redistributed here.
- **Inspiration**: the Luna visual style of Windows XP.

## Disclaimer

Luna Neo is an unofficial fan project. It is not affiliated with or endorsed by Zorin OS
Technologies Ltd. or Microsoft. "Zorin" and the Zorin logo are trademarks of Zorin OS
Technologies Ltd., and "Windows" and "Windows XP" are trademarks of Microsoft Corporation.
They are used here only to describe what the theme works with and what it looks like.
Luna Neo contains no Microsoft artwork.

## License

[GPL-3.0](LICENSE)
