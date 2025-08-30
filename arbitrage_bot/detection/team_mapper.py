from typing import Dict
import json
import os


class TeamMapper:
    """Handles team name standardization across different sportsbooks"""

    def __init__(self, mappings_file: str = None):
        self.mappings_file = mappings_file or "config/team_mappings.json"
        self.team_mappings = self._load_mappings()

    def _load_mappings(self) -> Dict[str, str]:
        """Load team name mappings from file"""
        default_mappings = {
            "Kansas St": "Kansas State",
        }

        if os.path.exists(self.mappings_file):
            try:
                with open(self.mappings_file, "r") as f:
                    return json.load(f)
            except:
                return default_mappings
        else:
            return default_mappings

    def standardize_team_name(self, team_name: str) -> str:
        """Convert team name to standardized format"""
        return self.team_mappings.get(team_name, team_name)

    def are_same_teams(self, team1: str, team2: str) -> bool:
        """Check if two team names refer to the same team"""
        return self.standardize_team_name(team1) == self.standardize_team_name(team2)

    def get_standardized_name(self, team_name: str) -> str:
        """Get the standardized name for a team"""
        return self.standardize_team_name(team_name)
