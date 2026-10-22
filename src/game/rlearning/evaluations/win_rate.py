from collections import defaultdict


def get_score(results):
    groups = defaultdict(list)

    for result in results:
        groups[result["matchup"]].append(result)

    breakdown = {}

    for key, rows in groups.items():
        completed = [
            row for row in rows
            if row["status"] == "completed"
        ]

        wins = sum(
            row["outcome"] == "win"
            for row in completed
        )
        draws = sum(
            row["outcome"] == "draw"
            for row in completed
        )

        breakdown[key] = {
            "games": len(rows),
            "completed": len(completed),
            "wins": wins,
            "draws": draws,
            "losses": len(completed) - wins - draws,
            "score": (
                100 * (wins + 0.5 * draws) / len(completed)
                if completed else None
            ),
        }

    valid = bool(results) and all(
        row["status"] == "completed"
        and row["outcome"] in {"win", "loss", "draw"}
        for row in results
    )

    return {
        "valid": valid,
        "score": (
            sum(
                item["score"]
                for item in breakdown.values()
            ) / len(breakdown)
            if valid else None
        ),

        "completed": sum(
            row["status"] == "completed"
            for row in results
        ),
        "truncated": sum(
            row["status"] == "truncated"
            for row in results
        ),
        "errors": sum(
            row["status"] == "error"
            for row in results
        ),

        "by_matchup": breakdown,
    }