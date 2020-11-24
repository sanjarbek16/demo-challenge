// firebase configuration
var firebaseConfig = {
  apiKey: "AIzaSyC4ygtft0BU4qkF_kVWv3a6etBqbaloT_s",
  authDomain: "fitmeasure-ac726.firebaseapp.com",
  databaseURL: "https://fitmeasure-ac726.firebaseio.com",
  projectId: "fitmeasure-ac726",
  storageBucket: "fitmeasure-ac726.appspot.com",
  messagingSenderId: "1020504775390",
  appId: "1:1020504775390:web:6d8432d029a3e540b6004f",
  measurementId: "G-ZBXQWMKM2J",
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const userId = 0;
const getRemaining = (countDownDate) => {
  // Get today's date and time
  var now = new Date().getTime();
  // Find the distance between now and the count down date
  var distance = countDownDate + 86400000 - now;
  if (distance < 0) {
    return false;
  }
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  if (hours == 0 && minutes == 0) return false;
  hours == 0
    ? (hours = ``)
    : hours == 1
    ? (hours = `${hours} hour `)
    : (hours = `${hours} hours `);
  minutes == 0
    ? (minutes = ``)
    : minutes == 1
    ? (minutes = `${minutes} minutes `)
    : (minutes = `${minutes} minutes `);

  return hours + minutes;
};
function createId(length) {
  var result = "";
  var characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

// Challenge page
const getChallenges = async () => {
  const snapshot = await db.collection("challenges").orderBy("createdAt").get();
  const challenges = snapshot.docs.map((doc) => doc.data());
  const createButton = el("btn.btn btn-primary float-right", {
    style: {},
    innerHTML: `<i class="fas fa-plus" style="margin-right: 5px"></i>Create`,
  });

  var create = el(
    ".text-center",
    el("button.btn btn-primary", {
      innerHTML: `<i class="fas fa-plus" style="margin-right: 5px"></i>Create a challenge`,
      "data-toggle": "modal",
      "data-target": "#exampleModal",
      style: {
        marginBottom: 0,
        marginTop: "15px",
        width: "95%",
      },
    })
  );

  document.getElementById("challenges1").appendChild(create);
  challenges.forEach((challenge) => {
    const remaining = getRemaining(challenge.createdAt);
    joinButton = el("button.btn btn-success float-right", {
      innerText: "Joined",
      disabled: true,
    });
    if (remaining) {
      window.ch = challenge;
      var joinButton;
      if (!challenge.participants[userId])
        joinButton = el("button.btn btn-primary float-right", {
          innerText: "Join",
          // Update DB if joined
          onclick: () => {
            console.log(db.collection("challenges").doc(challenge.id));
            db.collection("challenges")
              .doc(challenge.id)
              .update({
                participants: {
                  ...challenge.participants,
                  [userId]: { score: 0 },
                },
              });
            document
              .getElementById(challenge.id)
              .children[0].children[0].children[0].remove();
            document
              .getElementById(challenge.id)
              .children[0].children[0].appendChild(
                el("button.btn btn-success float-right", {
                  innerText: "Joined",
                  disabled: true,
                })
              );
          },
        });
      if (
        Object.keys(ch.participants).length == 10 &&
        !challenge.participants[userId]
      )
        joinButton = el("button.btn btn-danger float-right", {
          innerText: "Full",
          disabled: true,
        });

      const card = el(
        ".card mx-auto",
        { id: challenge.id },
        el(
          ".card-body bg-light",
          el(".card-title large", { innerText: challenge.title }, joinButton),
          // el("p.card-title", {innerHTML: '' }),
          el("p.card-title", {innerHTML: challenge.description + '<br> Available for: '}),
          el("p.card-text", { innerText: remaining }),
          

        )
      );
      document.getElementById("challenges").appendChild(card);
      setTimer(challenge.id, challenge.createdAt)
    }
    
  });
};
getChallenges();

//check if a form filled properly
function checkforms() {
  // get all the inputs within the submitted form
  var inputs = document.getElementsByTagName("input");
  for (var i = 0; i < inputs.length; i++) {
    // only validate the inputs that have the required attribute
    if (inputs[i].hasAttribute("required")) {
      if (inputs[i].value == "") {
        // found an empty field that is required
        alert("Please fill all required fields");
        return false;
      }
    }
  }
  return true;
}

//create new challenge
const submit = () => {
  const check = checkforms();
  if (!check) return;
  const challengeId = createId(16);

  var now = new Date().getTime();
  const formValues = {
    title: document.getElementById("title").value,
    description: document.getElementById("description").value,
  };
  db.collection("challenges")
    .doc(challengeId)
    .set({
      ...formValues,
      createdBy: userId,
      participants: { [userId]: { score: 0 } },
      id: challengeId,
      createdAt: now,
    });
  const joinButton = el("button.btn btn-success float-right", {
    innerText: "Joined",
    disabled: true,
  });
  const card = el(
    ".card mx-auto",
    { id: challengeId },
    el(
      ".card-body bg-light",
      el(".card-title large", { innerText: formValues.title }, joinButton),
      el("p.card-text", { innerText: getRemaining(now) })
    )
  );
  document.getElementById("challenges").prepend(card);
  document.getElementById("exampleModal").click();
};

const getLeaderBoard = async () => {
  const snapshot = await db.collection("leaderboard").orderBy("score").get();
  const leaderboard = snapshot.docs.map((doc) => doc.data());
  console.log(leaderboard);
};
getLeaderBoard();
const Router = (ref) => {
  if (!ref) {
    const path = window.location.pathname;
    var ref = path.replace("/", "");
    if (!ref) {
      ref = "chal";
    }
  }
  var elems = document.querySelectorAll(".nav__link--active");
  [].forEach.call(elems, function (el) {
    el.classList.remove("nav__link--active");
  });

  document.getElementById(ref).classList.add("nav__link--active");
  //   history.pushState({}, ref, ref);
};


//setTimer for challenges

function setTimer(i, countDownDate) {
  // Set the date we're counting down to
  // var countDownDate = new Date("Jan 5, 2021 15:37:25").getTime();

  // Update the count down every 1 second
  var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countDownDate - now + 86400000;

  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="demo"
  var elem = $('#'+i).find('.card-text')[0]
  elem.innerText = "Remaining time: " + hours + "h " + minutes + "m " + seconds + "s ";

  // If the count down is finished, write some text
  if (distance < 0) {
      clearInterval(x);
      elem.innerText = "FINISHED";
      // document.getElementById("active"+i).removeClass('active').addClass('finished')
  }
  }, 1000);
}

