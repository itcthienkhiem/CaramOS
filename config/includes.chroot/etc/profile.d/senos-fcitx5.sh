#!/bin/sh
# SenOS: make Fcitx 5 the default input method for GTK/Qt/XIM sessions.
# This is read by Xsession and many desktop launch paths.
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export INPUT_METHOD=fcitx
export SDL_IM_MODULE=fcitx
