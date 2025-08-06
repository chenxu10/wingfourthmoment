#!/usr/bin/env python3
"""
Generate all 84 strategy plots and compile them into one comprehensive markdown file
"""

import os
import sys
from pathlib import Path
import time

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from option_analyzer.factory import StrategyFactory
from option_analyzer.visualization import VisualizationEngine


def generate_all_plots(output_dir="strategy_plot", base_price=100.0):
    """Generate plots for all 84 strategies"""
    print("🚀 Generating all 84 Options Strategy plots...")
    print("=" * 60)
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    factory = StrategyFactory()
    strategies = factory.list_strategies()
    
    print(f"📊 Total strategies to generate: {len(strategies)}")
    print()
    
    successful_plots = []
    failed_plots = []
    
    for i, code in enumerate(strategies, 1):
        try:
            print(f"[{i:2d}/{len(strategies)}] Generating {code}...", end=" ")
            
            # Create strategy
            strategy = factory.create_strategy(code, base_price)
            if not strategy:
                print("❌ Failed to create strategy")
                failed_plots.append(code)
                continue
            
            # Generate visualization
            viz = VisualizationEngine(strategy, output_dir)
            viz.generate_full_analysis()
            
            successful_plots.append(code)
            print("✅ Done")
            
            # Small delay to prevent overwhelming the system
            time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            failed_plots.append(code)
    
    print()
    print("=" * 60)
    print(f"✅ Successfully generated: {len(successful_plots)} plots")
    if failed_plots:
        print(f"❌ Failed to generate: {len(failed_plots)} plots")
        print(f"Failed strategies: {', '.join(failed_plots)}")
    print()
    
    return successful_plots, failed_plots


def create_comprehensive_markdown(successful_plots, output_dir="strategy_plot"):
    """Create a comprehensive markdown file with all strategy plots"""
    print("📝 Creating comprehensive markdown file...")
    
    factory = StrategyFactory()
    
    # Read the Bagua analysis for strategy details
    bagua_file = Path("strategy_bagua_analysis.md")
    bagua_content = ""
    if bagua_file.exists():
        with open(bagua_file, 'r', encoding='utf-8') as f:
            bagua_content = f.read()
    
    markdown_content = []
    
    # Header
    markdown_content.extend([
        "# Complete Options Strategy Analysis - All 84 Strategies",
        "",
        "This comprehensive document contains visual analysis for all 84 options strategies from the Options Strategy Bagua Analysis.",
        "",
        f"**Generated on:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total Strategies:** {len(successful_plots)}",
        f"**Base Stock Price:** $100.00",
        "",
        "## Table of Contents",
        "",
    ])
    
    # Create table of contents
    categories = {
        "Long Call Strategies (C1-C15)": [f"C{i}" for i in range(1, 16)],
        "Long Put Strategies (P1-P15)": [f"P{i}" for i in range(1, 16)],
        "Short Call Strategies (SC1-SC15)": [f"SC{i}" for i in range(1, 16)],
        "Short Put Strategies (SP1-SP15)": [f"SP{i}" for i in range(1, 16)],
        "Spread Strategies (S1-S24)": [f"S{i}" for i in range(1, 25)]
    }
    
    for category, codes in categories.items():
        markdown_content.append(f"- [{category}](#{category.lower().replace(' ', '-').replace('(', '').replace(')', '')})")
        for code in codes:
            if code in successful_plots:
                strategy_info = factory.get_strategy_info(code)
                markdown_content.append(f"  - [{code}: {strategy_info.name}](#{code.lower()})")
    
    markdown_content.extend([
        "",
        "---",
        "",
    ])
    
    # Generate content for each category
    for category, codes in categories.items():
        markdown_content.extend([
            f"## {category}",
            "",
        ])
        
        for code in codes:
            if code not in successful_plots:
                continue
                
            strategy_info = factory.get_strategy_info(code)
            plot_file = f"{code}_analysis.png"
            plot_path = Path(output_dir) / plot_file
            
            markdown_content.extend([
                f"### {code}",
                "",
                f"**Strategy:** {strategy_info.name}",
                f"**Type:** {strategy_info.strategy_type.title()}",
                f"**Moneyness:** {strategy_info.moneyness}",
                f"**Time Frame:** {strategy_info.time_frame}",
                f"**Description:** {strategy_info.description}",
                "",
            ])
            
            # Add Bagua analysis details if available
            if bagua_content and code in bagua_content:
                # Try to extract the row for this strategy from the Bagua table
                lines = bagua_content.split('\n')
                for line in lines:
                    if line.startswith(f"| {code} "):
                        # Parse the table row
                        parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last
                        if len(parts) >= 12:
                            markdown_content.extend([
                                "**Bagua Analysis:**",
                                f"- **Risk Level:** {parts[4]}",
                                f"- **Max Profit Potential:** {parts[5]}",
                                f"- **Leverage:** {parts[6]}",
                                f"- **Risk/Reward Rating:** {parts[7]}",
                                f"- **Breakeven:** {parts[8]}",
                                f"- **Suitable Markets:** {parts[9]}",
                                f"- **Unsuitable Markets:** {parts[10]}",
                                f"- **Key Characteristics:** {parts[11]}",
                                "",
                            ])
                        break
            
            # Add the plot image
            if plot_path.exists():
                markdown_content.extend([
                    "**Analysis Chart:**",
                    "",
                    f"![{code} Analysis]({output_dir}/{plot_file})",
                    "",
                ])
            else:
                markdown_content.extend([
                    "**Analysis Chart:** *Plot not available*",
                    "",
                ])
            
            markdown_content.extend([
                "---",
                "",
            ])
    
    # Footer
    markdown_content.extend([
        "## About This Analysis",
        "",
        "This comprehensive analysis was generated using the Options Strategy Analyzer framework, which implements:",
        "",
        "- **Black-Scholes Pricing Model** for accurate option valuations",
        "- **Greeks Calculations** (Delta, Theta, Vega, Gamma) for risk analysis",
        "- **4-Panel Visualization** showing:",
        "  - Expiration payoff diagrams",
        "  - Time decay analysis over multiple timeframes",
        "  - Volatility impact analysis",
        "  - Strategy summary with key metrics",
        "",
        "All strategies are based on the comprehensive **Options Strategy Bagua Analysis** which categorizes 84 different option strategies across:",
        "- 5 moneyness levels (Deep OTM, Shallow OTM, ATM, Shallow ITM, Deep ITM)",
        "- 3 time frames (Near 0-30 days, Medium 30-90 days, Long 90+ days)",
        "- Multiple strategy types (Long/Short Calls/Puts, Complex Spreads)",
        "",
        f"**Generated with:** Options Strategy Analyzer v1.0",
        f"**Generation Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Base Parameters:** Stock Price = $100.00, Risk-free rate = 5%, Volatility = 20%",
    ])
    
    # Write the markdown file
    output_file = "complete_strategy_analysis.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_content))
    
    print(f"✅ Comprehensive markdown file created: {output_file}")
    print(f"📄 Total lines: {len(markdown_content)}")
    
    return output_file


def main():
    """Main function to generate all plots and markdown"""
    print("🎯 Options Strategy Complete Analysis Generator")
    print("=" * 60)
    
    # Generate all plots
    successful_plots, failed_plots = generate_all_plots()
    
    if not successful_plots:
        print("❌ No plots were generated successfully. Exiting.")
        return
    
    # Create comprehensive markdown
    markdown_file = create_comprehensive_markdown(successful_plots)
    
    print()
    print("🎉 Analysis Complete!")
    print("=" * 60)
    print(f"📊 Generated {len(successful_plots)} strategy plots in 'strategy_plot/' directory")
    print(f"📝 Created comprehensive markdown: {markdown_file}")
    
    if failed_plots:
        print(f"⚠️  {len(failed_plots)} strategies failed to generate")
    
    print()
    print("Next steps:")
    print(f"1. Review plots in the 'strategy_plot/' directory")
    print(f"2. Open '{markdown_file}' to view the complete analysis")
    print("3. Use individual plots for presentations or reports")


if __name__ == "__main__":
    main() 