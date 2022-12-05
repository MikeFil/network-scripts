import ipaddress
import json
import requests
from jinja2 import Environment, FileSystemLoader


def get_cr_nets(file):
    with open('{}'.format(file), 'r') as ip_list:
        ips = []
        for l in ip_list.readlines():
            ips.append(ipaddress.ip_network(l.strip()))

        return ips


def get_start_end(network):
    start = network[0]
    end = network.broadcast_address
    return start, end


def create_template(networks, count):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.txt')
    config = []
    counter = count

    for i in networks:
        start, end = get_start_end(i)
        data = {'i': count, 'start': start, 'end': end}
        config.append(template.render(data))
        counter += 1

    return config


def write_config(config):
    with open('config.txt', 'w') as f:
        for i in config:
            f.write(i)


def check_country(ip):
    response = requests.get('http://api.ipapi.com/{}?access_key=f36a3251f85cc21a3e998f7a5a26c050'.format(ip))
    ip_geolocation = json.loads(response.content.decode('utf-8'))["country_code"]

    return ip_geolocation


def main():
    nets = get_cr_nets('ips02.txt')
    config = create_template(nets, 591)
    write_config(config)


if __name__ == '__main__':
    main()
