class CameraException(Exception):
    """
    Master Exception used if camera is not accessible
    """
    pass

class CameraBusy(Exception):
    msg = ("No frame received from Camera.\n"
           "Possible causes:\n"
           "    Camera disconnected\n"
           "    Camera not released properly\n"
           "Attempting to reset and reconnect")