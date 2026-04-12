# Automations

The framework is scheduler-agnostic. Your control plane and subsystems can run on any scheduling mechanism — do not make the architecture depend on one specific agent shell or IDE.

## Supported Schedulers

### cron (Linux / macOS)

```crontab
# Run control-plane aggregation every hour
0 * * * * cd /path/to/ai-os-framework && python3 scripts/build_demo_war_room_snapshot.py

# Validate contracts daily at 8am
0 8 * * * cd /path/to/ai-os-framework && python3 scripts/validate_contracts.py
```

### launchd (macOS)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.aios.warroom</string>
  <key>ProgramArguments</key>
  <array>
    <string>python3</string>
    <string>/path/to/ai-os-framework/scripts/build_demo_war_room_snapshot.py</string>
  </array>
  <key>StartInterval</key>
  <integer>3600</integer>
</dict>
</plist>
```

### systemd timer (Linux)

```ini
# /etc/systemd/system/aios-warroom.timer
[Unit]
Description=AI OS War Room aggregation

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

## Choosing a Scheduler

| Scheduler | Best for | Trade-off |
|-----------|----------|-----------|
| cron | Simple recurring tasks | No dependency tracking |
| launchd | macOS-native, wake-on-schedule | macOS only |
| systemd | Linux servers, logging built in | Linux only |
| Container scheduler | Cloud / Docker environments | More infrastructure |

## What Belongs Here

- Scheduler configuration files for your environment
- Wrapper scripts that chain multiple control-plane steps
- Retry and error-handling wrappers

## Key References

- Portability docs: `docs/portability.md`
- Bootstrap script: `scripts/bootstrap.sh`
