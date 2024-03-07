"Set compatibility to Vim only.
set nocompatible

"Helps force plug-ins to load correctly when it is turned back on below.
filetype off

"Turn on syntax highlighting.
syntax enable

"For plug-ins to load correctly.
filetype plugin indent on

" Find files also in subdirectories
set path+=**
set wildmenu
set mouse=a

" Automatically wrap text that extends beyond the screen length.
set wrap

set textwidth=80
set formatoptions=tcqrn1
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set noshiftround
set nobackup
set noswapfile
set undodir=~/.vim/undodir
set undofile
set smartindent
" Show line numbers
set number relativenumber

set showmode
set showmatch
set showcmd

set list
set listchars=tab:›\ ,trail:•,extends:#,nbsp:.

" Encoding
set encoding=utf-8

" Highlight matching pairs of brackets. Use the '%' character to jump
" between them.
set matchpairs+=<:>

" more natural splits
set splitbelow
set splitright

" Funzioni per evidenziare il gli elementi cercati
set hlsearch
set incsearch
set ignorecase
set smartcase

" if hidden is not set, TextEdit might fail.
set hidden
" Some servers have issues with backup files, see #649 set nobackup set nowritebackup
" Better display for messages set cmdheight=2
" You will have bad experience for diagnostic messages when it's default 4000.
set updatetime=300

" don't give |ins-completion-menu| messages.
set shortmess+=c

" always show signcolumns
set signcolumn=yes

" tutti i keybindings personalizzati vanno qua "spazio"+...
let mapleader = " "

nnoremap <leader>l :bn<CR>
nnoremap <leader>h :bp<CR>
nnoremap <leader>w :bd<CR>
