# Database Design Document
## ECU Diagnostic Tool

### Document Information
**Product Name:** ECU Diagnostic Tool  
**Version:** 1.0  
**Document Version:** 1.0  
**Date:** 2025-09-06  
**Document Type:** Database Design Specification  

---

## 1. Overview

This document defines the database design and data management strategy for the ECU Diagnostic Tool. The system uses JSON-based file storage optimized for embedded systems with limited resources.

## 2. Database Architecture

### 2.1 Storage Strategy
- **File-based JSON storage** for simplicity and portability
- **Atomic write operations** to prevent data corruption
- **Backup and recovery mechanisms** for data protection
- **Separation of system and user data** for update safety

### 2.2 Data Organization
```
/db/
├── systems.json          # System database (read-only, updatable via firmware)
├── user_settings.json    # User preferences and state (persistent)
├── custom_systems.json   # User-defined systems (persistent)
├── error_log.json        # System error log (rotating)
└── backups/              # Automatic backup directory
    ├── user_settings_backup.json
    └── custom_systems_backup.json
```

## 3. Schema Definitions

### 3.1 Systems Database Schema

#### 3.1.1 Primary Structure
```json
{
  "version": "1.0",
  "last_updated": "2025-09-06T00:00:00Z",
  "systems": [
    {
      "id": "unique_system_id",
      "brand": "Vehicle manufacturer",
      "type": "System category",
      "system_name": "Specific system identifier",
      "description": "Human readable description",
      "tools": [
        {
          "id": "unique_tool_id",
          "name": "Tool display name",
          "type": "Tool category",
          "description": "Tool description",
          "config": {
            "sensor_config": {},
            "parameters": {},
            "validation": {}
          }
        }
      ],
      "metadata": {
        "created": "timestamp",
        "modified": "timestamp",
        "version": "string"
      }
    }
  ]
}
```

#### 3.1.2 RPM Simulator Tool Configuration
```json
{
  "id": "rpm_simulator_001",
  "name": "RPM Simulator",
  "type": "rpm_simulation",
  "description": "Crankshaft and camshaft signal simulation",
  "config": {
    "sensor_config": {
      "crank": {
        "degrees_per_tooth": 6,
        "missing_teeth": 2,
        "total_teeth": 58,
        "signal_type": "hall_effect",
        "voltage_high": 5.0,
        "voltage_low": 0.0
      },
      "cam": {
        "degrees_per_tooth": 12,
        "tooth_pattern": [1,1,1,1,1,1,0,1,1,1,1,1],
        "signal_type": "hall_effect",
        "voltage_high": 5.0,
        "voltage_low": 0.0
      }
    },
    "parameters": {
      "rpm_range": {
        "min": 0,
        "max": 10000,
        "default": 800,
        "step": 50
      },
      "update_frequency": 10
    },
    "validation": {
      "required_fields": ["crank", "cam"],
      "rpm_limits": [0, 10000]
    }
  }
}
```

#### 3.1.3 DTC Tool Configuration
```json
{
  "id": "dtc_manager_001",
  "name": "DTC Manager",
  "type": "dtc_management",
  "description": "Diagnostic trouble code operations",
  "config": {
    "operations": ["read", "clear"],
    "supported_protocols": ["OBD2", "KWP2000", "UDS"],
    "dtc_definitions": {
      "P0300": "Random/Multiple Cylinder Misfire Detected",
      "P0420": "Catalyst System Efficiency Below Threshold",
      "P0171": "System Too Lean (Bank 1)"
    },
    "parameters": {
      "timeout": 5000,
      "retry_count": 3
    }
  }
}
```

### 3.2 User Settings Schema

#### 3.2.1 Primary Structure
```json
{
  "version": "1.0",
  "last_updated": "2025-09-06T00:00:00Z",
  "device_id": "unique_device_identifier",
  "last_selected": {
    "brand": "VW",
    "system": "Engine",
    "system_name": "Bosch ME7.9.7",
    "tool": "RPM Simulator",
    "timestamp": "2025-09-06T00:00:00Z"
  },
  "wifi": {
    "ssid": "network_name",
    "password": "encrypted_password",
    "auto_connect": true,
    "connection_history": [
      {
        "ssid": "network_name",
        "last_connected": "timestamp",
        "success_count": 10,
        "failure_count": 1
      }
    ]
  },
  "preferences": {
    "theme": "light",
    "language": "en",
    "auto_update": true,
    "screen_timeout": 300,
    "brightness": 80,
    "sound_enabled": true
  },
  "usage_statistics": {
    "boot_count": 25,
    "total_runtime": 3600,
    "feature_usage": {
      "rpm_simulator": 15,
      "dtc_manager": 8,
      "live_data": 3
    }
  }
}
```

### 3.3 Custom Systems Schema

#### 3.3.1 User-Defined Systems
```json
{
  "version": "1.0",
  "last_updated": "2025-09-06T00:00:00Z",
  "custom_systems": [
    {
      "id": "custom_001",
      "name": "Custom Engine System",
      "brand": "Custom",
      "type": "Engine",
      "system_name": "User Defined ECU",
      "description": "User-created system configuration",
      "tools": [
        {
          "id": "custom_rpm_001",
          "name": "Custom RPM Simulator",
          "type": "rpm_simulation",
          "config": {
            "sensor_config": {
              "crank": {
                "degrees_per_tooth": 10,
                "missing_teeth": 1
              },
              "cam": {
                "degrees_per_tooth": 20,
                "tooth_pattern": [1,0,1,0,1,0]
              }
            }
          }
        }
      ],
      "metadata": {
        "created_by": "user",
        "created": "2025-09-06T00:00:00Z",
        "modified": "2025-09-06T00:00:00Z"
      }
    }
  ]
}
```

### 3.4 Error Log Schema

#### 3.4.1 Error Logging Structure
```json
{
  "version": "1.0",
  "max_entries": 100,
  "current_count": 25,
  "entries": [
    {
      "id": "error_001",
      "timestamp": "2025-09-06T00:00:00Z",
      "severity": "ERROR",
      "category": "wifi",
      "message": "Connection timeout",
      "context": {
        "function": "wifi_manager.connect",
        "ssid": "network_name",
        "timeout": 30
      },
      "stack_trace": "optional_stack_trace",
      "resolved": false
    }
  ]
}
```

## 4. Data Access Patterns

### 4.1 Read Operations

#### 4.1.1 System Data Access
```python
def load_systems():
    """Load systems database with caching"""
    try:
        with open('/db/systems.json', 'r') as f:
            data = ujson.load(f)
            return data.get('systems', [])
    except (OSError, ValueError) as e:
        log_error(f"Failed to load systems: {e}")
        return []

def get_system_by_id(system_id):
    """Get specific system by ID"""
    systems = load_systems()
    for system in systems:
        if system.get('id') == system_id:
            return system
    return None

def get_tools_for_system(brand, system_type, system_name):
    """Get available tools for a system"""
    systems = load_systems()
    for system in systems:
        if (system.get('brand') == brand and 
            system.get('type') == system_type and
            system.get('system_name') == system_name):
            return system.get('tools', [])
    return []
```

#### 4.1.2 User Settings Access
```python
def load_user_settings():
    """Load user settings with defaults"""
    try:
        with open('/db/user_settings.json', 'r') as f:
            return ujson.load(f)
    except (OSError, ValueError):
        return get_default_settings()

def get_last_selected():
    """Get last selected system and tool"""
    settings = load_user_settings()
    last_selected = settings.get('last_selected', {})
    return (
        last_selected.get('brand'),
        last_selected.get('system'),
        last_selected.get('system_name'),
        last_selected.get('tool')
    )

def get_wifi_config():
    """Get WiFi configuration"""
    settings = load_user_settings()
    return settings.get('wifi', {})
```

### 4.2 Write Operations

#### 4.2.1 Atomic Write Pattern
```python
def atomic_write(file_path, data):
    """Atomic write operation to prevent corruption"""
    temp_path = file_path + '.tmp'
    try:
        # Write to temporary file
        with open(temp_path, 'w') as f:
            ujson.dump(data, f)
        
        # Atomic rename
        os.rename(temp_path, file_path)
        return True
    except Exception as e:
        # Clean up temporary file
        try:
            os.remove(temp_path)
        except:
            pass
        log_error(f"Atomic write failed: {e}")
        return False

def save_user_settings(settings):
    """Save user settings atomically"""
    settings['last_updated'] = time.time()
    return atomic_write('/db/user_settings.json', settings)

def update_last_selected(brand, system, system_name, tool):
    """Update last selected system"""
    settings = load_user_settings()
    settings['last_selected'] = {
        'brand': brand,
        'system': system,
        'system_name': system_name,
        'tool': tool,
        'timestamp': time.time()
    }
    return save_user_settings(settings)
```

### 4.3 Backup and Recovery

#### 4.3.1 Backup Operations
```python
def create_backup():
    """Create backup of user data"""
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    
    # Backup user settings
    try:
        with open('/db/user_settings.json', 'r') as src:
            with open(f'/db/backups/user_settings_{timestamp}.json', 'w') as dst:
                dst.write(src.read())
    except Exception as e:
        log_error(f"User settings backup failed: {e}")
    
    # Backup custom systems
    try:
        with open('/db/custom_systems.json', 'r') as src:
            with open(f'/db/backups/custom_systems_{timestamp}.json', 'w') as dst:
                dst.write(src.read())
    except Exception as e:
        log_error(f"Custom systems backup failed: {e}")

def restore_from_backup(backup_timestamp):
    """Restore data from backup"""
    try:
        # Restore user settings
        backup_file = f'/db/backups/user_settings_{backup_timestamp}.json'
        with open(backup_file, 'r') as src:
            with open('/db/user_settings.json', 'w') as dst:
                dst.write(src.read())
        
        # Restore custom systems
        backup_file = f'/db/backups/custom_systems_{backup_timestamp}.json'
        with open(backup_file, 'r') as src:
            with open('/db/custom_systems.json', 'w') as dst:
                dst.write(src.read())
        
        return True
    except Exception as e:
        log_error(f"Restore failed: {e}")
        return False
```

## 5. Data Validation and Integrity

### 5.1 Schema Validation
```python
def validate_system_schema(system_data):
    """Validate system data against schema"""
    required_fields = ['id', 'brand', 'type', 'system_name', 'tools']
    
    for field in required_fields:
        if field not in system_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate tools
    for tool in system_data.get('tools', []):
        validate_tool_schema(tool)
    
    return True

def validate_tool_schema(tool_data):
    """Validate tool data against schema"""
    required_fields = ['id', 'name', 'type', 'config']
    
    for field in required_fields:
        if field not in tool_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Type-specific validation
    tool_type = tool_data.get('type')
    if tool_type == 'rpm_simulation':
        validate_rpm_config(tool_data.get('config', {}))
    
    return True

def validate_rpm_config(config):
    """Validate RPM simulator configuration"""
    if 'sensor_config' not in config:
        raise ValueError("Missing sensor_config")
    
    sensor_config = config['sensor_config']
    
    # Validate crank configuration
    if 'crank' in sensor_config:
        crank = sensor_config['crank']
        if 'degrees_per_tooth' not in crank:
            raise ValueError("Missing crank degrees_per_tooth")
    
    # Validate cam configuration
    if 'cam' in sensor_config:
        cam = sensor_config['cam']
        if 'tooth_pattern' not in cam:
            raise ValueError("Missing cam tooth_pattern")
```

## 6. Performance Optimization

### 6.1 Caching Strategy
- In-memory caching of frequently accessed data
- Lazy loading of large datasets
- Cache invalidation on data updates
- Memory-conscious cache size limits

### 6.2 File I/O Optimization
- Minimize file operations during runtime
- Batch write operations when possible
- Use streaming for large data sets
- Implement read-ahead caching for predictable access patterns

---

**Document Control:**
- Created: 2025-09-06
- Last Modified: 2025-09-06
- Next Review: 2025-12-06
- Version: 1.0
