from Updater import Updater


def main():
    updater = Updater("config.json")
    print("Checking for updates...")
    outdated = updater.check_for_updates()
    if not outdated:
        print("Everything is up to date!")
        return
    print("Performing updates:")
    for soft in outdated:
        print(soft)
    updater.update_all(outdated)


if __name__ == "__main__":
    main()
