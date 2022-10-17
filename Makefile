all:
	mkdocs build
	git commit -am 'updates'; git push
	#cp -r ./site/* ../eth-sec.github.io/
	#cd ../eth-sec.github.io/; git add -A; git commit -am 'updates'; git push

