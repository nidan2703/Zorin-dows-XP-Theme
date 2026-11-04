#!/usr/bin/env python3
"""Generate the Luna Neo theme family (an updated Windows XP look for Zorin OS).

Each variant gets a GNOME Shell theme (taskbar, Start button and XP-coloured Start
menu, layered on top of Zorin's own shell theme so the Zorin Menu keeps its layout) and GTK3/GTK4 themes
(XP-style title bars, window buttons and selection colours on top of Zorin's
GTK themes).

    python3 build.py            -> writes ./themes/Luna-Neo-<Variant>/ and
                                   ./themes/Luna-Neo-<Variant>-Dark/
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "themes"

# Zorin themes we layer on top of. The shell base is the one currently in use,
# which keeps the Zorin Menu's layout exactly as it is now.
# Dark variants use Zorin's matching dark theme instead.
ZORIN_BASE = "/usr/share/themes/ZorinBlue-{mode}"

# Colours that differ between the light and the dark variants.
MODES = {
    "Light": dict(
        menu_bg="#ffffff", menu_fg="#000000", side_fg="#0a246a",
        side_line="rgba(10, 36, 106, 0.18)", popover_fg="#123354",
        adw_colors=""),
    "Dark": dict(
        menu_bg="#111111", menu_fg="#f0f0f0", side_fg="#e4ebfa",
        side_line="rgba(255, 255, 255, 0.15)", popover_fg="#e8e8e8",
        adw_colors="""
@define-color window_bg_color #161616;
@define-color window_fg_color #eeeeee;
@define-color view_bg_color #0c0c0c;
@define-color view_fg_color #eeeeee;
@define-color sidebar_bg_color #1c1c1c;
@define-color card_bg_color rgba(255, 255, 255, 0.06);
@define-color dialog_bg_color #1c1c1c;
@define-color popover_bg_color #1c1c1c;
"""),
}

GREEN_START = dict(start_top="#5cc15c", start_bot="#2a8a2a", start_edge="#1d6a1d")

VARIANTS = {
    # The three colour schemes Windows XP shipped with ...
    "Blue": dict(
        side_bg="#d3e5fa",
        label="Blue (Luna)",
        bar_top="#3f86f5", bar_bot="#1747b8", bar_edge="#0c3593", bar_fg="#ffffff",
        title_top="#3d8df7", title_bot="#0a50d6", title_fg="#ffffff",
        idle_top="#9db7f2", idle_bot="#7f9ee3", idle_fg="#e8efff",
        btn_top="#6aa6ff", btn_bot="#2a68e0",
        accent="#316ac5", overlay="255,255,255", **GREEN_START),
    "OliveGreen": dict(
        side_bg="#e6ecd4",
        label="Olive Green",
        bar_top="#b6c88f", bar_bot="#7c9150", bar_edge="#5f7238", bar_fg="#ffffff",
        title_top="#b5c78e", title_bot="#7a9150", title_fg="#ffffff",
        idle_top="#dbe2c6", idle_bot="#c9d3ad", idle_fg="#f7f9f0",
        btn_top="#c9d8a6", btn_bot="#8da35f",
        accent="#7f9450", overlay="255,255,255",
        start_top="#7fb04c", start_bot="#4b7a22", start_edge="#3b6119"),
    "Silver": dict(
        side_bg="#ececf2",
        label="Silver",
        bar_top="#fbfbfd", bar_bot="#b8bbcb", bar_edge="#8e91a5", bar_fg="#1c1c28",
        title_top="#fdfdfe", title_bot="#c3c5d4", title_fg="#1c1c28",
        idle_top="#f4f4f6", idle_bot="#e4e5ea", idle_fg="#8a8a98",
        btn_top="#ffffff", btn_bot="#cfd1dd", btn_fg="#3c3d4f",
        accent="#6f7a9b", overlay="0,0,0", **GREEN_START),
    # ... plus the later official variants (Media Center, Zune, Embedded).
    "Royale": dict(
        side_bg="#d6e1f5",
        label="Royale (Media Center)",
        bar_top="#3a6fdc", bar_bot="#0e2a7c", bar_edge="#081d5a", bar_fg="#ffffff",
        title_top="#3b74e4", title_bot="#0f379f", title_fg="#ffffff",
        idle_top="#8ea3d6", idle_bot="#6f86c0", idle_fg="#e3e9f8",
        btn_top="#5d8ff0", btn_bot="#1d47b6",
        accent="#3360ad", overlay="255,255,255", **GREEN_START),
    "RoyaleNoir": dict(
        side_bg="#e6e6e6",
        label="Royale Noir",
        bar_top="#555555", bar_bot="#0c0c0c", bar_edge="#000000", bar_fg="#ffffff",
        title_top="#585858", title_bot="#111111", title_fg="#ffffff",
        idle_top="#9a9a9a", idle_bot="#777777", idle_fg="#eeeeee",
        btn_top="#6e6e6e", btn_bot="#2a2a2a",
        accent="#4a74c9", overlay="255,255,255", **GREEN_START),
    "Zune": dict(
        side_bg="#f3e7dc",
        label="Zune",
        bar_top="#454545", bar_bot="#0a0a0a", bar_edge="#000000", bar_fg="#ffffff",
        title_top="#474747", title_bot="#0e0e0e", title_fg="#ffffff",
        idle_top="#999999", idle_bot="#767676", idle_fg="#eeeeee",
        btn_top="#5e5e5e", btn_bot="#222222",
        accent="#e8741c", overlay="255,255,255",
        start_top="#ffa64d", start_bot="#d9620a", start_edge="#a84a05"),
    "Embedded": dict(
        side_bg="#dce5f5",
        label="Embedded",
        bar_top="#5c86da", bar_bot="#2a4c9e", bar_edge="#1c3878", bar_fg="#ffffff",
        title_top="#5b88df", title_bot="#2850ae", title_fg="#ffffff",
        idle_top="#a7b8de", idle_bot="#8ea2cf", idle_fg="#eef2fb",
        btn_top="#7ea2ea", btn_bot="#3a62c0",
        accent="#3a6cc0", overlay="255,255,255", **GREEN_START),
}

# Zorin logo (from zorin-menu's zorin-icon-symbolic.svg), each bar painted in
# one of the four Windows-flag colours.
START_LOGO = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 16 16">
  <defs>
    <linearGradient id="r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a4a"/><stop offset="1" stop-color="#e2361a"/></linearGradient>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a6e23a"/><stop offset="1" stop-color="#5aa500"/></linearGradient>
    <linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4cc3ff"/><stop offset="1" stop-color="#0a78d6"/></linearGradient>
    <linearGradient id="y" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffdb4d"/><stop offset="1" stop-color="#f5a000"/></linearGradient>
  </defs>
  <g stroke="#ffffff" stroke-opacity="0.75" stroke-width="0.45" stroke-linejoin="round" paint-order="stroke">
    <path fill="url(#r)" d="M3.385 3.994L4.536 2h6.928l1.151 1.994z"/>
    <path fill="url(#g)" d="M14.923 8l-1.161 2.012H6.394l7.368-4.025z"/>
    <path fill="url(#b)" d="M1.077 8l1.161-2.012h7.368l-7.368 4.025z"/>
    <path fill="url(#y)" d="M3.385 12.006L4.536 14h6.928l1.151-1.994z"/>
  </g>
</svg>
"""

SHELL_CSS = """/* Luna Neo {label} - GNOME Shell theme.
 * Everything not overridden here comes from Zorin's theme. */
@import url("file://{zorin_shell}");

/* ---- Taskbar ------------------------------------------------------------ */
/* Zorin Taskbar copies #panel's colour onto its outer actor as an inline
 * background-color, which becomes the start of this gradient. */
#panel {{
  background-color: {bar_top};
  color: {bar_fg};
}}

.zorintaskbarPanel {{
  background-gradient-direction: vertical;
  background-gradient-end: {bar_bot};
}}

.zorintaskbarPanel.dock {{
  border: 1px solid {bar_edge};
  box-shadow: none; /* the shell clips outer shadows to a square box */
}}

.zorintaskbarPanel #panel {{
  box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.35);
}}

#panel .panel-button,
#panel .panel-button.clock-display,
#panel .panel-button .clock {{
  color: {bar_fg};
}}

#panel .panel-button:hover,
#panel .panel-button:focus,
#panel .panel-button.clock-display:hover .clock {{
  box-shadow: inset 0 0 0 100px rgba({overlay}, 0.16);
}}

#panel .panel-button:active,
#panel .panel-button:checked,
#panel .panel-button.clock-display:checked .clock {{
  box-shadow: inset 0 0 0 100px rgba(0, 0, 0, 0.18);
}}

/* Running / focused apps */
#zorintaskbarScrollview .overview-tile:hover .dtp-container,
#zorintaskbarScrollview .overview-tile:selected .dtp-container {{
  background-color: rgba({overlay}, 0.16);
}}

#zorintaskbarScrollview .overview-tile:focus .dtp-container,
#zorintaskbarScrollview .overview-tile.focused .overview-icon {{
  background-color: rgba(0, 0, 0, 0.18);
  box-shadow: inset 0 1px 2px 0 rgba(0, 0, 0, 0.3);
}}

#zorintaskbarScrollview .overview-tile:active .dtp-container,
#zorintaskbarScrollview .overview-tile:checked .dtp-container {{
  background-color: rgba(0, 0, 0, 0.26);
}}

/* ---- Start button (the Zorin Menu button sits alone in the left box) ---- */
#panel #panelLeft .panel-button,
.zorintaskbarMainPanel #panelLeft .panel-button {{
  border: 1px solid {start_edge};
  border-radius: 11px 20px 20px 11px;
  margin: 4px 6px 4px 4px;
  -natural-hpadding: 16px;
  -minimum-hpadding: 12px;
  background-color: {start_top};
  background-gradient-direction: vertical;
  background-gradient-start: {start_top};
  background-gradient-end: {start_bot};
  box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.45);
}}

#panel #panelLeft .panel-button:hover,
#panel #panelLeft .panel-button:focus {{
  background-gradient-start: {start_top_hi};
  background-gradient-end: {start_top};
  box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.6);
}}

#panel #panelLeft .panel-button:active,
#panel #panelLeft .panel-button:checked {{
  background-gradient-start: {start_bot};
  background-gradient-end: {start_top};
  box-shadow: inset 0 2px 3px 0 rgba(0, 0, 0, 0.35);
}}

/* Hide the monochrome symbolic logo and paint the coloured one instead. */
#panel #panelLeft .panel-button .popup-menu-icon {{
  color: transparent;
  background-image: url("assets/start-logo.svg");
  background-size: contain;
  background-repeat: no-repeat;
}}

/* ---- Start menu: Zorin layout, XP colours ------------------------------ */
/* Blue frame = XP header/footer bands, white app column, tinted places column. */
.zorin-menu .popup-menu-content {{
  padding: 12px 5px;
  border-radius: 12px;
  border: 1px solid {bar_edge};
  background-color: {title_top};
  background-gradient-direction: vertical;
  background-gradient-start: {title_top};
  background-gradient-end: {title_bot};
  box-shadow: none;
}}

.zorin-menu .all-layout-box {{
  padding: 0;
}}

.zorin-menu .apps-box {{
  background-color: {menu_bg};
  border-radius: 8px 0 0 8px;
  padding: 6px;
  color: {menu_fg};
}}

.zorin-menu .shortcuts-box {{
  background-color: {side_bg};
  border-radius: 0 8px 8px 0;
  padding: 6px;
  color: {side_fg};
}}

.zorin-menu .vertical-separator {{
  margin: 0;
  width: 2px;
  background-color: #f0a040;
  border-right-width: 0;
}}

.zorin-menu .vertical-separator .popup-separator-menu-item-separator {{
  background-color: transparent;
}}

.zorin-menu .shortcuts-box .popup-separator-menu-item-separator {{
  background-color: {side_line};
}}

.zorin-menu .popup-menu-item:hover,
.zorin-menu .popup-menu-item:focus,
.zorin-menu .popup-menu-item.selected,
.zorin-menu .session-buttons-section .system-menu-action:hover,
.zorin-menu .session-buttons-section .system-menu-action:focus {{
  background-color: {accent};
  color: #ffffff;
}}

.zorin-menu .popup-menu-item:active,
.zorin-menu .popup-menu-item:checked {{
  background-color: {accent_dark};
  color: #ffffff;
}}

.zorin-menu .search-entry:focus {{
  border-color: {accent};
}}

/* ---- XP-style tooltips --------------------------------------------------- */
.dash-label {{
  background-color: #ffffe1;
  color: #000000;
  border: 1px solid #6e6e6e;
  border-radius: 4px;
  padding: 4px 8px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.25);
}}
"""

# Shared GTK3/GTK4 rules for title bars and window buttons.
TITLEBAR_CSS = """
/* ---- XP title bars -------------------------------------------------- */
headerbar,
.titlebar:not(headerbar),
window.csd > .titlebar:not(headerbar) {{
  background-color: {title_bot};
  background-image: linear-gradient(to bottom, {title_hi}, {title_top} 3px, {title_bot} 85%, shade({title_bot}, 0.92));
  box-shadow: inset 0 1px rgba(255, 255, 255, 0.35);
  border-color: {bar_edge};
  color: {title_fg};
}}

headerbar:backdrop,
.titlebar:not(headerbar):backdrop {{
  background-color: {idle_bot};
  background-image: linear-gradient(to bottom, {idle_top}, {idle_bot});
  color: {idle_fg};
}}

headerbar .title,
.titlebar .title {{
  font-weight: bold;
  color: {title_fg};
  text-shadow: {title_shadow};
}}

headerbar:backdrop .title,
.titlebar:backdrop .title,
headerbar .subtitle {{
  color: {idle_fg};
  text-shadow: none;
}}

/* Window controls: XP squares with a white rim, bevel and bold glyphs */
headerbar button.titlebutton,
.titlebar button.titlebutton,
windowcontrols > button {{
  min-width: 21px;
  min-height: 21px;
  padding: 0;
  margin: 0 1px;
  border-radius: 3px;
  border: 1px solid #ffffff;
  background-color: {btn_bot};
  background-image: linear-gradient(135deg, {btn_top}, {btn_bot} 70%, shade({btn_bot}, 0.85));
  color: {btn_fg};
  box-shadow: inset 1px 1px rgba(255, 255, 255, 0.45), inset -1px -1px rgba(0, 0, 0, 0.25);
  -gtk-icon-shadow: 1px 0 {btn_fg};
}}

windowcontrols > button > image {{
  background: none;
  box-shadow: none;
  color: inherit;
}}

headerbar button.titlebutton:hover,
.titlebar button.titlebutton:hover,
windowcontrols > button:hover {{
  background-image: linear-gradient(135deg, shade({btn_top}, 1.12), shade({btn_bot}, 1.12) 70%, {btn_bot});
}}

headerbar button.titlebutton:active,
.titlebar button.titlebutton:active,
windowcontrols > button:active {{
  background-image: linear-gradient(135deg, shade({btn_bot}, 0.85), {btn_bot});
  box-shadow: inset 1px 1px rgba(0, 0, 0, 0.3);
}}

headerbar button.titlebutton.close,
.titlebar button.titlebutton.close,
windowcontrols > button.close {{
  background-color: #c8401c;
  background-image: linear-gradient(135deg, #f0906c, #d4461f 70%, #b5340f);
  color: #ffffff;
  -gtk-icon-shadow: 1px 0 #ffffff;
}}

headerbar button.titlebutton.close:hover,
.titlebar button.titlebutton.close:hover,
windowcontrols > button.close:hover {{
  background-image: linear-gradient(135deg, #ffab88, #e5552a 70%, #c43d15);
}}

headerbar button.titlebutton.close:active,
.titlebar button.titlebutton.close:active,
windowcontrols > button.close:active {{
  background-image: linear-gradient(135deg, #a52c0c, #d4461f);
  box-shadow: inset 1px 1px rgba(0, 0, 0, 0.3);
}}

headerbar button.titlebutton:backdrop,
.titlebar button.titlebutton:backdrop,
windowcontrols > button:backdrop {{
  opacity: 0.75;
}}

/* Ordinary buttons sitting on the title bar */
headerbar > button:not(.titlebutton):not(.suggested-action):not(.destructive-action),
headerbar > box > button:not(.suggested-action):not(.destructive-action),
headerbar > box > box > button:not(.suggested-action):not(.destructive-action),
headerbar > stackswitcher > button,
headerbar > box > stackswitcher > button {{
  color: {title_fg};
  background-color: rgba({overlay}, 0.12);
  background-image: none;
  border-color: rgba({overlay}, 0.25);
  box-shadow: none;
  text-shadow: none;
  -gtk-icon-shadow: none;
}}

headerbar > button:not(.titlebutton):hover,
headerbar > box > button:hover,
headerbar > box > box > button:hover,
headerbar > stackswitcher > button:hover,
headerbar > box > stackswitcher > button:hover {{
  background-color: rgba({overlay}, 0.22);
}}

headerbar > button:not(.titlebutton):checked,
headerbar > box > button:checked,
headerbar > box > box > button:checked,
headerbar > stackswitcher > button:checked,
headerbar > box > stackswitcher > button:checked {{
  background-color: rgba(0, 0, 0, 0.2);
}}

headerbar popover {{
  color: {popover_fg};
  text-shadow: none;
}}

/* ---- Accent colour ---------------------------------------------------- */
selection,
*:selected,
row:selected,
.view:selected,
treeview.view:selected,
iconview:selected,
flowbox flowboxchild:selected,
calendar:selected {{
  background-color: {accent};
  color: #ffffff;
}}

button.suggested-action {{
  background-color: {accent};
  background-image: linear-gradient(to bottom, shade({accent}, 1.15), {accent});
  border-color: shade({accent}, 0.8);
  color: #ffffff;
}}

switch:checked {{
  background-color: {accent};
  background-image: none;
  border-color: shade({accent}, 0.85);
}}

progressbar progress,
scale highlight,
levelbar block.filled {{
  background-color: {accent};
  background-image: none;
  border-color: shade({accent}, 0.85);
}}

entry:focus,
entry:focus-within {{
  border-color: {accent};
  box-shadow: inset 0 0 0 1px {accent};
}}
"""

GTK3_CSS = """/* Luna Neo {label} - GTK 3 */
@import url("zorin-base.css");
""" + TITLEBAR_CSS

GTK4_CSS = """/* Luna Neo {label} - GTK 4 (plain GTK 4 apps and window frames of X11 apps) */
@import url("zorin-base.css");
@import url("libadwaita.css");
"""

# Loaded via ~/.config/gtk-4.0/gtk.css so libadwaita apps follow the theme too.
LIBADWAITA_CSS = """/* Luna Neo {label} - libadwaita colours */
@define-color accent_color shade({accent}, 0.9);
@define-color accent_bg_color {accent};
@define-color accent_fg_color #ffffff;
@define-color headerbar_bg_color {title_bot};
@define-color headerbar_fg_color {title_fg};
@define-color headerbar_backdrop_color {idle_bot};
@define-color headerbar_border_color {bar_edge};
@define-color sidebar_bg_color @window_bg_color;
{adw_colors}
toolbarview > .top-bar,
.top-bar {{
  background-image: linear-gradient(to bottom, {title_top}, {title_bot});
  color: {title_fg};
}}

toolbarview > .top-bar:backdrop,
.top-bar:backdrop {{
  background-image: linear-gradient(to bottom, {idle_top}, {idle_bot});
  color: {idle_fg};
}}

toolbarview > .top-bar headerbar,
.top-bar headerbar {{
  background: none;
  box-shadow: none;
}}
""" + TITLEBAR_CSS

INDEX_THEME = """[Desktop Entry]
Type=X-GNOME-Metatheme
Name=Luna Neo {label}{suffix}
Comment=An updated Windows XP look for Zorin OS
Encoding=UTF-8

[X-GNOME-Metatheme]
GtkTheme=Luna-Neo-{key}{suffix}
MetacityTheme=Luna-Neo-{key}{suffix}
IconTheme={icon_theme}
"""


def lighten(hex_color, amount):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda c: round(c + (255 - c) * amount)
    return "#{:02x}{:02x}{:02x}".format(mix(r), mix(g), mix(b))


def darken(hex_color, amount):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#{:02x}{:02x}{:02x}".format(*(round(c * (1 - amount)) for c in (r, g, b)))


def build(key, v, mode):
    base = ZORIN_BASE.format(mode=mode)
    suffix = "-Dark" if mode == "Dark" else ""
    if mode == "Dark":
        # Places column: the variant's title-bar colour, darkened almost to black.
        v = dict(v, side_bg=darken(v["title_bot"], 0.75))
    v = dict({"btn_fg": "#ffffff"}, **v)
    v = dict(v, **MODES[mode], key=key, suffix=suffix,
             icon_theme="Win11-black-dark" if mode == "Dark" else "Win11-black",
             zorin_shell=f"{base}/gnome-shell/gnome-shell.css",
             start_top_hi=lighten(v["start_top"], 0.2),
             accent_dark=darken(v["accent"], 0.15),
             title_hi=lighten(v["title_top"], 0.35),
             title_shadow="none" if v["title_fg"] != "#ffffff"
             else "0 1px 1px rgba(0, 0, 0, 0.45)")
    root = OUT / f"Luna-Neo-{key}{suffix}"
    files = {
        "index.theme": INDEX_THEME,
        "gnome-shell/gnome-shell.css": SHELL_CSS,
        "gnome-shell/assets/start-logo.svg": START_LOGO,
        "gtk-3.0/gtk.css": GTK3_CSS,
        "gtk-3.0/gtk-dark.css": GTK3_CSS,
        "gtk-4.0/gtk.css": GTK4_CSS,
        "gtk-4.0/gtk-dark.css": GTK4_CSS,
        "gtk-4.0/libadwaita.css": LIBADWAITA_CSS,
    }
    for rel, template in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(template if template is START_LOGO else template.format(**v))
    # Flatpak apps can read ~/.themes but have their own /usr/share, so the GTK base
    # has to live inside the theme. An import from /usr/share/themes would fail there
    # and leave menus without a background.
    for gtk in ("gtk-3.0", "gtk-4.0"):
        shutil.copy(f"{base}/{gtk}/gtk.css", root / gtk / "zorin-base.css")
        shutil.copytree(f"{base}/{gtk}/assets", root / gtk / "assets", dirs_exist_ok=True)
    # Zorin Appearance only lists application themes that have a gtk-2.0 folder.
    shutil.copytree(f"{base}/gtk-2.0", root / "gtk-2.0", dirs_exist_ok=True)
    return root


if __name__ == "__main__":
    for key, variant in VARIANTS.items():
        for mode in MODES:
            print("built", build(key, variant, mode).relative_to(HERE))
