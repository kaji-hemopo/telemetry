#!/usr/bin/env python3
"""
Data Validation Module for Felix's Research Data
Validates data structure, completeness, and consistency
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataValidator:
    """Validates research data against expected formats"""
    
    def __init__(self):
        self.validation_rules = self._load_validation_rules()
        self.validation_results = []
    
    def _load_validation_rules(self):
        """Load validation rules for different data types"""
        return {
            "area_comparison": {
                "required_fields": ["name", "region", "property_count", "avg_price"],
                "field_types": {
                    "name": str,
                    "region": str,
                    "property_count": int,
                    "avg_price": (int, float),
                    "competition_score": (int, float),
                    "regulation_score": (int, float),
                    "notes": str
                },
                "constraints": {
                    "property_count": lambda x: x >= 0,
                    "avg_price": lambda x: x >= 0,
                    "competition_score": lambda x: 0 <= x <= 10,
                    "regulation_score": lambda x: 0 <= x <= 10
                }
            },
            "cost_breakdown": {
                "required_fields": ["category", "item", "estimated_cost"],
                "field_types": {
                    "category": str,
                    "item": str,
                    "estimated_cost": (int, float),
                    "frequency": str,
                    "notes": str
                },
                "constraints": {
                    "estimated_cost": lambda x: x >= 0,
                    "frequency": lambda x: x in ["one_time", "monthly", "annual", "per_guest"]
                }
            },
            "timeline": {
                "required_fields": ["phase", "task", "estimated_days"],
                "field_types": {
                    "phase": str,
                    "task": str,
                    "estimated_days": int,
                    "dependencies": list,
                    "status": str
                },
                "constraints": {
                    "estimated_days": lambda x: x >= 0,
                    "status": lambda x: x in ["pending", "in_progress", "completed", "blocked"]
                }
            }
        }
    
    def validate_data(self, data: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """Validate data against rules for specific type"""
        results = {
            "data_type": data_type,
            "timestamp": datetime.now().isoformat(),
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "stats": {}
        }
        
        if data_type not in self.validation_rules:
            results["errors"].append(f"Unknown data type: {data_type}")
            results["is_valid"] = False
            return results
        
        rules = self.validation_rules[data_type]
        
        # Check required fields
        for field in rules["required_fields"]:
            if field not in data:
                results["errors"].append(f"Missing required field: {field}")
                results["is_valid"] = False
        
        # Check field types
        for field, expected_type in rules["field_types"].items():
            if field in data:
                value = data[field]
                if not isinstance(value, expected_type):
                    if not (isinstance(expected_type, tuple) and isinstance(value, expected_type)):
                        results["errors"].append(
                            f"Field '{field}' has wrong type. "
                            f"Expected {expected_type}, got {type(value)}"
                        )
                        results["is_valid"] = False
        
        # Check constraints
        for field, constraint_func in rules["constraints"].items():
            if field in data:
                value = data[field]
                if not constraint_func(value):
                    results["errors"].append(
                        f"Field '{field}' violates constraint: {value}"
                    )
                    results["is_valid"] = False
        
        # Generate statistics
        results["stats"] = self._generate_stats(data, data_type)
        
        # Store validation result
        self.validation_results.append(results)
        
        return results
    
    def _generate_stats(self, data: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """Generate statistics about the data"""
        stats = {}
        
        if data_type == "area_comparison":
            if "avg_price" in data:
                stats["avg_price"] = data["avg_price"]
            if "property_count" in data:
                stats["property_count"] = data["property_count"]
        
        elif data_type == "cost_breakdown":
            if "estimated_cost" in data:
                stats["estimated_cost"] = data["estimated_cost"]
            if "frequency" in data:
                stats["frequency"] = data["frequency"]
        
        elif data_type == "timeline":
            if "estimated_days" in data:
                stats["estimated_days"] = data["estimated_days"]
            if "status" in data:
                stats["status"] = data["status"]
        
        return stats
    
    def validate_dataset(self, dataset: List[Dict[str, Any]], data_type: str) -> Dict[str, Any]:
        """Validate a list of data items"""
        results = {
            "data_type": data_type,
            "timestamp": datetime.now().isoformat(),
            "total_items": len(dataset),
            "valid_items": 0,
            "invalid_items": 0,
            "item_results": [],
            "summary": {}
        }
        
        for i, item in enumerate(dataset):
            item_result = self.validate_data(item, data_type)
            results["item_results"].append(item_result)
            
            if item_result["is_valid"]:
                results["valid_items"] += 1
            else:
                results["invalid_items"] += 1
        
        # Generate summary
        results["summary"] = {
            "validity_rate": results["valid_items"] / max(results["total_items"], 1),
            "total_errors": sum(len(r["errors"]) for r in results["item_results"]),
            "total_warnings": sum(len(r["warnings"]) for r in results["item_results"])
        }
        
        return results
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of all validations performed"""
        total_validations = len(self.validation_results)
        successful = sum(1 for r in self.validation_results if r["is_valid"])
        
        return {
            "total_validations": total_validations,
            "successful_validations": successful,
            "success_rate": successful / max(total_validations, 1),
            "last_validation": self.validation_results[-1] if self.validation_results else None
        }

# Test function
def test_validator():
    """Test the data validator"""
    validator = DataValidator()
    
    # Test with sample area data
    sample_area = {
        "name": "Shonan",
        "region": "Kanagawa",
        "property_count": 15,
        "avg_price": 85000000,
        "competition_score": 7.5,
        "regulation_score": 6.0,
        "notes": "Beach area, high seasonal demand"
    }
    
    result = validator.validate_data(sample_area, "area_comparison")
    
    print("✅ Data Validator Ready")
    print(f"   Validation result: {'VALID' if result['is_valid'] else 'INVALID'}")
    print(f"   Errors: {len(result['errors'])}")
    print(f"   Warnings: {len(result['warnings'])}")
    
    return validator

if __name__ == "__main__":
    validator = test_validator()