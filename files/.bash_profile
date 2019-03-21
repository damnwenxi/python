
# Setting PATH for Python 3.7
# The original version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin:${PATH}"
export PATH=${PATH}:/usr/local/mysql/bin
export PATH=${PATH}:/Library/Frameworks/Python.framework/Versions/3.7/bin
alias python="/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7"
# for color
export CLICOLOR=1
# \h:\W \u\$
export PS1='\[\033[01;36m\] \u@ \[\033[01;33m\]\h \[\033[01;35m\]\t \[\033[01;31m\]\W\$ \[\033[00m\] '
export LSCOLORS=gxfxcxdxcxegedabagacad  
