## Install
	git clone https://github.com/jonnyreeves/jonnyreeves.github.io -b source
	mkdir pelican-themes && cd $_
	git clone git@github.com:jonnyreeves/Flex.git

	easy_install pip
	brew install python
	pip install pelican Markdown ghp-import

## Dev Server
	./develop_server.sh start
	open http://localhost:8000

## Publishing
	./publish.sh