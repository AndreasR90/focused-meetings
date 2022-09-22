<template>
  <div>
    <div v-if="loggedIn">
      <div class="mainPage">
        <div class="heading">Willkommen {{ userName }}</div>
        <input
          class="focusButton"
          type="submit"
          :value="focusText"
          @click="toggleFocus"
        />
        <div class="currentStatus">
          <span>Stand</span>
          <span class="dot" :style="{ 'background-color': statusColor }"></span>
        </div>
        <div class="myCard members">
          <span class="cardHeader">Mitglieder</span>
          <ul class="list" v-for="member in members" v-bind:key="member.id">
            <li class="member">
              {{ member.name }}
            </li>
          </ul>
        </div>
        <div class="link">
          <span>
            <a
              id="session"
              :href="`/?session_id=${sessionId}`"
              class="sessionLink"
            >
              {{ sessionId }}
            </a>
            <a href="#" @click="CopyToClipboard" class="clipboard"
              ><i class="fa fa-copy"></i>
            </a>
          </span>
        </div>
      </div>
    </div>

    <div v-if="!loggedIn">
      <div class="loginPage">
        <div class="heading">Next Generation Meeting Helper</div>
        <label for="user" class="userLabel">Name</label>
        <input v-model="userName" class="userInput" type="text" />
        <label for="session" class="sessionLabel">Session</label>
        <span class="sessionLink">
          <a id="session" :href="`?session_id=${sessionId}`">
            {{ sessionId }}</a
          >
          <a href="#" @click="CopyToClipboard" class="clipboard"
            ><i class="fa fa-copy"></i>
          </a>
        </span>
        <input type="submit" class="submit" value="Login" @click="login" />
      </div>
    </div>
  </div>
</template>

<script>
import { WebsocketConnection } from "../helper/websocket";
import { uuid } from "vue-uuid";
const focusDict = {
  focused: {
    color: "green",
    text: "Verlieren Fokus",
  },
  unfocused: { color: "red", text: "Fokus wieder da" },
};

export default {
  data() {
    return {
      userName: null,
      loggedIn: false,
      userFocused: true,
      groupFocused: true,
      sessionId: 123,
      userId: null,
      focusThreshold: 2,
      members: [],
      statusColor: null,
      focusText: null,
    };
  },
  mounted() {
    this.setSessionId();

    this.websocket = new WebsocketConnection(this.sessionId);
    this.websocket.connection.onmessage = this.handleEvent;
    this.websocket.onmessage = this.handleEvent;
  },
  methods: {
    login() {
      this.websocket.login(this.userName);
    },
    toggleFocus() {
      this.websocket.toggleFocus(this.userId);
    },
    handleEvent(event) {
      console.debug("Received event");
      console.log(event.data);
      const inputData = JSON.parse(event.data);
      const functionDictionary = {
        user_id: this.userIdEvent,
        user_update: this.userUpdateEvent,
      };
      functionDictionary[inputData.event](inputData.data);
      console.log(inputData);
    },
    userIdEvent(data) {
      this.userId = data;
      this.loggedIn = true;
    },
    userUpdateEvent(data) {
      const userData = data;
      const numberUnfocused = userData.filter((x) => !x.focused).length;
      const isFocused = numberUnfocused < this.focusThreshold;
      this.setStatus(isFocused);
      const thisUser = userData.filter((x) => x.id == this.userId)[0];
      this.setText(thisUser);
      this.members = userData;
    },
    setStatus(isFocused) {
      this.groupFocused = isFocused;
      const focusStatus = isFocused ? "focused" : "unfocused";
      this.statusColor = focusDict[focusStatus].color;
    },
    setText(user) {
      console.log("setText");
      console.log(user);
      const focusStatus = user.focused ? "focused" : "unfocused";
      this.focusText = focusDict[focusStatus].text;
    },
    setSessionId() {
      let urlSessionId = new URLSearchParams(window.location.search).get(
        "session_id"
      );
      if (urlSessionId == null) {
        urlSessionId = uuid.v4();
      }
      this.sessionId = urlSessionId;
    },
    CopyToClipboard() {
      const link = `${location.href}?session_id=${this.sessionId}`;
      this.$copyText(link);
    },
  },
};
</script>
<style scoped>
.loginPage {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  display: grid;
  grid-template-columns: min-content 1fr;
  grid-column-gap: 0.5rem;
  grid-row-gap: 1rem;
}
.heading {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  color: var(--primary);
  font-size: 1.5rem;
  text-align: center;
  line-height: 1.2;
  white-space: nowrap;
}
.userLabel {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
  font-size: 1.2rem;
  align-self: center;
  justify-self: end;
}

.userInput {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
  padding: 0 0.5rem;
  width: 100%;
  min-width: 8rem;
}

.userInput:focus {
  border-color: var(--primary-light);
}

.sessionLabel {
  grid-column: 1 / 2;
  grid-row: 3 / 4;
  font-size: 1.2rem;
  align-self: center;
  justify-self: end;
}

.sessionLink {
  grid-column: 2 / 3;
  grid-row: 3 / 4;
  align-self: center;
  color: var(--primary);
}

.submit {
  --button-width: 100%;
  grid-column: 1 / 3;
  grid-row: 4 / 5;
}
.mainPage {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  display: grid;
  grid-template-columns: min-content 1fr;
  grid-column-gap: 0.5rem;
  grid-row-gap: 1rem;
}
.heading {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  color: var(--primary);
  font-size: 1.5rem;
  text-align: center;
  line-height: 1.2;
  white-space: nowrap;
}
.currentStatus {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
}
.focusButton {
  grid-column: 2 / 3;
  grid-row: 3 / 4;
}
.myCard {
  border: solid 1px var(--primary);
  border-radius: 10px;
  margin: 2px;
  padding: 3px;
}
.members {
  grid-column: 2 / 3;
  grid-row: 4 / 5;
  color: var(--tertiary);
  font-size: 1.1rem;
  margin-left: 0px;
  padding-left: 0px;
}
.cardHeader {
  color: var(--primary);
  text-align: left;
  font-weight: bold;
}
.list {
  text-align: center;
  padding: 1px;
  margin: 3px;
}
.member {
  margin-top: 20px;
  list-style-type: none; /* Remove bullets */
  padding: 0; /* Remove padding */
  margin: 0; /* Remove margins */
}
.dot {
  height: 25px;
  width: 25px;
  margin-left: 20px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
}
.link {
  grid-column: 2 / 3;
  grid-row: 5 / 6;
}
.clipboard {
  margin-left: 10px;
  padding: 2px;
  border: solid 2px;
}
</style>
