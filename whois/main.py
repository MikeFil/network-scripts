import requests
import json
from jinja2 import Environment, FileSystemLoader


def get_ips(file):
    with open('{}'.format(file), 'r') as ip_list:
        ips = []
        for l in ip_list.readlines():
            ips.append(l)

        return ips


def get_cleaned_list(data):
    clean_ips = []
    for i, d in enumerate(data):
        clean_ips.append(data[i].strip())

    return clean_ips


def check_country(ip):
    response = requests.get('http://api.ipapi.com/{}?access_key=f36a3251f85cc21a3e998f7a5a26c050'.format(ip))
    ip_geolocation = json.loads(response.content.decode('utf-8'))["country_code"]

    return ip_geolocation


def prepare_template(file):
    env = Environment(loader=FileSystemLoader('.'))
    templ = env.get_template('ip_range.txt')

    config = []
    codes = []
    dcodes = dict()

    with open('{}'.format(file), 'r') as f:
        for i in f.readlines():
            start, end, code = i.strip().split(' ')
            codes.append(code)

    c = set(codes)

    for i in c:
        globals()['{}'.format(i)] = []
        for cod in codes:
            start, end, code = cod.strip().split(' ')
            if code == i:
                globals()['{}'.format(i)].append(start + ' ' + end)

    for i in c:
        dcodes['{}'.format(i)] = globals()['{}'.format(i)]

    for i in dcodes.keys():
        strc = ''
        strc += 'edit ' + i + '\n'
        strc += 'set country-id ' + i + '\n'
        strc += 'config ip-range\n'
        count = 0
        for d in dcodes.get(i):
            start, end = d.strip().split(' ')
            data = {'number': count, 'start': start, 'end': end}
            strc += templ.render(data)
            count += 1
        strc += '\n' + 'end\n'
        strc += 'next\n'
        config.append(strc)

    with open('config.txt', 'w') as f:
        for i in config:
            f.write(i)


def main():
    file = get_ips('ips.txt')
    clean_data = get_cleaned_list(file)
    ip_with_code = []
    ip_with_two_code = []

    for i in clean_data:
        start, end = i.split(' - ')
        start_c = check_country(start)
        end_c = check_country(end)
        if start_c == end_c:
            ip_with_code.append(i + ' ' + start_c)

        else:
            ip_with_two_code.append(start + ' ' + start_c + ' - ' + end + ' ' + end_c)

    with open('ip_with_code.txt', 'w') as f:
        for i in ip_with_code:
            f.write('{}\n'.format(i))

    with open('ip_with_two_code.txt', 'w') as f:
        for i in ip_with_two_code:
            f.write('{}\n'.format(i))

    prepare_template('ip_with_code.txt')


if __name__ == '__main__':
    main()
