# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jekyll-based GitHub Pages site for the SNF/AUS research project "Anomaly and Fraud Detection in Blockchain Networks". Content is scraped from the Wix-hosted site at digital-finance-msca.com/blockchain.

**Repository:** Digital-AI-Finance/Anomaly_and_Fraud_Detection_in_Blockchain_Networks (private)

## Commands

### Local Development
```bash
# Install Ruby dependencies
bundle install

# Run local Jekyll server (preview at http://localhost:4000)
bundle exec jekyll serve

# Build static site
bundle exec jekyll build
```

### Content Scraping
```bash
# Install Python dependencies
pip install playwright requests
playwright install chromium

# Re-scrape content from source Wix site
python scrape_wix_site.py
```

## Architecture

This is a static Jekyll site with two main components:

1. **Jekyll Site** (`_config.yml`, `_layouts/`, `index.html`, `assets/`)
   - Single-page landing site with sections: Hero, About, Team, Output, Publications, Funding, Contact
   - Custom CSS in `assets/css/style.css` (no Sass preprocessing)
   - Team photos and logos in `assets/images/`
   - Uses `jekyll-remote-theme` with minimal theme, but mostly custom styling

2. **Scraper Utility** (`scrape_wix_site.py`)
   - Playwright-based scraper for JavaScript-rendered Wix content
   - Outputs to `scraped_content.json` and downloads images to `assets/images/`
   - Run when source content at digital-finance-msca.com/blockchain changes

## GitHub Pages Status

Currently private repository. GitHub Pages requires:
- Public repository on free plan, OR
- GitHub Team/Enterprise plan for private repo Pages

The `baseurl` in `_config.yml` is set for GitHub Pages deployment path.
