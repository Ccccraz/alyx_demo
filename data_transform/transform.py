from gc import is_finalized
import os
from typing import Union
from pathlib import Path
from io import BufferedReader
from smbclient import register_session, open_file, stat
import smbclient
import smbprotocol
import smbprotocol.exceptions
from tqdm.auto import tqdm


class SmbClient:
    def __init__(
        self, server: str, share_name: str, username: str, password: str
    ) -> None:
        self.server = server
        self.share_name = share_name
        register_session(server=server, username=username, password=password)

    def _ensure_remote_dir(self, target):
        directory, filename = target.rsplit("\\", 1)
        directory = directory + "\\"
        try:
            smbclient.makedirs(directory, exist_ok=True)
        except smbprotocol.exceptions.SMBOSError as e:
            print(e)

    def _ensure_local_dir(self, data: Path):
        try:
            data.parent.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            pass

    def copy_file(self, fsrc: BufferedReader, fdst: BufferedReader, file_size):
        buf_size = 1024
        with tqdm(
            total=file_size, unit="B", unit_scale=True, unit_divisor=1024
        ) as pbar:
            while True:
                buf = fsrc.read(buf_size)
                if not buf:
                    break
                fdst.write(buf)
                pbar.update(len(buf))

    def upload(self, data: Union[str, Path], base_path: Path):
        target = self.convert_remote_path(Path(data), base_path)
        self._ensure_remote_dir(target)
        file_size = os.path.getsize(data)
        with open(data, mode="rb") as local_fh:
            with open_file(target, mode="wb") as remote_fh:
                self.copy_file(local_fh, remote_fh, file_size)  # type: ignore

    def _download(self, data: Union[str, Path], target: str):
        self._ensure_local_dir(Path(data))

        file_size = stat(target).st_size
        with open_file(target, mode="rb") as remote_fh:
            with open(data, mode="wb") as local_fh:
                self.copy_file(remote_fh, local_fh, file_size)  # type: ignore

    def download(self, data: Union[str, Path], base_path: Path):
        target = self.convert_remote_path(Path(data), base_path)
        files = smbclient.listdir(target)
        for file in files:
            file_path = rf"{target}\{file}"
            data_path = Path(data).joinpath(file)
            self._download(data_path, file_path)

    def convert_remote_path(self, data: Path, base_path: Path) -> str:
        smb_path = str(data.relative_to(base_path))
        smb_path = rf"\\{self.server}\{self.share_name}\{smb_path}"
        return smb_path


# TODO
if __name__ == "__main__":
    client = SmbClient(r"172.16.102.77", "cog_platform", "cog_platform", "uScSjM5*fh5Z")
    # data = Path(r".\data\YangLab\Subjects\0589\2024-11-07\001\alf\mock.table.pqt")
    # data = Path.cwd().joinpath(data)

    # client.upload(data, Path.cwd().joinpath("data"))

    local_path = Path(
        r"d:\projects\engineering\alyx_demo\get_data\YangLab\Subjects\0589\2024-11-07\003"
    )

    client.download(local_path.joinpath("alf"), Path.cwd().joinpath("get_data"))
