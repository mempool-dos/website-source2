all:
	git commit -am 'updates'; git push -u origin master
	mkdocs build
	cp -r ./site/* ../eth-sec.github.io/
	cd ../eth-sec.github.io/; git add -A; git commit -am 'updates'; git push

