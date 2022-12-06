import subprocess
import re
import yaml
from sys import argv


def get_ntp_list():
    with open('./metronoms.yml', 'r') as file:
        ntp = yaml.safe_load(file)
        ntp_list = ntp.get('metronoms')

        return ntp_list


def writing_to_file(ntp_list, file_name):
    with open('./{}.yml'.format(file_name), 'w') as file:
        yaml.dump(ntp_list, file)


def check_year(ntp_list, year):
    wrong_year = []
    no_ntp = []

    for host in ntp_list:
        sntp = 'sntp -t 1 {} | sed -n 2p'.format(host)
        outp = str(subprocess.check_output(sntp, shell=True))
        t = re.search(r'(\d\d\d\d)', outp)
        try:
            t = int(t.groups()[0])
            if t != int(year):
                wrong_year.append(host)

        except AttributeError:
            no_ntp.append(host)

    return wrong_year, no_ntp


def main():
    year = argv[1]
    ntp_list = get_ntp_list()
    incorrect_ntp, error_ntp = check_year(ntp_list, year)
    writing_to_file(incorrect_ntp, 'incorrect_ntp')
    writing_to_file(error_ntp, 'error_ntp')


if __name__ == '__main__':
    main()
