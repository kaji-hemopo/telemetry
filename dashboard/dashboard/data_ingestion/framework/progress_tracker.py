#!/usr/bin/env python3
"""
Progress Tracking Display System
Tracks data ingestion progress and displays status
"""

import json
from datetime import datetime
from pathlib import Path

class ProgressTracker:
    """Tracks and displays data ingestion progress"""
    
    def __init__(self, display_dir="data_ingestion/display"):
        self.display_dir = Path(display_dir)
        self.display_dir.mkdir(exist_ok=True)
        self.status_file = self.display_dir / "ingestion_status.json"
        
    def update_status(self, stage: str, status: str, details: dict = None):
        """Update ingestion status"""
        current_status = self.get_current_status()
        
        stage_update = {
            "stage": stage,
            "status": status,
            "updated_at": datetime.now().isoformat(),
            "details": details or {}
        }
        
        # Add or update stage
        stage_found = False
        for i, existing_stage in enumerate(current_status["stages"]):
            if existing_stage["stage"] == stage:
                current_status["stages"][i] = stage_update
                stage_found = True
                break
        
        if not stage_found:
            current_status["stages"].append(stage_update)
        
        # Update overall status
        current_status["last_updated"] = datetime.now().isoformat()
        current_status["overall_status"] = self._calculate_overall_status(current_status["stages"])
        
        # Save status
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(current_status, f, indent=2)
        
        # Generate display HTML
        self._generate_display_html(current_status)
        
        return current_status
    
    def get_current_status(self):
        """Get current ingestion status"""
        if self.status_file.exists():
            with open(self.status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default status
        return {
            "project": "Airbnb Research Data Integration",
            "overall_status": "waiting",
            "last_updated": datetime.now().isoformat(),
            "stages": [
                {
                    "stage": "framework_setup",
                    "status": "completed",
                    "updated_at": datetime.now().isoformat(),
                    "details": {"message": "Data ingestion framework ready"}
                },
                {
                    "stage": "data_structure_specs",
                    "status": "waiting",
                    "updated_at": datetime.now().isoformat(),
                    "details": {"message": "Awaiting Felix's data structure specifications"}
                },
                {
                    "stage": "data_ingestion",
                    "status": "pending",
                    "updated_at": datetime.now().isoformat(),
                    "details": {"message": "Ready when specs received"}
                },
                {
                    "stage": "validation",
                    "status": "pending",
                    "updated_at": datetime.now().isoformat(),
                    "details": {"message": "Will validate against specs"}
                },
                {
                    "stage": "dashboard_integration",
                    "status": "pending",
                    "updated_at": datetime.now().isoformat(),
                    "details": {"message": "Will update dashboard with real data"}
                }
            ]
        }
    
    def _calculate_overall_status(self, stages):
        """Calculate overall status from stage statuses"""
        status_priority = {
            "failed": 4,
            "in_progress": 3,
            "completed": 2,
            "waiting": 1,
            "pending": 0
        }
        
        # Get highest priority status
        highest_priority = max(status_priority.get(stage["status"], 0) for stage in stages)
        
        # Map back to status name
        for status_name, priority in status_priority.items():
            if priority == highest_priority:
                return status_name
        
        return "unknown"
    
    def _generate_display_html(self, status_data):
        """Generate HTML display of progress"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airbnb Data Ingestion Progress</title>
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0f172a;
            color: #f1f5f9;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #1e293b;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #334155;
        }}
        
        .project-title {{
            font-size: 24px;
            font-weight: 600;
            color: #10b981;
            margin-bottom: 8px;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            margin-top: 10px;
        }}
        
        .status-waiting {{ background: #f59e0b22; color: #f59e0b; }}
        .status-completed {{ background: #10b98122; color: #10b981; }}
        .status-in_progress {{ background: #3b82f622; color: #3b82f6; }}
        .status-pending {{ background: #64748b22; color: #64748b; }}
        .status-failed {{ background: #ef444422; color: #ef4444; }}
        
        .stages-container {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        
        .stage-card {{
            background: #334155;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid;
            transition: all 0.2s;
        }}
        
        .stage-card:hover {{
            background: #475569;
            transform: translateX(4px);
        }}
        
        .stage-waiting {{ border-left-color: #f59e0b; }}
        .stage-completed {{ border-left-color: #10b981; }}
        .stage-in_progress {{ border-left-color: #3b82f6; }}
        .stage-pending {{ border-left-color: #64748b; }}
        .stage-failed {{ border-left-color: #ef4444; }}
        
        .stage-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        
        .stage-name {{
            font-weight: 600;
            font-size: 16px;
        }}
        
        .stage-status {{
            font-size: 14px;
            padding: 4px 10px;
            border-radius: 12px;
        }}
        
        .stage-details {{
            color: #94a3b8;
            font-size: 14px;
            margin-top: 8px;
        }}
        
        .timestamp {{
            text-align: center;
            color: #64748b;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #334155;
        }}
        
        .progress-bar {{
            height: 6px;
            background: #334155;
            border-radius: 3px;
            margin: 20px 0;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: #10b981;
            border-radius: 3px;
            transition: width 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="project-title">Airbnb Research Data Integration</div>
            <div class="status-badge status-{status_data['overall_status']}">
                {status_data['overall_status'].replace('_', ' ').title()}
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width: {self._calculate_progress_percentage(status_data['stages'])}%"></div>
        </div>
        
        <div class="stages-container">
"""
        
        for stage in status_data["stages"]:
            stage_class = f"stage-{stage['status']}"
            html_content += f"""
            <div class="stage-card {stage_class}">
                <div class="stage-header">
                    <div class="stage-name">{stage['stage'].replace('_', ' ').title()}</div>
                    <div class="stage-status status-{stage['status']}">
                        {stage['status'].replace('_', ' ').title()}
                    </div>
                </div>
                <div class="stage-details">
                    {stage['details'].get('message', 'No details available')}
                </div>
            </div>
"""
        
        html_content += f"""
        </div>
        
        <div class="timestamp">
            Last updated: {datetime.fromisoformat(status_data['last_updated']).strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => {{
            location.reload();
        }}, 30000);
    </script>
</body>
</html>
"""
        
        html_file = self.display_dir / "progress_display.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def _calculate_progress_percentage(self, stages):
        """Calculate progress percentage"""
        total_stages = len(stages)
        completed_stages = sum(1 for stage in stages if stage["status"] == "completed")
        
        if total_stages == 0:
            return 0
        
        # Weight stages differently
        stage_weights = {
            "framework_setup": 10,
            "data_structure_specs": 20,
            "data_ingestion": 30,
            "validation": 20,
            "dashboard_integration": 20
        }
        
        total_weight = sum(stage_weights.get(stage["stage"], 10) for stage in stages)
        completed_weight = 0
        
        for stage in stages:
            weight = stage_weights.get(stage["stage"], 10)
            if stage["status"] == "completed":
                completed_weight += weight
            elif stage["status"] == "in_progress":
                completed_weight += weight * 0.5  # Half credit for in-progress
        
        return int((completed_weight / total_weight) * 100)

# Test function
def test_tracker():
    """Test the progress tracker"""
    tracker = ProgressTracker()
    status = tracker.get_current_status()
    
    print("✅ Progress Tracker Ready")
    print(f"   Overall status: {status['overall_status']}")
    print(f"   Stages: {len(status['stages'])}")
    print(f"   Display HTML generated at: data_ingestion/display/progress_display.html")
    
    return tracker

if __name__ == "__main__":
    tracker = test_tracker()