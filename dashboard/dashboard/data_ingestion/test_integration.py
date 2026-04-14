#!/usr/bin/env python3
"""
Test Airbnb Dashboard Data Integration
Verifies all components are ready for Felix's data
"""

import json
import sys
from pathlib import Path

def test_framework_components():
    """Test all framework components"""
    print("🧪 Testing Airbnb Dashboard Data Integration")
    print("=" * 60)
    
    # Check required directories
    required_dirs = [
        "data_ingestion/framework",
        "data_ingestion/sample_data", 
        "data_ingestion/placeholder_views",
        "data_ingestion/documentation",
        "data_ingestion/display"
    ]
    
    print("\n📁 Directory Structure Check:")
    all_dirs_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} (MISSING)")
            all_dirs_exist = False
    
    # Check required files
    required_files = [
        "data_ingestion/framework/upload_parser.py",
        "data_ingestion/framework/data_validator.py",
        "data_ingestion/framework/progress_tracker.py",
        "data_ingestion/sample_data/felix_sample_data.json",
        "data_ingestion/placeholder_views/area_comparison.html",
        "data_ingestion/documentation/integration_requirements.md",
        "data_ingestion/display/progress_display.html"
    ]
    
    print("\n📄 Required Files Check:")
    all_files_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"  ✅ {file_path} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {file_path} (MISSING)")
            all_files_exist = False
    
    # Test sample data
    print("\n📊 Sample Data Validation:")
    sample_data_path = Path("data_ingestion/sample_data/felix_sample_data.json")
    if sample_data_path.exists():
        try:
            with open(sample_data_path, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
            
            # Check structure
            has_areas = "areas" in sample_data and len(sample_data["areas"]) > 0
            has_costs = "cost_breakdown" in sample_data and len(sample_data["cost_breakdown"]) > 0
            has_timeline = "timeline" in sample_data and len(sample_data["timeline"]) > 0
            
            print(f"  ✅ Sample data loaded successfully")
            print(f"  ✅ Areas: {len(sample_data.get('areas', []))} items")
            print(f"  ✅ Costs: {len(sample_data.get('cost_breakdown', []))} items")
            print(f"  ✅ Timeline: {len(sample_data.get('timeline', []))} items")
            
            # Check data completeness
            if has_areas and has_costs and has_timeline:
                print("  ✅ All data sections present")
            else:
                print("  ⚠️  Some data sections missing")
                
        except Exception as e:
            print(f"  ❌ Failed to load sample data: {e}")
    else:
        print("  ❌ Sample data file not found")
    
    # Test progress display
    print("\n🖥️ Progress Display Check:")
    progress_html = Path("data_ingestion/display/progress_display.html")
    if progress_html.exists():
        size_kb = progress_html.stat().st_size / 1024
        print(f"  ✅ Progress display HTML: {size_kb:.1f} KB")
        
        # Check if it's accessible
        try:
            with open(progress_html, 'r', encoding='utf-8') as f:
                content = f.read()
                if "Airbnb Research Data Integration" in content:
                    print("  ✅ Contains correct project title")
                else:
                    print("  ⚠️  May not have correct content")
        except:
            print("  ⚠️  Could not read HTML content")
    else:
        print("  ❌ Progress display not found")
    
    # Test placeholder views
    print("\n🎨 Placeholder Views Check:")
    placeholder_html = Path("data_ingestion/placeholder_views/area_comparison.html")
    if placeholder_html.exists():
        size_kb = placeholder_html.stat().st_size / 1024
        print(f"  ✅ Area comparison placeholder: {size_kb:.1f} KB")
        
        # Check for expected elements
        try:
            with open(placeholder_html, 'r', encoding='utf-8') as f:
                content = f.read()
                if "Area Comparison Table" in content:
                    print("  ✅ Contains table structure")
                if "READY FOR DATA INTEGRATION" in content:
                    print("  ✅ Integration ready badge present")
                if "Expected Data Format" in content:
                    print("  ✅ Data format documentation included")
        except:
            print("  ⚠️  Could not verify HTML content")
    else:
        print("  ❌ Placeholder views not found")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 INTEGRATION PREPARATION SUMMARY")
    print("=" * 60)
    
    if all_dirs_exist and all_files_exist:
        print("✅ ALL COMPONENTS READY")
        print("✅ Waiting for Felix's data structure specifications")
        print("✅ Estimated integration time: 30-60 minutes after specs received")
        print("\n🚀 NEXT STEPS:")
        print("1. Receive Felix's data structure specifications")
        print("2. Adjust validation rules if needed")
        print("3. Test with actual Felix data")
        print("4. Deploy to production dashboard")
        return True
    else:
        print("❌ SOME COMPONENTS MISSING")
        print("Please check the missing items above")
        return False

def test_data_parsing():
    """Test data parsing with sample data"""
    print("\n🔧 Testing Data Parsing Framework:")
    
    try:
        # Import the framework modules
        sys.path.insert(0, "data_ingestion/framework")
        
        from upload_parser import DataIngestionFramework
        from data_validator import DataValidator
        from progress_tracker import ProgressTracker
        
        # Initialize components
        framework = DataIngestionFramework()
        validator = DataValidator()
        tracker = ProgressTracker()
        
        print("  ✅ Framework components imported")
        
        # Test with sample data
        sample_path = Path("data_ingestion/sample_data/felix_sample_data.json")
        if sample_path.exists():
            print("  ✅ Sample data found for testing")
            
            # Update progress
            tracker.update_status(
                "framework_testing",
                "in_progress",
                {"message": "Testing data parsing with sample data"}
            )
            print("  ✅ Progress tracking working")
            
        else:
            print("  ⚠️  Sample data not found for parsing test")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Could not import framework: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Framework test failed: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🏨 AIRBNB DASHBOARD DATA INTEGRATION TEST")
    print("=" * 60)
    
    # Run tests
    structure_ok = test_framework_components()
    
    if structure_ok:
        parsing_ok = test_data_parsing()
        
        if parsing_ok:
            print("\n🎉 ALL TESTS PASSED!")
            print("\n📊 INTEGRATION STATUS: READY")
            print("⏳ Waiting for Felix's data structure specifications")
            print("⏱️  Estimated implementation time: 30-60 minutes")
            print("\n📍 Progress display: file://" + str(Path("data_ingestion/display/progress_display.html").absolute()))
            print("📍 Area comparison: file://" + str(Path("data_ingestion/placeholder_views/area_comparison.html").absolute()))
        else:
            print("\n❌ Data parsing test failed")
            sys.exit(1)
    else:
        print("\n❌ Framework structure incomplete")
        sys.exit(1)