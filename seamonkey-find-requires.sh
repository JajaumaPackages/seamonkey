#!/bin/sh

set -e

list=$(mktemp ${TMPDIR:-/tmp}/googleearth-rpm.XXXXXX)
tmp=$(mktemp ${TMPDIR:-/tmp}/googleearth-rpm.XXXXXX)

trap cleanup EXIT
cleanup()
{
    set +e
    [ -z "$list" -o ! -f "$list" ] || rm -f "$list"
    [ -z "$tmp" -o ! -f "$tmp" ] || rm -f "$tmp"
}

req=/usr/lib/rpm/redhat/find-requires
[ -e $req ] || req=/usr/lib/rpm/find-requires

prov=/usr/lib/rpm/redhat/find-provides
[ -e $prov ] || prov=/usr/lib/rpm/find-provides

cat >$list

sh $prov <$list | sort >$tmp
sh $req <$list | sort | join -v1 - $tmp
