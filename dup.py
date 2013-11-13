#!/usr/bin/python
# vim: ai et sw=4 si sta sts=4 ts=4 tw=80 :

'''Duplicate a file according to rules mapping current user@host:path
to destination user@host:prefix/'''

from __future__ import print_function
import sys
import collections


def print_usage():
    '''Print usage'''
    print('Usage:', sys.argv[0], 'map_file source_file [...]', file=sys.stderr)

MapEntryPart = collections.namedtuple('MapEntryPart', ['user', 'host', 'path'])
MapEntry = collections.namedtuple('MapEntry', ['source', 'destination'])


def parse_part(part_string):
    '''Convert string of form [[user@]host:]path to MapEntryPart'''
    before, _, after = part_string.partition(':')
    if after == '':
        return MapEntryPart(None, None, before)
    else:
        path = after
        before, _, after = before.partition('@')
        if after == '':
            return MapEntryPart(None, before, path)
        else:
            return MapEntryPart(before, after, path)


def matches(entry, user, host, path):
    print('matches(', entry, user, host, path, ')')
    return False


class DuplicationMap(object):

    def __init__(self, map_file_name):
        self._map_file_name = map_file_name
        self._entries = []
        with open(self._map_file_name) as map_file:
            line_num = 0
            for line in map_file.readlines():
                line_num += 1
                if not line.lstrip().startswith('#'):
                    parts = line.split()
                    if len(parts) != 2:
                        print('bad entry on line', line_num, file=sys.stderr)
                    else:
                        source_part = parse_part(parts[0])
                        destination_part = parse_part(parts[1])
                        entry = MapEntry(source_part, destination_part)
                        self._entries.append(entry)

    @property
    def map_file_name(self):
        return self._map_file_name

    def dump(self):
        print('DuplicationMap(', self.map_file_name, ')')
        for i, entry in enumerate(self._entries):
            print(i, ':', entry)

    def search(self, source_user, source_host, source_path):
        for entry in self._entries:
            if matches(entry, source_user, source_host, source_path):
                return entry.destination
        return None


class Duplicator(object):

    '''Duplicator based on a given map'''

    def __init__(self, duplication_map):
        self._map = duplication_map

    @property
    def map(self):
        return self._map

    def dup(self, source_path):
        '''Duplicate the source file'''
        destination = self.map.search(None, None, source_path)
        print(source_path, '->', destination)


def main(map_file_name, source_paths):
    '''Duplicate source files according to map'''
    the_map = DuplicationMap(map_file_name)
    the_map.dump()
    the_dup = Duplicator(the_map)
    for source_path in source_paths:
        the_dup.dup(source_path)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2:])
