import sys

from selenium import webdriver
from time import sleep
import argparse


def parse_arg() -> tuple[bool, str, int]:
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--dry-run", action="store_true", help="If set, do dry run")
    arg_parser.add_argument(
        "-t", "--time", type=str, action="store", required=True, help="Book time, 10AM, 12PM, 9PM, etc.")
    arg_parser.add_argument(
        "--slot", type=int, action="store", required=False, default=1, help="# of slot to book")

    args = arg_parser.parse_args()

    print(repr(args))

    return args.dry_run, args.time, args.slot


if __name__ == '__main__':
    dryRun, bookTime, slot = parse_arg()

    driver = webdriver.Chrome()

    try:
        driver.get("https://nvbc.ezfacility.com/Sessions")

        login_button = driver.find_element_by_xpath('//a[contains(text(), "Login")]')
        login_button.click()

        sleep(0.5)

        username_input = driver.find_element_by_xpath('//input[@id="Username"]')
        password_input = driver.find_element_by_xpath('//input[@id="Password"]')
        login_button = driver.find_element_by_xpath('//button[@id="btnLogin"]')

        username_input.send_keys("allenjia")
        password_input.send_keys("xxxx")
        login_button.click()

        for i in range(0, 5):
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

                if dryRun:
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
