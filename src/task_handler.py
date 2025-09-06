"""
Task Handler for ECU Diagnostic Tool
Manages LVGL task handling and periodic updates
"""

import utime as time

class TaskHandler:
    """Handles periodic tasks and LVGL updates"""
    
    def __init__(self):
        self.tasks = []
        self.last_update = time.ticks_ms()
        self.update_interval = 50  # ms
        
    def add_task(self, task_func, interval_ms=1000):
        """Add a periodic task"""
        task = {
            'func': task_func,
            'interval': interval_ms,
            'last_run': time.ticks_ms()
        }
        self.tasks.append(task)
    
    def update(self):
        """Update all tasks"""
        current_time = time.ticks_ms()
        
        # Run periodic tasks
        for task in self.tasks:
            if time.ticks_diff(current_time, task['last_run']) >= task['interval']:
                try:
                    task['func']()
                    task['last_run'] = current_time
                except Exception as e:
                    print(f"Task error: {e}")
    
    def remove_task(self, task_func):
        """Remove a task"""
        self.tasks = [task for task in self.tasks if task['func'] != task_func]
