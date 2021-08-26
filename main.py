import sys

from selenium import webdriver
from time import sleep
import argparse
import yaml


def parse_arg() -> tuple[bool, str, int, str]:
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--dry-run", action="store_true",
        help="optional - if set, do dry run (run the process but does NOT click 'book' button)")
    arg_parser.add_argument(
        "-t", "--time", type=str, action="store", required=True, help="required - book time, 10AM, 12PM, 9PM, etc.")
    arg_parser.add_argument(
        "--slot", type=int, action="store", required=False, default=1,
        help="optional, default = 1 - # of slot to book. If there are multiple slots, book the specified slot. "
             + "For example, if courts 3,4,5,6,7 are available, "
             + " SLOT=2 means book count #4 (2nd slot)")
    arg_parser.add_argument(
        "-p", "--property-file", type=str, action="store", required=False, default="property.yml",
        help="optional, property file. Default to property.yml")

    args = arg_parser.parse_args()

    print(repr(args))

    return args.dry_run, args.time, args.slot, args.property_file


if __name__ == '__main__':
    dry_run, bookTime, slot, property_file = parse_arg()

    with open(property_file) as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)

    users = read_data['users']

    slot_user = {}
    for i in range(9):
        slot_user[i + 1] = users[i % len(users)]

    user_in_use = slot_user[slot]

    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()

    try:
        driver.get("https://nvbc.ezfacility.com/Sessions#")

        login_button = driver.find_element_by_xpath('//a[contains(text(), "Login")]')
        login_button.click()

        sleep(0.5)

        username_input = driver.find_element_by_xpath('//input[@id="Username"]')
        password_input = driver.find_element_by_xpath('//input[@id="Password"]')
        login_button = driver.find_element_by_xpath('//button[@id="btnLogin"]')

        username_input.send_keys(user_in_use['username'])
        password_input.send_keys(user_in_use['password'])

        login_button.click()
        sleep(0.5)

        for i in range(0, 3):
            driver.get("https://nvbc.ezfacility.com/Sessions")
            sleep(1)

            # noinspection PyBroadException
            try:
                available_slots = driver.find_elements_by_xpath('//tbody/tr/td[contains(@class, "fc-event-container")]')

                if available_slots is None or len(available_slots) == 0:
                    print("no available slot, " + i)
                    continue

                print("# of available slots: " + str(len(available_slots)))

                available_slots_matching_time = []

                for available_slot in available_slots:
                    row_text = available_slot.text.split("\n")
                    time = row_text[0]
                    start_time = time.split(' ')[0]
                    desc: str = row_text[1]

                    if bookTime == start_time and desc == 'Available Court':
                        available_slots_matching_time.append(available_slot)

                num_slot = len(available_slots_matching_time)

                if len(available_slots_matching_time) == 0:
                    print("no available slot matching time")
                    continue

                print("# of available slots matching time: " + str(num_slot))

                slot = slot if slot <= num_slot else num_slot
                slot = slot - 1

                available_slot = available_slots_matching_time[slot]

                available_slot.click()
                sleep(0.5)
                btn_book = driver.find_element_by_xpath('//button[@id="btnBook"]')

                if dry_run:
                    print("Dry run ... do nothing")
                else:
                    btn_book.click()
                    print("clicked")
                    sleep(0.5)
                    sys.exit()

            except KeyboardInterrupt:
                sys.exit()
            except:
                print("Error getting available_slots. Continue to try")
    finally:
        print("Closing browser ...")
        driver.close()
        driver.quit()
        print("Done")
