# FTP Upload

This is a simple FTP upload script for uploading files to a FTP server.

## Usage

```bash
$ ./ftp_upload.sh <arguments>=<value>
```

## Arguments
| Argument | Short | Description                        | Example                    |
| -------- |-------|------------------------------------|----------------------------|
| `--path` | `-p`  | The path to the file to upload     | `-p /home/user/file.txt`   |
| `--remote` | `-r`  | The remote directory to upload to | `-r /remote/path/file.txt` |
| `--host` | `-h`  | The FTP host                       | `-h ftp.example.com`       |
| `--user` | `-u`  | The FTP user                       | `-u user`                  |
| `--password` | `-pw`  | The FTP password                   | `-pw password`             |

## Example

```shell
# Upload file.txt to ftp.example.com in the /remote/path/ directory
# Final path on remote will be /remote/path/file.txt
python ftp_upload.py -p /home/user/file.txt -r /remote/path/ -h ftp.example.com -u user -pw password

# Upload ExampleFolder to ftp.example.com in the /remote/path/ directory
# Final path on remote will be /remote/path/ExampleFolder
python ftp_upload.py -p /home/user/ExampleFolder -r /remote/path/ -h ftp.example.com -u user -pw password
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
