#!/usr/bin/env python3
"""
Simple GitHub Contribution Visualizer
Clean, readable card-style visualization showing impact-weighted contributions.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict
import json

try:
    from github import Github
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install PyGithub --quiet")
    from github import Github


class SimpleContributionVisualizer:
    """Simple, readable contribution visualization."""
    
    def __init__(self, github_token: str, username: str):
        self.github = Github(github_token)
        self.username = username
        self.user = self.github.get_user(username)
        
    def get_metrics(self, days: int = 365) -> Dict:
        """Get contribution metrics."""
        since = datetime.now() - timedelta(days=days)
        
        metrics = {
            'prs_merged': 0,
            'prs_opened': 0,
            'reviews': 0,
            'issues': 0,
            'repos': set(),
            'impact_score': 0
        }
        
        print(f"Analyzing contributions for {self.username}...")
        
        repos = list(self.user.get_repos())
        print(f"Scanning {len(repos)} repositories...")
        
        for repo in repos:
            try:
                # PRs merged
                for pr in repo.get_pulls(state='closed', sort='updated'):
                    if pr.merged_at and pr.merged_at >= since and pr.user.login == self.username:
                        metrics['prs_merged'] += 1
                        metrics['repos'].add(repo.name)
                
                # PRs opened
                for pr in repo.get_pulls(state='all', sort='updated'):
                    if pr.created_at >= since and pr.user.login == self.username:
                        metrics['prs_opened'] += 1
                
                # Reviews (comments on PRs)
                for pr in repo.get_pulls(state='all', sort='updated'):
                    if pr.updated_at >= since:
                        for comment in pr.get_comments():
                            if comment.user.login == self.username and comment.created_at >= since:
                                metrics['reviews'] += 1
                
                # Issues
                for issue in repo.get_issues(state='all', sort='updated'):
                    if issue.created_at >= since and issue.user.login == self.username:
                        if issue.pull_request is None:
                            metrics['issues'] += 1
            except Exception as e:
                continue
        
        metrics['repos'] = len(metrics['repos'])
        metrics['impact_score'] = (
            metrics['prs_merged'] * 5 +
            metrics['prs_opened'] * 3 +
            metrics['reviews'] * 2 +
            metrics['issues'] * 1
        )
        
        return metrics
    
    def generate_card_svg(self, metrics: Dict) -> str:
        """Generate clean card-style SVG."""
        
        # Modern color palette
        bg = '#0d1117'
        card_bg = '#161b22'
        text_primary = '#f0f6fc'
        text_secondary = '#8b949e'
        accent = '#58a6ff'
        success = '#3fb950'
        
        width = 600
        height = 300
        
        svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#58a6ff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#3fb950;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{bg}" rx="8"/>
  
  <!-- Card -->
  <rect x="20" y="20" width="{width-40}" height="{height-40}" fill="{card_bg}" rx="8" stroke="#30363d" stroke-width="1"/>
  
  <!-- Title -->
  <text x="40" y="55" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="600" fill="{text_primary}">
    Real Contributions
  </text>
  <text x="40" y="75" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="{text_secondary}">
    Impact-weighted • Not just commit count
  </text>
  
  <!-- Metrics Grid -->
  <g transform="translate(40, 100)">
    <!-- PRs Merged -->
    <rect x="0" y="0" width="120" height="80" fill="#0e4429" rx="6"/>
    <text x="60" y="25" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="700" fill="{success}" text-anchor="middle">
      {metrics['prs_merged']}
    </text>
    <text x="60" y="45" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="{text_secondary}" text-anchor="middle">
      PRs Merged
    </text>
    <text x="60" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="{text_secondary}" text-anchor="middle">
      5 pts each
    </text>
    
    <!-- PRs Opened -->
    <rect x="140" y="0" width="120" height="80" fill="#1c2128" rx="6"/>
    <text x="200" y="25" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="700" fill="{accent}" text-anchor="middle">
      {metrics['prs_opened']}
    </text>
    <text x="200" y="45" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="{text_secondary}" text-anchor="middle">
      PRs Opened
    </text>
    <text x="200" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="{text_secondary}" text-anchor="middle">
      3 pts each
    </text>
    
    <!-- Reviews -->
    <rect x="280" y="0" width="120" height="80" fill="#1c2128" rx="6"/>
    <text x="340" y="25" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="700" fill="{accent}" text-anchor="middle">
      {metrics['reviews']}
    </text>
    <text x="340" y="45" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="{text_secondary}" text-anchor="middle">
      Reviews
    </text>
    <text x="340" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="{text_secondary}" text-anchor="middle">
      2 pts each
    </text>
    
    <!-- Issues -->
    <rect x="420" y="0" width="120" height="80" fill="#1c2128" rx="6"/>
    <text x="480" y="25" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="700" fill="{text_primary}" text-anchor="middle">
      {metrics['issues']}
    </text>
    <text x="480" y="45" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="{text_secondary}" text-anchor="middle">
      Issues
    </text>
    <text x="480" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="{text_secondary}" text-anchor="middle">
      1 pt each
    </text>
  </g>
  
  <!-- Impact Score -->
  <g transform="translate(40, 220)">
    <rect x="0" y="0" width="{width-80}" height="40" fill="url(#grad)" opacity="0.1" rx="6"/>
    <text x="20" y="20" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="{text_secondary}" dominant-baseline="middle">
      Total Impact Score
    </text>
    <text x="{width-100}" y="20" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="700" fill="{accent}" text-anchor="end" dominant-baseline="middle">
      {metrics['impact_score']}
    </text>
  </g>
  
  <!-- Footer -->
  <text x="{width-20}" y="{height-10}" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="{text_secondary}" text-anchor="end">
    {metrics['repos']} repos • Last 365 days
  </text>
</svg>'''
        
        return svg


def main():
    """Main entry point."""
    github_token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_USERNAME') or os.getenv('GITHUB_ACTOR')
    output_file = os.getenv('OUTPUT_FILE', 'contributions-simple.svg')
    
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    if not username:
        print("Error: GITHUB_USERNAME or GITHUB_ACTOR environment variable not set")
        sys.exit(1)
    
    print(f"Generating simple contribution card for {username}...")
    
    visualizer = SimpleContributionVisualizer(github_token, username)
    metrics = visualizer.get_metrics(days=365)
    
    print(f"\n📊 Metrics:")
    print(f"  PRs Merged: {metrics['prs_merged']}")
    print(f"  PRs Opened: {metrics['prs_opened']}")
    print(f"  Reviews: {metrics['reviews']}")
    print(f"  Issues: {metrics['issues']}")
    print(f"  Impact Score: {metrics['impact_score']}")
    
    svg = visualizer.generate_card_svg(metrics)
    
    with open(output_file, 'w') as f:
        f.write(svg)
    
    print(f"\n✅ Generated {output_file}")
    print(f"📈 Shows real impact, not just commit frequency")


if __name__ == '__main__':
    main()
