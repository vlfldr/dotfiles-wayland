#! /bin/bash

# exit on no args
if [ $# -eq 0 ]; then
 echo "usage: sudo ./setup.sh \$USER"
 exit 1
fi

cd "/home/$1" || exit 1 

echo "Updating system packages. This will take a while..."
dnf upgrade --refresh -y

echo "Installing and configuring git..."
dnf install -y git
echo ".cfg" >> .gitignore

echo "Cloning and checking out dotfiles..."
sudo -u "$1" git clone --bare "https://github.com/vlfldr/dotfiles-wayland" "./.cfg"
config() {
    /usr/bin/git --git-dir=.cfg/ --work-tree=. "$@"
}
config checkout
config config --local status.showUntrackedFiles no

echo "Applying dnf settings..."
mv ./.config/setup/dnf.conf /etc/dnf/dnf.conf
mv ./.config/setup/*.repo /etc/yum.repos.d/

echo "Installing RPM fusion repositories..."
dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-"$(rpm -E %fedora)".noarch.rpm
dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-"$(rpm -E %fedora)".noarch.rpm

echo "Updating repo keys..."
dnf upgrade -y

echo "Installing rice packages..."
dnf install -y ImageMagick bat bluez borgbackup cava codium fish freeglut fzf git grim slurp kernel-modules-extra \
kernel-tools hyprland kitty light lsd mpv ncmpcpp neofetch neovim network-manager-applet python3-pillow ranger \
rpmfusion-free-release rpmfusion-nonfree-release swww sxiv wayland-logout wofi eww

dnf install -y .config/setup/gotop*.rpm
rm -f .config/setup/gotop*.rpm

# fix wayland DPI bug with custom .desktop entry
desktop-file-install ".local/share/applications/codium.desktop"

# echo "Installing eww dependencies..."
# dnf install -y gtk3-devel gdk-pixbuf2-devel cairo-devel glib2-devel glibc-devel libgcc gtk-layer-shell-devel pango-devel

# echo "Downloading and configuring rust..."
# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# source "$HOME/.cargo/env"

# echo "Downloading and building eww..."
# git clone https://github.com/elkowar/eww
# cd eww && cargo build --release --no-default-features --features=wayland

# echo "Installing eww..."
# chmod a+x ./target/release/eww && mv ./target/release/eww /usr/bin/eww

# echo "Cleaning up..."
# cd ..
# rm -rf ./eww "$HOME/.rustup"

echo "Setting default shell to fish..."
sudo -u "$1" chsh -s /usr/bin/fish

echo "Installing Cozette font..."
mkdir -p /usr/local/share/fonts/cozette
mv .config/setup/CozetteVector.otf /usr/local/share/fonts/cozette
chown -R root: /usr/local/share/fonts/cozette
chmod 644 /usr/local/share/fonts/cozette/*
restorecon -RF /usr/local/share/fonts/cozette
su -c "fc-cache -r 2&>1" - "$1"

echo "Installing Neovim plugins..."
su -c "nvim --headless -c 'autocmd User PackerComplete quitall' -c 'PackerSync'" - "$1"

read -r -p "Install VS Codium (open source VS Code) themes & extensions? [y/n]: " input
case $input in [yY])
    su -c "xargs -n1 codium --install-extension" - "$1" < ".config/setup/rice_extensions_list.txt"
    ;; *)
esac

read -r -p "Install python LSP sesyrver? [y/n]: " input
case $input in [yY]) dnf install python-lsp-server ;; *) esac

read -r -p "Install bash LSP server? [y/n]: " input
case $input in [yY]) dnf install nodejs-bash-language-server;; *) esac

read -r -p "Download and theme Firefox Nightly? [y/n]: " input
case $input in [yY])
    wget --content-disposition "https://download.mozilla.org/?product=firefox-nightly-latest-ssl&os=linux64&lang=en-US"
    tar -xvf ./firefox-*.tar.bz2 --directory=/opt
    rm -rf ./firefox-*.tar.bz2
    desktop-file-install ".local/share/applications/nightly.desktop"

    ###
    # TODO: firefox rice
    ###
    ;; *)
esac

read -r -p "Download and apply KDE theme? [y/n]: " input
case $input in [yY])
    ###
    # TODO: KDE, gtk, cursor theme
    ###
    ;; *)
esac

echo ""
echo "Setup complete! To use mpd/ncmpcpp, mount or move your library to ~/music."
echo "Please reboot and select the Hyprland session at login. "
read -r -p "Would you like to reboot now? [y/n]: " input

case $input in [yY])
    reboot;; *)
    exit 0;;
esac
