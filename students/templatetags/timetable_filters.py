from django import template

register = template.Library()

@register.filter
def filter_day(timetable, day):
    return [entry for entry in timetable if entry.day == day]
