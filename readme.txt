Hi there!

This is an autobreeding bot i've used for a couple of months, I hope it will 
be useful to you as much as it has been useful to me. :) Below are instructions on how to put it on an amazon aws account, which are free for a year approximately.

Requirements:
# api-key from infura.io, get it by signing up at https://infura.io/signup
# amazon aws account, get by creating an account at https://aws.amazon.com/

*******************************************
******** INSTALLATION INSTRUCTIONS ********
*******************************************
First we will need to set up the virtual machine where the autobreeder 
will be running. So go to aws.amazon.com and create an account and then follow
the instruction images labeled with EC2.

**** Sidenote -> I will be putting brackets around code snippets that you can
Copy-paste into your terminal/cmd like so: [code snippet] you will need to copy only the insides of this so without the brackets. ****

In image 6 you will need to name a private key, I will be referring to this as my_privatekey.pem

From image 9 and forward you will start using the terminal/command prompt.
1. You will need to "cd" aka. Move to the location where your private key was 
Downloaded from Amazon. 

1.5 (default is Downloads so you can probably just do: [cd Downloads] 

2. Once at the location you will first need to make the key only readable by you, its owner, do this by writing: [chmod 400 my_privatekey.pem]

3. Now you can ssh to your new amazon EC2 instance. Do so by using this command, replace the X's after @ with your public dns which you got at image 8:
[ssh -i "my_privatekey.pem" ec2-user@XXXXXXXXXXXXX]

4. You should now have logged into your ec2 instance, if asked if you really want to connect, write [yes] (otherwise write to me and we'll find out what went wrong)

5. Copy all the text in install.txt and paste it in your cmd/terminal 

6. In run.txt lies the command for starting up the autobreeder and the command for stopping

**********************************
*** Setting up the autobreeder ***
**********************************
7. Open autobreeder.py in a texteditor (notepad is preferred) and on the 14th row it says private_key = 'insert private key here', you should replace [insert private key here] with your wallets private key, this is so that the bot will be able to make transactions for you since it needs to make these in order to breed two kitties together. You should leave one ' on both sides of the key, this makes python realise it is a string variable.

8. In row 20 replace api_key_here with your api key from infura.io

9. In row 28 replace public_wallet_address with your public wallet address.

10. Go into the file breedingpairs.json

11. Here you can edit the sire and matron, each pair is contained within the { }, you should not change nonce, cooldown, status and gasprice. Just copy and paste a row for each pair and don't forget the comma separating the rows (no need for comma on the last row)

11.5 It's easy to accidentally do something so you should copy the breedingpairs.json somewhere so you can go back and see how the structure should be :)

10. You will now need to upload autobreeder.py and breedingpairs.json to the ec2 instance using an ftp-client, I myself preferr Cyberduck (can be downloaded safely from their homepage https://cyberduck.io/)

11. You can follow the images in the images_FTP folder if you want help using Cyberduck.

*****************************************************
******** HOW TO USE AUTOBREEDER INSTRUCTIONS ********
*****************************************************
12. Whenever you want to update the breeding pairs, just update breedingpairs.json and reupload the file to Cyberduck. You will need to restart the autobreeder whenever you do this, the command is in run.txt

13. Reconnect to your ec2 instance using the terminal/command prompt with: [ssh -i "my_privatekey.pem" ec2-user@XXXXXXXXXXXXX]

14. When you have connected to the ec2-instance you will be able to start, restart and stop the autobreeder, these commands can be found in run.txt


