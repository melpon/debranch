#!/bin/bash

mode="git"

while [[ "$1" =~ ^--. ]]; do
  case "$1" in
    --git)
      mode="git"
      ;;
    --git-submodule)
      mode="gitmodule"
      ;;
    --svn|--subversion)
      mode="svn"
      ;;
    --*)
      echo "unknown mode '$1'"
      exit 1
  esac
  shift
done

repo="$*"

shift

exec 5>&1-
exec 6>&2-
exec 2> /dev/null
exec 1> /dev/null
mkdir -p "${DEBRANCHCACHE:=$HOME/.debranch-cache}"

if [ -z "$repo" ]; then
  echo /dev/null >&5
  echo "usage: $0 {remote repository}" >&6
  exit 1
fi

erepo=`echo $repo | base64 -w0 | tr +/ -_`_$mode

#cd @@LOCALSTATEDIR@@
( cd "$DEBRANCHCACHE" && mkdir -p "$erepo" )
case "$mode" in
  git)
    cd "$DEBRANCHCACHE/$erepo"
    if ! git rev-parse HEAD; then
      echo "*** cloning $repo" >&6
      rm -rf .
      git clone "$repo" --bare . 2>&6 1>&6
    else
      echo "*** updating $repo" >&6
      git fetch -t --prune 2>&6 1>&6
    fi
    ;;
  svn)
    cd "$DEBRANCHCACHE/$erepo"
    if ! svn info; then
      echo "*** checking $repo out" >&6
      rm -rf .
      for i in `seq 20`; do
        if svn co "$repo" 2>&6 1>&6; then
          break
        fi
      done
    else
      echo "*** updating $repo" >&6
      svn up 2>&6 1>&6
    fi
    ;;
  gitmodule)
    if [ `git config --get remote.origin.url`module != "$DEBRANCHCACHE/$erepo" ]; then
      echo "must run in local clone" >&6
    else
      git submodule init
      for m in $(git submodule | sed 's/^.[^ ]* \([^ ]*\).*/\1/'); do
        r=`git config --get submodule.$m.url | sed "s,^$DEBRANCHCACHE/,../,"`
        if echo $r | grep ://; then
          git config submodule.$m.url $("$0" --git "$r" 2>&6)
        elif echo $r | grep '^.\?./'; then
          git config submodule.$m.url $("$0" --git "$repo/$r" 2>&6)
        fi
      done
    fi
    ;;
  *)
    echo "unknown mode $mode" >&6
    ;;
esac

echo "$DEBRANCHCACHE/$erepo" >&5



