local ensure_packer = function()
  local fn = vim.fn
  local install_path = fn.stdpath('data')..'/site/pack/packer/start/packer.nvim'
  if fn.empty(fn.glob(install_path)) > 0 then
    fn.system({'git', 'clone', '--depth', '1', 'https://github.com/wbthomason/packer.nvim', install_path})
    vim.cmd [[packadd packer.nvim]]
    return true
  end
  return false
end

local packer_bootstrap = ensure_packer()

return require('packer').startup(function(use)
    use 'wbthomason/packer.nvim'
    use 'xiyaowong/nvim-transparent'	-- transparency
    use 'norcalli/nvim-colorizer.lua'   -- RGB highlighting
    use 'neovim/nvim-lspconfig'     -- LSP presets
    use 'hrsh7th/nvim-cmp'          -- autocompletion
    use 'hrsh7th/cmp-nvim-lsp'
    use 'nvim-telescope/telescope.nvim' -- fuzzy finder
    use 'nvim-lua/plenary.nvim'     -- lua library
    use 'startup-nvim/startup.nvim' -- startup screen
    use 'kylechui/nvim-surround'    -- surround with quotes/brackets
    use 'nvim-lualine/lualine.nvim' -- status bar
    use 'ellisonleao/gruvbox.nvim'  -- colors
    use 'elkowar/yuck.vim'          -- eww syntax highlighting
    use 'kyazdani42/nvim-web-devicons'  -- extra devicons
    use 'ryanoasis/vim-devicons'    -- icons

    if packer_bootstrap then
        require('packer').sync()
    end
end)
