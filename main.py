import time
import yaml
from datetime import datetime
from helpers import push_to_pixoo, push_solid_color
from spotify import fetch_album_art, get_current_track


# currently displays spotify album art during the day, and a warm solid color at night (00:00–06:59).

with open("config.yaml") as f:
    _cfg = yaml.safe_load(f)

MAC           = _cfg["pixoo"]["mac"]
POLL_INTERVAL = 5  # seconds

NIGHT_START = 0   # midnight
NIGHT_END   = 7   # 07:00 — night mode window: 00:00–06:59


def is_night() -> bool:
    h = datetime.now().hour
    print(f"[time] current hour: {h:02d} — {'night' if NIGHT_START <= h < NIGHT_END else 'day'} mode")
    return NIGHT_START <= h < NIGHT_END


def run_night_mode():
    print("[night] setting warm light")
    push_solid_color(MAC, 255, 60, 10)  # deep red-orange


def main():
    last_track_id = None
    last_mode     = None  # "day" | "night"

    print("Starting Pixoo daemon... (Ctrl+C to stop)")
    while True:
        try:
            mode = "night" if is_night() else "day"

            if mode == "night":
                if last_mode != "night":
                    run_night_mode()
                    last_track_id = None
                last_mode = "night"

            else:
                if last_mode == "night":
                    print("[day] resuming Spotify mode")
                last_mode = "day"

                track_id, name, artist, art_url = get_current_track()
                if track_id and track_id != last_track_id:
                    print(f"Now playing: {name} — {artist}")
                    img = fetch_album_art(art_url)
                    push_to_pixoo(MAC, img)
                    last_track_id = track_id
                elif not track_id:
                    print("Nothing playing.")

        except Exception as e:
            print(f"[error] {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
