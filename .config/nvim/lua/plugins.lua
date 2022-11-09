vim.api.nvim_exec([[
augroup packer_user_config
    autocmd!
    autocmd BufWritePost init.lua PackerCompile
augroup end
]], false)

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
end)
