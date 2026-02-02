"""
Analytics Module - Application Statistics for CV Crafter V2

Provides functions to calculate and aggregate application statistics
for the Stats Header dashboard.
"""

from typing import Dict
from collections import Counter

# Import the data loading function - handle both direct and package imports
try:
    from data_manager import load_applications
except ImportError:
    from .data_manager import load_applications


def get_application_stats() -> Dict[str, int]:
    """
    Calculate aggregate statistics for all applications.
    
    Returns:
        Dictionary with status counts and totals:
        {
            "total": int,
            "draft": int,
            "created": int,
            "applied": int,
            "interviewing": int,
            "rejected": int,
            "offer": int,
            "accepted": int,
            "withdrawn": int
        }
    """
    applications = load_applications()
    
    # Count by status
    status_counts = Counter(app.get("status", "unknown") for app in applications)
    
    # Define all possible statuses with defaults
    all_statuses = [
        "draft", "created", "applied", "interviewing", 
        "rejected", "offer", "accepted", "withdrawn"
    ]
    
    stats = {"total": len(applications)}
    
    for status in all_statuses:
        stats[status] = status_counts.get(status, 0)
    
    return stats


def get_active_applications_count() -> int:
    """
    Get count of 'active' applications (not rejected/withdrawn/accepted).
    
    Returns:
        Number of applications still in progress
    """
    stats = get_application_stats()
    inactive = stats.get("rejected", 0) + stats.get("withdrawn", 0) + stats.get("accepted", 0)
    return stats["total"] - inactive


def get_success_rate() -> float:
    """
    Calculate the success rate (offers / total applied).
    
    Returns:
        Success rate as a percentage (0-100), or 0 if no applications
    """
    stats = get_application_stats()
    
    # Only count apps that have actually been applied
    applied_states = ["applied", "interviewing", "rejected", "offer", "accepted"]
    total_applied = sum(stats.get(s, 0) for s in applied_states)
    
    if total_applied == 0:
        return 0.0
    
    offers = stats.get("offer", 0) + stats.get("accepted", 0)
    return round((offers / total_applied) * 100, 1)


def get_interview_rate() -> float:
    """
    Calculate the interview rate (interviews / applied).
    
    Returns:
        Interview rate as a percentage (0-100)
    """
    stats = get_application_stats()
    
    applied_onwards = ["applied", "interviewing", "rejected", "offer", "accepted"]
    total_applied = sum(stats.get(s, 0) for s in applied_onwards)
    
    if total_applied == 0:
        return 0.0
    
    # Interviewing includes current + past interviews that led to offer/reject
    interview_or_beyond = stats.get("interviewing", 0) + stats.get("offer", 0) + stats.get("accepted", 0)
    # Note: rejected could be pre or post interview, so we're conservative
    
    return round((interview_or_beyond / total_applied) * 100, 1)


def get_stats_summary() -> Dict:
    """
    Get a comprehensive stats summary for the dashboard header.
    
    Returns:
        Dictionary with all relevant stats for display
    """
    stats = get_application_stats()
    
    return {
        "total": stats["total"],
        "active": get_active_applications_count(),
        "applied": stats.get("applied", 0),
        "interviewing": stats.get("interviewing", 0),
        "offers": stats.get("offer", 0) + stats.get("accepted", 0),
        "rejected": stats.get("rejected", 0),
        "success_rate": get_success_rate(),
        "interview_rate": get_interview_rate(),
    }
