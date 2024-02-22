install: clean
	pyinstaller ./py_modules/decimal_calc.py
	clear

run: clean dir
	@./main

dir:
	@mkdir result

clean:
	@rm -rf result
	@rm -f test
	@rm -rf ./build ./dist ./*.spec
