
import re
import util


class VersionSlurper:
    def __init__(self, config_path: str):
        self.config = self.___load_config__(config_path)

    def ___load_config__(self, path):
        return util.load_config(path)

    def __get_latest_winget__(self, package_id):
        result = util.run_winget("show", package_id)
        if result.returncode != 0:
            return None
        return self.__extract_version__(result.stdout)

    def __extract_version__(self, output):
        if not output:
            return None
        match = re.search(r"Version:\s*(\S+)", output)
        return match.group(1) if match else None

    def get_latest_version(self, app: dict):
        if app["type"] == "winget":
            return self.__get_latest_winget__(app["id"])
        return ''

    def get_all_latest_versions(self):
        if not self.config or not self.config["apps"]:
            raise KeyError("Cannot load config properly")
        return {
            app["name"]: self.get_latest_version(app)
            for app in self.config["apps"]
        }


if __name__ == "__main__":
    slurper = VersionSlurper("config.json")
    res = slurper.get_all_latest_versions()
    print(res)
