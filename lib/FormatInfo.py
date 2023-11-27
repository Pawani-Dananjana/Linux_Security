import grp, pwd
import time
import stat
import os

# Get group name based on the group number obtained from stat
def linuxGroupInfo(st_gid: int):
    """
    Get group name based on the group number obtained from stat
    :param st_gid: Group number
    :return: str Group name
    """
    try:
        entry = grp.getgrgid(st_gid)
        return entry.gr_name
    except:
        return 'UNKNOWN'

# Get user name based on the user number obtained from stat
def linuxUserInfo(st_uid: int):
    """
    Get user name based on the user number obtained from stat
    :param st_uid: User ID
    :return: str User name
    """
    try:
        entry = pwd.getpwuid(st_uid)
        return entry.pw_name
    except:
        return 'UNKNOWN'

# Format time in a human-readable format
def formatTime(Time: float):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(Time))

# Format file mode as a string
def formatMode(mode: int):
    return stat.filemode(mode)

# Determine the type of object based on the mode
def objectType(mode: int):
    if stat.S_ISDIR(mode):
        return 'Directory'
    elif stat.S_ISREG(mode):
        return 'Regular file'
    elif stat.S_ISLNK(mode):
        return 'Shortcut'
    elif stat.S_ISSOCK(mode):
        return 'Socket'
    elif stat.S_ISFIFO(mode):
        return 'Named pipe'
    elif stat.S_ISBLK(mode):
        return 'Block special device'
    elif stat.S_ISCHR(mode):
        return 'Character special device'

# On Linux, get device name based on device number
def linuxDeviceToName(no: int):
    """
    On Linux, get device name based on device number
    :param no: Device number
    :return: str
    """
    for line in open('/proc/partitions'):
        fields = line.split()
        if 0 in fields and 1 in fields and 3 in fields \
                and int(fields[0]) == os.major(no) \
                and int(fields[1]) == os.minor(no):
            return fields[3]
    return 'Unknown'
