"""module to handle front end"""
#!/usr/bin/env python

# -----------------------------------------------------------------------
# reg.py
# Author: Ekow Bentsi-Enchill
# -----------------------------------------------------------------------

import os
from flask import Flask, request, make_response, render_template

# -----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """home page"""

    questions = {
        "acquired": "was info or communication acquired?",
        "surveillance": "is this device an electronic, mechanical, or other surveillance device?",
        "wire": "was the communication a wire?",
        "radio": "was the communication a radio?",
        "US_location_sender": "was the sender in the United States during the acquisition?",
        "US_location_attacker": "was the potential attacker in the United States during the acquisition?",
        "targeted_sender": "was the sender targeted?",
        "targeted_recipient": "was the recipient targeted?",
        "privacy": "was there a reasonable expectation of privacy for this person?",
        "warrant": "would a warrant be required for law enforcement?",
        "us_person": "is this person considered a US person? or is any person within this list of person considered a US person?",
        "known_and_particular": "is a person in this list is particular and known to be a US person?",
        "privacy_sender": "did the sender have a reasonable expectation of privacy?",
        "privacy_recipients": "did the recipient have a reasonable expectation of privacy?",
        "intended_recipients_US": "are the intended recipients US persons?",
        "known_and_particular_recipients": "is a person in the list of intended recipients particular and known to be a US person?",
        "intended_recipients_in_US": "are the intended recipients US persons?",
        "consented_sender": "did the sender consent to the acquisition in question?",
        "consented_recipient": "did the recipient consent to the acquisition in question?",
        "covered": "is this the communication of computer trespassers, permissible under section 2511(2)(i) of title 18?",
        "monitoring": "was this device installed or used for monitoring to acquire info?",
        "intentional": "was the acquisition intentional?",

    }



    html = render_template('index.html',
                            success=None,
                            questions=questions)
    response = make_response(html)
    return response

@app.route('/check_FISA', methods=['GET'])
def check_FISA():
    # print(request.args.get('axioms'))

    definitions = """
COMM: TYPE;
DEVICE: TYPE;
COMM_TYP: TYPE;
PERSON: TYPE;
PLACE: TYPE;
ATTACK: TYPE;

% Varying constants
attack: ATTACK;
attacker: PERSON;
sender: PERSON;
intended_recipients: PERSON;
device: DEVICE;
communication: COMM;
US: PLACE;

% Immutable constants
wire, radio: COMM_TYP;

acquired: COMM -> BOOLEAN;                                  % was info or communication acquired?
surveillance_device: DEVICE -> BOOLEAN;                     % is Device an electronic, mechanical, or other surveillance device?
communication_type: (COMM, COMM_TYP) -> BOOLEAN;            % iff COMMUNICATION is of this COMM_TYPE, ret true
location: (PERSON, PLACE) -> BOOLEAN;                       % iff person is in place, ret true
targeted: PERSON -> BOOLEAN;                                % is person intentionally targeted?
privacy: PERSON -> BOOLEAN;                                 % did person have reasonable expectation of privacy?
warrant: ATTACK -> BOOLEAN;                                 % would a warrant be required for law enforcement
US_person: PERSON -> BOOLEAN;                               % is Person a US Person
known_and_particular: PERSON -> BOOLEAN;                    % if Person is Particular and Known to be US_Person, ret true
consented: PERSON -> BOOLEAN;                               % did person consent to this attack?
covered: ATTACK -> BOOLEAN;                                 % is this the communication of computer trespassers, permissible under section 2511(2)(i) of title 18
monitoring: DEVICE -> BOOLEAN;                              % was this device installed or used for monitoring to acquire info
intentional: ATTACK -> BOOLEAN;                             % was acquisition intentional?
electronic_surveillance: ATTACK -> BOOLEAN;                 % What we want to know.

"""
    axioms = request.args.get('axioms')
    formulas = """
ASSERT ( 
    acquired(communication) AND surveillance_device(device) AND (communication_type(communication, wire) OR communication_type(communication, radio))
) AND (
    ( 
        US_person(sender) AND known_and_particular(sender) AND location(sender, US)
    ) OR (
        US_person(intended_recipients) AND known_and_particular(intended_recipients) AND location(intended_recipients, US) 
    )
) AND (
    (
        privacy(sender) OR privacy(intended_recipients)
    ) AND (
        warrant(attack)
    )
) => electronic_surveillance(attack);


ASSERT ( 
    acquired(communication) AND surveillance_device(device) AND communication_type(communication, wire)
    ) AND (
        location(sender, US) OR location(intended_recipients, US)
    ) AND (
        NOT consented(sender) AND NOT consented(intended_recipients) AND location(attacker, US) AND NOT covered(attack)
    ) => electronic_surveillance(attack);


ASSERT (
        intentional(attack) AND acquired(communication) AND surveillance_device(device) 
    ) AND (
        privacy(sender) OR privacy(intended_recipients)
    ) AND (
        warrant(attack) AND location(sender, US) AND location(intended_recipients, US)
    ) => electronic_surveillance(attack);


ASSERT (
        monitoring(device) AND surveillance_device(device) AND location(attacker, US)
    ) AND (
        NOT (communication_type(communication, wire) OR communication_type(communication, radio))
    ) AND (
        privacy(sender) OR privacy(intended_recipients)
    ) AND (
        warrant(attack)
    )=> electronic_surveillance(attack);

QUERY electronic_surveillance(attack);
"""

    f = open("fisa_es_readable.cvc", "w")
    f.write("")
    f.write(definitions)
    f.write(axioms)
    f.write(formulas)
    f.close()

    os.system("cvc4 -im fisa_es_readable.cvc")
    output = os.popen("cvc4 -im fisa_es_readable.cvc").read().strip()
    print(output)

    if output == "entailed":
        html = """
                This is an attack
        """
    else:
        html = """
                This ain't an attack
        """
        
    response = make_response(html)
    return response

    # print(request.form.get())
