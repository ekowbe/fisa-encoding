# fisa-encoding
By Ekow Bentsi-Enchill, Autumn Pearce, Elven Shum

## Installation
0. ensure you have python dependancies installed (python3, flask) 
1. install CVC4 on your local computer, following the instructions here: https://cvc4.github.io/downloads.html
2. clone this repo from github onto your local computer: https://github.com/ekowbe/fisa-encoding

## Running the Web App 
1. cd to the cloned repo, and in your terminal, run "$python3 runserver.py 2"
2. in your browser, go to local host "http://127.0.0.1:2"
3. answer relevant questions, and click "submit" to determine whether Electronic Surveillance has happened
4. the Web app will welly ou if its Electronic Surveillance or Inconclusive
5. to run again, refresh your page
## Ambiguous Wording, and our Solution
When FISA uses the phrase “a person has a reasonable expectation of privacy” (1, 3, 4), it's not clear from the text what theyre referring to. The only possibly reasonable interpretations for who needs the privacy expectation are: Just the Sender, Just the Intended_recipients, AtLeastOne of them, or Both.

We chose to incode it, how we thought it ought be read. We chose to encode it as "Both" because we thought that the sender and the intended_recipients both need to have a reasonable expectation of privacy to count as surveillance. If it was simply one, the act in question seems like something else: unintended viewing. Yet, it could be convievable to *ask* whether different people had different privacy expectations, so our question "did (person), by default, have reasonable expectation of privacy?" reflects this.
For more lengthy philosophical discussion on this, see our presentation, message Elven. 
