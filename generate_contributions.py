#!/usr/bin/env python3
"""
GitHub Contribution Visualizer
Generates a beautiful SVG showing real contributions weighted by impact,
not just commit frequency.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict

try:
    import requests
    from github import Github
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install PyGithub requests --quiet")
    from github import Github


class ContributionVisualizer:
    """Generates contribution visualizations based on real GitHub activity."""

    def __init__(self, github_token: str, username: str):
        self.github = Github(github_token)
        self.username = username
        self.user = self.github.get_user(username)

    def get_contribution_metrics(self, days: int = 365) -> Dict:
        """Fetch real contribution metrics from GitHub API."""
        since = datetime.now() - timedelta(days=days)

        metrics = {
            "prs_merged": 0,
            "prs_opened": 0,
            "prs_reviewed": 0,
            "issues_opened": 0,
            "issues_closed": 0,
            "repos_contributed": set(),
            "total_impact_score": 0,
            "daily_activity": {},
        }

        print(f"Fetching contribution data for {self.username}...")

        # Get user's repositories
        repos = list(self.user.get_repos())
        print(f"Found {len(repos)} repositories")

        # Get PRs (merged and opened)
        for repo in repos:
            try:
                # PRs merged (high impact)
                prs_merged = repo.get_pulls(state="closed", sort="updated")
                for pr in prs_merged:
                    if pr.merged_at and pr.merged_at >= since:
                        if pr.user.login == self.username:
                            metrics["prs_merged"] += 1
                            metrics["repos_contributed"].add(repo.name)
                            date_key = pr.merged_at.date().isoformat()
                            metrics["daily_activity"][date_key] = (
                                metrics["daily_activity"].get(date_key, 0) + 5
                            )  # PR merge = 5 points

                # PRs opened
                prs_opened = repo.get_pulls(state="all", sort="updated")
                for pr in prs_opened:
                    if pr.created_at >= since and pr.user.login == self.username:
                        metrics["prs_opened"] += 1
                        date_key = pr.created_at.date().isoformat()
                        metrics["daily_activity"][date_key] = (
                            metrics["daily_activity"].get(date_key, 0) + 3
                        )  # PR opened = 3 points

                # PRs reviewed (comments on PRs)
                prs = repo.get_pulls(state="all", sort="updated")
                for pr in prs:
                    if pr.updated_at >= since:
                        comments = pr.get_comments()
                        for comment in comments:
                            if (
                                comment.user.login == self.username
                                and comment.created_at >= since
                            ):
                                metrics["prs_reviewed"] += 1
                                date_key = comment.created_at.date().isoformat()
                                metrics["daily_activity"][date_key] = (
                                    metrics["daily_activity"].get(date_key, 0) + 2
                                )  # Review = 2 points

                # Issues
                issues = repo.get_issues(state="all", sort="updated")
                for issue in issues:
                    if issue.created_at >= since and issue.user.login == self.username:
                        if issue.pull_request is None:  # It's an issue, not a PR
                            metrics["issues_opened"] += 1
                            date_key = issue.created_at.date().isoformat()
                            metrics["daily_activity"][date_key] = (
                                metrics["daily_activity"].get(date_key, 0) + 1
                            )  # Issue = 1 point
                            if issue.state == "closed":
                                metrics["issues_closed"] += 1
            except Exception as e:
                print(f"Error processing {repo.name}: {e}")
                continue

        # Calculate total impact score
        metrics["total_impact_score"] = (
            metrics["prs_merged"] * 5
            + metrics["prs_opened"] * 3
            + metrics["prs_reviewed"] * 2
            + metrics["issues_opened"] * 1
        )
        metrics["repos_contributed"] = len(metrics["repos_contributed"])

        return metrics

    def generate_svg(self, metrics: Dict, style: str = "modern") -> str:
        """Generate beautiful SVG visualization."""

        # Color scheme (modern, accessible)
        colors = {
            "background": "#0d1117",
            "text_primary": "#c9d1d9",
            "text_secondary": "#8b949e",
            "accent": "#58a6ff",
            "success": "#3fb950",
            "warning": "#d29922",
            "grid_0": "#161b22",
            "grid_1": "#0e4429",
            "grid_2": "#006d32",
            "grid_3": "#26a641",
            "grid_4": "#39d353",
        }

        # Calculate activity levels for heatmap
        if metrics["daily_activity"]:
            max_activity = max(metrics["daily_activity"].values())
        else:
            max_activity = 1

        # Generate heatmap data (last 365 days)
        today = datetime.now().date()
        heatmap_data = []
        for i in range(365):
            date = today - timedelta(days=364 - i)
            date_key = date.isoformat()
            activity = metrics["daily_activity"].get(date_key, 0)

            # Normalize to 0-4 scale
            if max_activity > 0:
                level = min(4, int((activity / max_activity) * 4))
            else:
                level = 0

            heatmap_data.append({"date": date, "activity": activity, "level": level})

        # Group by weeks (53 weeks = 371 days, we'll use 53)
        weeks = []
        current_week = []
        for i, day in enumerate(heatmap_data):
            current_week.append(day)
            if len(current_week) == 7 or i == len(heatmap_data) - 1:
                weeks.append(current_week)
                current_week = []

        # SVG dimensions
        cell_size = 12
        cell_gap = 3
        week_width = cell_size + cell_gap
        week_count = len(weeks)
        width = (week_count * week_width) + 120  # Extra space for labels
        height = (7 * week_width) + 100  # 7 days + header + footer

        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{colors["background"]}"/>',
        ]

        # Title
        svg_parts.append(
            f'<text x="10" y="25" font-family="system-ui, -apple-system, sans-serif" '
            f'font-size="16" font-weight="600" fill="{colors["text_primary"]}">'
            f"Real Contributions (Impact-Weighted)</text>"
        )

        # Metrics summary
        y_offset = 50
        svg_parts.append(
            f'<text x="10" y="{y_offset}" font-family="system-ui, -apple-system, sans-serif" '
            f'font-size="12" fill="{colors["text_secondary"]}">'
            f'PRs Merged: {metrics["prs_merged"]} • '
            f'PRs Opened: {metrics["prs_opened"]} • '
            f'Reviews: {metrics["prs_reviewed"]} • '
            f'Issues: {metrics["issues_opened"]} • '
            f'Impact Score: {metrics["total_impact_score"]}</text>'
        )

        # Heatmap grid
        start_x = 120
        start_y = 80

        for week_idx, week in enumerate(weeks):
            x = start_x + (week_idx * week_width)

            for day_idx, day in enumerate(week):
                y = start_y + (day_idx * week_width)

                color = colors[f'grid_{day["level"]}']

                svg_parts.append(
                    f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                    f'fill="{color}" rx="2" data-date="{day["date"]}" '
                    f'data-activity="{day["activity"]}"/>'
                )

        # Month labels
        month_labels = []
        current_month = None
        for week_idx, week in enumerate(weeks):
            if week:
                first_day = week[0]["date"]
                month = first_day.strftime("%b")
                if month != current_month:
                    month_labels.append((week_idx, month))
                    current_month = month

        for week_idx, month in month_labels:
            x = start_x + (week_idx * week_width)
            svg_parts.append(
                f'<text x="{x}" y="{start_y - 5}" font-family="system-ui, -apple-system, sans-serif" '
                f'font-size="10" fill="{colors["text_secondary"]}">{month}</text>'
            )

        # Day labels
        day_names = ["Mon", "Wed", "Fri"]
        day_positions = [0, 2, 4]
        for day_name, day_pos in zip(day_names, day_positions):
            y = start_y + (day_pos * week_width) + (cell_size // 2)
            svg_parts.append(
                f'<text x="{start_x - 40}" y="{y + 4}" font-family="system-ui, -apple-system, sans-serif" '
                f'font-size="10" fill="{colors["text_secondary"]}" text-anchor="end">{day_name}</text>'
            )

        # Legend
        legend_y = height - 40
        svg_parts.append(
            f'<text x="10" y="{legend_y}" font-family="system-ui, -apple-system, sans-serif" '
            f'font-size="11" fill="{colors["text_secondary"]}">Less</text>'
        )

        legend_x = 50
        for i in range(5):
            color = colors[f"grid_{i}"]
            x = legend_x + (i * 20)
            svg_parts.append(
                f'<rect x="{x}" y="{legend_y - 8}" width="12" height="12" '
                f'fill="{color}" rx="2"/>'
            )

        svg_parts.append(
            f'<text x="{legend_x + 120}" y="{legend_y}" font-family="system-ui, -apple-system, sans-serif" '
            f'font-size="11" fill="{colors["text_secondary"]}">More</text>'
        )

        # Footer
        svg_parts.append(
            f'<text x="10" y="{height - 15}" font-family="system-ui, -apple-system, sans-serif" '
            f'font-size="10" fill="{colors["text_secondary"]}">'
            f"Weighted by impact: PRs (5pts) • Reviews (2pts) • Issues (1pt) • Not just commit count</text>"
        )

        svg_parts.append("</svg>")

        return "\n".join(svg_parts)


def main():
    """Main entry point."""
    github_token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USERNAME") or os.getenv("GITHUB_ACTOR")
    output_file = os.getenv("OUTPUT_FILE", "contributions.svg")

    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    if not username:
        print("Error: GITHUB_USERNAME or GITHUB_ACTOR environment variable not set")
        sys.exit(1)

    print(f"Generating contribution visualization for {username}...")

    visualizer = ContributionVisualizer(github_token, username)
    metrics = visualizer.get_contribution_metrics(days=365)

    print("\nContribution Metrics:")
    print(f"  PRs Merged: {metrics['prs_merged']}")
    print(f"  PRs Opened: {metrics['prs_opened']}")
    print(f"  PRs Reviewed: {metrics['prs_reviewed']}")
    print(f"  Issues Opened: {metrics['issues_opened']}")
    print(f"  Repos Contributed: {metrics['repos_contributed']}")
    print(f"  Total Impact Score: {metrics['total_impact_score']}")

    svg = visualizer.generate_svg(metrics)

    with open(output_file, "w") as f:
        f.write(svg)

    print(f"\n✅ Generated {output_file}")
    print(
        "📊 Visualization shows impact-weighted contributions, not just commit frequency"
    )


if __name__ == "__main__":
    main()
