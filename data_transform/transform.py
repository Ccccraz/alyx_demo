import os
from typing import Union
from pathlib import Path
from io import BufferedReader
from smbclient import register_session, open_file, stat
from tqdm.rich import tqdm


class SmbClient:
    def __init__(self, server: str, username: str, password: str) -> None:
        register_session(server=server, username=username, password=password)

    def copy_file(self, fsrc: BufferedReader, fdst: BufferedReader, file_size):
        buf_size = 1024 * 1024
        with tqdm(
            total=file_size, unit="B", unit_scale=True, unit_divisor=1024
        ) as pbar:
            while True:
                buf = fsrc.read(buf_size)
                if not buf:
                    break
                fdst.write(buf)
                pbar.update(len(buf))

    def upload(self, data: Union[str, Path], target: Union[str, Path]):
        file_size = os.path.getsize(data)
        with open(data, mode="rb") as local_fh:
            with open_file(target, mode="wb") as remote_fh:
                self.copy_file(local_fh, remote_fh, file_size)  # type: ignore

    def download(self, data: Union[str, Path], target: Union[str, Path]):
        file_size = stat(data).st_size
        with open_file(target, mode="rb") as remote_fh:
            with open(data, mode="=wb") as local_fh:
                self.copy_file(remote_fh, local_fh, file_size)  # type: ignore


# TODO
if __name__ == "__main__":
    client = SmbClient("server", "user", "pass")
