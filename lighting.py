# upon run/initialization:
# attempts to set up lights according to lighting data file (contains lights, configurations, schedules)
    # if lighting connection fails, logs to console and skip
# marks all successful lights in an array (0 for unavailable, 1 for working) for the configurations
# turns on current configuration according to schedule (if on), otherwise goes to default
    # if a light is not available // does not respond correctly, this code skips it and adds the light to the retry list
# background process periodically retries the lights

# interface with this class:
# 1. press play to auto run on schedule
# 2. manual override via user commands (this class provides command list by giving access to all lights)
# 3. set up new configurations w/ available lights currently loaded AND save to file
# 4. add new light to file
# 5. (very optional) run diagnostic by turning on and off each light to test