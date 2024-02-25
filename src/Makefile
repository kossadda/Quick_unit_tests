run:
	@./bash_modules/main

clean:
	@rm -rf result

install: clean
	pyinstaller ./py_modules/decimal_calc.py
	@rm -rf ./build ./*.spec
	clear

uninstall: clean
	@rm -rf ./dist

dependencies:
	install pyton3-pip
	pip install pyinstaller
	pip install numpy
