# AGENTS.md — brutalTANKS

## Quick start
```powershell
venv\Scripts\python.exe main.py
```

## Architecture
- Flat project, no packages. Two files: `main.py` (entrypoint, game loop, UI) and `game_objects.py` (tank/object classes, sprite loading).
- **Circular import** (each does `from X import *`). `game_objects.py` also calls `pygame.init()` and `pygame.display.set_mode()` at module level — it cannot be imported standalone.
- Entrypoint: `main()` at line 2207; calls `init_user_info()` then `main()`.

## Key constants (`main.py`)
| Constant     | Value  |
|--------------|--------|
| TILE_SIZE    | 40     |
| FPS          | 15     |
| WINDOW_SIZE  | 600x600 |
| MAPS_DIR     | `data/maps` |
| SPRITES_DIR  | `sprites` (relative to `data/`) |

## Controls (defined in `main.py:46-61`)
- Green: WASD move/turn, Q/E turret, R shoot
- Layered constants: `FORWARD=91, BACK=92, TURN_RIGHT=93, ...` map to `pygame.K_*` values.

## Maps
- Tiled `.tmx` format, loaded via PyTMX. Edit with Tiled Map Editor.
- Tilesets: `tiles_map.tsx`, `tiles_map_lvl2.tsx` in `data/maps/`.
- Campaign: 10 levels (`1_lvl.tmx` … `10_lvl.tmx`), plus `local_game.tmx` for local multiplayer.

## Save data
- Pickled user data in `data/saved user info/` (auto-created, gitignored).

## Build
```powershell
pip install -r requirements.txt
pyinstaller main.spec
```
Produces `main.exe`. Spec at `main.spec`.

## Conventions
- All UI strings and commit messages are in **Russian**. Keep that style when adding user-facing text.
- No tests, no CI, no linting, no formatter.
- Dependencies pinned in `requirements.txt`: `pygame==2.0.0`, `PyTMX==3.24`, `pygame_gui==0.5.7`.

## Project roots
- `.idea/` — PyCharm project (configured for Python 3.8 but runs on 3.13).
- `venv/` — Python 3.13.9.
