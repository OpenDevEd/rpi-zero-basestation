#!/bin/bash

if [[ -f "$HOME/.ssh/id_rsa.pub" ]]
then
    echo "Public key (.ssh/id_rsa.pub) exists."
    cat $HOME/.ssh/id_rsa.pub
else
    ssh-keygen
    cat $HOME/.ssh/id_rsa.pub
fi
