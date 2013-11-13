
# vim: ai et sw=4 si sta sts=4 ts=4 tw=80 :

import pytest
import dup


def gethostname_short():
    import socket
    hostname = socket.gethostname()
    hostinfo = socket.gethostbyaddr(hostname)
    realhostname = hostinfo[0]
    before, _, _ = realhostname.partition('.')
    return realhostname if before == '' else before


def test_parse_scp_target():
    assert dup.parse_scp_target('p') == (None, None, 'p')
    assert dup.parse_scp_target('h:p') == (None, 'h', 'p')
    assert dup.parse_scp_target('u@h:p') == ('u', 'h', 'p')


def test_map_entry():
    assert dup.MapEntry(
        'host1',
        'path1',
        'user2',
        'host2',
        'path2'
    ) is not None


def test_parse_entry_comment():
    assert dup.parse_entry('# some comment') is None
    assert dup.parse_entry('  # comment with leading space') is None


def test_parse_entry():
    assert dup.parse_entry(
        'host1  path1  path2'
    ) == dup.MapEntry('host1', 'path1', None, None, 'path2')

    assert dup.parse_entry(
        'host1  path1  host2:path2'
    ) == dup.MapEntry('host1', 'path1', None, 'host2', 'path2')

    assert dup.parse_entry(
        'host1  path1  user2@host2:path2'
    ) == dup.MapEntry('host1', 'path1', 'user2', 'host2', 'path2')


def test_parse_entry_bad():
    with pytest.raises(ValueError):
        dup.parse_entry('')


def test_map(tmpdir):
    map_file_path = tmpdir.join('map.dup')
    map_file_path.write('host1 path1 user2@host2:path2')
    dup_map = dup.DuplicationMap(str(map_file_path))
    assert dup_map is not None


def test_matches_degenerates():
    assert dup.matches(None, None, None, None) is None
