export class WebsocketConnection {
  constructor(sessionId) {
    this.sessionId = sessionId;
    // var url = process.env.VUE_APP_URL
    const url = "ws://localhost:80/ws";
    this.connection = new WebSocket(url + "/" + sessionId);
    this.connection.onmessage = this.receiveSocket;
    this.connection.onopen = () => console.log("connectoin established");
    this.onmessage = this.connection.onmessage;
  }
  login(userName) {
    const data = {
      session_id: this.sessionId,
      name: userName,
    };
    console.log(data);
    this.send("login", data);
  }
  toggleFocus(userId) {
    const data = {
      session_id: this.sessionId,
      id: userId,
    };
    this.send("change_focus", data);
  }
  send(functionName, data) {
    this.connection.send(
      JSON.stringify({
        function: functionName,
        arguments: data,
      })
    );
  }
}
