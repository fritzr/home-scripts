source ~/.vimrc.local

" tab/indent settings
filetype indent on
set expandtab
set softtabstop=2
set shiftwidth=2
set autoindent
" set smartindent

au Filetype python set shiftwidth=4
au Filetype python set softtabstop=4

" searches follow case-sensitivity like emacs
set smartcase

" wrap text
set textwidth=79
map Q gq

" use mouse
set mouse=a

" allow backspacing over everything in insert mode
set backspace=indent,eol,start

filetype plugin on
" don't replace tab with spaces in Makefiles or commit logs
au Filetype make set noexpandtab
au BufNew,BufRead svn-commit*.tmp set filetype=gitcommit
au Filetype gitcommit set noexpandtab
au BufNew,BufRead *.inc,*.incp set filetype=fortran
au BufNew,BufRead *_fw.inc set filetype=c
au BufNew,BufRead *.link set filetype=ld

" highlight comments with cyan - better than dark blue on dark blue
hi Comment ctermfg=darkcyan
colorscheme delek
hi Search ctermbg=darkyellow

" highlight trailing whitespace for visibility
au BufNew,BufRead,BufEnter * hi ws ctermbg=red
au BufNew,BufRead,BufEnter * match ws /[ \t]\+$/

" syntax highlighting
if &t_Co > 2 || has("gui_running")
    syntax on
    set hlsearch
endif

" grep for definitions of selected function
"map <> viwy:!grep -n '^<C-R>"\>' *.c *.h<CR>
" find definition of selected function
map <C-J> viw"jy/^<C-R>j\><CR><CR>
" replace in selection
map <C-H> :<C-U>%s/\%V
" jump to label
map gl viw"ly/\<<C-R>l:<CR>

" Previous/Next function + center in screen
map <C-P> [[z.
map <C-N> ]]z.

" Find next git conflict
map <F2> ?^\(<<<<<<<\\|=======\\|>>>>>>>\)<CR>
map <F3> /^\(<<<<<<<\\|=======\\|>>>>>>>\)<CR>

" 'Save' with S. The default behavior for S is the same as 'cc'.
nnoremap S :w<CR>

" Open buffer list, ready to choose one
nnoremap ,b :ls<CR>:buffer<Space>

" Remove all trailing whitespace
nnoremap <F5> mr:<C-U>%s/[ \t]\+$//<CR>'rz.

" Map space to ':' since it is easier
nnoremap <space> :noh<CR>
vnoremap <space> :noh<CR>

" VNC viewer likes to ignore CTRL quite frequently.
" So remap some common CTRL-... commands.

" u=undo, U=redo
nnoremap U :redo<CR>
" - jump last,  = jump next
nnoremap - <C-O>
nnoremap = <C-I>
" \ down, | up (half-page)
noremap <Bar> <C-U>
noremap <Bslash> <C-D>

" use ',' as map leader, so '\'X is not bound to anything and
" works as <C-D> with no delay
let mapleader = ","

" jump to macro definition
map gm viw"my/#define \+<C-R>m\><CR><CR>

" 'jk' in insert mode will escape
inoremap jk <esc>
