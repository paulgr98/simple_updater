from SoftReader import SoftReader
from VersionSlurper import VersionSlurper
from packaging import version
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import util


class OutdatedSoftware:
    def __init__(self, name, current, latest):
        self.name = name
        self.current_version = current
        self.latest_version = latest

    def __str__(self):
        return f"{self.name}: {self.current_version} -> {self.latest_version}"

    def __repr__(self):
        return f"{self.name}: {self.current_version} -> {self.latest_version}"


class Updater:
    def __init__(self, config_path):
        self.config_path = config_path
        self.reader = SoftReader()
        self.slurper = VersionSlurper(self.config_path)

    def check_for_updates(self) -> list[OutdatedSoftware]:
        soft_list = self.reader.get_installed_software_list()
        try:
            versions = self.slurper.get_all_latest_versions()
        except KeyError as exc:
            print(f"Woopsie, something went wrong: {exc}")
            exit()
        return self.__find_outdated_software__(soft_list, versions)

    def __find_outdated_software__(self, soft_list, versions) -> list[OutdatedSoftware]:
        outdated_apps = []
        for name, latest_version in versions.items():
            installed_version = self.__find_installed_version__(
                name, soft_list
            )
            if self.__is_outdated__(installed_version, latest_version):
                outdated_apps.append(
                    OutdatedSoftware(
                        name,
                        installed_version,
                        latest_version
                    )
                )
        return outdated_apps

    def __find_installed_version__(self, name, soft_list):
        best_match = process.extractOne(
            name,
            soft_list,
            scorer=fuzz.token_sort_ratio
        )[0]
        _, installed_version = str(best_match).split(':')
        return installed_version

    def __is_outdated__(self, installed_version, latest_version):
        if not installed_version or not latest_version:
            return False
        try:
            return version.parse(latest_version.strip()) > version.parse(installed_version.strip())
        except Exception as exc:
            print(
                f"Cannot compare versions: installed={installed_version}, "
                f"latest={latest_version}. Reason: {exc}"
            )
            return False

    def update(self, software: OutdatedSoftware):
        package_id = self.__get_package_id__(software.name)
        result = self.__run_winget_update__(package_id)
        self.__handle_update_result__(result)

    def __get_package_id__(self, software_name):
        app = self.__find_app__(software_name)
        if not app:
            raise ValueError(f"Software not found: {software_name}")
        return app["id"]

    def __find_app__(self, software_name):
        config = util.load_config(self.config_path)
        return next(
            (
                app for app in config["apps"]
                if app["name"] == software_name
            ),
            None
        )

    def __run_winget_update__(self, package_id):
        return util.run_winget("update", package_id)

    def __handle_update_result__(self, result):
        if result.returncode != 0:
            return
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)

    def update_all(self, software_list: list[OutdatedSoftware]):
        for software in software_list:
            self.update(software)


if __name__ == "__main__":
    updater = Updater("config.json")
    outdated = updater.check_for_updates()
    print(outdated)
    updater.update_all(outdated)
