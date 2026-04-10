"""Real-time pipeline progress streaming.

Provides a unified ``ProgressStream`` that emits structured events as the
pipeline moves through its 23 stages.  Three transports are supported:

  ``LogTransport``      — writes to the Python logging system (always available)
  ``FileTransport``     — appends JSON-lines to ``progress.jsonl`` in the run dir
  ``WebSocketTransport``— pushes events through the existing ``ConnectionManager``

All transports implement the ``ProgressTransport`` protocol so they can be
composed in a ``MultiTransport``.

Usage (inside pipeline/executor.py or stage_impls)::

    from researchclaw.dashboard.progress_stream import ProgressStream, make_stream

    stream = make_stream(run_dir=run_dir, ws_manager=manager)

    with stream.stage("LITERATURE_COLLECT", stage_num=4, total_stages=23):
        papers = collect_papers(...)
        stream.update(f"Found {len(papers)} papers", count=len(papers))

    # or fire-and-forget:
    stream.info("Cache hit — skipping download")
    stream.metric("papers_found", 42)

The context manager automatically emits STAGE_START / STAGE_DONE / STAGE_FAILED
events so callers don't have to remember to close stages manually.
"""

from __future__ import annotations

import json
import logging
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Generator, Protocol, Sequence

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Event model
# ---------------------------------------------------------------------------


class ProgressEventType(str, Enum):
    PIPELINE_START = "pipeline_start"
    PIPELINE_DONE = "pipeline_done"
    PIPELINE_FAILED = "pipeline_failed"
    STAGE_START = "stage_start"
    STAGE_UPDATE = "stage_update"
    STAGE_DONE = "stage_done"
    STAGE_FAILED = "stage_failed"
    METRIC = "metric"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ProgressEvent:
    """A single progress event emitted by the pipeline."""

    event_type: ProgressEventType
    run_id: str
    stage_name: str = ""
    stage_num: int = 0
    total_stages: int = 23
    message: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    elapsed_sec: float = 0.0
    timestamp: str = ""

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    @property
    def progress_pct(self) -> float:
        """0–100 completion percentage based on stage number."""
        if self.total_stages == 0:
            return 0.0
        return round((self.stage_num / self.total_stages) * 100, 1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "run_id": self.run_id,
            "stage_name": self.stage_name,
            "stage_num": self.stage_num,
            "total_stages": self.total_stages,
            "progress_pct": self.progress_pct,
            "message": self.message,
            "metrics": self.metrics,
            "elapsed_sec": round(self.elapsed_sec, 2),
            "timestamp": self.timestamp,
        }

    def format_console(self) -> str:
        """Single-line human-readable representation."""
        stage_tag = (
            f"[{self.stage_num:02d}/{self.total_stages}] {self.stage_name}"
            if self.stage_name
            else f"[{self.stage_num:02d}/{self.total_stages}]"
        )
        icons = {
            ProgressEventType.PIPELINE_START: "🚀",
            ProgressEventType.PIPELINE_DONE: "✅",
            ProgressEventType.PIPELINE_FAILED: "💥",
            ProgressEventType.STAGE_START: "▶",
            ProgressEventType.STAGE_UPDATE: "•",
            ProgressEventType.STAGE_DONE: "✓",
            ProgressEventType.STAGE_FAILED: "✗",
            ProgressEventType.METRIC: "📊",
            ProgressEventType.WARNING: "⚠️",
            ProgressEventType.INFO: "ℹ",
        }
        icon = icons.get(self.event_type, "•")
        elapsed = f"  ({self.elapsed_sec:.1f}s)" if self.elapsed_sec > 0 else ""
        metric_str = ""
        if self.metrics:
            metric_str = "  " + "  ".join(f"{k}={v}" for k, v in self.metrics.items())
        return f"{icon} {stage_tag}  {self.message}{metric_str}{elapsed}"


# ---------------------------------------------------------------------------
# Transport protocol & implementations
# ---------------------------------------------------------------------------


class ProgressTransport(Protocol):  # pragma: no cover
    """Anything that can receive a ``ProgressEvent``."""

    def emit(self, event: ProgressEvent) -> None: ...


class LogTransport:
    """Emit events via Python's logging system (always available)."""

    def __init__(self, log_level: int = logging.INFO) -> None:
        self._level = log_level

    def emit(self, event: ProgressEvent) -> None:
        logger.log(self._level, event.format_console())


class FileTransport:
    """Append events as JSON-lines to ``<run_dir>/progress.jsonl``."""

    _FILENAME = "progress.jsonl"

    def __init__(self, run_dir: str | Path) -> None:
        self._path = Path(run_dir) / self._FILENAME
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: ProgressEvent) -> None:
        try:
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
        except OSError as exc:
            logger.debug("FileTransport write failed: %s", exc)


class WebSocketTransport:
    """Push events through the existing ``ConnectionManager``.

    The manager is imported lazily so this module stays importable
    even when the server is not running.
    """

    def __init__(self, manager: Any) -> None:
        self._manager = manager

    def emit(self, event: ProgressEvent) -> None:
        try:
            # Import here to match the existing broadcaster pattern
            from researchclaw.server.websocket.events import Event, EventType

            _type_map = {
                ProgressEventType.STAGE_START: EventType.RUN_STATUS_CHANGED,
                ProgressEventType.STAGE_DONE: EventType.STAGE_COMPLETE,
                ProgressEventType.STAGE_FAILED: EventType.RUN_STATUS_CHANGED,
                ProgressEventType.METRIC: EventType.METRIC_UPDATE,
                ProgressEventType.PIPELINE_DONE: EventType.RUN_STATUS_CHANGED,
                ProgressEventType.PIPELINE_FAILED: EventType.RUN_STATUS_CHANGED,
            }
            ws_event = Event(
                type=_type_map.get(event.event_type, EventType.RUN_STATUS_CHANGED),
                data=event.to_dict(),
            )
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.ensure_future(self._manager.broadcast(ws_event))
            else:
                loop.run_until_complete(self._manager.broadcast(ws_event))
        except Exception as exc:
            logger.debug("WebSocketTransport emit failed: %s", exc)


class CheckpointTransport:
    """Write current stage to ``checkpoint.json`` — keeps DashboardCollector working."""

    _FILENAME = "checkpoint.json"

    def __init__(self, run_dir: str | Path) -> None:
        self._path = Path(run_dir) / self._FILENAME

    def emit(self, event: ProgressEvent) -> None:
        if event.event_type not in (
            ProgressEventType.STAGE_START,
            ProgressEventType.STAGE_DONE,
            ProgressEventType.STAGE_FAILED,
            ProgressEventType.PIPELINE_DONE,
            ProgressEventType.PIPELINE_FAILED,
        ):
            return
        try:
            existing: dict[str, Any] = {}
            if self._path.exists():
                with self._path.open(encoding="utf-8") as fh:
                    existing = json.load(fh)
        except Exception:
            existing = {}

        existing.update(
            {
                "stage": event.stage_num,
                "stage_name": event.stage_name,
                "status": _checkpoint_status(event.event_type),
                "last_event": event.timestamp,
                "progress_pct": event.progress_pct,
            }
        )
        try:
            tmp = self._path.with_suffix(".tmp")
            with tmp.open("w", encoding="utf-8") as fh:
                json.dump(existing, fh, indent=2)
            tmp.replace(self._path)
        except OSError as exc:
            logger.debug("CheckpointTransport write failed: %s", exc)


def _checkpoint_status(etype: ProgressEventType) -> str:
    return {
        ProgressEventType.STAGE_START: "running",
        ProgressEventType.STAGE_DONE: "running",
        ProgressEventType.STAGE_FAILED: "failed",
        ProgressEventType.PIPELINE_DONE: "done",
        ProgressEventType.PIPELINE_FAILED: "failed",
    }.get(etype, "running")


class MultiTransport:
    """Fan-out to multiple transports."""

    def __init__(self, transports: Sequence[ProgressTransport]) -> None:
        self._transports = list(transports)

    def emit(self, event: ProgressEvent) -> None:
        for t in self._transports:
            try:
                t.emit(event)
            except Exception as exc:
                logger.debug("Transport %s failed: %s", type(t).__name__, exc)


# ---------------------------------------------------------------------------
# ProgressStream — the main interface callers use
# ---------------------------------------------------------------------------


class ProgressStream:
    """Unified progress emitter for a single pipeline run.

    All public methods are synchronous and safe to call from any thread.
    Internal state tracks the current stage and wall-clock start time so
    elapsed times are computed automatically.

    Args:
        run_id:       Pipeline run identifier (e.g. ``"rc-20260410-abc1"``).
        transport:    Any ``ProgressTransport`` (usually a ``MultiTransport``).
        total_stages: Total number of stages (default 23).
    """

    def __init__(
        self,
        run_id: str,
        transport: ProgressTransport,
        total_stages: int = 23,
    ) -> None:
        self._run_id = run_id
        self._transport = transport
        self._total = total_stages
        self._current_stage: str = ""
        self._current_num: int = 0
        self._stage_start: float = 0.0
        self._run_start: float = time.monotonic()

    # ------------------------------------------------------------------ #
    # Pipeline-level events                                                 #
    # ------------------------------------------------------------------ #

    def pipeline_start(self, topic: str = "") -> None:
        self._emit(
            ProgressEventType.PIPELINE_START,
            message=f"Pipeline started — topic: {topic}" if topic else "Pipeline started",
        )

    def pipeline_done(self) -> None:
        elapsed = time.monotonic() - self._run_start
        self._emit(
            ProgressEventType.PIPELINE_DONE,
            message=f"Pipeline complete in {_fmt_elapsed(elapsed)}",
            elapsed_sec=elapsed,
        )

    def pipeline_failed(self, reason: str = "") -> None:
        elapsed = time.monotonic() - self._run_start
        self._emit(
            ProgressEventType.PIPELINE_FAILED,
            message=f"Pipeline failed: {reason}" if reason else "Pipeline failed",
            elapsed_sec=elapsed,
        )

    # ------------------------------------------------------------------ #
    # Stage-level events                                                    #
    # ------------------------------------------------------------------ #

    def stage_start(self, stage_name: str, stage_num: int) -> None:
        self._current_stage = stage_name
        self._current_num = stage_num
        self._stage_start = time.monotonic()
        self._emit(
            ProgressEventType.STAGE_START,
            message=f"Starting {stage_name}",
        )

    def stage_done(self, summary: str = "") -> None:
        elapsed = time.monotonic() - self._stage_start
        self._emit(
            ProgressEventType.STAGE_DONE,
            message=summary or f"{self._current_stage} complete",
            elapsed_sec=elapsed,
        )

    def stage_failed(self, reason: str = "") -> None:
        elapsed = time.monotonic() - self._stage_start
        self._emit(
            ProgressEventType.STAGE_FAILED,
            message=f"{self._current_stage} failed: {reason}" if reason else f"{self._current_stage} failed",
            elapsed_sec=elapsed,
        )

    # ------------------------------------------------------------------ #
    # Inline update events                                                  #
    # ------------------------------------------------------------------ #

    def update(self, message: str, **kv: Any) -> None:
        """Emit a STAGE_UPDATE with an optional dict of key-value metrics."""
        self._emit(ProgressEventType.STAGE_UPDATE, message=message, metrics=kv or {})

    def metric(self, name: str, value: Any) -> None:
        """Emit a single named metric."""
        self._emit(ProgressEventType.METRIC, message=name, metrics={name: value})

    def warn(self, message: str) -> None:
        self._emit(ProgressEventType.WARNING, message=message)

    def info(self, message: str) -> None:
        self._emit(ProgressEventType.INFO, message=message)

    # ------------------------------------------------------------------ #
    # Context manager                                                       #
    # ------------------------------------------------------------------ #

    @contextmanager
    def stage(
        self, stage_name: str, stage_num: int, summary: str = ""
    ) -> Generator[ProgressStream, None, None]:
        """Context manager that wraps a stage with start/done/failed events.

        Usage::

            with stream.stage("LITERATURE_COLLECT", 4) as s:
                papers = collect(...)
                s.update(f"Found {len(papers)} papers", count=len(papers))
        """
        self.stage_start(stage_name, stage_num)
        try:
            yield self
        except Exception as exc:
            self.stage_failed(str(exc))
            raise
        else:
            self.stage_done(summary)

    # ------------------------------------------------------------------ #
    # Internal                                                              #
    # ------------------------------------------------------------------ #

    def _emit(
        self,
        event_type: ProgressEventType,
        message: str = "",
        metrics: dict[str, Any] | None = None,
        elapsed_sec: float = 0.0,
    ) -> None:
        event = ProgressEvent(
            event_type=event_type,
            run_id=self._run_id,
            stage_name=self._current_stage,
            stage_num=self._current_num,
            total_stages=self._total,
            message=message,
            metrics=metrics or {},
            elapsed_sec=elapsed_sec,
        )
        self._transport.emit(event)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def make_stream(
    run_id: str,
    run_dir: str | Path | None = None,
    ws_manager: Any | None = None,
    total_stages: int = 23,
    log_level: int = logging.INFO,
) -> ProgressStream:
    """Create a ``ProgressStream`` wired to all available transports.

    Args:
        run_id:       Pipeline run ID.
        run_dir:      Run directory (enables FileTransport + CheckpointTransport).
        ws_manager:   ``ConnectionManager`` instance (enables WebSocketTransport).
        total_stages: Total pipeline stages.
        log_level:    Log level for ``LogTransport``.

    Returns:
        Ready-to-use ``ProgressStream``.
    """
    transports: list[ProgressTransport] = [LogTransport(log_level=log_level)]

    if run_dir is not None:
        run_path = Path(run_dir)
        transports.append(FileTransport(run_path))
        transports.append(CheckpointTransport(run_path))

    if ws_manager is not None:
        transports.append(WebSocketTransport(ws_manager))

    transport = MultiTransport(transports)
    return ProgressStream(run_id=run_id, transport=transport, total_stages=total_stages)


# ---------------------------------------------------------------------------
# Reader — replay progress from a JSONL file (for CLI / dashboard)
# ---------------------------------------------------------------------------


def read_progress(run_dir: str | Path) -> list[ProgressEvent]:
    """Load all emitted events from ``progress.jsonl`` for a run.

    Useful for replaying progress in the dashboard or CLI status command.
    """
    path = Path(run_dir) / FileTransport._FILENAME
    if not path.exists():
        return []
    events: list[ProgressEvent] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                events.append(
                    ProgressEvent(
                        event_type=ProgressEventType(d.get("event_type", "info")),
                        run_id=str(d.get("run_id", "")),
                        stage_name=str(d.get("stage_name", "")),
                        stage_num=int(d.get("stage_num", 0)),
                        total_stages=int(d.get("total_stages", 23)),
                        message=str(d.get("message", "")),
                        metrics=d.get("metrics") or {},
                        elapsed_sec=float(d.get("elapsed_sec", 0)),
                        timestamp=str(d.get("timestamp", "")),
                    )
                )
            except Exception as exc:
                logger.debug("Skipping malformed progress line: %s", exc)
    return events


def print_progress(run_dir: str | Path) -> None:
    """Print all progress events from a run directory to stdout."""
    events = read_progress(run_dir)
    if not events:
        print("No progress events found.")
        return
    for ev in events:
        print(ev.format_console())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fmt_elapsed(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"
