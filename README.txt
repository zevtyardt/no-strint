ini adalah project iseng saya. masih versi beta jadi
jika masih ada output yg tidak sesuai atau terdapat
bug silahkan submit issue kalian ke sini

> https://github.com/zevtyardt/no-strint/issues <

* satu issue dari anda sangat berarti bagi saya.


#update -> 1.3.8
* fixed regex pattern
   sekarang sudah bisa gunain option
   [--only-strint] tanpa ada error, walaupun
   masih ada beberapa string yang gak ikut
   keambil

#first release
* masih versi beta
* [--only-strint] jika hanya program sederhana output masih bisa diexecute sebaliknya  kalau didalam file terdapat \" atau \" mungkin bakal ada syntax error dll.

Tips:
- copy string yang terdapat \" atau \" didalamnya
- obfuscate string yg kmu copy tadi
  python2 no-strint.py <string>
- replace string yang kamu copy dengan hasil obfuscate tadi
- lalu obfuscate lagi (otomatis)
  python2 no-strint.py --infile <file> --only-strint --outfile <file_output>
