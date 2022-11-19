#!/bin/sh

if [ ! -f $HOME/.huskyrc ]; then
  echo "export PATH=\"/usr/local/bin:/opt/homebrew/bin:\$PATH\"" > ~/.huskyrc
fi
