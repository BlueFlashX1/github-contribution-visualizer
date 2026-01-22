#!/usr/bin/env python3
"""
Generate Top Languages card for GitHub profile.
Shows languages from both private and public repositories.
"""

import os
from collections import defaultdict
from typing import Dict

from github import Github


class LanguageStatsGenerator:
    """Generate language statistics from GitHub repositories."""

    def __init__(self, token: str):
        """Initialize with GitHub token."""
        self.github = Github(token)
        self.user = self.github.get_user()

    def get_language_stats(self) -> Dict[str, int]:
        """Get aggregated language statistics from all repos (public + private)."""
        language_bytes = defaultdict(int)

        print("Fetching repositories...")
        repos = list(self.user.get_repos(affiliation="owner", sort="updated"))
        print(f"Found {len(repos)} repositories")

        for repo in repos:
            try:
                languages = repo.get_languages()
                for lang, bytes_count in languages.items():
                    language_bytes[lang] += bytes_count
                print(f"  Processed: {repo.name} ({len(languages)} languages)")
            except Exception as e:
                print(f"  Error processing {repo.name}: {e}")
                continue

        return dict(language_bytes)

    def generate_languages_svg(
        self, language_stats: Dict[str, int], top_n: int = 8
    ) -> str:
        """Generate SVG card showing top languages."""

        # Sort languages by bytes
        sorted_languages = sorted(
            language_stats.items(), key=lambda x: x[1], reverse=True
        )[:top_n]

        if not sorted_languages:
            return self._generate_empty_svg()

        total_bytes = sum(language_stats.values())
        top_languages = [
            (lang, bytes_count, (bytes_count / total_bytes) * 100)
            for lang, bytes_count in sorted_languages
        ]

        # Color palette for languages
        language_colors = {
            "Python": "#3776AB",
            "JavaScript": "#F7DF1E",
            "TypeScript": "#3178C6",
            "Java": "#ED8B00",
            "Go": "#00ADD8",
            "Rust": "#000000",
            "C++": "#00599C",
            "C": "#A8B9CC",
            "C#": "#239120",
            "Ruby": "#CC342D",
            "PHP": "#777BB4",
            "Swift": "#FA7343",
            "Kotlin": "#7F52FF",
            "R": "#276DC3",
            "SQL": "#4479A1",
            "HTML": "#E34F26",
            "CSS": "#1572B6",
            "Shell": "#89E051",
            "PowerShell": "#012456",
            "Lua": "#000080",
            "Dart": "#0175C2",
            "Scala": "#DC322F",
            "MATLAB": "#0076A8",
            "Jupyter Notebook": "#DA5B0B",
        }

        # Modern color palette
        bg = "#0d1117"
        card_bg = "#161b22"
        text_primary = "#f0f6fc"
        text_secondary = "#8b949e"
        border = "#30363d"

        # Calculate dimensions
        width = 700
        box_height = 50
        padding = 40
        title_height = 60
        spacing = 12
        total_height = (
            title_height
            + (len(top_languages) * (box_height + spacing))
            - spacing
            + (padding * 2)
        )

        svg = f"""<svg width="{width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="{width}" height="{total_height}" fill="{bg}" rx="8"/>

  <!-- Card -->
  <rect x="0" y="0" width="{width}" height="{total_height}" fill="{card_bg}" rx="8" stroke="{border}" stroke-width="1"/>

  <!-- Title -->
  <text x="{padding}" y="{padding + 20}" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="600" fill="{text_primary}">
    Top Languages
  </text>

  <!-- Language Bars -->
  <g transform="translate({padding}, {title_height})">
"""

        y_offset = 0
        for lang, bytes_count, percentage in top_languages:
            color = language_colors.get(lang, "#58a6ff")

            # Language name and percentage
            svg += f"""    <!-- {lang} -->
    <rect x="0" y="{y_offset}" width="{width - (padding * 2)}" height="{box_height}" fill="#1c2128" rx="6"/>

    <!-- Language name -->
    <text x="15" y="{y_offset + 25}" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="{text_primary}" dominant-baseline="middle">
      {lang}
    </text>

    <!-- Percentage -->
    <text x="{width - (padding * 2) - 15}" y="{y_offset + 25}" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="500" fill="{text_secondary}" text-anchor="end" dominant-baseline="middle">
      {percentage:.1f}%
    </text>

    <!-- Progress bar background -->
    <rect x="15" y="{y_offset + 35}" width="{width - (padding * 2) - 30}" height="8" fill="#0d1117" rx="4"/>

    <!-- Progress bar fill -->
    <rect x="15" y="{y_offset + 35}" width="{(width - (padding * 2) - 30) * (percentage / 100)}" height="8" fill="{color}" rx="4"/>
"""

            y_offset += box_height + spacing

        # Footer
        repo_count = len(list(self.user.get_repos(affiliation="owner")))
        svg += f"""  </g>

  <!-- Footer -->
  <text x="{width - padding}" y="{total_height - padding}" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="{text_secondary}" text-anchor="end">
    {repo_count} repos • Public & Private
  </text>
</svg>"""

        return svg

    def _generate_empty_svg(self) -> str:
        """Generate empty state SVG."""
        width = 700
        height = 200
        bg = "#0d1117"
        card_bg = "#161b22"
        text_secondary = "#8b949e"
        border = "#30363d"

        return f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" fill="{bg}" rx="8"/>
  <rect x="0" y="0" width="{width}" height="{height}" fill="{card_bg}" rx="8" stroke="{border}" stroke-width="1"/>
  <text x="{width // 2}" y="{height // 2}" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="{text_secondary}" text-anchor="middle" dominant-baseline="middle">
    No language data available
  </text>
</svg>"""


def main():
    """Main function."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        return

    generator = LanguageStatsGenerator(token)

    print("Fetching language statistics...")
    language_stats = generator.get_language_stats()

    if not language_stats:
        print("No language data found")
        return

    print(f"\nFound {len(language_stats)} languages")
    print("Top languages:")
    sorted_langs = sorted(language_stats.items(), key=lambda x: x[1], reverse=True)[:8]
    for lang, bytes_count in sorted_langs:
        percentage = (bytes_count / sum(language_stats.values())) * 100
        print(f"  {lang}: {percentage:.1f}%")

    print("\nGenerating SVG...")
    svg = generator.generate_languages_svg(language_stats)

    output_file = "languages.svg"
    with open(output_file, "w") as f:
        f.write(svg)

    print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()
