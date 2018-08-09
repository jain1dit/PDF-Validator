output_file="all_modules.txt"
rm ${output_file}

make clean

for file in $(find ./atoms/ -iname "*.py")
do
	echo $(dirname ${file}) >> ${output_file}
	rm $(dirname ${file})/*.rst
	sphinx-apidoc -o $(dirname ${file}) $(dirname ${file})
done

for file in $(find ./lib/ -iname "*.py")
do
        echo $(dirname ${file}) >> ${output_file}
	rm $(dirname ${file})/*.rst
	sphinx-apidoc -o $(dirname ${file}) $(dirname ${file})
done

make html
