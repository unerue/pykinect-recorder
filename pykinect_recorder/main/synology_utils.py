import argparse
import os

from synology_api import downloadstation, filestation


def upload(args: argparse.ArgumentParser):
    try:
        f1 = filestation.FileStation(
            args.Synology_Ip,
            args.Synology_Port,
            args.Username,
            args.Password,
            args.secure,
            args.cert_verify,
            args.dsm_version,
            args.debug,
            args.otp_code,
        )

        success = f1.upload_file(args.dest_path, args.file_path, verify=args.cert_verify)
        if type(success) == tuple:
            raise ConnectionAbortedError
        else:
            print(success)

    except ValueError:
        print("Connect Failed!! Please Check your ip, port, username, password, secure")

    except FileNotFoundError:
        print("file path does not exists!!! Please Check before run")

    except ConnectionAbortedError:
        print("dest path does not match!!! Please Check before run")


def download(args: argparse.ArgumentParser):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Synology Nas Upload/Download",
        description="Uploading video and audio which is recoded by Azure Kinect",
    )

    ## Synology nas
    parser.add_argument(
        "--Synology_Ip",
        type=str,
        default="hnvlab.synology.me",
        help="Set Ip address such as xxx.synology.me or 111.111.1.1",
    )
    parser.add_argument("--Synology_Port", type=str, default="", help="")
    parser.add_argument("--Username", type=str, default="", help="")
    parser.add_argument("--Password", type=str, default="", help="")
    parser.add_argument("--secure", type=bool, default=True, help="Set True if https is required")
    parser.add_argument(
        "--cert_verify",
        type=bool,
        default=True,
        help="Set True if you want to verify your certificate",
    )
    parser.add_argument("--dsm_version", type=int, default=7)
    parser.add_argument("--debug", type=bool, default=True)
    parser.add_argument("--otp_code", type=str, default=None)

    parser.add_argument(
        "--dest_path",
        type=str,
        default="/dataset/test",
        help="Destination path in synology nas",
    )
    parser.add_argument("--file_path", type=str, default="ecord_with_mic.py", help="Upload file path")

    args = parser.parse_args()
    # upload(args)
    download(args)
