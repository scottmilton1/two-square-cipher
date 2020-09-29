# two-square-cipher
An implementation of the two-square cipher in Python 3

This program encypts and decrypts messages using the two-square cipher,
aka double Playfair. There are two variations of the cipher, vertical
and horizontal, depending on how the two Playfair tables are arranged.
This implementation uses the first variation, so the two tables are
placed vertically.

System Requirements:

Python 3.8 or greater is required to run this program.

Dependencies:

No third-party packages are required.

This implementation has a main program with two modes: interactive and
command-line. The interactive mode offers users a a full menu of 
options for encrypting and decrypting messages. The program can be
run from the command-line to encrypt and decrypt messages as well, but
with fewer options. Here is a guide to command-line usage:

Command-line usage: 
* twosquare [OPTION] FILENAME KEY1 KEY2

or:
* twosquare [OPTION] "MESSAGE" KEY1 KEY2
    
OPTIONS: 
* -e, --encrypt  encrypt MESSAGE using KEY1 and KEY2
* -d, --decrypt  decrypt MESSAGE using KEY1 and KEY2
* -z, --remove_z remove trailing Z from MESSAGE :: decryption only
* -j, --omit_j   omit the letter J from MESSAGE :: decryption only
* -h, --help     display this help and exit
* -v, --version  output version information and exit
    
For interactive mode with a full in-program menu, run the program 
without adding any command-line arguments.

The functions in the global scope of this implementation can
also be used as a module.

This implementation includes a custom test suite (test.py) and
custom error classes (exceptions.py).

The Twosquare cipher uses two keys to encrypt and decrypt messages.
 
Each key can be a key word or phrase:
* Up to twenty-five letters in length
* ASCII letter characters only; no Unicode allowed
* Each letter may not be used more than once in a key
* A key may contain either 'I' or 'J', but not both
* Digits are not allowed so any numbers must be spelled out
* No white space, punctuation, or special characters
 
The Twosquare cipher uses two 5 x 5 Playfair tables to
encrypt and decrypt messages for you. These two tables
are each generated using one of the keys you create.
 
When encrypting a plaintext message, please note the 
following: All white space, punctuation, special characters,
and digits will be removed from the plaintext during the 
encryption process. In basic terms, all non-alpha characters,
while allowed, will be ignored and thus removed from the 
message. No data is stored about what was removed and 
therefore, when the ciphertext is later decrypted, the white
space, digits, and punctuation will not be restored.
 
Another thing to keep in mind is that 'I' and 'J' characters 
are combined into a single IJ letter by this cipher. The main
reason for this is to allow the entire twenty-six letter 
alphabet to fit into a 5 x 5 Playfair table with only twenty-
five cells. While this design choice solves the extra letter
problem, it can result in some loss of information when 
the process is reversed and the ciphertext is decrypted back 
to a plaintext. In practicality, this makes little 
difference, as the decoded message typically is still easy to 
read and understand.
 
If the number of characters in the plaintext is odd after 
removing all white space, special characters, and digits, a 
'Z' character is added to the end to make the number of 
characters even. This is necessary for the cipher to function
properly, as the text is broken into digraphs (two-letter 
combinations) during the encoding or decoding process. This
trailing character is, of course, easy enough to ignore when
reading the decrypted message. That said, this implementation 
has an option to remove a trailing 'Z' character from the
message automatically during the decryption process.
 
For these reasons, among others, the Twosquare cipher is not
a tool with practical use for encrypting and decrypting files
and documents where a loss of data would be unacceptable, or 
where high levels of data security and integrity are 
essential. It is best used as a relatively simple means of 
sending English alphabetic messages and is perhaps valuable 
in real terms mainly for its historical significance and for 
educational purposes.
 
This implementation enables loading and saving messages as .txt 
files. This is the only file type supported and files will not be
encrypted in place, that is to say, they will not be overwritten.
The reason for these restrictions is that the Twosquare cipher is
not suitable for encrypting all types of data or file, but rather 
only works with alphabetic ASCII character sets. The encoding 
process omits white space, digits, punctuation, special characters,
and other valuable data and thus is not suitable for general usage.
The file capabilities are provided merely to facilitate the storage
and transfer of messages at the personal discretion of the user.
Professional use is discouraged. No guarantee is made that the data
will be secure, and no warranty is made against the possibility of 
data loss or corruption. Use at your own risk.

For more information on the Twosquare cipher, check out
the Wikipedia article at: 

https://en.wikipedia.org/wiki/Two-square_cipher
 
>>> Program Credits <<<
* Creator: Scott Milton
* Contributors: <- (add your name here)
* License: GPL-3.0

If you would like to contribute to this project,
please feel free to visit the GitHub repo at: 

https://github.com/scottmilton1/two-square-cipher
 
This implementation is based on the description of the 
Twosquare cipher provided in the book Modern Cryptography:
Applied Mathematics for Encryption and Information Security
(First Version) by Chuck Eastom, McGraw Hill Publishing.

Special thanks to Chuck for writing such a great book!

This implementation is primarily function-based and aside from custom
error classes, it does not define and use classes. This was a design
decision made principally to focus energy on procedural programming 
techniques and to develop greater skill at writing and using functions 
as the basic modular unit. The decision had nothing to do with an
aversion to Object-Oriented Programming  and should not be taken
in any way as a reflection on the effectiveness or utility of the OOP
paradigm itself. Certainly, OOP could just as easily be used to 
satisfy the requirements of this project.

I hope you enjoy the program and welcome your comments and
contributions. 

Happy encrypting!

----- ----- -----

TODO's / Ideas for additional features:
--------------------------------------
* Optional: Make program work for either vertical or horizontal table alignment
* Optional: Add file viewer to load and save menu options (e.g. - os.listdir())
* Optional: Refactor display_title: add align arg with left, right, and center options
* Optional: Make program work for more than one cipher: (e.g. -	Playfair, Four-square, etc.)
