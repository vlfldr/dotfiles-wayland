fish_add_path ~/.cargo/bin
fish_add_path ~/.local/bin

set fish_greeting

alias c="clear"
alias v="nvim"
alias ls="lsd"
alias config="/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME"

set fish_prompt_pwd_dir_length 0
function fish_prompt
    printf '%s' (prompt_pwd) (set_color d79921) '  '
end
