from datetime import datetime, timezone


def judge_popularity(trades: list, now=None):
    """
    인기도 계산
    """
    now = now or datetime.now(timezone.utc)

    def dt(s):
        return datetime.fromisoformat(s.replace('Z', '+00:00'))

    created = []
    recent = 0
    ended_recent = 0
    sellers = set()

    for t in trades:
        ca = t.get("created_at")
        if ca:
            d = dt(ca)
            created.append(d)
            if (now - d).total_seconds() <= 48 * 3600:
                recent += 1
                if t.get("tradeStatus") is False:
                    ended_recent += 1
        info = t.get("traderDiscordInfo") or {}
        sellers.add(info.get("id") or info.get("provider_id") or info.get("name"))

    last_1h = sum((now - c).total_seconds() <= 3600 for c in created)
    recent_30m = sum((now - c).total_seconds() <= 1800 for c in created)
    sell_through = (ended_recent / recent * 100) if recent else 0.0
    unique_sellers = len([s for s in sellers if s])

    # 아주 단순 점수
    score = min(100, last_1h * 10 + sell_through * 0.8 + min(unique_sellers, 5) * 4)
    if last_1h >= 6 and sell_through >= 30 and recent_30m >= 1:
        label = "Hot"
    elif last_1h >= 3 or sell_through >= 15:
        label = "Moderately Active"
    else:
        label = "Quiet"

    latest = max(created).isoformat() if created else None
    return {
        "label": label, "score": round(score, 1),
        "last_1h": last_1h, "sell_through_48h_pct": round(sell_through, 1),
        "unique_sellers": unique_sellers, "latest_created_at": latest
    }
