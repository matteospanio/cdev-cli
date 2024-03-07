FROM ubuntu:latest

RUN yes | unminimize

RUN apt-get update && apt-get install -y sudo python3 python3-pip \
                        build-essential man-db manpages-dev neovim \
                        clang-format tmux most git python3.10-venv

RUN apt-get install -y curl wget gdb valgrind

RUN pip install pipx

RUN adduser --disabled-password --gecos '' cdev

RUN usermod -aG sudo cdev

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir -p /home/cdev/.config/nvim

COPY .vimrc /home/cdev/.vimrc

COPY init.vim /home/cdev/.config/nvim/init.vim

USER cdev

ENV TERM=xterm-256color

ENV PAGER="most"

RUN echo "export PATH=$PATH:/home/cdev/.local/bin" >> /home/cdev/.bashrc

RUN python3 -m pipx install tldr

WORKDIR /home/cdev
