from threading import Thread
import sys
import init_sensors
import calibrate_sensors
import mouse_control


def main():
    # Search for connected devices
    try:
        connected_device_port = init_sensors.main()
    except EnvironmentError as error:
        print("Program stopped because of following error: "+ error.message)
        sys.exit()

    # Wait for sensitivity level input
    remaining_tries = 2
    while True:
        try:
            sensitivity = calibrate_sensors.main()
            break
        except ValueError as error:
            if remaining_tries != 0:
                print(error)
                remaining_tries -= 1
                pass
            else:
                print("Program stopped because of following error " + error.message)
                exit()

    print("Mouse control is active now.")

    try:
        mouse_thread = Thread(target=mouse_control.main(connected_device_port, sensitivity))
        mouse_thread.start()
        mouse_thread.join()
    except (KeyboardInterrupt, SystemExit):
        print("Program cancelled due to keyboard interruption.")
        sys.exit()


if __name__ == '__main__':
    main()
