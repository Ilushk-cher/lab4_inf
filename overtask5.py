import re
import time

keywords = ["subject", "time", "type", "teacher", "format", "room", "location"]


class Schedule:
    def __init__(self):
        self.days = []


def prepared_file(file):
    lines = file.readlines()
    line = " ".join(lines)
    new_file = []
    counter = 0
    key_start_index = 0
    start_index = 0
    if '"' in line:
        for i in range(len(line)):
            if line[i] == '"' and counter == 0:
                counter += 1
                key_start_index = i
                break
        for i in range(key_start_index + 1, len(line)):
            if line[i] == '"' and line[i - 1] != '\\':
                counter += 1
            if (line[i] in '{[,}]') and counter % 2 == 0:
                end_index = i
                new_file.append(line[start_index: end_index + 1])
                start_index = i + 1
        new_file.append(line[start_index:])
    return new_file


def parse_file(file):
    schedule = Schedule()
    lesson = dict()
    begin_of_timetable = False
    begin_of_lessons = False
    begin_of_days = False
    in_lesson = False
    counter = 0
    counter_days = 0
    day = ''
    lessons_for_day = []

    for line in file:
        key_string = ''
        word = ''
        key_pattern = r'\"(.*?[^\\])\"'
        pair_pattern = r'\"(.*?[^\\])\"\s*:\s*\"(.*?[^\\])\"'

        if re.search(pair_pattern, line) is not None:
            key_string, word = re.findall(key_pattern, line)
        elif re.search(key_pattern, line) is not None:
            key_string = re.findall(key_pattern, line)[0]

        counter += line.count("{") - line.count("}")
        counter_days += line.count("[") - line.count("]")

        if key_string == "timetable":
            begin_of_timetable = True

        if not begin_of_timetable:
            continue

        if counter == 0:
            break

        if key_string in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
            begin_of_lessons = False
            begin_of_days = True
            day = key_string
            continue

        if key_string == "lesson1" and begin_of_days:
            begin_of_lessons = True
            continue

        if key_string == "subject" and begin_of_lessons:
            in_lesson = True

        if in_lesson:
            if key_string in keywords:
                lesson[key_string] = word

        if key_string == "location":
            lessons_for_day.append(lesson)
            lesson = dict()
            in_lesson = False

        if counter_days == 0 and begin_of_days:
            schedule.days.append([day, lessons_for_day])
            lessons_for_day = []
            begin_of_days = False
    return schedule


def file_to_markdown(file):
    schedule = parse_file(file)
    markdown = "# timetable\n"
    for i, day in enumerate(schedule.days):
        markdown += f"## {day[0]}\n"
        lessons = day[1]
        for j, lesson in enumerate(lessons):
            markdown += f"### lesson{j + 1}\n"
            for key, attribute in lesson.items():
                markdown += f"* **{key}**: *{attribute}*\n"
    return markdown


input_file_name = "weak_schedule"
output_file_name = "weak_schedule_converted"

start_time = time.time()
for i in range(100):
    with open(input_file_name + ".json", 'r', encoding='utf-8') as input_file:
        yaml_file = file_to_markdown(prepared_file(input_file))

    with open(output_file_name + ".md", 'w', encoding='utf-8') as output_file:
        output_file.write(yaml_file)

print(f'{time.time() - start_time:.5f}')
