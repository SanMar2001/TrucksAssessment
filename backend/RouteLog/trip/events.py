from datetime import timedelta, datetime


def split_events_by_day(events):
    result = []

    for event in events:
        start = event["start_datetime"]
        end = event["end_datetime"]

        while start.date() != end.date():
            end_of_day = datetime.combine(start.date(), datetime.max.time()).replace(microsecond=0)
            event_part = event.copy()
            event_part["start_datetime"] = start
            event_part["end_datetime"] = end_of_day
            event_part["event_day"] = start.date()
            result.append(event_part)

            start = end_of_day + timedelta(seconds=1)

        event_final = event.copy()
        event_final["start_datetime"] = start
        event_final["end_datetime"] = end
        event_final["event_day"] = start.date()
        result.append(event_final)

    return result


def group_events_by_day(events):
    grouped = []
    day_counter = 1
    current_date = None
    day_events = []

    for event in events:
        event_date = event["event_day"]
        if current_date != event_date:
            if day_events:
                grouped.append({
                    "day": day_counter,
                    "date": current_date,
                    "events": day_events
                })
                day_counter += 1
            current_date = event_date
            day_events = [event]
        else:
            day_events.append(event)

    if day_events:
        grouped.append({
            "day": day_counter,
            "date": current_date,
            "events": day_events
        })

    return grouped


def process_events(events):
    filtered_events = []
    drive_flag = False

    for i, event in enumerate(events):
        if event['type'] == 'drive':
            if not drive_flag:
                filtered_events.append(event)
                drive_flag = True
        else:
            filtered_events[-1]['end_datetime'] = events[i-1]['end_datetime']
            new_end = filtered_events[-1]['end_datetime']
            new_start = filtered_events[-1]['start_datetime']
            filtered_events[-1]['duration'] = round((new_end - new_start).total_seconds() / 3600)
            filtered_events.append(event)
            drive_flag = False

    divided_by_day = split_events_by_day(filtered_events)
    grouped = group_events_by_day(divided_by_day)
    return grouped