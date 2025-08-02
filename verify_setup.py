#!/usr/bin/env python3
"""
Setup verification script for Options Strategy Analyzer
Verifies that all dependencies are properly installed and configured
"""

import sys
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    min_version = (3, 8)
    
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version[:2] >= min_version:
        print("   ✅ Python version is compatible")
        return True
    else:
        print(f"   ❌ Python {min_version[0]}.{min_version[1]}+ required")
        return False

def check_dependency(name, import_name=None):
    """Check if a dependency is installed"""
    if import_name is None:
        import_name = name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"   ✅ {name}: {version}")
        return True
    except ImportError:
        print(f"   ❌ {name}: Not installed")
        return False

def check_dependencies():
    """Check all required dependencies"""
    print("\n📦 Dependencies:")
    
    dependencies = [
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"), 
        ("scipy", "scipy"),
        ("pytest", "pytest"),
    ]
    
    all_good = True
    for name, import_name in dependencies:
        if not check_dependency(name, import_name):
            all_good = False
    
    return all_good

def check_project_structure():
    """Check project file structure"""
    print("\n📁 Project Structure:")
    
    required_files = [
        "option_strategy_analyzer.py",
        "pyproject.toml",
        "tests/__init__.py",
        "tests/test_option_strategy_analyzer.py",
        "tests/test_delta_calculator.py",
    ]
    
    all_good = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}: Missing")
            all_good = False
    
    return all_good

def check_uv_installation():
    """Check if uv is installed"""
    print("\n⚡ UV Package Manager:")
    
    try:
        result = subprocess.run(['uv', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ uv: {version}")
            return True
        else:
            print("   ❌ uv: Command failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("   ❌ uv: Not installed")
        print("   💡 Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False

def test_imports():
    """Test that core modules can be imported"""
    print("\n🧪 Module Import Tests:")
    
    try:
        # Test main analyzer
        from option_strategy_analyzer import StrategyFactory
        factory = StrategyFactory()
        strategies = factory.list_strategies()
        print(f"   ✅ option_strategy_analyzer: {len(strategies)} strategies loaded")
        
        # Test delta calculator
        from delta_calculator import OptionCalculator  
        calculator = OptionCalculator()
        print("   ✅ delta_calculator: Successfully imported")
        
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic strategy analysis functionality"""
    print("\n🎯 Functionality Tests:")
    
    try:
        from option_strategy_analyzer import StrategyFactory
        
        # Test strategy creation
        factory = StrategyFactory()
        strategy = factory.create_strategy("SP7")
        
        if strategy:
            print("   ✅ Strategy creation: SP7 created successfully")
            
            # Test payoff calculation
            import numpy as np
            stock_prices = np.array([95, 100, 105])
            payoffs = strategy.calculate_payoff(stock_prices)
            
            if len(payoffs) == 3:
                print("   ✅ Payoff calculation: Working correctly")
                return True
            else:
                print("   ❌ Payoff calculation: Unexpected results")
                return False
        else:
            print("   ❌ Strategy creation: Failed to create SP7")
            return False
            
    except Exception as e:
        print(f"   ❌ Functionality test error: {e}")
        return False

def run_quick_test():
    """Run a quick test of the CLI"""
    print("\n🚀 CLI Test:")
    
    try:
        result = subprocess.run([
            sys.executable, 'option_strategy_analyzer.py', '--info', 'SP7'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "SP7" in result.stdout:
            print("   ✅ CLI: Working correctly")
            return True
        else:
            print("   ❌ CLI: Failed to get strategy info")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ CLI test error: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🔍 Options Strategy Analyzer - Setup Verification")
    print("=" * 55)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("UV Installation", check_uv_installation),
        ("Module Imports", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("CLI Interface", run_quick_test),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ {name}: Exception - {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 55)
    print("📋 Verification Summary:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {name}")
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Setup verification completed successfully!")
        print("   You're ready to analyze options strategies!")
        print("\n🚀 Try: python3 option_strategy_analyzer.py SP7")
        return True
    else:
        print(f"\n⚠️  {total - passed} issues found. Please fix them before proceeding.")
        print("\n💡 Setup help:")
        print("   1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")  
        print("   2. Install deps: uv sync")
        print("   3. Re-run verification: python3 verify_setup.py")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 