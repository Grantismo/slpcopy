import os
import io
import shutil
import psutil
import pathlib
import humanize
import dataclasses
from gooey import Gooey, GooeyParser
import sys
import slpname

in_terminal = False
try:
    sys.stdout.write('\n')
    sys.stdout.flush()
    in_terminal = True
except AttributeError:
    # dummy class to export a "do nothing methods", expected methods to be
    # called (read, write, flush, close)
    class Dummy:
        def __getattr__(*args):
            return lambda *args: None

    for x in ('stdout', 'stderr', 'stdin'):
        setattr(sys, x, Dummy())

from colored import stylize, attr, fg  # depends on stdout
try:
    import win32com.client
except BaseException:
    pass
try:
    import dbus
except BaseException:
    pass

FS_TYPES = set(['fat16', 'fat32', 'vfat', 'fat'])
SLP_EXTENSION = '*.slp'


@dataclasses.dataclass
class Drive:
    name: str
    device: str
    mountpoint: str
    size: int
    files: list

    def human_size(self):
        return humanize.naturalsize(self.size)

    def display_name(self):
        return self.name if self.name else self.device


def get_drive_names():
    if 'win32com.client' in sys.modules:
        wmi_service = win32com.client.Dispatch('WbemScripting.SWbemLocator')
        swbem_serivces = wmi_service.ConnectServer('.', 'root\\cimv2')
        return {
            item.DeviceId +
            '\\': item.VolumeName for item in swbem_serivces.ExecQuery("SELECT * from Win32_LogicalDisk")}
    # Linux
    if 'dbus' in sys.modules:
        bus = dbus.SystemBus()
        ud_manager_obj = bus.get_object(
            'org.freedesktop.UDisks2',
            '/org/freedesktop/UDisks2')
        ud_manager = dbus.Interface(
            ud_manager_obj,
            'org.freedesktop.DBus.ObjectManager')
        device_to_names = {}
        for k, v in ud_manager.GetManagedObjects().items():
            drive_info = v.get('org.freedesktop.UDisks2.Block', {})
            label = drive_info.get('IdLabel', '')
            if label:
                device = bytearray(
                    drive_info.get('Device')).replace(
                    b'\x00', b'').decode('utf-8')
                device_to_names[device] = label
        return device_to_names
    return {}


def get_drives():
    drive_names = get_drive_names()
    drives = []
    for device in psutil.disk_partitions():
        if device.fstype.lower() not in FS_TYPES or device.mountpoint == '/boot/efi':
            continue
        drive = Drive(
            device=device.device,
            name=drive_names.get(device.device, ''),
            mountpoint=device.mountpoint,
            size=psutil.disk_usage(
                device.mountpoint).total,
            files=[])

        print(
            stylize(
                'Searching device {} ({})'.format(
                    drive.display_name(),
                    drive.human_size()),
                fg('light_blue')))
        slp_files = find_slp_files(drive)
        if slp_files:
            print(
                stylize(
                    'Found {} slp replay files.'.format(
                        len(slp_files)),
                    fg('light_blue') +
                    attr('bold')))
            drive.files = slp_files
        else:
            print(stylize('Found no slp replay files.', fg('light_gray')))
        print()
        drives.append(drive)
    return drives


def find_slp_files(drive):
    return list(pathlib.Path(drive.mountpoint).rglob(SLP_EXTENSION))


def replay_folder_name(num):
    return 'Setup {:03d}'.format(num)


def resource_path(path):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, path)

def rename_slp_file(target_path):
    destination_name = slpname.descriptive_filename(target_path)
    os.rename(target_path, os.path.join(os.path.dirname(target_path), destination_name))

def copy_and_delete_original(target_file, destination_folder, delete_original=False, rename=False):
    try:
        copied_path = shutil.copy2(target_file, destination_folder)
        if rename:
            # rename after copy for faster IO
            rename_slp_file(copied_path)
    except IOError as e:
        print(
            stylize(
                'Unable to copy file {}. {}'.format(
                    target_file,
                    e),
                fg('red') +
                attr('bold')))
        return False
    if delete_original:
        target_file.unlink()
    return True



def get_numbered_folder_path(output_path, cur_dir=0):
    while True:
        folder_path = pathlib.Path(output_path).joinpath(
            replay_folder_name(cur_dir))
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=False)
            break
        cur_dir += 1
    return folder_path, cur_dir


def get_folder_path(output_path, folder_name):
    folder_path = pathlib.Path(output_path).joinpath(folder_name)
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=False)
    return folder_path

def print_args(args):
    print(stylize('===== Settings =====', fg('light_gray')))
    print(
        stylize(
            'Remove after copy: {}'.format(
                args.remove_after_copy),
            fg('light_gray')))
    print(
        stylize(
            'Use custom drive names: {}'.format(
                args.use_custom_drive_names),
            fg('light_gray')))
    print(
        stylize(
            'Rename files: {}'.format(
                args.rename_files),
            fg('light_gray')))
    print()

def copy_files(drives, args):
    output_path = pathlib.Path(args.output_path)
    total_files = sum(len(d.files) for d in drives)
    i = 0
    cur_dir = 1
    if not total_files:
        print(stylize('No files to copy.', fg('dark_gray') + attr('bold')))
    for drive in drives:
        if not drive.files:
            continue
        if args.use_custom_drive_names and drive.name:
            folder_path = get_folder_path(output_path, drive.name)
        else:
            folder_path, cur_dir = get_numbered_folder_path(
                output_path, cur_dir)

        successful_copies = 0
        for f in drive.files:
            print('progress: {}/{}'.format(i + 1, total_files))
            sys.stdout.flush()
            if copy_and_delete_original(
                    f, folder_path, delete_original=args.remove_after_copy, rename=args.rename_files):
                successful_copies += 1
            i += 1
        if successful_copies > 0:
            print(
                stylize(
                    'Copied {} slp replay files from {} to {}'.format(
                        successful_copies,
                        drive.display_name(),
                        folder_path.resolve()),
                    fg('green')))
            if args.remove_after_copy:
                print(
                    stylize(
                        'Deleted {} replay files from {}'.format(
                            successful_copies,
                            drive.display_name()),
                        fg('green')))
        if successful_copies != len(drive.files):
            print(stylize('Unable to copy {} files.'.format(
                len(drive.files) - successful_copies), fg('red') + attr('bold')))

def run(args):
    drives = get_drives()
    if drives:
        print(stylize(
            'Searching {} connected drives for *.slp files.'.format(len(drives)), attr('bold')))
    else:
        print(
            stylize(
                'No conncted drives to search.',
                fg('dark_gray') +
                attr('bold')))
    copy_files(drives, args)
    print(stylize('Complete.\n\n', fg('green') + attr('bold')))


@Gooey(program_name='SlpCopy',
       progress_regex=r'^progress: (?P<current>\d+)/(?P<total>\d+)$',
       progress_expr='current / total * 100',
       requires_shell=in_terminal,
       richtext_controls=True,
       hide_progress_msg=True,
       image_dir=resource_path('img'),
       default_size=(610, 700),
       timing_options={
           'show_time_remaining': not in_terminal,
           'hide_time_remaining_on_complete': not in_terminal,
       })
def main():
    parser = GooeyParser(
        description='blorppppp\'s *.slp copy tool. Copies all *.slp files from thumbdrives onto your machine.')
    parser.add_argument(
        'output_path',
        metavar='Output Path',
        help='The directory to copy *.slp files into.',
        widget='DirChooser')
    parser.add_argument(
        '--remove_after_copy',
        metavar='Remove after copy',
        help='Delete original *.slp files off thumbdrives after succesfully copying to your machine.',
        action='store_true',
        default=True,
        widget='BlockCheckbox')
    parser.add_argument(
        '--use_custom_drive_names',
        metavar='Use custom drive names',
        help='Copy *.slp files into a folder with each thumbdrive\'s custom name (if applicable). If unchecked a new folder will be created for each drive (e.g. "Setup 001")',
        action='store_true',
        default=True,
        widget='BlockCheckbox')
    parser.add_argument(
        '--rename_files',
        metavar='Rename files',
        help='Rename *.slp files into a more human readable format.\n"Game_20211025T160457.slp" -> "20211025T160457 - Fox (Green) vs Samus (Green) - Battlefield.slp"',
        action='store_true',
        default=True,
        widget='BlockCheckbox')

    args = parser.parse_args()
    print_args(args)
    run(args)



if __name__ == '__main__':
    main()
