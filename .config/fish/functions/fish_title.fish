function fish_title
    set -q argv[1]; or set argv ""
    echo $argv (prompt_pwd);
end
