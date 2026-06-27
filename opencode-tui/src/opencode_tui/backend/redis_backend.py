"""Redis backend implementation.

Migrates the existing dashboard.py Redis pub/sub + polling logic here.
Shares the same Backend interface as the OpenCode backend.
"""

import json
import os
from datetime import datetime, timezone
from typing import AsyncIterator, Optional

from opencode_tui.backend.base import Backend


class RedisBackend(Backend):
    """Redis backend."""

    PROGRESS_CH = "academic:progress"
    OUTBOX_CH = "academic:outbox"
    INBOX_CH = "academic:inbox"
    STATE_KEY = "academic:phase:state"

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self._r = None
        self._pubsub = None
        self._connected = False

    @property
    def name(self) -> str:
        return "redis"

    async def connect(self) -> bool:
        try:
            from redis.asyncio import Redis
            self._r = Redis.from_url(self.redis_url, decode_responses=True)
            await self._r.ping()
            self._connected = True
            self._pubsub = self._r.pubsub()
            await self._pubsub.subscribe(self.PROGRESS_CH, self.OUTBOX_CH)
            return True
        except Exception:
            return False

    async def disconnect(self):
        self._connected = False
        if self._pubsub:
            await self._pubsub.unsubscribe()
        if self._r:
            await self._r.close()

    async def send_message(self, text: str) -> str:
        msg = json.dumps({
            "type": "user_message",
            "chat_id": "opencode-tui",
            "text": text,
        })
        await self._r.publish(self.INBOX_CH, msg)
        return ""

    async def subscribe(self) -> AsyncIterator[dict]:
        while self._connected:
            try:
                msg = await self._pubsub.get_message(
                    timeout=1.0, ignore_subscribe_messages=True
                )
            except Exception:
                break
            if msg is None:
                continue
            try:
                data = json.loads(msg["data"])
                channel = msg.get("channel", b"").decode() if isinstance(msg.get("channel"), bytes) else msg.get("channel", "")
                data["_source"] = "redis"
                data["_channel"] = channel
                yield data
            except (json.JSONDecodeError, Exception):
                continue

    async def get_phase_state(self) -> dict:
        try:
            state = await self._r.json().get(self.STATE_KEY)
            return state or {"status": "idle", "current_phase": 0, "completed_phases": []}
        except Exception:
            return {"status": "idle", "current_phase": 0, "completed_phases": []}

    async def get_cost_summary(self) -> dict:
        try:
            state = await self._r.json().get(self.STATE_KEY) or {}
            pid = state.get("project_id") or "default"

            from redis import Redis as SyncRedis

            def _read():
                r = SyncRedis.from_url(self.redis_url, decode_responses=True)
                try:
                    # TokenBudget: read session usage directly
                    session_key = f"budget:session:{pid}:total"
                    s_tokens = int(r.hget(session_key, "tokens") or 0)
                    s_calls = int(r.hget(session_key, "calls") or 0)
                    SESSION_LIMIT = 128000
                    session_pct = round(s_tokens / SESSION_LIMIT * 100, 1) if SESSION_LIMIT else 0

                    # Task budget
                    task_key = f"budget:task:{pid}:total"
                    t_tokens = int(r.hget(task_key, "tokens") or 0)
                    t_calls = int(r.hget(task_key, "calls") or 0)
                    TASK_LIMIT = 512000
                    task_pct = round(t_tokens / TASK_LIMIT * 100, 1) if TASK_LIMIT else 0

                    # Cost: read project total
                    total_cost = float(r.get(f"cost:{pid}:total") or 0.0)

                    # Cost: read first session's detail
                    session_ids = r.smembers(f"cost:{pid}:sessions") or set()
                    agent_cost = 0.0
                    if session_ids:
                        sid = sorted(session_ids)[0]
                        raw = r.lrange(f"costs:{pid}:{sid}", 0, -1)
                        for entry in raw:
                            import json as _j
                            try:
                                e = _j.loads(entry)
                                agent_cost += float(e.get("cost_usd", 0.0))
                            except Exception:
                                pass

                    return {
                        "session_pct": int(session_pct),
                        "task_pct": int(task_pct),
                        "session_cost": agent_cost,
                        "task_cost": total_cost,
                        "total_cost": total_cost,
                        "action": "ok",
                    }
                finally:
                    try:
                        r.close()
                    except Exception:
                        pass

            import asyncio
            return await asyncio.to_thread(_read)
        except Exception:
            return {
                "session_pct": 0, "task_pct": 0,
                "session_cost": 0.0, "task_cost": 0.0, "total_cost": 0.0,
            }

    async def get_gate_results(self) -> dict:
        try:
            state = await self._r.json().get(self.STATE_KEY)
            return (state or {}).get("gate_results", {})
        except Exception:
            return {}

    async def get_project_info(self) -> dict:
        try:
            state = await self._r.json().get(self.STATE_KEY)
            if state:
                return {
                    "title": state.get("project_title", ""),
                    "status": state.get("status", "idle"),
                    "project_id": state.get("project_id", ""),
                }
        except Exception:
            pass
        return {"title": "", "status": "disconnected", "project_id": ""}

    async def get_available_agents(self) -> list[dict]:
        return []

    async def get_available_models(self) -> list[dict]:
        return []

    def is_connected(self) -> bool:
        return self._connected
