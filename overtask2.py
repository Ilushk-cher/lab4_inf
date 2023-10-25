import re

keywords = ["subject", "time", "type", "teacher", "format", "room", "location"]


class Schedule:
    def __init__(self):
        self.day = ""
        self.lessons = []


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
    in_lesson = False
    counter = 0

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

        if key_string == "timetable":
            begin_of_timetable = True

        if not begin_of_timetable:
            continue

        if counter == 0:
            break

        if key_string == "day" and not begin_of_lessons:
            schedule.day = word
            continue

        if key_string == "lesson1":
            begin_of_lessons = True
            continue

        if key_string == "subject":
            in_lesson = True

        if in_lesson:
            if key_string in keywords:
                lesson[key_string] = word

        if key_string == "location":
            in_lesson = False
            schedule.lessons.append(lesson)
            lesson = dict()

    return schedule


def file_to_yaml(file):
    schedule = parse_file(file)
    yaml = "timetable:\n"
    yaml += f"  day: {schedule.day}\n"
    for i, lesson in enumerate(schedule.lessons):
        yaml += f"  lesson{i + 1}:\n"
        for key, attribute in lesson.items():
            yaml += f"    {key}: {attribute}\n"
    return yaml


input_file_name = "schedule"
output_file_name = "schedule_converted"

with open(input_file_name + ".json", 'r', encoding='utf-8') as input_file:
    yaml_file = file_to_yaml(prepared_file(input_file))

with open(output_file_name + ".yaml", 'w', encoding='utf-8') as output_file:
    output_file.write(yaml_file)
