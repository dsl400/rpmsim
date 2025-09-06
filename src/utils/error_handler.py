"""
Error Handling Framework for ECU Diagnostic Tool
Provides centralized error handling, logging, and user notification
"""

import time
import lvgl as lv

class ErrorHandler:
    """Centralized error handling and logging system"""
    
    def __init__(self):
        self.error_log = []
        self.max_log_size = 100
        self.severity_levels = {
            "INFO": 0,
            "WARNING": 1,
            "ERROR": 2,
            "CRITICAL": 3
        }
    
    def handle_error(self, error, context="", severity="ERROR"):
        """
        Handle and log errors with appropriate user feedback
        
        Args:
            error (Exception or str): Error object or message
            context (str): Additional context information
            severity (str): Error severity level (INFO, WARNING, ERROR, CRITICAL)
        """
        error_entry = {
            "timestamp": time.time(),
            "error": str(error),
            "context": context,
            "severity": severity,
            "severity_level": self.severity_levels.get(severity, 2)
        }
        
        # Add to log
        self.error_log.append(error_entry)
        if len(self.error_log) > self.max_log_size:
            self.error_log.pop(0)
        
        # Print to console for debugging
        print(f"[{severity}] {context}: {error}")
        
        # Show user notification for ERROR and CRITICAL levels
        if severity in ["ERROR", "CRITICAL"]:
            self.show_error_dialog(error, context, severity)
    
    def show_error_dialog(self, error, context, severity):
        """
        Show error dialog to user
        
        Args:
            error (Exception or str): Error object or message
            context (str): Additional context
            severity (str): Error severity level
        """
        try:
            # Get current active screen
            current_screen = lv.screen_active()
            if not current_screen:
                return
            
            # Create modal dialog with LVGL 9.x API
            title_text = "Critical Error" if severity == "CRITICAL" else "Error"

            # Set message text
            if context:
                message = f"{context}\n\nError: {str(error)}"
            else:
                message = f"Error: {str(error)}"

            dialog = lv.msgbox(current_screen, title_text, message, ["OK"], False)
            dialog.center()
            
        except Exception as e:
            # Fallback - just print if UI creation fails
            print(f"Failed to show error dialog: {e}")
    
    def show_warning_dialog(self, message, title="Warning"):
        """
        Show warning dialog to user
        
        Args:
            message (str): Warning message
            title (str): Dialog title
        """
        try:
            current_screen = lv.screen_active()
            if not current_screen:
                return
            
            dialog = lv.msgbox(current_screen, title, message, ["OK"], False)
            dialog.center()
            
        except Exception as e:
            print(f"Failed to show warning dialog: {e}")
    
    def show_info_dialog(self, message, title="Information"):
        """
        Show information dialog to user
        
        Args:
            message (str): Information message
            title (str): Dialog title
        """
        try:
            current_screen = lv.screen_active()
            if not current_screen:
                return
            
            dialog = lv.msgbox(current_screen, title, message, ["OK"], False)
            dialog.center()
            
        except Exception as e:
            print(f"Failed to show info dialog: {e}")
    
    def get_error_log(self, severity_filter=None, limit=None):
        """
        Get error log entries
        
        Args:
            severity_filter (str): Filter by severity level
            limit (int): Maximum number of entries to return
            
        Returns:
            list: List of error log entries
        """
        filtered_log = self.error_log
        
        if severity_filter:
            min_level = self.severity_levels.get(severity_filter, 0)
            filtered_log = [
                entry for entry in filtered_log 
                if entry["severity_level"] >= min_level
            ]
        
        if limit:
            filtered_log = filtered_log[-limit:]
        
        return filtered_log
    
    def clear_log(self):
        """Clear the error log"""
        self.error_log.clear()
    
    def get_log_summary(self):
        """
        Get summary of error log
        
        Returns:
            dict: Summary with counts by severity level
        """
        summary = {
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0,
            "total": len(self.error_log)
        }
        
        for entry in self.error_log:
            severity = entry.get("severity", "ERROR")
            if severity in summary:
                summary[severity] += 1
        
        return summary

def handle_errors(func):
    """
    Decorator for automatic error handling
    
    Args:
        func: Function to wrap with error handling
        
    Returns:
        Wrapped function with error handling
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.handle_error(e, f"Function: {func.__name__}")
            return None
    return wrapper

# Global error handler instance
error_handler = ErrorHandler()
