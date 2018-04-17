import os
import subprocess
import sys
import time


def flash(rom_path):
    output = subprocess.check_output(["adb", "reboot", "bootloader"])
    print output

    time.sleep(5)

    for img in ("boot", "system", "recovery"):
        f = os.path.join(rom_path, img + ".img")
        output = subprocess.check_output(["fastboot", "flash", img, f])
        print output

    output = subprocess.check_output(["fastboot", "reboot"])
    print output


def main(argv):
    if len(argv) == 2:
        flash(argv[1])


if __name__ == "__main__":
    main(sys.argv)