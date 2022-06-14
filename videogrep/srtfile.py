import json, time

def format_float_time(time):
    mon, sec = divmod(time, 60)
    hr, mon = divmod(mon, 60)
    s = "%02d:%02d:%06.3f" % (hr, mon, sec)
    return s # s.replace('.', ',')

def from_list(items):
    srt_items = []
    for i, e in enumerate(items):
        sentence = e["content"]
        time_beg = format_float_time(e["start"])
        time_end = format_float_time(e["end"])
        srt_item = f"{i + 1}\n{time_beg} --> {time_end}\n{sentence}\n"
        srt_items.append(srt_item)
    return "\n".join(srt_items)
