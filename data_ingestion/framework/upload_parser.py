#!/usr/bin/env python3
"""
Data Upload & Parsing System for Felix's Research Data
Prepares dashboard for integration with standardized data formats
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

class DataIngestionFramework:
    """Framework for parsing and validating research data"""
    
    def __init__(self, data_dir="data_ingestion/uploaded_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.progress_file = self.data_dir / "ingestion_progress.json"
        
    def parse_uploaded_file(self, file_path, expected_format="felix_research"):
        """Parse uploaded JSON file with validation"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Basic validation
            if not isinstance(data, dict):
                raise ValueError("Data must be a JSON object")
            
            # Format-specific validation
            if expected_format == "felix_research":
                validated_data = self._validate_felix_format(data)
            else:
                validated_data = data  # Accept any valid JSON for now
            
            # Save parsed data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.data_dir / f"parsed_{timestamp}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(validated_data, f, indent=2)
            
            # Update progress
            self._update_progress({
                "file": str(file_path),
                "timestamp": timestamp,
                "format": expected_format,
                "status": "parsed",
                "output_file": str(output_file)
            })
            
            return validated_data
            
        except Exception as e:
            self._update_progress({
                "file": str(file_path),
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "status": "failed"
            })
            raise
    
    def _validate_felix_format(self, data):
        """Validate expected Felix research data format"""
        validated = {"metadata": {}, "areas": [], "costs": [], "timeline": []}
        
        # Check for expected sections
        if "areas" in data:
            validated["areas"] = self._validate_areas(data["areas"])
        
        if "cost_breakdown" in data:
            validated["costs"] = self._validate_costs(data["cost_breakdown"])
        
        if "timeline" in data:
            validated["timeline"] = self._validate_timeline(data["timeline"])
        
        # Add metadata
        validated["metadata"] = {
            "source": data.get("source", "felix_research"),
            "version": data.get("version", "1.0"),
            "generated_at": data.get("generated_at", datetime.now().isoformat()),
            "parsed_at": datetime.now().isoformat()
        }
        
        return validated
    
    def _validate_areas(self, areas_data):
        """Validate area comparison data"""
        validated_areas = []
        if isinstance(areas_data, list):
            for area in areas_data:
                if isinstance(area, dict):
                    validated_areas.append({
                        "name": area.get("name", "Unknown"),
                        "region": area.get("region", ""),
                        "property_count": area.get("property_count", 0),
                        "avg_price": area.get("avg_price", 0),
                        "competition_score": area.get("competition_score", 0),
                        "regulation_score": area.get("regulation_score", 0),
                        "notes": area.get("notes", "")
                    })
        return validated_areas
    
    def _validate_costs(self, costs_data):
        """Validate cost breakdown data"""
        validated_costs = []
        if isinstance(costs_data, list):
            for cost in costs_data:
                if isinstance(cost, dict):
                    validated_costs.append({
                        "category": cost.get("category", ""),
                        "item": cost.get("item", ""),
                        "estimated_cost": cost.get("estimated_cost", 0),
                        "frequency": cost.get("frequency", "one_time"),
                        "notes": cost.get("notes", "")
                    })
        return validated_costs
    
    def _validate_timeline(self, timeline_data):
        """Validate timeline data"""
        validated_timeline = []
        if isinstance(timeline_data, list):
            for event in timeline_data:
                if isinstance(event, dict):
                    validated_timeline.append({
                        "phase": event.get("phase", ""),
                        "task": event.get("task", ""),
                        "estimated_days": event.get("estimated_days", 0),
                        "dependencies": event.get("dependencies", []),
                        "status": event.get("status", "pending")
                    })
        return validated_timeline
    
    def _update_progress(self, update_data):
        """Update ingestion progress tracking"""
        progress = {"ingestions": [], "last_updated": datetime.now().isoformat()}
        
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                progress = json.load(f)
        
        progress["ingestions"].append(update_data)
        
        # Keep only last 20 ingestions
        if len(progress["ingestions"]) > 20:
            progress["ingestions"] = progress["ingestions"][-20:]
        
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2)
    
    def get_progress(self):
        """Get current ingestion progress"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"ingestions": [], "last_updated": datetime.now().isoformat()}

# Test function
def test_framework():
    """Test the data ingestion framework"""
    framework = DataIngestionFramework()
    
    # Create sample data directory for testing
    sample_dir = Path("data_ingestion/sample_data")
    sample_dir.mkdir(exist_ok=True)
    
    print("✅ Data Ingestion Framework Ready")
    print(f"   Data directory: {framework.data_dir}")
    print(f"   Progress file: {framework.progress_file}")
    print("   Waiting for Felix's data structure specs...")
    
    return framework

if __name__ == "__main__":
    framework = test_framework()