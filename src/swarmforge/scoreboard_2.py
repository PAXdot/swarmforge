import time
from typing import Dict, List, Optional
from collections import defaultdict

from swarmforge import timestamp

class Scoreboard:
    """Keeps track of bots' scores based on heartbeat frequency."""

    def __init__(self):
        self.last_heartbeats: Dict[str, timestamp.Timestamp] = {}
        self.scores: Dict[str, int] = defaultdict(int)

    def heartbeat_received(self, bot_id: str, timestamp: timestamp.Timestamp) -> None:
        """Update bot's score if heartbeat received within acceptable interval."""
        current_time = timestamp.now()
        if bot_id in self.last_heartbeats:
            last_heartbeat = self.last_heartbeats[bot_id]
            interval = current_time - last_heartbeat
            if interval < 5:  # Assuming acceptable interval is 5 seconds
                self.scores[bot_id] += 1
            else:
                self.scores[bot_id] = 0  # Reset score if heartbeat is late
        self.last_heartbeats[bot_id] = current_time

    def get_scores(self) -> Dict[str, int]:
        """Return current scores of all bots."""
        return self.scores.copy()

    def get_ranking(self) -> List[Tuple[str, int]]:
        """Return bots ranked by their scores in descending order."""
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
