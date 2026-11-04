#!/usr/bin/env bash
# Install and switch the Luna Neo themes on Zorin OS.
#
#   ./luna-neo.sh install           copy all variants into ~/.themes and the bundled
#                                   Win11 icons into ~/.local/share/icons
#   ./luna-neo.sh apply <Variant>   switch shell, GTK and icon theme, make the taskbar content-width
#                                   (append -Dark for the dark version, e.g. Blue-Dark)
#   ./luna-neo.sh revert            restore the settings saved by the first "apply"
#   ./luna-neo.sh list              show available variants
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
THEMES_DIR="$HOME/.themes"
ICONS_DIR="$HOME/.local/share/icons"
STATE_DIR="$HOME/.config/luna-neo"
BACKUP="$STATE_DIR/backup.env"
GTK4_CSS="$HOME/.config/gtk-4.0/gtk.css"
TASKBAR=org.gnome.shell.extensions.zorin-taskbar
AUTO_THEME=com.zorin.desktop.auto-theme
AUTO_THEME_DESKTOP=com.zorin.desktop.auto-theme.desktop

variants() {
    [ -d "$HERE/themes" ] || python3 "$HERE/build.py" >/dev/null
    (cd "$HERE/themes" && ls -d Luna-Neo-* | sed 's/^Luna-Neo-//')
}

icon_theme_installed() {
    local dir
    for dir in "$ICONS_DIR" "$HOME/.icons" /usr/share/icons /usr/local/share/icons; do
        [ -f "$dir/$1/index.theme" ] && return 0
    done
    return 1
}

install_themes() {
    python3 "$HERE/build.py" >/dev/null
    mkdir -p "$THEMES_DIR"
    for dir in "$HERE"/themes/Luna-Neo-*; do
        rm -rf "${THEMES_DIR:?}/$(basename "$dir")"
        cp -r "$dir" "$THEMES_DIR/"
    done
    echo "Installed $(variants | wc -l) variants into $THEMES_DIR"

    # Win11 icon theme by yeyushengfan258 (GPL-3.0). Both folders go side by side,
    # because Win11-black-dark links into Win11-black.
    mkdir -p "$ICONS_DIR"
    for dir in "$HERE"/icons/*/; do
        local icons
        icons="$(basename "$dir")"
        if icon_theme_installed "$icons"; then
            echo "Icon theme $icons already installed, skipping"
            continue
        fi
        cp -a "$dir" "$ICONS_DIR/$icons"
        gtk-update-icon-cache -q -f "$ICONS_DIR/$icons" 2>/dev/null || true
        echo "Installed icon theme $icons into $ICONS_DIR"
    done
}

# Zorin's day/night switcher would replace Luna Neo with a Zorin theme on its schedule.
# Same steps as choosing Light or Dark in Zorin Appearance; the running process watches the key.
stop_auto_theme() {
    gsettings writable $AUTO_THEME enabled >/dev/null 2>&1 || return 0
    gsettings set $AUTO_THEME enabled false
    rm -f "$HOME/.config/autostart/$AUTO_THEME_DESKTOP"
}

# Set every monitor's taskbar to "dynamic" length (-1): it only takes the width it needs.
# Zorin Taskbar also accepts monitor numbers as keys, which covers fresh accounts that
# have no saved monitor IDs yet.
dock_mode() {
    local anchors lengths
    anchors="$(gsettings get $TASKBAR panel-anchors)"
    lengths="$(python3 - "$anchors" "$(gsettings get $TASKBAR panel-element-positions)" <<'EOF'
import json, sys
monitors = {str(i) for i in range(4)}
for raw in sys.argv[1:]:
    raw = raw.strip().strip("'")
    if raw.startswith("@"):
        raw = raw.split(" ", 1)[1].strip("'")
    try:
        monitors |= set(json.loads(raw or "{}"))
    except ValueError:
        pass
print(json.dumps({m: -1 for m in sorted(monitors)}))
print(json.dumps({m: "MIDDLE" for m in sorted(monitors)}))
EOF
)"
    gsettings set $TASKBAR panel-lengths "$(sed -n 1p <<<"$lengths")"
    gsettings set $TASKBAR panel-anchors "$(sed -n 2p <<<"$lengths")"
}

apply_variant() {
    local name="Luna-Neo-$1"
    [ -d "$THEMES_DIR/$name" ] || install_themes
    [ -d "$THEMES_DIR/$name" ] || { echo "Unknown variant: $1"; variants; exit 1; }

    mkdir -p "$STATE_DIR"
    if [ ! -f "$BACKUP" ]; then
        {
            printf 'GTK_THEME=%q\n' "$(gsettings get org.gnome.desktop.interface gtk-theme)"
            printf 'SHELL_THEME=%q\n' "$(gsettings get org.gnome.shell.extensions.user-theme name)"
            printf 'COLOR_SCHEME=%q\n' "$(gsettings get org.gnome.desktop.interface color-scheme)"
            printf 'PANEL_LENGTHS=%q\n' "$(gsettings get $TASKBAR panel-lengths)"
            printf 'PANEL_ANCHORS=%q\n' "$(gsettings get $TASKBAR panel-anchors)"
            printf 'ICON_THEME=%q\n' "$(gsettings get org.gnome.desktop.interface icon-theme)"
            printf 'AUTO_THEME_ENABLED=%q\n' "$(gsettings get $AUTO_THEME enabled 2>/dev/null || echo false)"
        } >"$BACKUP"
        [ -f "$GTK4_CSS" ] && ! grep -q "Luna Neo" "$GTK4_CSS" && cp "$GTK4_CSS" "$STATE_DIR/gtk4-gtk.css.orig"
        echo "Saved current settings to $BACKUP"
    fi

    stop_auto_theme

    # libadwaita apps follow the colour scheme, not the GTK theme.
    local icons
    case "$name" in
        *-Dark) gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'; icons=Win11-black-dark ;;
        *) gsettings set org.gnome.desktop.interface color-scheme 'default'; icons=Win11-black ;;
    esac
    icon_theme_installed "$icons" || install_themes
    gsettings set org.gnome.desktop.interface icon-theme "$icons"
    gsettings set org.gnome.desktop.interface gtk-theme "$name"
    gsettings set org.gnome.shell.extensions.user-theme name "$name"

    mkdir -p "$(dirname "$GTK4_CSS")"
    printf '/* Luna Neo - managed by luna-neo.sh */\n@import url("file://%s/%s/gtk-4.0/libadwaita.css");\n' \
        "$THEMES_DIR" "$name" >"$GTK4_CSS"

    dock_mode
    echo "Applied $name. Restart open apps to see the new title bars."
}

revert() {
    [ -f "$BACKUP" ] || { echo "Nothing to revert."; exit 0; }
    # shellcheck disable=SC1090
    source "$BACKUP"
    gsettings set org.gnome.desktop.interface gtk-theme "$GTK_THEME"
    gsettings set org.gnome.shell.extensions.user-theme name "$SHELL_THEME"
    gsettings set org.gnome.desktop.interface color-scheme "$COLOR_SCHEME"
    gsettings set $TASKBAR panel-lengths "$PANEL_LENGTHS"
    gsettings set $TASKBAR panel-anchors "$PANEL_ANCHORS"
    [ -n "${ICON_THEME:-}" ] && gsettings set org.gnome.desktop.interface icon-theme "$ICON_THEME"
    if [ -f "$STATE_DIR/gtk4-gtk.css.orig" ]; then
        cp "$STATE_DIR/gtk4-gtk.css.orig" "$GTK4_CSS"
    elif [ -f "$GTK4_CSS" ] && grep -q "Luna Neo" "$GTK4_CSS"; then
        rm "$GTK4_CSS"
    fi
    if [ "${AUTO_THEME_ENABLED:-false}" = true ]; then
        gsettings set $AUTO_THEME enabled true
        mkdir -p "$HOME/.config/autostart"
        cp "/usr/share/applications/$AUTO_THEME_DESKTOP" "$HOME/.config/autostart/" || true
        setsid -f zorin-auto-theme >/dev/null 2>&1 || true
    fi
    rm -f "$BACKUP" "$STATE_DIR/gtk4-gtk.css.orig"
    echo "Restored previous settings."
}

case "${1:-}" in
    install) install_themes ;;
    apply) [ -n "${2:-}" ] || { echo "Usage: $0 apply <Variant>"; variants; exit 1; }; apply_variant "$2" ;;
    revert) revert ;;
    list) variants ;;
    *) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
