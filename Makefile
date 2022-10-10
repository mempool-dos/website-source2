all:
	git commit -am 'updates'; git push --set-upstream origin main
	mkdocs build
	cp -r ./site/* ../eth-sec.github.io/
	cd ../eth-sec.github.io/; git add -A; git commit -am 'updates'; git push

