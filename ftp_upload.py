import ftplib
import sys
from pathlib import Path

DEFAULT_HOST = '64.226.79.119'
DEFAULT_USER = 'root'
DEFAULT_PASSWORD = 'rootroot'


def _parse_arguments():
    path = ""
    remote = '/'
    host = DEFAULT_HOST
    user = DEFAULT_USER
    password = DEFAULT_PASSWORD
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith('--path='):
            path = arg.replace('--path=', '')
        elif arg.startswith('--remote='):
            remote = arg.replace('--remote=', '')
        elif arg.startswith('--host='):
            host = arg.replace('--host=', '')
        elif arg.startswith('--user='):
            user = arg.replace('--user=', '')
        elif arg.startswith('--password='):
            password = arg.replace('--password=', '')

        elif arg.startswith('-p='):
            path = arg.replace('-p=', '')
        elif arg.startswith('-r='):
            remote = arg.replace('-r=', '')
        elif arg.startswith('-h='):
            host = arg.replace('-h=', '')
        elif arg.startswith('-u='):
            user = arg.replace('-u=', '')
        elif arg.startswith('-pw='):
            password = arg.replace('-pw=', '')
        elif arg == '-h' or arg == '--help':
            print()
            print('Help: ')
            print('     --path=<value> or -p=<value>: Path to file or directory to upload')
            print('     --remote=<value> or -r=<value>: Remote directory to upload to')
            print('     --host=<value> or -h=<value>: Host to connect to')
            print('     --user=<value> or -u=<value>: User to connect with')
            print('     --password=<value> or -pw=<value>: Password to connect with')
            print('     --help or -h: Show this help')
            print()
            exit(0)
        else:
            print('Invalid argument: ' + arg + '. Help: ftp_upload.py -h')
            exit(-1)

    if path == "":
        print('Path is required. Help: ftp_upload.py -h')
        exit(-1)

    return path, remote, host, user, password


def _upload_file(ftp_session, local, remote):
    with open(local, 'rb') as file:
        try:
            ftp_session.storbinary('STOR ' + remote, file)
        except ftplib.all_errors as e:
            print(e)
            raise


def _create_dir_if_not_exist(ftp_session, remote_dir_path):
    try:
        ftp_session.mkd(remote_dir_path)
    except ftplib.all_errors as e:
        if e.args[0].startswith('550'):
            print('Directory already exists: ' + remote_dir_path + ' Skipping...')
        else:
            print(e)
            raise


def file_upload(ftp_session, target, remote_dir_path='/'):
    if remote_dir_path != '/':
        _create_dir_if_not_exist(ftp_session, remote_dir_path)
    _upload_file(ftp_session, target, remote_dir_path + '/' + target.name)


def dir_file_upload(ftp_session, target, remote_dir_path='/'):
    all_files = list(target.rglob('*'))
    all_dirs = [file for file in all_files if file.is_dir()]
    all_dirs.insert(0, target)
    if remote_dir_path != '/':
        paths = remote_dir_path.split('/')
        paths = [x for x in paths if x.strip() != '']
        for i in range(len(paths)):
            path = '/'.join(paths[:i + 1])
            _create_dir_if_not_exist(ftp_session, path)

    all_remote_dirs = [str(file).replace(str(target.parent), '') for file in all_dirs]
    all_files = [file for file in all_files if file.is_file()]
    all_remote_files = [str(file).replace(str(target.parent), '') for file in all_files]
    all_remote_files = [remote_dir_path + file for file in all_remote_files]

    for remote_dir in all_remote_dirs:
        remote_dir = remote_dir.replace('\\', '/')
        if remote_dir[0] == '/':
            remote_dir = remote_dir[1:]
        remote_dir = remote_dir_path + remote_dir
        _create_dir_if_not_exist(ftp_session, remote_dir)

    for i in range(len(all_files)):
        print('Uploading file: ' + str(i + 1) + '/' + str(len(all_files)), end='\r')
        remote_file = all_remote_files[i]
        remote_file = remote_file.replace('\\', '/')
        local_file = all_files[i]
        _upload_file(ftp_session, local_file, remote_file)


def main():
    path, remote, host, user, password = _parse_arguments()
    session = ftplib.FTP(host, user, password)
    print('Connected to: ' + DEFAULT_HOST)
    target_path = Path(path)
    if target_path.is_dir():
        print('Uploading directory: ' + str(target_path))
        dir_file_upload(session, target_path.absolute(), remote)
    else:
        print('Uploading file: ' + str(target_path) + ' to ' + remote)
        file_upload(session, target_path.absolute(), remote)

    session.quit()
    print('\nUpload complete!')


if __name__ == '__main__':
    main()
