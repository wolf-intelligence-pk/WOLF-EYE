#!/usr/bin/env bash

# Color definitions for styling
R='\033[91m'    # Red
G='\033[92m'    # Green
C='\033[96m'    # Cyan
W='\033[0m'     # White
Y='\033[93m'    # Yellow
B='\033[94m'    # Blue
M='\033[95m'    # Magenta
BL='\033[1m'    # Bold
GR='\033[90m'   # Gray

LOG_DIR=$PWD/logs
DB_DIR=$PWD/db
ILOG=$LOG_DIR/install.log

mkdir -p $LOG_DIR $DB_DIR

# Animated spinner function
spinner() {
    local pid=$1
    local message=$2
    local delay=0.1
    local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf "\r${M}[%c] ${C}%s${W}" "$spinstr" "$message"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
    done
    printf "\r${G}[*] ${C}%s${W}\n" "$message"
}

# Progress bar function without bc dependency
progress_bar() {
    local duration=$1
    local message=$2
    local width=40
    local sleep_time=$(awk "BEGIN {print $duration / $width}")
    
    for ((i=0; i<=width; i++)); do
        local percent=$((i * 100 / width))
        printf "\r${B}[${G}"
        for ((j=0; j<i; j++)); do printf "="; done
        printf "${GR}"
        for ((j=i; j<width; j++)); do printf "="; done
        printf "${B}] ${C}%d%% ${W}%s" $percent "$message"
        sleep $sleep_time
    done
    printf "\n"
}

# Clean ASCII banner
show_banner() {
    clear
    echo -e "\n${M}"
    echo -e "██╗    ██╗ ██████╗ ██╗     ███████╗"
    echo -e "██║    ██║██╔═══██╗██║     ██╔════╝"
    echo -e "██║ █╗ ██║██║   ██║██║     █████╗  "
    echo -e "██║███╗██║██║   ██║██║     ██╔══╝  "
    echo -e "╚███╔███╔╝╚██████╔╝███████╗██║     "
    echo -e " ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝     "
    echo -e "${W}"
    echo -e "███████╗██╗   ██╗███████╗"
    echo -e "██╔════╝╚██╗ ██╔╝██╔════╝"
    echo -e "█████╗   ╚████╔╝ █████╗  "
    echo -e "██╔══╝    ╚██╔╝  ██╔══╝  "
    echo -e "███████╗   ██║   ███████╗"
    echo -e "╚══════╝   ╚═╝   ╚══════╝"
    echo -e "\n${G}     INSTALLATION WIZARD${W}"
    echo -e "${C}     WOLF INTELLIGENCE PK${W}\n"
    sleep 1
}

# Status check
status_check() {
    if [ $? -eq 0 ]; then
        echo -e "${G}  [INSTALLED]${W} $1"
    else
        echo -e "${R}  [FAILED]${W} $1"
    fi
}

# System detection
detect_system() {
    echo -e "\n${Y}  SYSTEM DETECTION${W}\n"
    for i in {1..3}; do
        printf "\r${M}  Scanning system"
        for j in $(seq 1 $i); do
            printf "."
        done
        printf "${W}"
        sleep 0.2
    done
    echo -e "\n"
}

debian_install() {
    echo -e "\n${B}  INSTALLING FOR DEBIAN/UBUNTU${W}\n"
    echo -e '=====================\nINSTALLING FOR DEBIAN\n=====================\n' > "$ILOG"

    local pkgs="python3 python3-pip python3-requests python3-packaging python3-psutil php"
    local total=$(echo $pkgs | wc -w)
    local current=0
    local failed=0

    for pkg_name in $pkgs; do
        current=$((current + 1))
        echo -e "\n${C}  Package [$current/$total]: ${Y}$pkg_name${W}"
        
        sudo apt -y install $pkg_name &>> "$ILOG" &
        spinner $! "Installing $pkg_name"
        status_check $pkg_name
        if [ $? -ne 0 ]; then
            failed=$((failed + 1))
        fi
        echo -e '\n--------------------\n' >> "$ILOG"
    done
    
    return $failed
}

fedora_install() {
    echo -e "\n${B}  INSTALLING FOR FEDORA${W}\n"
    echo -e '=====================\nINSTALLING FOR FEDORA\n=====================\n' > "$ILOG"

    local pkgs="python3 python3-pip python3-requests python3-packaging python3-psutil php"
    local total=$(echo $pkgs | wc -w)
    local current=0
    local failed=0

    for pkg_name in $pkgs; do
        current=$((current + 1))
        echo -e "\n${C}  Package [$current/$total]: ${Y}$pkg_name${W}"
        
        sudo dnf install $pkg_name -y &>> "$ILOG" &
        spinner $! "Installing $pkg_name"
        status_check $pkg_name
        if [ $? -ne 0 ]; then
            failed=$((failed + 1))
        fi
        echo -e '\n--------------------\n' >> "$ILOG"
    done
    
    return $failed
}

termux_install() {
    echo -e "\n${B}  INSTALLING FOR TERMUX${W}\n"
    echo -e '=====================\nINSTALLING FOR TERMUX\n=====================\n' > "$ILOG"

    local pkgs="python php"
    local pip_pkgs="requests packaging psutil"
    local total=$(echo $pkgs $pip_pkgs | wc -w)
    local current=0
    local failed=0

    echo -e "${Y}  Installing System Packages...${W}\n"
    for pkg_name in $pkgs; do
        current=$((current + 1))
        echo -e "${C}  Package [$current/$total]: ${Y}$pkg_name${W}"
        
        apt -y install $pkg_name &>> "$ILOG" &
        spinner $! "Installing $pkg_name"
        status_check $pkg_name
        if [ $? -ne 0 ]; then
            failed=$((failed + 1))
        fi
        echo -e '\n--------------------\n' >> "$ILOG"
    done

    echo -e "\n${Y}  Installing Python Packages...${W}\n"
    for pkg_name in $pip_pkgs; do
        current=$((current + 1))
        echo -e "${C}  Package [$current/$total]: ${Y}$pkg_name${W}"
        
        pip install -U $pkg_name &>> "$ILOG" &
        spinner $! "Installing $pkg_name"
        status_check $pkg_name
        if [ $? -ne 0 ]; then
            failed=$((failed + 1))
        fi
        echo -e '\n--------------------\n' >> "$ILOG"
    done
    
    return $failed
}

arch_install() {
    echo -e "\n${B}  INSTALLING FOR ARCH LINUX${W}\n"
    echo -e '=========================\nINSTALLING FOR ARCH LINUX\n=========================\n' > "$ILOG"

    local pkgs="python3 python-pip python-requests python-packaging python-psutil php"
    local total=$(echo $pkgs | wc -w)
    local current=0
    local failed=0

    for pkg_name in $pkgs; do
        current=$((current + 1))
        echo -e "\n${C}  Package [$current/$total]: ${Y}$pkg_name${W}"
        
        yes | sudo pacman -S $pkg_name --needed &>> "$ILOG" &
        spinner $! "Installing $pkg_name"
        status_check $pkg_name
        if [ $? -ne 0 ]; then
            failed=$((failed + 1))
        fi
        echo -e '\n--------------------\n' >> "$ILOG"
    done
    
    return $failed
}

# Success message
show_success() {
    echo -e "\n${G}  *** INSTALLATION COMPLETE ***${W}\n"
}

# Warning message
show_warning() {
    local failed_count=$1
    echo -e "\n${Y}  WARNING: $failed_count package(s) failed to install${W}\n"
}

# Launch wolf-eye.py
launch_script() {
    echo -e "\n${M}  LAUNCHING WOLF-EYE...${W}\n"
    
    # Countdown
    for i in {3..1}; do
        printf "\r${C}  Starting in ${Y}%d${C}...${W}" $i
        sleep 0.5
    done
    printf "\r${G}  LAUNCHING NOW!          ${W}\n\n"
    sleep 0.5
    
    # Clear screen for clean start
    clear
    
    # Run wolf-eye.py with any passed arguments
    if [ -f "wolf-eye.py" ]; then
        echo -e "${G}  WOLF-EYE is now running...${W}\n"
        python3 wolf-eye.py "$@"
    elif [ -f "wolf-eye.py" ]; then
        echo -e "${G}  WOLF-EYE is now running...${W}\n"
        python3 wolf-eye.py "$@"
    else
        echo -e "${R}  wolf-eye.py not found!${W}"
        echo -e "${Y}  Please make sure the Python script is in the current directory${W}"
        echo -e "${C}  Current directory: ${W}$PWD${W}"
        echo -e "${C}  Available Python files:${W}"
        ls -la *.py 2>/dev/null || echo -e "${R}  No Python files found!${W}"
        exit 1
    fi
}

# Main execution
main() {
    show_banner
    detect_system
    
    echo -e "${C}  Installing Dependencies...${W}\n"
    progress_bar 1.5 "Preparing installation"
    
    local failed=0

    if [ -f '/etc/arch-release' ]; then
        arch_install
        failed=$?
    elif [ -f '/etc/fedora-release' ]; then
        fedora_install
        failed=$?
    else
        if [ -z "${TERMUX_VERSION}" ]; then
            debian_install
            failed=$?
        else
            termux_install
            failed=$?
        fi
    fi

    echo -e '\n=========\nCOMPLETED\n=========\n' >> "$ILOG"

    echo -e "\n${G}[+]${C} Log Saved: ${W}$ILOG${W}"
    
    if [ $failed -eq 0 ]; then
        show_success
        echo -e "${G}  All packages installed successfully!${W}"
        echo -e "${C}  Auto-launching WOLF-EYE...${W}\n"
        sleep 2
        launch_script "$@"
    else
        show_warning $failed
        echo -e "${Y}  Some packages failed to install.${W}"
        echo -e "${Y}  Attempting to launch anyway...${W}\n"
        sleep 2
        launch_script "$@"
    fi
}

# Run main function with all script arguments
main "$@"