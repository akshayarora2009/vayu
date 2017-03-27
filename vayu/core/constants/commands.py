class Linux:
    get_all_details="uname -a"
    get_kernal_name = "uname -s"
    get_node_name = "uname -n"
    get_kernal_release = "uname -r"
    get_kernal_version = "uname -v"
    get_machine = "uname -m"
    get_processor = "uname -p"
    get_hardware = "uname -i"
    get_operating_system = "uname -o"
    make_dir = "mkdir -p "
    ping = "ping "
    ping_complete = " -w 5 | grep rtt"
    lsb_release = "lsb_release -a"


    class Ubuntu:
        apt_update= "apt-get update"
        install_git= "apt-get install git"
        check_git = "git --version"
