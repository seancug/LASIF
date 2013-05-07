#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Station Cache class.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2013
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""
from binascii import crc32
import os
import sqlite3


class FileInfoCache(object):
    """
    Object able to cache information about arbitrary files on the filesystem.

    Intended to be subclassed.
    """
    def __init__(self, cache_db_file):
        self.cache_db_file = cache_db_file
        self._init_database()
        self.update()

    def __del__(self):
        try:
            self.db_conn.close()
        except:
            pass

    def _init_database(self):
        """
        Inits the database connects, turns on foreign key support and creates
        the tables if they do not already exist.
        """
        # Init database and enable foreign key support.
        self.db_conn = sqlite3.connect(self.cache_db_file)
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute("PRAGMA foreign_keys = ON;")
        self.db_conn.commit()
        # Make sure that foreign key support has been turned on.
        if self.db_cursor.execute("PRAGMA foreign_keys;").fetchone()[0] != 1:
            try:
                self.db_conn.close()
            except:
                pass
            msg = ("Could not enable foreign key support for SQLite. Please "
                "contact the LASIF developers.")
            raise ValueError(msg)

        # Create the tables.
        SQL_CREATE_FILES_TABLE = """
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                last_modified REAL,
                crc32_hash INTEGER
            );
        """
        self.db_cursor.execute(SQL_CREATE_FILES_TABLE)

        SQL_CREATE_INDEX_TABLE = """
            CREATE TABLE IF NOT EXISTS indices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                %s,
                filepath_id INTEGER,
                FOREIGN KEY(filepath_id) REFERENCES files(id) ON DELETE CASCADE
            );
        """ % ",\n".join(["%s %s" % _i for _i in self.index_values])

        self.db_cursor.execute(SQL_CREATE_INDEX_TABLE)
        self.db_conn.commit()

    def _get_all_files(self):
        """
        Find all files for all filetypes.
        """
        self.files = {}
        for filetype in self.filetypes:
            get_file_fct = "_find_files_%s" % filetype
            self.files[filetype] = getattr(self, get_file_fct)()

    def update(self):
        """
        Updates the database.
        """
        # Get all files first.
        self._get_all_files()

        # Get all files currently in the database and reshape into a
        # dictionary. The dictionary key is the filename and the value a tuple
        # of (id, last_modified, crc32 hash).
        db_files = self.db_cursor.execute("SELECT * FROM files").fetchall()
        db_files = {_i[1]: (_i[0], _i[2], _i[3]) for _i in db_files}

        # Now update all filetypes separately.
        for filetype in self.filetypes:
            for filename in self.files[filetype]:
                if filename in db_files:
                    # Delete the file from the list of files to keep track of
                    # files no longer available.
                    this_file = db_files[filename]
                    del db_files[filename]
                    last_modified = os.path.getmtime(filename)
                    # If the last modified time is identical, nothing to do.
                    if last_modified == this_file[1]:
                        continue
                    # Otherwise check the hash.
                    with open(filename, "rb") as open_file:
                        hash_value = crc32(open_file.read())
                    if hash_value == this_file[2]:
                        continue
                    self._update_file(filename, filetype, this_file[0])
                else:
                    self._update_file(filename, filetype)

        # Remove all files no longer part of the cache DB.
        for filename in db_files:
            self.db_cursor.execute("DELETE FROM files WHERE filename='%s';" %
                filename)
        self.db_conn.commit()

    def _update_file(self, filename, filetype, filepath_id=None):
        """
        Updates or creates a new entry for the given file. If id is given, it
        will be interpreted as an update, otherwise as a fresh record.
        """
        # Remove all old indices for the file if it is an update.
        if filepath_id is not None:
            self.db_cursor.execute("DELETE FROM indices WHERE "
                "filepath_id = %i" % filepath_id)
            self.db_conn.commit()

        # Get the hash
        with open(filename, "rb") as open_file:
            filehash = crc32(open_file.read())

        # Add or update the file.
        if filepath_id is not None:
            self.db_cursor.execute("UPDATE files SET last_modified=%f, "
                "crc32_hash=%i WHERE id=%i;" % (os.path.getmtime(filename),
                filehash, filepath_id))
            self.db_conn.commit()
        else:
            self.db_cursor.execute("INSERT into files(filename, last_modified,"
                " crc32_hash) VALUES('%s', %f, %i);" % (
                filename, os.path.getmtime(filename), filehash))
            self.db_conn.commit()
            filepath_id = self.db_cursor.lastrowid

        # Get all indices from the file.
        indices = getattr(self, "_extract_index_values_%s" %
            filetype)(filename)
        if not indices:
            return

        # Append the filepath id to every index.
        for index in indices:
            index.append(filepath_id)

        sql_insert_string = "INSERT INTO indices(%s, filepath_id) VALUES(%s);"

        self.db_conn.executemany(sql_insert_string % (
            ",".join([_i[0] for _i in self.index_values]),
            ",".join(["?"] * (len(indices[0])))),
            indices)

        self.db_conn.commit()