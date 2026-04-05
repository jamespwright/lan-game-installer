# Download and install logic (no UI dependencies).
#
# Iterates over a list of games, optionally downloading their installers
# from OneDrive, then running each installer silently.

import os
import subprocess
from typing import Callable

from . import BASE_DIR
from .downloader import download_game

StatusCallback = Callable[[str, str], None]


def run_installs(
    games: list[dict],
    install_dir: str,
    player: str,
    input_values: dict[str, str] | None = None,
    download_url: str | None = None,
    status_callback: StatusCallback | None = None,
    download_only: bool = False,
) -> list[str]:
    """Download (when *download_url* is set) and install each game.

    When *download_only* is True, only the download phase runs and installation
    is skipped.  Returns a list of error messages (empty = all OK).
    """
    errors: list[str] = []

    for game in games:
        name = game["name"]

        def _notify(msg: str, _name: str = name) -> None:
            if status_callback:
                status_callback(_name, msg)

        try:
            # ── Download phase ─────────────────────────────────────────
            if download_url and game.get("base_path"):
                dl_errors = download_game(download_url, game, _notify)
                if dl_errors:
                    errors.extend(f"{name}: {e}" for e in dl_errors)
                    continue

            if download_only:
                continue

            # ── Install phase ──────────────────────────────────────────
            _notify("Installing\u2026")

            base_path = BASE_DIR / game["base_path"] if game.get("base_path") else BASE_DIR
            target_dir = os.path.normpath(os.path.join(install_dir, game["name"]))

            # Prerequisites
            for prereq in game.get("prerequisites", []):
                prereq_path = BASE_DIR / prereq["path"]
                args = prereq.get("args", "")
                subprocess.run(f'"{prereq_path}" {args}'.strip(), shell=True, check=False)

            installer_type = game.get("installer_type", "msi")
            params_template = game.get("parameters", "")

            if installer_type == "exe_setup":
                exe_rel = game.get("install_exe", "")
                if not exe_rel:
                    continue
                exe_path = base_path / exe_rel
                params = params_template.format(target_dir=target_dir, player=player, **(input_values or {}))
                cmd = f'"{exe_path}" {params}'.strip()
                subprocess.run(cmd, shell=True, check=True)

            if installer_type == "msi":
                msi_rel = game.get("install_msi", "")
                if not msi_rel:
                    continue
                msi_path = base_path / msi_rel
                params = params_template.format(target_dir=target_dir, player=player, **(input_values or {}))
                cmd_parts = ["msiexec", "/i", f'"{msi_path}"']
                if params:
                    cmd_parts.append(params)
                cmd_parts.append("/qb")
                subprocess.run(" ".join(cmd_parts), shell=True, check=True)

            _notify("Complete")

        except subprocess.CalledProcessError as exc:
            errors.append(f'{name}: installer exited with code {exc.returncode}')
            _notify(f"Error (exit {exc.returncode})")
        except Exception as exc:  # noqa: BLE001
            errors.append(f'{name}: {exc}')
            _notify(f"Error: {exc}")

    return errors
