class Linux:
    get_all_details="uname -a"
    get_kernal = "uname -s"
    get_node_name = "uname -n"
    get_kernal_release = "uname -r"
    get_kernal_version = "uname -v"
    get_machine = "uname -m"
    get_processor = "uname -p"
    get_hardware = "uname -h"
    get_operating_system = "uname -o"

    class Ubuntu:
        apt_update= "apt-get update"
        install_git= "apt-get install git"
        check_git = "git --version"