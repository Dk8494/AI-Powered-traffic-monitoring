from alert_engine_api import generate_alerts


def display_alerts(prediction, weather, accident, event):
    """Return alert payload for frontend consumption.

    This wraps `generate_alerts` so existing callers can continue
    calling `display_alerts(...)` but receive structured data.
    """
    return generate_alerts(prediction=prediction, weather=weather, accident=accident, event=event)
