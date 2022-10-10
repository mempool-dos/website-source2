all:
	git commit -am 'updates'; git push
	mkdocs build
	cp -r ./site/* ../eth-sec.github.io/
	cd ../eth-sec.github.io/; git add -A; git commit -am 'updates'; git push

