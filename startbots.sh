#!/bin/bash

for pid in \
	$(\
		ps aux | egrep "(python3 )(discord_bot.py|reddit.py)" | \
		sed -e's/ \{1,\}/ /g' | \
		cut -f 2 -d ' '\
	); do
	kill $pid
done

if [ "$1" = "--kill" ]; then exit; fi

cd /home/raptor8134/Programs/wojak-meme-bot/
export SUBREDDITS="wojakmemebot politicalcompassmemes"
. ./login.sh

python3 discord_bot.py &
for SUB in $SUBREDDITS; do
	export R_SUBREDDIT="$SUB"
	python3 reddit.py &
done
