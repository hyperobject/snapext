#!/usr/bin/python
"""Example Snap! extension using the snapext module."""
import snapext

handler = snapext.SnapHandler

doors_open = True
# Replace with library for spaceship door interaction

@handler.route('/doors/set')
def set_doors(is_open):
    global doors_open
    print is_open
    if is_open:
        doors_open = True
        # Open spaceship doors
    else:
        doors_open = False
        # Close spaceship doors -- don't let humans in!

@handler.route('/doors/is_open')
def get_doors():
    return doors_open

if __name__ == "__main__":
    # Run the server
    snapext.main(handler, 47543)

