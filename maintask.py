keywords = ["subject", "time", "type", "teacher", "format", "room", "location"]


class Schedule:
    def __init__(self):
        self.day = ""
        self.lessons = []


def fined_word(line, end_key_index):
    index = line.rfind('"')
    value_start_index = line[end_key_index + 1:].find('"') + end_key_index + 1
    return line[value_start_index + 1: index]


def parse_pair(line, key_string, end_key_index):
    word = fined_word(line, end_key_index)
    return key_string, word


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
    end_key_index = 0

    for line in file:
        key_string = ''
        if '"' in line:
            begin_key_index = line.find('"')
            end_key_index = line[begin_key_index + 1:].find('"') + begin_key_index + 1

            key_string = line[begin_key_index + 1: end_key_index]

        counter += line.count("{") - line.count("}")

        if key_string == "timetable":
            begin_of_timetable = True

        if not begin_of_timetable:
            continue

        if counter == 0:
            break

        if key_string == "day" and not begin_of_lessons:
            key, word = parse_pair(line, key_string, end_key_index)
            schedule.day = word
            continue

        if key_string == "lesson1":
            begin_of_lessons = True
            continue

        if key_string == "subject":
            in_lesson = True

        if in_lesson:
            key, word = parse_pair(line, key_string, end_key_index)
            if key in keywords:
                lesson[key] = word

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
