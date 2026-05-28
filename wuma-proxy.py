"""
wuma-proxy: 명조 맵스 LAN 프록시
- 컴퓨터2에서 실행
- maps.wuwa.moe 로컬 연동(ws://localhost:46821)을 컴퓨터1 트래커로 중계
"""

import asyncio
import os
import sys
import logging
import ipaddress
from pathlib import Path

try:
    import websockets
    from websockets.server import serve as ws_serve
    from websockets.client import connect as ws_connect
    from websockets.exceptions import ConnectionClosed
except ImportError:
    print("[ERROR] websockets package not found. Run: pip install websockets")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else Path(__file__).parent)
CONFIG_FILE  = BASE_DIR / "tracker_ip.txt"
LISTEN_PORT  = 46821
TRACKER_PORT = 46821
# ─────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("wuma-proxy")


def load_tracker_ip() -> str:
    if CONFIG_FILE.exists():
        ip = CONFIG_FILE.read_text().strip()
        if ip:
            log.info(f"Loaded tracker IP: {ip}")
            return ip

    print("")
    print("=" * 55)
    print("  First time setup")
    print("  Enter Computer 1 (tracker PC) IP address.")
    print("  Find it on Computer 1: run 'ipconfig' in cmd")
    print("  Look for 'IPv4 Address' (e.g. 192.168.0.10)")
    print("=" * 55)
    while True:
        ip = input("  Tracker PC IP address: ").strip()
        try:
            ipaddress.IPv4Address(ip)
            CONFIG_FILE.write_text(ip)
            log.info(f"Saved tracker IP: {ip}")
            return ip
        except ValueError:
            print(f"  [ERROR] '{ip}' is not a valid IPv4 address. Try again.")


async def proxy_connection(client_ws, client_addr, tracker_url: str):
    log.info(f"[CONNECT] {client_addr}")
    try:
        async with ws_connect(tracker_url) as tracker_ws:
            log.info(f"[RELAY] {client_addr} <-> {tracker_url}")

            async def client_to_tracker():
                async for message in client_ws:
                    await tracker_ws.send(message)

            async def tracker_to_client():
                async for message in tracker_ws:
                    await client_ws.send(message)

            done, pending = await asyncio.wait(
                [
                    asyncio.create_task(client_to_tracker()),
                    asyncio.create_task(tracker_to_client()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()

    except ConnectionClosed:
        pass
    except OSError as e:
        log.warning(f"[ERROR] Cannot connect to tracker: {e}")
        log.warning(f"  -> Is tracker running on Computer 1?")
        log.warning(f"  -> Is tracker IP set to 0.0.0.0 in advanced settings?")
    except Exception as e:
        log.error(f"[ERROR] {e}")
    finally:
        log.info(f"[DISCONNECT] {client_addr}")


async def run_proxy(tracker_url: str):
    async def handler(websocket):
        await proxy_connection(websocket, websocket.remote_address, tracker_url)

    log.info("=" * 55)
    log.info("  wuma-proxy started")
    log.info("=" * 55)
    log.info(f"  Tracker : {tracker_url}")
    log.info(f"  Listening : ws://localhost:{LISTEN_PORT}")
    log.info("")
    log.info("  maps.wuwa.moe -> Local Connect button to use")
    log.info("  Delete tracker_ip.txt to change tracker IP")
    log.info("=" * 55)
    log.info("  Press Ctrl+C to stop.")
    log.info("=" * 55)

    async with ws_serve(handler, "127.0.0.1", LISTEN_PORT):
        await asyncio.Future()


def main():
    print("=" * 55)
    print("  wuma-proxy - Wuthering Waves Maps LAN Proxy")
    print("=" * 55)

    tracker_ip = load_tracker_ip()
    tracker_url = f"ws://{tracker_ip}:{TRACKER_PORT}"

    try:
        asyncio.run(run_proxy(tracker_url))
    except KeyboardInterrupt:
        log.info("Proxy stopped.")
    except OSError as e:
        if e.errno in (98, 10048):
            log.error(f"[ERROR] Port {LISTEN_PORT} is already in use.")
            log.error("  -> Close the tracker app on this PC if it is running.")
        else:
            log.error(f"[ERROR] {e}")
        input("\nPress any key to exit...")


if __name__ == "__main__":
    main()
