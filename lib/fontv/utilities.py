#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================================================
# Copyright 2018 Christopher Simpkins
# MIT License
# ====================================================

from __future__ import unicode_literals

import os

import git.repo.fun


def dir_exists(dirpath):
    """Tests for existence of a directory on the string filepath"""
    if os.path.exists(dirpath) and os.path.isdir(
        dirpath
    ):  # test that exists and is a directory
        return True
    else:
        return False


def file_exists(filepath):
    """Tests for existence of a file on the string filepath"""
    if os.path.exists(filepath) and os.path.isfile(
        filepath
    ):  # test that exists and is a file
        return True
    else:
        return False


def get_git_root_path(filepath):
    """
    Recursively searches for git root path over 5 directory levels above working directory
    :param filepath: (string) - path to the font file that is under git version control
    :return: validated git root path as string
    :raises: IOError if unable to detect the root of the git repository through this path traversal
    """

    if "GIT_DIR" in os.environ:
        dot_git = os.path.abspath(os.environ["GIT_DIR"])
        if git.repo.fun.is_git_dir(dot_git):
            return os.path.dirname(dot_git)

    # begin by defining directory that contains font as the git root needle
    gitroot_path = os.path.dirname(os.path.abspath(filepath))

    # search up to five directories above for the git repo root
    for _ in range(6):
        dot_git = os.path.join(gitroot_path, ".git")
        if git.repo.fun.is_git_dir(dot_git):
            return gitroot_path
        elif file_exists(dot_git):
            # Returns something like ".../font-v/.git/worktrees/work-worktrees-work"
            worktree_path = git.repo.fun.find_worktree_git_dir(dot_git)
            if worktree_path:
                # ".../font-v/.git/worktrees/work-worktrees-work" -> ".../font-v"
                return worktree_path.split("/.git/worktrees/", 2)[0]

        gitroot_path = os.path.dirname(gitroot_path)

    raise IOError(
        "Unable to determine git repository root for font file " + filepath
    )


def is_font(filepath):
    """
    Tests filepath argument to determine if it has a .ttf or .otf file extension (definition of "font" for this
    application)

    :param filepath: (string) file path to a font file for testing
    :return: (boolean) True = appears to be a font file path; False = does not appear to be a font file path
    """
    if len(filepath) > 4:
        if filepath[-4:].lower() == ".ttf" or filepath[-4:].lower() == ".otf":
            return True
        else:
            return False
    else:
        return False
