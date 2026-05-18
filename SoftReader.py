import winreg as wrg
from functools import total_ordering


@total_ordering
class SoftInfo():
    def __init__(self, key_name, name, version):
        self.key_name = key_name
        self.name = name
        self.version = version

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return f"{self.name}:{self.version}"

    def __repr__(self):
        return f"{self.name}:{self.version}"

    def __len__(self):
        return len(f"{str(self)}")

    def __iter__(self):
        return str(f"{self.name}:{self.version}").__iter__()

    def __getitem__(self, key):
        return str(self)[key]


class SoftReader:
    def __init__(self):
        self.lm = wrg.HKEY_LOCAL_MACHINE
        self.cu = wrg.HKEY_CURRENT_USER
        self.soft_key = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
        self.soft32_key = r"SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"

    def get_installed_software_list(self) -> list[SoftInfo]:
        installed = []
        installed.extend(self.__get_lm_soft_list__())
        installed.extend(self.__get_lm_soft32_list__())
        installed.extend(self.__get_cu_soft_list__())
        installed.extend(self.__get_cu_soft32_list__())
        return sorted(set(installed))

    def __get_lm_soft_list__(self):
        return self.__get_generic_soft_list__(self.lm, self.soft_key)

    def __get_lm_soft32_list__(self):
        return self.__get_generic_soft_list__(self.lm, self.soft32_key)

    def __get_cu_soft_list__(self):
        return self.__get_generic_soft_list__(self.cu, self.soft_key)

    def __get_cu_soft32_list__(self):
        return self.__get_generic_soft_list__(self.cu, self.soft32_key)

    def __get_generic_soft_list__(self, main_key, sub_key):
        hkey = None
        try:
            hkey = wrg.OpenKey(main_key, sub_key, 0, wrg.KEY_READ)
            return self.__read_registry__(hkey)
        except FileNotFoundError as err:
            print(err)
            return []
        finally:
            if hkey:
                wrg.CloseKey(hkey)

    def __read_registry__(self, hkey):
        soft = []
        for key_name in self.__enum_keys__(hkey):
            soft_info = self.__read_single_registry_key__(hkey, key_name)
            if soft_info:
                soft.append(soft_info)
        return soft

    def __enum_keys__(self, hkey):
        index = 0
        while True:
            try:
                yield wrg.EnumKey(hkey, index)
                index += 1
            except OSError:
                break

    def __read_single_registry_key__(self, hkey, key_name):
        try:
            with wrg.OpenKey(hkey, key_name) as hsubkey:
                return self.__read_soft_info__(hsubkey, key_name)
        except OSError:
            return None

    def __read_soft_info__(self, hsubkey, key_name):
        try:
            display_name = wrg.QueryValueEx(hsubkey, "DisplayName")[0]
            display_version = wrg.QueryValueEx(hsubkey, "DisplayVersion")[0]
            return SoftInfo(
                key_name,
                display_name,
                display_version
            )
        except OSError:
            return None


if __name__ == "__main__":
    reader = SoftReader()
    all_soft = reader.get_installed_software_list()
    for s in all_soft:
        print(s)
