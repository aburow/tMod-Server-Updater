import requests
import wget
import json
import os
import sys
import shutil


class VersionUpdate:
    def __init__(self) -> None:
        self.root_dir = "/root"
        self.installed_version = self.get_latest_version()
        self.latest_version = self.get_installed_version()

        self.data_dir = ".local/share/Terraria"

        self.image_url = ("https://github.com/tModLoader/tModLoader/releases/"
                          "latest")
        self.log_file = f"{self.root_dir}/tModLoader/tModLoader-Logs/server.log"

    def get_latest_version(self) -> str:
        """Returns the latest version of tmodloader from the official Github
            releases page.

        Calls are pointed to a redirection page at Github, a URL is passed back
        and the end of the URL gives the latest version number.
        """
        r = requests.get(self.image_url)
        return r.url.split("/v")[-1]  # last part is the version

    def get_installed_version(self) -> str:
        """Returns the currently installed version of tmodloader.

        This function looks at the first line of the logfile and extracts the
        version number.
        """
        try:
            with open("version_update.json", "r") as vu:
                jvu = json.load(vu)
                version = jvu.get("version")
                if version is not None:
                    return version

        except FileNotFoundError:
            print("version_update.json not found")

        with open(self.log_file, "r") as f:
            first_line = f.readline().strip("\n").split("+")
            version_is = first_line[1].split("|")
        return version_is[0]  # first part is the version

    def backup_execs(self) -> ...:
        """Does a full backup of the current running server executables in-situ.

        The backup can be restored directly back into the original directory or
        copied to another server for deployment.

        Returns:
            Nothing intelligible at the moment. ahem I mean, not implemented.
        """
        shutil.make_archive(
            f"./tMod-execs-{self.installed_version}",
            "gztar",
            f"{self.root_dir}/",
            "tModLoader")
        result = shutil.move(
            f"./tMod-execs-{self.installed_version}.tar.gz",
            "./backup")
        return result

    def backup_datafiles(self) -> ...:
        """Does a full backup of the current servers data files, including maps and
            plugins.

        Returns:
            Nothing intelligible at the moment. ahem I mean, not implemented.
        """
        shutil.make_archive(
            f"./tMod-datafiles-{self.installed_version}",
            "gztar",
            f"{self.root_dir}/",
            ".local/share/Terraria")
        result = shutil.move(
            f"./tMod-datafiles-{self.installed_version}.tar.gz",
            "./backup")
        return result

    @staticmethod
    def move_current_dir(version_number: str) -> None:
        """Renames the "tModLoader" directory to the format "tModLoader-v{
            version_number}"

        Parameters:
            version_number (str): The version number.
        """
        result = os.rename("tModLoader", f"tModLoader-v{version_number}")
        return result

    @staticmethod
    def make_new_dir() -> None:
        """Makes a new "tModLoader" directory.
        """
        result = os.mkdir("tModLoader")
        return result

    def get_latest_zip(self) -> str:
        """Gets the requested version of the tModLoader installation files.

        Parameters:
            version (str): The version that you want to download.
        """
        image_file = (
            "https://github.com/tModLoader/tModLoader/releases/download/"
            f"v{self.latest_version}/tModLoader.zip")
        result = wget.download(
            image_file,
            out=f"tModLoader/tModLoader-v{self.latest_version}.zip")
        return result

    def server_setup(self) -> ...:
        """Unpack the server distribution zip.

        Precondition:
            The version is already downloaded and in the expected location.
        """
        image_file = f"tModLoader/tModLoader-v{self.latest_version}.zip"
        extract_dir = "/root/tModLoader"
        result = shutil.unpack_archive(image_file, extract_dir)
        return result

    @staticmethod
    def deploy_startfiles() -> ...:
        """Redeploy config and startup shell files to new directory structure.
        """
        image_file = "tModBootScripts.tgz"
        result = shutil.unpack_archive(image_file)

        return result

    def precheck(self) -> bool:
        if self.latest_version == self.installed_version:
            quit(0)
        quit(42)

    def main(self) -> None:
        print("Start Check")
        print(f"Latest Release    : {self.latest_version}")
        print(f"Installed Release : {self.installed_version}")
        check = self.latest_version != self.installed_version
        print(f"Update Status     : {check}")
        if check:
            print("Backup Executables: ", end='')
            print(self.backup_execs())
            print("Backup Data Files : ", end='')
            print(self.backup_datafiles())
            print("Move Current Inst.: ", end='')
            print(self.move_current_dir())
            print("Prepare Directory : ", end='')
            print(self.make_new_dir())
            print("Retrieve File     : ", end='')
            print(self.get_latest_zip())
            print("Unzip New Server  : ", end='')
            print(self.server_setup())
            print("Deploy Start Files: ", end='')
            print(self.deploy_startfiles())
            print("You can now reboot")


if __name__ == "__main__":
    vu = VersionUpdate()

    args = sys.argv[1:]
    filename = os.path.basename(__file__)

    if len(args) != 1 or args[0] not in ["check", "upgrade"]:
        print(f"USAGE: {filename} <check|upgrade>")
        quit(2)

    if args[0] == "check":
        print(f"Installed Release : {vu.installed_version}")
        print(f"Latest Release    : {vu.latest_version}")
        check = vu.latest_version != vu.installed_version
        print(f"Update Status     : {check}\n")
        vu.precheck()

    if args[0] == "update":
        vu.main()
        quit(88)
