#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import os

import _unitex

from unitex import *

_LOGGER = logging.getLogger(__name__)



def cp(source_path, target_path):
    """
    This function copies a file. Both pathes can be on the virtual
    filesystem or the disk filesystem. Therefore, this function can be
    used to virtualize a file or to dump a virtual file.

    *Arguments:*

    - **source_path [str]** -- source file path
    - **target_path [str]** -- target file path

    *Return [bool]:*

      **True** if it succeeds, **False** otherwise.
    """
    _LOGGER.info("Copying file '%s' to '%s'..." % (source_path, target_path))
    ret = _unitex.unitex_cp(source_path, target_path)
    if ret is False:
        _LOGGER.info("[FAILED!]")

    return ret

def rm(path):
    """
    This function removes a file. The path can be on the virtual
    filesystem or the disk filesystem.

    *Argument:*

    - **path [str]** -- file path

    *Return [bool]:*

      **True** if it succeeds, **False** otherwise.
    """
    _LOGGER.info("Removing file '%s'..." % path)
    ret = _unitex.unitex_rm(path)
    if ret is False:
        _LOGGER.info("[FAILED!]")

    return ret

def mv(old_path, new_path):
    """
    This function moves/renames a file. Both pathes can be on the
    virtual filesystem or the disk filesystem.

    *Arguments:*

    - **old_path [str]** -- old file path
    - **new_path [str]** -- new file path

    *Return [bool]:*

      **True** if it succeeds, **False** otherwise.
    """
    _LOGGER.info("Moving file '%s' to '%s'..." % (old_path, new_path))
    ret = _unitex.unitex_mv(old_path, new_path)
    if ret is False:
        _LOGGER.info("[FAILED!]")

    return ret

def mkdir(path):
    """
    This function creates a directory on the disk.

    *Argument:*

    - **path [str]** -- directory path

    *Return [bool]:*

      **True** if it succeeds, **False** otherwise.
    """
    _LOGGER.info("Creating directory '%s'..." % path)
    ret = _unitex.unitex_mkdir(path)
    if ret is False:
        _LOGGER.info("[FAILED!]")

    return ret

def rmdir(path):
    """
    This function removes a directory from the disk.

    *Argument:*

    - **path [str]** -- directory path

    *Return [bool]:*

      **True** if it succeeds, **False** otherwise.
    """
    _LOGGER.info("Removing directory '%s'..." % path)
    ret = _unitex.unitex_rmdir(path)
    if ret is False:
        _LOGGER.info("[FAILED!]")

    return ret

def ls(path):
    """
    This function lists (disk or virtual) directory contents.

    *Argument:*

    - **path [str]** -- directory path

    *Return [list(str)]:*

      The function returns a list of files (not directories) if the
      directory is not empty and an empty list otherwise.
    """
    _LOGGER.info("Listing directory '%s'..." % path)
    return _unitex.unitex_ls(path)

def exists(path):
    """
    This function verify if a file exists (on disk or virtual
    filesystem).

    *Argument:*

    - **path [str]** -- directory path

    *Return [bool]:*

      **True** if the path exists, **False** otherwise.
    """
    if path.startswith(UnitexConstants.VFS_PREFIX) is False:
        return os.path.exists(path)
    return path in ls(path)



class UnitexFile(object):
    """
    The UnitexFile class provides the minimum functionality necessary to
    manipulate files on the disk and the virtual filesystems. It's
    mainly useful to read files from virtual filesystem whithout having
    to copy them to the disk.

    **WARNING: the encoding must be UTF-8 and the data Unicode
    strings.**
    """

    def __init__(self):
        self.__use_bom = None

        self.__path = None
        self.__mode = None

    def open(self, file, mode=None, use_bom=False):
        """
        This function opens a file from the disk or from the virtual
        filesystem.
        **WARNING: the I/O encoding is limited to UTF-8.**

        *Arguments:*

        - **file [str]** -- the file path

        - **mode [str]** -- specifies the mode in which the file is
          open. Possible values are:

          - 'r': open for reading (default);
          - 'b': open for reading (binary file);
          - 'w': open for writing;
          - 'a': open for writing (append to the end of file if it
            exists).

        - **use_bom [int]** -- 1 to writes the UTF-8 bom ('w' mode only,
          0 otherwise.

        *No return.*
        """

        if self.__path is not None:
            raise UnitexException("You must close the current file (%s) before open another one..." % self.__path)
        self.__use_bom = use_bom

        self.__path = file

        if mode is None:
            mode = "r"
        self.__mode = mode

    def close(self):
        """
        This function close the opened file and reset all the internal
        parameters.
        """
        if self.__path is None:
            raise UnitexException("There is no file to close...")
        self.__path = None
        self.__mode = None

    def write(self, data):
        """
        This function writes/append data to the opened file. The file
        must be opened in 'w' or 'a' mode.

        *Arguments:*

        - **data [unicode]** -- the content to write.

        *No return.*
        """
        if self.__path is None:
            raise UnitexException("You must open a file before writing...")
        if self.__mode not in ("w", "a"):
            raise UnitexException("File '%s' is opened in read mode..." % self.__path)

        if self.__mode == "w":
            bom = 1 if self.__use_bom is True else 0
            _unitex.unitex_write_file(self.__path, data, bom)
        else:
            _unitex.unitex_append_to_file(self.__path, data)

    def read(self):
        """
        This function reads data from the opened file. The file must be
        opened in 'r' mode.

        *No arguments.*

        *Return [unicode]:*

          The data read are returned as a unicode string.
        """
        if self.__path is None:
            raise UnitexException("You must open a file before reading...")
        if self.__mode not in ["r", "b"]:
            raise UnitexException("File '%s' is opened in write/append mode..." % self.__path)

        if self.__mode == "r":
            return _unitex.unitex_read_file(self.__path)
        elif self.__mode == "b":
            return _unitex.unitex_read_binary_file(self.__path)
