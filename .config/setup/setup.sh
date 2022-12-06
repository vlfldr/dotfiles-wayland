#! /bin/bash

# exit on no args
if [ $# -eq 0 ]; then
 echo "usage: sudo ./setup.sh \$USER"
 exit 1
fi

cd "/home/$1"

echo "Updating system packages. This will take a while..."
dnf upgrade --refresh -y

echo "Installing and configuring git..."
dnf install -y git
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
echo ".cfg" >> .gitignore

echo "Cloning and checking out dotfiles..."
git clone --bare https://github.com/vlfldr/dotfiles-wayland "./.cfg"
config checkout
config config --local status.showUntrackedFiles no

echo "Applying dnf settings..."
mv ./.config/setup/dnf.conf /etc/dnf/dnf.conf
mv ./.config/setup/*.repo /etc/yum.repos.d/

echo "Installing RPM fusion repositories..."
dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

echo "Updating repo keys..."
dnf upgrade -y

echo "Installing rice packages..."
dnf install -y ImageMagick bat bluez borgbackup cava codium fish freeglut fzf git grim slurp kernel-modules-extra \
kernel-tools hyprland kitty light lsd mpv ncmpcpp neofetch neovim network-manager-applet python3-pillow ranger \
rpmfusion-free-release rpmfusion-nonfree-release swww sxiv wayland-logout wofi

dnf install -y ./*gotop*.rpm

echo "Installing eww dependencies..."
dnf install -y gtk3-devel gdk-pixbuf2-devel cairo-devel glib2-devel glibc-devel libgcc gtk-layer-shell-devel pango-devel

echo "Downloading and configuring rust..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

echo "Downloading and building eww..."
git clone https://github.com/elkowar/eww
cd eww && cargo build --release --no-default-features --features=wayland

echo "Installing eww..."
chmod +x ./target/release/eww && mv ./target/release/eww /usr/bin/eww

echo "Cleaning up..."
cd ..
rm -rf ./eww "$HOME/.rustup"

echo "Setting default shell to fish..."
sudo -u "$1" chsh -s /usr/bin/fish

echo ""
echo "Setup complete! Please reboot and select the Hyprland session at login. "
read -r -p "Would you like to reboot now? [y/n]: " input

case $input in [yY][eE][sS]|[yY])
    reboot;; *)
    exit 0;;
esac