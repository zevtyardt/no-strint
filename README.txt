! nemu bug atau output yang tidak sesuai? silahkan buat issue kalian kesini

> https://github.com/zevtyardt/no-strint/issues <

* satu issue dari anda sangat berarti bagi saya.

>> installation
   $ git clone https://github.com/zevtyardt/no-strint
   $ cd no-strint
   $ python2 setup.py install or pip install .
   $ strint -h

# update -> 1.4.3
* Add new options: [--no-space] generate output strings
                   without spaces

# update -> 1.4.2
* fix a bug where the character escape cannot work

# update -> 1.4.1
* OOP (Object Oriented Programming)
* fix some bugs

# update -> 1.3.8
* fixed regex pattern
  sekarang sudah bisa gunain option [--only-strint] tanpa ada error, walaupun
  masih ada beberapa string yang gak ikut keambil.

# first release
* masih versi beta
* [--only-strint] jika hanya program sederhana output masih bisa diexecute
  sebaliknya  kalau didalam file terdapat \" atau \" mungkin bakal ada syntax error dll.

Tips:
- copy string yang terdapat \" atau \" didalamnya
- obfuscate string yg kmu copy tadi
  python2 no-strint.py <string>
- replace string yang kamu copy dengan hasil obfuscate tadi
- lalu obfuscate lagi (otomatis)
  python2 no-strint.py --infile <file> --only-strint --outfile <file_output>
