def convert_duration_to_seconds(duration):
    """
    Convert ISO 8601 duration to seconds.
    Example duration: "PT10M30S" => 630 seconds
    """
    import re
    time_parts = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', duration)
    minutes = int(time_parts.group(1) or 0)
    seconds = int(time_parts.group(2) or 0)
    return (minutes * 60) + seconds
