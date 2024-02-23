run:
	@./bash_modules/main

install: clean
	pyinstaller ./py_modules/decimal_calc.py
	@rm -rf ./build ./*.spec
	clear

clean:
	@rm -rf result

clean_all: clean
	@rm -rf ./dist
