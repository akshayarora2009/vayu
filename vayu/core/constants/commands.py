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
    moveToDirectory = "cd "


    class Ubuntu:
        apt_update= "apt-get update"
        install_git= "apt-get install git"
        check_git = "git --version"
        check_node = "node -v"
        install_npm = "sudo apt-get -y install npm"
        install_nvmfromnpm = "npm install nvm"
        install_nodefromnpm = "npm install node"
        install_node_legacy = "sudo apt-get -y install nodejs-legacy"
        install_node_js = "sudo apt-get -y install nodejs"
        install_node = "sudo apt-get -y install node"
        run_nodejsappplication = "node "


