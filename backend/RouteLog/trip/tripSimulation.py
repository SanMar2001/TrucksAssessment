from datetime import datetime, timedelta
from .models import Leg

BREAK_DURATION = 0.5
FUEL_DURATION = 0.5
REST_10H = 10
FUEL_EVERY_MILES = 1000
PICKUP_DURATION = 1
DROPOFF_DURATION = 1


def add_break_event(start_time):
    end_time = start_time + timedelta(hours=BREAK_DURATION)
    return {
        "type": "break",
        "duration": BREAK_DURATION,
        "start_datetime": start_time,
        "end_datetime": end_time,
        "event_day": start_time.date()
    }, end_time


def add_fuel_event(start_time):
    end_time = start_time + timedelta(hours=FUEL_DURATION)
    return {
        "type": "fuel",
        "duration": FUEL_DURATION,
        "start_datetime": start_time,
        "end_datetime": end_time,
        "event_day": start_time.date()
    }, end_time


def add_rest_event(reason, start_time):
    end_time = start_time + timedelta(hours=REST_10H)
    return {
        "type": "rest_10h",
        "duration": REST_10H,
        "reason": reason,
        "start_datetime": start_time,
        "end_datetime": end_time,
        "event_day": start_time.date()
    }, end_time


def add_pickup_event(start_time):
    end_time = start_time + timedelta(hours=PICKUP_DURATION)
    return {
        "type": "pickup",
        "duration": PICKUP_DURATION,
        "start_datetime": start_time,
        "end_datetime": end_time,
        "event_day": start_time.date()
    }, end_time


def add_dropoff_event(start_time):
    end_time = start_time + timedelta(hours=DROPOFF_DURATION)
    return {
        "type": "dropoff",
        "duration": DROPOFF_DURATION,
        "start_datetime": start_time,
        "end_datetime": end_time,
        "event_day": start_time.date()
    }, end_time


def process_trip(route, initial_state):
    events = []
    legs = []

    cycle_remaining = 70 - initial_state.get("cycle_hours", 0)
    duty_window = 0
    driving_today = 0
    driving_since_break = 0
    miles_since_fuel = 0

    current_time = initial_state.get("start_datetime", datetime.now())
    first_index = 0

    for i, leg_data in enumerate(route["legs"]):
        distance = [d / 1609.34 for d in leg_data["annotation"]["distance"]]
        duration = [t / 3600 for t in leg_data["annotation"]["duration"]]

        index = len(duration)

        if i == 0:
            first_index = index
            coordinates = route["geometry"]["coordinates"][1:index+1]
        else:
            coordinates = route["geometry"]["coordinates"][first_index+1:]

        legs.append(Leg(distance, duration, coordinates, index))

    for leg_idx, leg in enumerate(legs):
        for point_idx in range(len(leg.distance)):
            dist = leg.distance[point_idx]
            dur = leg.duration[point_idx]
            coord = leg.coordinates[point_idx]

            if driving_today + dur > 11:
                event, current_time = add_rest_event("11h limit reached", current_time)
                events.append(event)
                duty_window = 0
                driving_today = 0
                driving_since_break = 0
                continue

            if duty_window + dur > 14:
                event, current_time = add_rest_event("14h window reached", current_time)
                events.append(event)
                duty_window = 0
                driving_today = 0
                driving_since_break = 0
                continue

            if driving_since_break >= 8:
                event, current_time = add_break_event(current_time)
                events.append(event)
                duty_window += BREAK_DURATION
                cycle_remaining -= BREAK_DURATION
                driving_since_break = 0

            if miles_since_fuel >= FUEL_EVERY_MILES:
                event, current_time = add_fuel_event(current_time)
                events.append(event)
                duty_window += FUEL_DURATION
                cycle_remaining -= FUEL_DURATION
                miles_since_fuel = 0

            start_time = current_time
            end_time = start_time + timedelta(hours=dur)

            events.append({
                "type": "drive",
                "duration": dur,
                "coordinate": coord,
                "start_datetime": start_time,
                "end_datetime": end_time,
                "event_day": start_time.date()
            })

            current_time = end_time
            driving_today += dur
            driving_since_break += dur
            duty_window += dur
            cycle_remaining -= dur
            miles_since_fuel += dist

        if leg_idx == 0:
            event, current_time = add_pickup_event(current_time)
            events.append(event)
            duty_window += PICKUP_DURATION
            cycle_remaining -= PICKUP_DURATION
        elif leg_idx == 1:
            event, current_time = add_dropoff_event(current_time)
            events.append(event)
            duty_window += DROPOFF_DURATION
            cycle_remaining -= DROPOFF_DURATION

    return events