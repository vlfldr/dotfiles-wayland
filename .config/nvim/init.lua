-- Load plugins
require("plugins")

-- Relative line numbers
vim.wo.number = true
vim.wo.relativenumber = true

-- syntax highlighting based on file extension
vim.o.syntax = ON

-- copy/paste settings
vim.o.clipboard = unnamedplus

-- enable mouse
vim.o.mouse = 'a'

-- save history to file
vim.opt.undofile = true

-- Remove highlighting after search
vim.o.hlsearch = false

-- highlight openeing bracket upon inserting closing
vim.o.showmatch = true

-- indentation
vim.o.tabstop = 4
vim.o.shiftwidth = 4
vim.o.softtabstop = 4
vim.o.expandtab = true
vim.o.smarttab = true
vim.o.shiftround = true
-- preserve existing tabs when changing indentation
-- vim.o.preserveindent = true
vim.o.smartindent = true
vim.o.breakindent = true

-- case insensitve search
vim.o.ignorecase = true
vim.o.smartcase = true

-- faster updates
vim.o.updatetime = 250
vim.wo.signcolumn = 'yes'

-- command bar
vim.o.showmode = false
vim.o.showcmd = false
vim.o.cmdheight=0

-- popup/floating window transparency
vim.o.pumblend = 15
vim.o.winblend = 15

-- colors
vim.o.termguicolors = true
vim.o.background = 'dark'


-- PLUGINS --
require('gruvbox').setup({
    transparent_mode = true
})
vim.cmd [[colorscheme gruvbox]]

-- surrounding brackets
require('nvim-surround').setup()

-- startup screen
require('startup').setup({
  -- ASCII header
  header =  {
    type = "text", 
    align = "center", 
    fold_section = false, 
    margin = 0, 
    highlight = "GruvboxBlue",
    content = {
        [[      ....                          ]],
        [[   ,od88888bo.                      ]],
        [[ ,d88888888888b                     ]],
        [[,dP""'   `"Y888b       ,.           ]],
        [[d'         `"Y88b     .d8b. ,       ]],
        [['            `Y88[  , `Y8P' db      ]],
        [[              `88b  Ybo,`',d88)     ]],
        [[               ]88[ `Y888888P"      ]],
        [[              ,888)  `Y8888P'       ]],
        [[             ,d888[    `""'         ]],
        [[          .od8888P          ...     ]],
        [[     ..od88888888bo,      .d888b    ]],
        [[          `""Y888888bo. .d888888b   ]],
        [[.             `Y88b"Y88888P"' `Y8b  ]],
        [[:.             `Y88[ `"""'     `88[ ]],
        [[|b              |88b            Y8b.]],
        [[`8[             :888[ ,         :88)]],
        [[ Yb             :888) `b.       d8P']],
        [[ `8b.          ,d888[  `Ybo.  .d88[ ]],
        [[  Y8b.        .d888P'   `Y8888888P  ]],
        [[  `Y88bo.  .od8888P'      "Y888P'   ]],
        [[   `"Y8888888888P"'         `"'     ]],
        [[      `"Y8888P""'                   ]],
        [[         `""'                       ]]
    }
  },
  commands = {
    type = "mapping",
    align = "center",
    fold_section = false,
    margin = 0,
    highlight = "@method",
    content = {
        {" Empty Buffer", "enew", "e"},
        {" New File", "lua require('startup').new_file()", "n"},
        {" Recent Files", "Telescope oldfiles", "r"},
        {"⏻ Quit", "exit", "q"}
    }
  },
  options = {
      mapping_keys = true, -- display mapping (e.g. <leader>ff)
      -- if < 0 fraction of screen width
      -- if > 0 numbers of column
      cursor_column = 0.75,

      empty_lines_between_mappings = true,
      disable_statuslines = true -- disable status-, buffer- and tablines
      --paddings = {1,2}, -- amount of empty lines before each section (must be equal to amount of sections)
  },
  mappings = {
    execute_command = "<CR>",
    open_file = "o",
    open_file_split = "<c-o>",
    open_section = "<TAB>",
    open_help = "?",
  },
  colors = {
    background = "#1f2227",
    folded_section = "#56b6c2", -- the color of folded sections
  },
  parts = {"header", "commands" } 
})

-- RGB highlighting
require('colorizer').setup()

-- lualine
require('lualine').setup {
    options = { 
        theme = 'gruvbox',
    },
    sections = {
        lualine_x = {'filetype'},
        lualine_y = {},
    },
}

-- transparency
require('transparent').setup({
    enable = true,
    exclude = {}
})

-- LSP
local nvim_lsp = require 'lspconfig'
local LSPs = { 'pylsp', 'bashls' }

local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

for _, lsp in ipairs(LSPs) do
    nvim_lsp[lsp].setup { on_attach=on_attach, capabilities=capabilities }
end

--local runtime_path = vim.split(package.path, ';')
--table.insert(runtime_path, 'lua/?.lua')
--table.insert(runtime_path, 'lua/?/init.lua')

-- autocomplete
vim.o.completeopt = 'menuone,noselect'
