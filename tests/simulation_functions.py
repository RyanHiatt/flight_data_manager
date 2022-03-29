import os
import secrets
import random
import datetime
import xml.etree.ElementTree as ET


def generate_simulated_sd(path: str, clean: bool = True):
    """
    Generates:
    One file containing "rpt_.csv"
    One xml file named "airframe_info.xml" with consistent formatting
    One directory named "data_log" with x number of .csv data files inside
    Possibly a .gcl or .ace file or other irrelevant files
    Other extraneous files or missing required files if clean = False

    :param path: {str} The path to where the simulated files and directories should be created.
    :param clean: {bool} If False then various other files may appear or an absence of required files may occur.
    :return:
    """

    airframe_names = ['Cessna 172S', 'Cirrus SR20', 'Cessna 165A', 'Cirrus SR22', 'Cessna 208C']
    system_ids = ['A4230C5A35', 'C7A12097DA', '38A7FC7085', 'FDF51CCBAD', '392EE09698']

    if clean:
        # Generate airframe_info.xml
        airframe_info = ET.Element('airframe_info')
        airframe_info.set('info_version', '1.00')
        airframe_name = ET.SubElement(airframe_info, 'airframe_name')
        system_id = ET.SubElement(airframe_info, 'system_id')
        airframe_name.text = random.choice(airframe_names)
        system_id.text = random.choice(system_ids)
        tree = ET.ElementTree(airframe_info)
        tree.write(f"{path}/airframe_info.xml")

        # Generate data_log
        os.mkdir(f"{path}/data_log")
        for i in range(0, random.randint(2, 8)):
            with open(file=f"{path}/data_log/log_{secrets.token_hex(4)}.csv", mode="w") as data_csv:
                pass

        # Generate rpt_.csv
        with open(file=f"{path}/rpt_{secrets.token_hex(4)}.csv", mode="w") as rpt_csv:
            pass

        # Create extraneous files
        with open(file=f"{path}/{secrets.token_hex(4)}.gcl", mode="w") as a_file:
            pass
        with open(file=f"{path}/{secrets.token_hex(4)}.ace", mode="w") as b_file:
            pass

    else:

        if bool(random.getrandbits(1)):  # True or False
            # Generate airframe_info.xml
            airframe_info = ET.Element('airframe_info')
            airframe_info.set('info_version', '1.00')
            airframe_name = ET.SubElement(airframe_info, 'airframe_name')
            system_id = ET.SubElement(airframe_info, 'system_id')
            airframe_name.text = random.choice(airframe_names)
            system_id.text = random.choice(system_ids)
            tree = ET.ElementTree(airframe_info)
            tree.write(f"{path}/airframe_info.xml")

        if bool(random.getrandbits(1)):  # True or False
            # Generate data_log
            os.mkdir(f"{path}/data_log")
            for i in range(0, random.randint(2, 8)):
                with open(file=f"{path}/data_log/log_{secrets.token_hex(4)}.csv", mode="w") as data_csv:
                    pass

        if bool(random.getrandbits(1)):  # True or False
            # Generate rpt_.csv
            with open(file=f"{path}/rpt_{secrets.token_hex(4)}.csv", mode="w") as rpt_csv:
                pass

        if bool(random.getrandbits(1)):  # True or False
            # Generate someone's homework
            with open(file=f"{path}/John_Doe_Homework.csv", mode="w") as hw:
                pass

            # Generate someone's diary
            with open(file=f"{path}/Jane_Doe_Diary.txt", mode="w") as etc:
                pass


def generate_simulated_hd(path: str, num_entries: int):
    """
    Generates simulated hard drive data containing x number of entries for 25 randomly generated aircraft
    from January 1, 2021, 01:00:00 to December 31, 2022, 24:59:59. Data is generated in the format used
    by the main application.

    :param path: {str} The path to where the simulated files and directories should be created.
    :param num_entries: {int} The number of data uploads that should be simulated to have occurred.
    :return:
    """

    # Used to generate names and dates
    airframe_names = ['Cessna 172S', 'Cirrus SR20', 'Cessna 165A', 'Cirrus SR22', 'Cessna 208C']
    system_ids = ['A4230C5A35', 'C7A12097DA', '38A7FC7085', 'FDF51CCBAD', '392EE09698']
    d1 = datetime.datetime.strptime('2021-01-01T01-00-00', '%Y-%m-%dT%H-%M-%S')
    d2 = datetime.datetime.now()

    for i in range(num_entries):
        # Generate a random plane
        plane_dir = f"{random.choice(airframe_names)}-{random.choice(system_ids)}"

        # Generate a random date between January 1, 2021, 01:00:00 and December 31, 2022, 24:59:59
        delta = d2 - d1
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        entry_dir = d1 + datetime.timedelta(seconds=random_second)
        entry_dir = entry_dir.strftime('%Y-%m-%dT%H-%M-%S')

        # Create the generated directories
        if not os.path.isdir(f"{path}/{plane_dir}/{entry_dir}"):
            os.makedirs(f"{path}/{plane_dir}/{entry_dir}", exist_ok=True)

        # Generate rpt_.csv
        with open(f"{path}/{plane_dir}/{entry_dir}/rpt_{secrets.token_hex(4)}.csv", "w") as rpt_csv:
            pass

        # Generate sample data files
        for j in range(0, random.randint(2, 8)):
            with open(f"{path}/{plane_dir}/{entry_dir}/log_{secrets.token_hex(4)}.csv", "w") as data_csv:
                pass


if __name__ == '__main__':
    # generate_simulated_sd(path="/Users/ryanhiatt/dev/projects/flight_data_manager/tests/test_sd", clean=True)
    generate_simulated_hd(path="/home/ryanhiatt/dev/projects/flight_data_manager/tests/test_hd", num_entries=10)
