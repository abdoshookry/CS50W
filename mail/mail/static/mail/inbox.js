
document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(false));

  // By default, load the inbox
  load_mailbox('inbox');

});


function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if (email === false) {
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
  else {
    document.querySelector('#compose-recipients').value = `${email.sender}`;
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote : 
${email.body}`;
  }


  document.querySelector('#compose-form').onsubmit = function () {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.getElementById('compose-recipients').value,
        subject: document.getElementById('compose-subject').value,
        body: document.getElementById('compose-body').value
      })
    })
      .then(response => response.json())
      .then(result => {
        // Print result
        console.log(result);

        load_mailbox('sent')

      });

    return false;

  }
}



function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  document.querySelector('#emails').innerHTML = ''

  fetch(`/emails/${mailbox}`, {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  })
    .then(response => response.json())
    .then(emails => {
      // Print emails

      console.log(emails)

      // ... do something else with emails ...



      emails.forEach(email => {


        const elements = document.createElement('button');
        elements.className = 'emails';

        if (email.read === true) {
          elements.className = 'read';
        }

        elements.innerHTML =
          `<table class="${email.id}">
        <tr  >
        <th class="sender"> ${email.sender} </th>
        <th class="subject">   ${email.subject} </th>
        <th class="timestamp">  ${email.timestamp} </th>
        </tr>
        </table> `;

        const reply = document.createElement('span');
        reply.innerHTML = `<button class="btn btn-link"> reply </button>`

        reply.addEventListener('click', function () {
          compose_email(email);
        });

        const archive = document.createElement('span');

        switch (mailbox) {
          case 'inbox':

            archive.innerHTML = `<button class="btn btn-link"> archive </button> `

            archive.addEventListener('click', function () {
              archive();
              async function archive() {
                const response = await fetch(`/emails/${email.id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived: true
                  })
                });

                load_mailbox('inbox');
              }
            });

            break;

          case 'archive':

            archive.innerHTML = `<button class="btn btn-link"> unarchive </button> `

            archive.addEventListener('click', function () {
              archive();
              async function archive() {
                const response = await fetch(`/emails/${email.id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived: false
                  })
                });

                load_mailbox('inbox');
              }
            });
        }

        elements.addEventListener('click', function () {

          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          })

          console.log(email)

          const element = document.createElement('div');
          element.innerHTML =
            `<div id = "email${email.id}">
              <span>from: ${email.sender}</span><br>
              <span>to: ${email.recipients}</span><br>
              <span>subject:  ${email.subject}</span> <br>
              <span>timestamp:  ${email.timestamp}</span> 
              <hr>
              <div class="content"> ${email.body}</div>
            </div>`;

          document.querySelector('#emails').innerHTML = '';
          document.querySelector('#emails').append(element);
          document.querySelector('#emails').append(reply);
          document.querySelector('#emails').append(archive);
          document.querySelector('#emails-view').style.display = 'none';

        });

        document.querySelector('#emails').append(elements);
        document.querySelector('#emails').append(reply);
        document.querySelector('#emails').append(archive);
      });
    });

}


