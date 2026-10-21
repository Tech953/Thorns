# Thorns 0.5.0 — shared content refinement

Stable regional surface descriptions, player-specific dialogue variation and local witness memory now share one generation module with Rose. Open **Local Contact** in an Open world room to use six new dialogue topics. Read [the systems update](CONTENT-GENERATION-REFINEMENT.md) for controls, source boundaries, save behavior and verification.

Presentation updated to v0.4.1. See PRESENTATION-AUDIT.md for DOCX evidence, applied changes, and remaining visual acceptance checks.

# THORNS v0.4 — open-world expansion

Start with `Start-Windows.bat` (Python required) or `python launcher.py`. Select Open world grid at room creation; Hardcore survival is optional. See `OPEN-WORLD-GUIDE.md` for the new systems and prototype limits, `WINDOWS-BUILD.md` for EXE preparation, and `VALIDATION.md` for test status. Original chapter mode remains available.

---

# THORNS — The Voluntary Signal (0.2)

**New:** character creation, 25 proficiency records, 25 reputation tracks, regional procedural encounters and consensual distance-based PvP. Start with `SYSTEMS-GUIDE.md` for the new rules and `SOURCE-CROSSWALK.md` for source grounding.

A playable, self-hosted cooperative choose-your-own-adventure RPG adapted from your five world previews and two map drawings. This is a first chapter prototype, not a finished commercial game. It supports one to six people per room using their browsers. No paid API, model download, JavaScript package installation, or external assets are required. The host needs Python 3.10 or newer.

## Start on Windows

1. Extract the ZIP completely.
2. Install Python 3.10+ if needed, with its launcher / PATH option enabled.
3. Double-click `Start-Windows.bat`. Keep its terminal open.
4. Open `http://localhost:8765` in your browser.
5. Name your character, choose a discipline and create an expedition.
6. Invite everyone before clicking **Begin expedition**. Rooms lock after starting.

On macOS/Linux, run `python3 server.py` from this folder (or `./start.sh`). A local solo game works without an internet connection after Python is installed. This is source software with a launcher, not a compiled EXE or APK.

## LAN play

Run ONE server on a computer all players can reach. On Windows, run `ipconfig` to find that computer's active IPv4 address. Other players open `http://HOST-LAN-IP:8765` (for example, `http://192.168.1.20:8765`) and enter the same room code. If Windows prompts, allow Python on the private network. Players need the server address AND the room code. A code alone does not discover servers. Wi-Fi client isolation can prevent LAN connections.

## Internet play

The same server supports remote HTTP connections, but this package does not include a hosted server or a tunneling account. Two deployment options:

- Private group: use a private mesh VPN you control, run the server on the host, and give friends `http://HOST-VPN-IP:8765`. Restrict access to your group.
- Hosted server: run the included Dockerfile on a host with persistent storage and an HTTPS reverse proxy. Route the public HTTPS address to the app's internal port 8765. Mount a persistent volume at `/data`; the included container writes its SQLite saves there. The `PORT` environment variable can override 8765. Give friends the HTTPS address and room code. This uses short polling, so it does not require WebSocket forwarding.

Example build/run:

```sh
docker build -t thorns .
docker run --name thorns -p 127.0.0.1:8765:8765 -v thorns-data:/data thorns
```

This example exposes the app only to a reverse proxy on the Docker host. Configure that proxy's domain and TLS before remote play. Internet hosting is NOT deployed or live-tested by this deliverable. Do not expose raw HTTP over the public internet: session credentials need transport encryption. This stdlib server is a friends-group prototype, not a hardened public matchmaking service; use proxy access control and request limits for a hosted instance.

## Play

The host chooses the specialist for the next choice before any votes arrive. Every character votes for one option, and may change that vote until the choice resolves. Once everyone has voted, the most popular option resolves automatically. Server randomness breaks ties. The host can explicitly resolve current votes early if someone is away; absent players do not block the expedition indefinitely.

Checks: D20 + chosen attribute + experience bonus + applicable practice + findings >= difficulty. Practice combines training and an eligible registered mod, capped at +2. Natural 1 always fails, natural 20 always succeeds. Each attempt gives its specialist 1 XP; every 3 XP adds +1 (maximum +2). Relevant discoveries add up to +3 at final contact. Six disciplines specialize in body, tech, percept, or rapport. Every failed check costs 2 shared cohesion, starting at 10. At 0, the expedition withdraws. CHECKPOINT.RESID restores cohesion if reached before the expedition fails. Cohesion represents the capacity to continue, not a claim that the source's death protections apply everywhere.

Choose between CITY_CLOUD_S and ENACT_HILLS, visit AETHERGALE, and optionally engage a remote NULL_FIELD.OMNI query. The endings include refusal, withdrawal, witnessing, voluntary contact, and a dangerous marked-query conclusion. You cannot roll your way through RED>GATE> or defeat immutable authorities with a high die. Consensual non-lethal duels are available; a full tactical combat subsystem is not implemented.

## Saves and sessions

Every state mutation saves to `thorns-saves.sqlite3` beside `server.py` (container: `/data/thorns-saves.sqlite3`). Stop the server before copying that file for a backup. Restart with the same database and port to continue. Never distribute your live save database; it contains room session credentials.

The browser tab keeps its active session in sessionStorage. A recovery copy for the last created/joined expedition is kept in localStorage. On the same browser and server address, use **Resume last expedition in this browser** to recover after closing a tab or exiting. Browser storage must remain intact. This is a bearer session: do not share browser storage, and use a trusted device. Cross-device recovery and account passwords are not implemented. A new join/create replaces the previous recovery copy; keep older game tabs open if running multiple rooms.

**Leave expedition** removes the player and transfers host authority if needed; **Exit terminal** keeps the seat and the recovery copy. If all host credentials are lost or browser data is cleared, start a new room. The host can resolve early for absent players.

Separate browser profiles or independently opened tabs can represent different players for local testing. Do not duplicate an existing game tab: some browsers copy sessionStorage, yielding the same player session.

## Canon and adaptation

`reference/` contains extracted text of the five supplied documents, preserved as reference material. The two original map photos are in `static/` and viewable inside the game. Your world, names, factions, and original drawings remain your supplied creative material; no additional license to that material is asserted.

All mission dialogue, the transit spool, travel edges, playable discipline statistics, XP, cohesion, checks, and endings are new prototype adaptations for review. The chapter's title is also new. NPCs and known institutions are drawn from the previews. In particular:

- Lila and Khi's situation comes from AETHERGALE; the proposed communication outcome is newly written and does not cure the prism.
- PYRI's emphasis on autonomy informs a new lesson; it does not establish new official canon.
- RED>GATE> is not opened or traversed by players. The NULL_FIELD scenes use observations and the described query channel.
- The source stops mid-sentence about YU.ZU_CaPSULaTE's interior. That interior remains undefined.
- Sanctuary protections are local; the game does not assume general resurrection.
- Routes are game abstractions, not exact scale reconstructions of the drawings.

## Extend and verify

Edit `content.py` to add scenes, checks, gated choices, and codex entries. `server.py` owns all outcomes, voting, credentials and saves; `static/app.js` renders the server state. Clients cannot submit rolls, XP or destinations. The global lock serializes mutations, and room revisions reject stale gameplay actions. The single SQLite process is intended for a small friends group, not multi-worker scaling.

Run `python -m unittest -v test_game.py test_systems.py test_http.py`. Tests exercise room capacity, authorization, concurrent voting, stale writes, both critical dice outcomes, branch traversal, host transfer and persistence. Visual interface and local HTTP checks are reported in `VALIDATION.md`.

Potential next production work: recoverable player accounts, reconnect invitations, stronger network abuse controls, campaign import/export, ongoing character inventories and expanded tactical encounters, and a signed installer. This chapter intentionally needs no AI to run.
